import csv
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QFileDialog, QTableWidgetItem
from PyQt6.QtCore import QSettings

class DateFormatDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("setdateformat_dialog.ui", self)

        self.cancelBtn.clicked.connect(self.closeDialog)
        self.saveBtn.clicked.connect(self.save_date_format)
        self.opencsvfileBtn.clicked.connect(self.open_file_dialog)

        self.setupDateComboBox()

    def save_date_format(self):
        selected_date_format = self.dateselect.currentText()
        self.settings = QSettings("FullAccount", "FullAccount")
        self.settings.setValue("date_format", selected_date_format)
        # with open('dateformat.ini', 'w') as file:
        #     file.write(selected_date_format)
        
        #main_window = self.parent()
        main_window = self
        while main_window.parentWidget(): main_window = main_window.parentWidget()
        if main_window:
            main_window.statusBar.showMessage("Date format has been saved", 5000)

        self.accept()

    def closeDialog(self):
        self.accept()

    def setupDateComboBox(self):
        date_formats = [
            "MM/dd/yyyy",    # Month/Day/Year (e.g., 10/25/2024)
            "yyyy-MM-dd",    # Year-Month-Day (e.g., 2024-10-25)
            "dd/MM/yyyy",    # Day/Month/Year (e.g., 25/10/2024)
            "dd.MM.yyyy",    # Day.Month.Year (e.g., 25.10.2024)
            "yyyy/MM/dd",    # Year/Month/Day (e.g., 2024/10/25)
            "dd-MM-yyyy",    # Day-Month-Year (e.g., 25-10-2024)
            "yyyy.MM.dd"     # Year.Month.Day (e.g., 2024.10.25)
        ]

        for date_format in date_formats:
            self.dateselect.addItem(date_format)

    def on_country_selected(self, index):
        """Handle the selection of a country in the combo box."""
        date_format = self.combo_box.itemData(index)
        self.date_format_label.setText(f"Date Format: {date_format}")

    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File",'',"CSV Files (*.csv)")
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                first_row = next(reader)

                # display all the columns in the table
                self.tableWidget.setColumnCount(len(first_row))
                self.tableWidget.setHorizontalHeaderLabels(first_row)

                # display the first 3 rows of the CSV file in the table
                for i, row in enumerate(reader):
                    if i < 10:  
                        self.tableWidget.insertRow(i)
                        for j, item in enumerate(row):
                            self.tableWidget.setItem(i, j, QTableWidgetItem(item))

