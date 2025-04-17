import sqlite3
import datetime
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QDate

import utils,data
from calendar import monthrange

from PyQt6.QtWidgets import (
    QTableWidgetItem,
    QVBoxLayout,
    QMessageBox,
    QComboBox,
    QHeaderView,
    QWidget,
    QDialog,QLabel,QLineEdit,QPushButton,QHBoxLayout,QDateEdit,
)

from importtransactions import ImportTransactionsCSVDialog

from PyQt6.QtWidgets import QTableWidgetItem, QComboBox, QMessageBox, QHeaderView, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton

class Transactions(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('transactions.ui', self)

        self.importTransactionCSVBtn.clicked.connect(self.load_transactions_csv)

        self.addSingleTransactionBtn.clicked.connect(self.add_transaction)

        self.display_transactions()
       

    def load_transactions_csv(self):
         dialog = ImportTransactionsCSVDialog(parent=self)
         if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
             self.display_transactions()

    def display_transactions(self):
        # Disconnect the double-click signal to prevent multiple connections
        try:
            self.transactionsTable.doubleClicked.disconnect(self.edit_transaction)
        except TypeError:
            pass

        categories = utils.loadCategories(self)

        date_format = utils.loadDateFormat(self)

        # Build the table
    
        self.transactionsTable.setRowCount(0)  # Clear existing rows

        # Set the number of columns and header labels
        self.transactionsTable.setColumnCount(6)  # Update to 6 columns
        self.transactionsTable.setHorizontalHeaderLabels(["Account", "Date", "Description", "Amount", "Merchant", "Category"])
        header = self.transactionsTable.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)

        # Adjust column widths
        self.transactionsTable.setColumnWidth(0, 100)  # Account Type
        self.transactionsTable.setColumnWidth(1, 100)  # Date
        self.transactionsTable.setColumnWidth(2, 200)  # Description
        self.transactionsTable.setColumnWidth(3, 80)   # Amount
        self.transactionsTable.setColumnWidth(4, 150)  # Merchant
        self.transactionsTable.setColumnWidth(5, 150)  # Category (Dropdown)

        if data.transactions_list is not None:
            
            for row_num, row_data in enumerate(data.transactions_list):
                self.transactionsTable.insertRow(row_num)
                entry_id, accounttype, date, description, amount, merchant, category = row_data

                # Account Type
                accounttype_item = QTableWidgetItem(accounttype)
                accounttype_item.setData(Qt.ItemDataRole.UserRole, entry_id)  # Store ID
                self.transactionsTable.setItem(row_num, 0, accounttype_item)

                # Date
                tdate = utils.convert_timestamp(self,date, date_format)
                date_item = QTableWidgetItem(tdate)
                self.transactionsTable.setItem(row_num, 1, date_item)

                # Description
                description_item = QTableWidgetItem(description)
                self.transactionsTable.setItem(row_num, 2, description_item)

                # Amount
                amount_item = QTableWidgetItem(f"{amount:.2f}")  # Format amount to 2 decimal places
                self.transactionsTable.setItem(row_num, 3, amount_item)

                # Merchant
                merchant_item = QTableWidgetItem(merchant)
                self.transactionsTable.setItem(row_num, 4, merchant_item)

                # Category (Dropdown)
                category_combo = QComboBox()
                category_combo.addItems(categories)
                category_combo.setCurrentText(category)
                category_combo.setProperty("row", row_num)  # Store row number
                category_combo.setProperty("entry_id", entry_id)  # Store entry_id
                category_combo.currentIndexChanged.connect(self.update_category)
                self.transactionsTable.setCellWidget(row_num, 5, category_combo)


        # Connect double-click signal to edit function
        self.transactionsTable.doubleClicked.connect(self.edit_transaction)

        


    def edit_transaction(self, index):
        
        row = index.row()
        entry_id = self.transactionsTable.item(row, 0).data(Qt.ItemDataRole.UserRole)  # Get the entry ID

        # Retrieve current values from the row
        accounttype = self.transactionsTable.item(row, 0).text()
        date = self.transactionsTable.item(row, 1).text()
        description = self.transactionsTable.item(row, 2).text()
        amount = self.transactionsTable.item(row, 3).text()
        merchant = self.transactionsTable.item(row, 4).text()
        category = self.transactionsTable.cellWidget(row, 5).currentText()

        # Create a dialog for editing
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Transaction")
        dialog.setFixedWidth(350)  # Set the width of the dialog to 350 pixels
        layout = QVBoxLayout(dialog)

        # Create input fields
        accounttype_input = QComboBox()
        
        # Load account names from the database
        try:
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM accounts")
            accounts = cursor.fetchall()
            conn.close()

            # Populate the accounttype_input dropdown
            accounttype_input.addItems([account[0] for account in accounts])
            accounttype_input.setCurrentText(accounttype)  # Set current account type
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

        date_format = utils.loadDateFormat(self)

        date_input = QDateEdit(self)
        date_input.setDisplayFormat(date_format)  # Set the display format

        date_obj = datetime.datetime.strptime(date, utils.convert_format_string(self,date_format)).date()

        date_input.setDate(QDate(date_obj.year, date_obj.month, date_obj.day))
        date_input.setCalendarPopup(True)

        description_input = QLineEdit(description)
        amount_input = QLineEdit(amount)
        merchant_input = QLineEdit(merchant)
        category_input = QComboBox()
        category_input.addItems(utils.loadCategories(self))
        category_input.setCurrentText(category)

        # Add fields to layout
        layout.addWidget(QLabel("Account Type:"))
        layout.addWidget(accounttype_input)
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(date_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(description_input)
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(amount_input)
        layout.addWidget(QLabel("Merchant:"))
        layout.addWidget(merchant_input)
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(category_input)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Save button
        save_button = QPushButton("Save")
        button_layout.addWidget(save_button)

        # Cancel button
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(cancel_button)

        # Delete button
        delete_button = QPushButton("Delete")
        button_layout.addWidget(delete_button)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # Save changes to the database
        def save_changes():

            date_format = utils.loadDateFormat(self)

            new_accounttype = accounttype_input.currentText()
            new_date = date_input.text()
            new_description = description_input.text()
            new_amount = amount_input.text()
            new_merchant = merchant_input.text()
            new_category = category_input.currentText()

            # description validation
            if not new_description:
                QMessageBox.warning(dialog, "Validation Error", "Description cannot be empty.")
                return
            
            # amount validation
            if not new_amount:
                QMessageBox.warning(dialog, "Validation Error", "Amount cannot be empty.")
                return
            
            try:
                float(new_amount)
            except ValueError:
                QMessageBox.warning(dialog, "Validation Error", "Amount must be a valid number.")
                return
            
            # check for valid date
            try:
                new_date = utils.convert_custom_date_to_timestamp(self, new_date, date_format)
            except ValueError:
                QMessageBox.warning(dialog, "Validation Error", "Invalid date format.")
                return

            # Update the database
            try:
                conn = sqlite3.connect('fullaccount.db')
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE transactions
                    SET accounttype = ?, date = ?, description = ?, amount = ?, merchant = ?, category = ?
                    WHERE id = ?
                """, (new_accounttype, new_date, new_description, new_amount, new_merchant, new_category, entry_id))
                conn.commit()
                conn.close()

                # Update the table
                self.transactionsTable.item(row, 0).setText(new_accounttype)
                self.transactionsTable.item(row, 1).setText(utils.convert_timestamp(self,new_date, date_format))
                self.transactionsTable.item(row, 2).setText(new_description)
                self.transactionsTable.item(row, 3).setText(new_amount)
                self.transactionsTable.item(row, 4).setText(new_merchant)
                category_combo = self.transactionsTable.cellWidget(row, 5)
                category_combo.setCurrentText(new_category)

                dialog.accept()  # Close the dialog
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", str(e))

        save_button.clicked.connect(save_changes)

        # Cancel button functionality
        cancel_button.clicked.connect(dialog.reject)  # Close the dialog without saving

        # Delete button functionality
        def delete_transaction():

            reply = QMessageBox.question(dialog, "Delete Transaction", 
                                        "Are you sure you want to delete this transaction?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    conn = sqlite3.connect('fullaccount.db')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM transactions WHERE id = ?", (entry_id,))
                    conn.commit()
                    conn.close()

                    # Remove the row from the table
                    self.transactionsTable.removeRow(row)
                    dialog.accept()  # Close the dialog
                except sqlite3.Error as e:
                    QMessageBox.critical(self, "Database Error", str(e))

        delete_button.clicked.connect(delete_transaction)

        dialog.exec()  # Show the dialog
        
    def update_category(self, index):
        combo = self.sender()
        row = combo.property("row")
        entry_id = combo.property("entry_id")
        new_category = combo.currentText()

        try:
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE transactions SET category = ? WHERE id = ?", (new_category, entry_id)
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
                    QMessageBox.critical(self, "Database Error", str(e))

 
    def add_transaction(self):
        # Create a dialog for adding a transaction
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Transaction")
        dialog.setFixedWidth(350)  # Set the width of the dialog to 350 pixels
        layout = QVBoxLayout(dialog)

        # Create input fields
        accounttype_input = QComboBox()
        
        # Load account names from the database
        try:
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM accounts")
            accounts = cursor.fetchall()
            conn.close()

            # Populate the accounttype_input dropdown
            accounttype_input.addItems([account[0] for account in accounts])
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

        date_format = utils.loadDateFormat(self)

        date_input = QDateEdit(self)
        date_input.setDisplayFormat(date_format)  # Set the display format
        date_input.setDate(QDate.currentDate())
        date_input.setCalendarPopup(True)

        description_input = QLineEdit()
        amount_input = QLineEdit()
        merchant_input = QLineEdit()
        category_input = QComboBox()
        category_input.addItems(utils.loadCategories(self))

        # Add fields to layout
        layout.addWidget(QLabel("Account Type:"))
        layout.addWidget(accounttype_input)
        layout.addWidget(QLabel("Date:"))
        layout.addWidget(date_input)
        layout.addWidget(QLabel("Description:"))
        layout.addWidget(description_input)
        layout.addWidget(QLabel("Amount:"))
        layout.addWidget(amount_input)
        layout.addWidget(QLabel("Merchant:"))
        layout.addWidget(merchant_input)
        layout.addWidget(QLabel("Category:"))
        layout.addWidget(category_input)

        # Create a horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Save button
        save_button = QPushButton("Save")
        button_layout.addWidget(save_button)

        # Cancel button
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(cancel_button)

        # Add the button layout to the main layout
        layout.addLayout(button_layout)

        # Save changes to the database
        def save_changes():
            date_format = utils.loadDateFormat(self)

            new_accounttype = accounttype_input.currentText()
            new_date = date_input.text()
            new_description = description_input.text()
            new_amount = amount_input.text()
            new_merchant = merchant_input.text()
            new_category = category_input.currentText()

            # description validation
            if not new_description:
                QMessageBox.warning(dialog, "Validation Error", "Description cannot be empty.")
                return
            
            # amount validation
            if not new_amount:
                QMessageBox.warning(dialog, "Validation Error", "Amount cannot be empty.")
                return
            
            try:
                float(new_amount)
            except ValueError:
                QMessageBox.warning(dialog, "Validation Error", "Amount must be a valid number.")
                return
            
            # check for valid date
            try:
                new_date = utils.convert_custom_date_to_timestamp(self, new_date, date_format)
            except ValueError:
                QMessageBox.warning(dialog, "Validation Error", "Invalid date format.")
                return

            # Insert the new transaction into the database
            try:
                conn = sqlite3.connect('fullaccount.db')
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO transactions (accounttype, date, description, amount, merchant, category, accountnumber)
                    VALUES (?, ?, ?, ?, ?, ?,0)
                """, (new_accounttype, new_date, new_description, new_amount, new_merchant, new_category))
                conn.commit()
                conn.close()

                #self.load_transactions()
                #self.HomeSection.load_transactions()
                dialog.accept()  # Close the dialog

            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", str(e))

        save_button.clicked.connect(save_changes)
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec()


    
