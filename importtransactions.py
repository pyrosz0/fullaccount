import csv
import datetime
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QSettings
import os
from nltk.stem import PorterStemmer

import utils
import time

# Initialize the Porter Stemmer
stemmer = PorterStemmer()

class ImportTransactionsCSVDialog(QtWidgets.QDialog):

    csvFileToImport = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("importtransactions.ui", self)

        self.loadCSVFileBtn.clicked.connect(self.open_file_dialog)
        self.closeBtn.clicked.connect(self.closeDialog)
        self.importBtn.clicked.connect(self.import_transactions)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", '', "CSV Files (*.csv)")
        if file_name:
            self.importdetailslabel.setText(file_name)
        
            self.importBtn.setEnabled(True)
            self.csvFileToImport = file_name

    def import_transactions(self):

        self.importBtn.setEnabled(False)
        rows_processed = self.processTransactionFile(self.csvFileToImport)
        if not rows_processed:
            self.importdetailslabel.setText("No transactions were imported.")
        else:
            self.importdetailslabel.setText(f"Processed {rows_processed} rows from {self.csvFileToImport}")
            main_window = self
            while main_window.parentWidget(): main_window = main_window.parentWidget()
            if main_window:
                main_window.statusBar.showMessage(f"Processed {rows_processed} rows from {self.csvFileToImport}", 5000)

    def closeDialog(self):
        self.accept()

    def fetch_categories_from_db(self):
        categories = []
        conn = None
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()

            # Fetch all rows from the categories table
            cursor.execute("SELECT name, keywords FROM categories")
            rows = cursor.fetchall()

            # Build the categories list
            for row in rows:
                category_name, keywords = row
                # Split the keywords string into a list
                search_terms = [term.strip() for term in keywords.split(",")]
                categories.append({
                    "category": category_name,
                    "search_terms": search_terms
                })

        except sqlite3.Error as e:
            self.show_error(f"Database error: {e}")
        finally:
            # Close the database connection
            if conn:
                conn.close()

        return categories

    def stem_text(self, text):
        """Stem each word in the input text."""
        return " ".join([stemmer.stem(word) for word in text.split()])

    def categorize_transaction(self, transaction_description, transaction_categories):
        # Convert the input string to lowercase and stem it
        transaction_description = self.stem_text(transaction_description.lower())

        # Initialize a dictionary to store the best match for each category
        best_matches = {}

        # Iterate through each category
        for category_data in transaction_categories:
            category = category_data["category"]
            search_terms = category_data["search_terms"]

            # Initialize the best match score for this category
            best_match_score = 0

            # Iterate through each search term in the category
            for term in search_terms:
                term = self.stem_text(term.lower())  # Stem the search term

                # Check for full-word matches
                if term in transaction_description:
                    # Full-word match is given higher priority
                    best_match_score = max(best_match_score, 2)
                    break  # No need to check further for this category

                # Check for partial-word matches
                if term in transaction_description:
                    best_match_score = max(best_match_score, 1)

            # Store the best match score for this category
            best_matches[category] = best_match_score

        # Find the category with the highest match score
        best_category = max(best_matches, key=best_matches.get)

        # If no match is found, return "uncategorized"
        if best_matches[best_category] == 0:
            return "uncategorized"
        else:
            return best_category

    def process_line(self, line, date_format, sequence):
        """
        Process a line from the CSV file based on the number sequence.
        """
        processed_fields = []
        for part in sequence.split(','):
            if '+' in part:
                # Concatenate fields if there's a plus sign
                indices = part.split('+')
                concatenated_field = ''.join([line[int(i)] for i in indices])
                processed_fields.append(concatenated_field)
            else:
                # Add the field as is
                processed_fields.append(line[int(part)])

        # Convert the date field to the specified format
        date_string = processed_fields[1]

        try:
            date_timestamp = utils.convert_custom_date_to_timestamp(self,date_string, date_format)
            processed_fields[1] = int(date_timestamp)
            return processed_fields
        except ValueError as e:
            #self.show_error(f"Error processing date: {e}")
            return None  # Skip this line if the date is invalid

    def load_csv(self, file_path, date_format, sequence, transaction_categories):
        """
        Load a CSV file, process each line based on the number sequence, and return the results.
        """
        processed_data = []
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header line
                for line in reader:
                    processed_line = self.process_line(line, date_format, sequence)
                    if processed_line:  # Skip invalid lines
                        processed_line.append(self.categorize_transaction(processed_line[2], transaction_categories))
                        processed_data.append(processed_line)
                    else:
                        processed_data = None
        except Exception as e:
            self.show_error(f"Error reading CSV file: {e}")
        return processed_data

    def processTransactionFile(self, file_path):
        conn = None
        try:
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()

            transaction_categories = self.fetch_categories_from_db()

            self.settings = QSettings("FullAccount", "FullAccount")
            sequence = self.settings.value("import_format")
            
            # Load the import format from the importformat.ini file
            # ini_file_path = "importformat.ini"
            # if not os.path.exists(ini_file_path):
            #     raise FileNotFoundError(f"The file {ini_file_path} does not exist.")

            # with open(ini_file_path, mode='r', encoding='utf-8') as ini_file:
            #     first_line = ini_file.readline().strip()
            #     if not first_line:
            #         raise ValueError("The first line of the file is empty.")
            #     sequence = first_line

            date_format = utils.loadDateFormat(self)

            # Load and process the CSV file
            processed_data = self.load_csv(file_path, date_format, sequence, transaction_categories)

            if not processed_data:
                self.show_error("Issue processing the CSV file. Please check the date format is correct.")
            else:
                # Extract account types from processed data
                account_types = {row[0] for row in processed_data}  # account type is the first column

                # Insert account types if they do not exist
                for account_type in account_types:                    
                    cursor.execute("SELECT name FROM accounts WHERE name = ?", (account_type,))
                    existing_account = cursor.fetchone()

                    if existing_account:
                        pass
                    else:
                        cursor.execute("""
                            INSERT INTO accounts (name) VALUES (?)
                        """, (account_type,))



                # Commit the changes for account types
                conn.commit()

                # Prepare to insert all processed data at once
                cursor.executemany("""
                    INSERT INTO transactions (accounttype, date, description, amount, merchant, accountnumber, category)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, processed_data)

                # Commit the changes
                conn.commit()

                # Remove duplicate transactions
                cursor.execute("""
                DELETE FROM transactions
                WHERE id NOT IN (
                    SELECT MIN(id)
                    FROM transactions
                    GROUP BY accounttype, date, description, amount, merchant, accountnumber, category
                )""")

                conn.commit()

                return len(processed_data)  # Return the number of processed rows

        except Exception as e:
            self.show_error(f"Error processing transaction file: {e}")
            return 0
        finally:
            if conn:
                conn.close()

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(
            self, "Error", message,
            QtWidgets.QMessageBox.StandardButton.Ok
        )
