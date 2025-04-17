import csv
import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt6.QtCore import Qt, QSettings

class ImportBuilderDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("csv_import_builder.ui", self)

        self.loadCSVFileBtn.clicked.connect(self.open_file_dialog)
        self.saveBtn.clicked.connect(self.save_import_format)
        self.cancelBtn.clicked.connect(self.closeDialog)

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File",'',"CSV Files (*.csv)")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                first_row = next(reader)
               
                self.accounttype.addItems(first_row)
                self.date.addItems(first_row)
                self.description.addItems(first_row)
                self.amount.addItems(first_row)
                self.merchant.addItems(first_row)
                self.accountnumber.addItems(first_row)

                # display all the columns in the table
                self.tableWidget.setColumnCount(len(first_row))
                self.tableWidget.setHorizontalHeaderLabels(first_row)

                # display the first 3 rows of the CSV file in the table
                for i, row in enumerate(reader):
                    if i < 3:  
                        self.tableWidget.insertRow(i)
                        for j, item in enumerate(row):
                            self.tableWidget.setItem(i, j, QTableWidgetItem(item))

    def save_import_format(self):
        selected_indices = self.description.selectedIndexes()
        if not selected_indices:
            self.show_error("Please select at least one description field.")
            return
    
        # Extract the row numbers from each QModelIndex
        indexes = [index.row() for index in selected_indices]
        
        # Convert to strings and join with '+'
        indices_str = "+".join(map(str, indexes))
        import_format = str(self.accounttype.currentIndex()) + ',' + str(self.date.currentIndex()) + ',' + str(indices_str) + ',' + str(self.amount.currentIndex()) + ',' + str(self.merchant.currentIndex()) + ',' + str(self.accountnumber.currentIndex())
        
        self.settings = QSettings("FullAccount", "FullAccount")
        self.settings.setValue("import_format", import_format)

        self.accept()

        # with open('importformat.ini', 'w') as file:
        #     file.write(import_format)
        #     self.accept()

    def closeDialog(self):
        self.reject()
        
    def show_error(self, message):
        QtWidgets.QMessageBox.critical(
            self, "Error", message,
            QtWidgets.QMessageBox.StandardButton.Ok
        )