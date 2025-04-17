import datetime,os
import sqlite3
import typing
from PyQt6.QtWidgets import QMessageBox,QMainWindow,QApplication
from PyQt6.QtCore import QSettings

def loadAccountTypes(self):
        try:
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM accounts ORDER BY name")
            account_types = cursor.fetchall()  
            self.accountsFilter.clear()
            
            return account_types
                
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

def loadCategories(self):
    try:
        conn = sqlite3.connect('fullaccount.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM categories ORDER BY name")
        categories = cursor.fetchall()  # Fetch all results

        # Extract category names from the list of tuples
        category_list = [category[0] for category in categories]  # Get the first element of each tuple

        conn.close()
        return category_list  # Return the list of category names

    except sqlite3.Error as e:
        QMessageBox.critical(self, "Database Error", str(e))
        return []  # Return an empty list in case of an error

def loadDateFormat(self):
    

    # Load the date format from the dateformat.ini file
    # dateformat_file_path = "dateformat.ini"
    # if not os.path.exists(dateformat_file_path):
    #     raise FileNotFoundError(f"The file {dateformat_file_path} does not exist.")

    # with open(dateformat_file_path, mode='r', encoding='utf-8') as ini_file:
    #     first_line = ini_file.readline().strip()
    #     if not first_line:
    #         raise ValueError("The first line of the date format file is empty.")
    #     date_format = first_line

    date_format = "MM/dd/yyyy"
    self.settings = QSettings("FullAccount", "FullAccount")
    date_format = self.settings.value("date_format", date_format)

    return date_format

def convert_custom_date_to_timestamp(self, date_str, custom_format):
    # Define a mapping from the custom format tokens to strptime tokens
    mapping = {
        "dd": "%d",
        "MM": "%m",
        "yyyy": "%Y",
    }

    # Replace the tokens in the provided custom format
    python_format = custom_format
    for token, py_token in mapping.items():
        python_format = python_format.replace(token, py_token)

    # Parse the date string using the python format string
    dt = datetime.datetime.strptime(date_str, python_format)

    # Convert datetime to a Unix timestamp (in seconds) and remove any trailing decimals
    timestamp = int(dt.timestamp())

    
    return timestamp

def convert_timestamp(self, timestamp, custom_format):
    if not timestamp:
        return ""

    # Define a mapping from the custom format tokens to strftime tokens
    mapping = {
        "dd": "%d",
        "MM": "%m",
        "yyyy": "%Y",
    }

    # Replace the tokens in the provided custom format
    python_format = custom_format
    for token, py_token in mapping.items():
        python_format = python_format.replace(token, py_token)

    # Ensure the timestamp is an integer
    timestamp = int(timestamp)

    # Convert the timestamp to a datetime object
    dt = datetime.datetime.fromtimestamp(timestamp)

    # Format the datetime object to the custom format
    formatted_date = dt.strftime(python_format)
    return formatted_date

def convert_format_string(self, format_str: str) -> str:
    # Mapping of common date format strings to strftime format codes
    format_mapping = {
        "dd/mm/yyyy": "%d/%m/%Y",
        "mm/dd/yyyy": "%m/%d/%Y",
        "dd-mm-yyyy": "%d-%m-%Y",
        "mm-dd-yyyy": "%m-%d-%Y",
        "yyyy/mm/dd": "%Y/%m/%d",
        "yyyy-mm-dd": "%Y-%m-%d",
        "dd.mm.yyyy": "%d.%m.%Y",
        "mm.dd.yyyy": "%m.%d.%Y",
        "yyyy.mm.dd": "%Y.%m.%d",
        "dd mmm yyyy": "%d %b %Y",  # e.g., 01 Jan 2023
        "mmm dd, yyyy": "%b %d, %Y",  # e.g., Jan 01, 2023
    }

    # Normalize the input format string
    normalized_format = format_str.lower().replace(" ", "")  # Remove spaces for matching

    # Return the corresponding strftime format or an error message
    return format_mapping.get(normalized_format, "Error: Format not recognized.")


def findMainWindow() -> typing.Union[QMainWindow, None]:
    # Global function to find the (open) QMainWindow in application
    app = QApplication.instance()
    for widget in app.topLevelWidgets():
        if isinstance(widget, QMainWindow):
            return widget
    return None