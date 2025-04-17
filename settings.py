from PyQt6 import uic
from PyQt6.QtCore import QSettings
from PyQt6.QtWidgets import QWidget, QMessageBox
#import qdarktheme

from importbuilder import ImportBuilderDialog
from dateformatselect import DateFormatDialog

import categories
import accounts
import setupdb

class Settings(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('settings.ui', self)
        
        self.importFormatBtn.clicked.connect(self.load_import_format)
        self.setDateFormatBtn.clicked.connect(self.load_date_format)
        self.resetDatabaseBtn.clicked.connect(self.resetDatabase)
        self.manageCategoriesBtn.clicked.connect(self.load_categories)
        self.manageAccountsBtn.clicked.connect(self.load_accounts)

    def load_import_format(self):
         dialog = ImportBuilderDialog(parent=self)
         dialog.exec()

    def load_date_format(self):
         dialog = DateFormatDialog(parent=self)
         dialog.exec()

    def load_categories(self):
        categories_widget = categories.Categories()
        main_window = self
        while main_window.parentWidget(): main_window = main_window.parentWidget()
        main_window.clearLayout()
        main_window.layout.addWidget(categories_widget)
        main_window.contentBox.setLayout(main_window.layout)
    
    def load_accounts(self):
        accounts_widget = accounts.Accounts()
        main_window = self
        while main_window.parentWidget(): main_window = main_window.parentWidget()
        main_window.clearLayout()
        main_window.layout.addWidget(accounts_widget)
        main_window.contentBox.setLayout(main_window.layout)

    def resetDatabase(self):
        reply = QMessageBox.question(self, "Delete Database", 
                                        "Are you sure you want to delete all user entered information in the datbase? This will clear all transactions. This action cannot be undone.",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            setupdb.create_database()