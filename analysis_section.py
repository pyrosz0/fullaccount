import sqlite3
from PyQt6 import uic
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QWidget, QMessageBox, QVBoxLayout
import utils
from calendar import monthrange
import a_spending_by_category as a_spending_by_category

transaction_list = None

class AnalysisSection(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('analysis.ui', self)

        self.getTransactionsBtn.clicked.connect(self.load_transactions)

        date_format = utils.loadDateFormat(self)

        self.dateFromFilter.setDisplayFormat(date_format)
        self.dateToFilter.setDisplayFormat(date_format)

        # Set dateFromFilter to the first day of the current month
        current_date = QDate.currentDate()
        self.dateFromFilter.setDate(QDate(current_date.year(), current_date.month(), 1))

        # Set dateToFilter to the last day of the current month
        self.dateToFilter.setDate(QDate(current_date.year(), current_date.month(), monthrange(current_date.year(), current_date.month())[1]))

        categories_list = utils.loadCategories(self)
        account_types = utils.loadAccountTypes(self)

        for account_type_id, name in account_types:
            self.accountsFilter.addItem(name, account_type_id)

        transaction_list = self.load_transactions()
    
        # spending_by_category_widget = a_spending_by_category.ASpendingByCategory(transaction_list,categories_list)
        # self.tab_1.setLayout(QVBoxLayout())
        # self.tab_1.layout().addWidget(spending_by_category_widget)


    def filter_text_changed(self, text):
        self.filter_timer.stop()
        self.filter_timer.setSingleShot(True)
        self.filter_timer.start(500)

   ######################

    def load_transactions(self):
        filter_text = self.filtertext.text()
        date_format = utils.loadDateFormat(self)

        try:
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()

            start_date = self.dateFromFilter.date().toString(date_format)
            start_date = utils.convert_custom_date_to_timestamp(self, start_date, date_format)

            end_date = self.dateToFilter.date().toString(date_format)
            end_date = utils.convert_custom_date_to_timestamp(self, end_date, date_format)

            account_type_id = self.accountsFilter.currentText()

            if account_type_id:
                if filter_text:
                    cursor.execute("""
                        SELECT id, accounttype, date, description, amount, merchant, category
                        FROM transactions
                        WHERE date BETWEEN ? AND ?
                        AND accounttype = ?
                        AND (description LIKE ? OR merchant LIKE ? OR category LIKE ? OR amount LIKE ?)
                        ORDER BY date DESC
                    """, (start_date, end_date, account_type_id, f'%{filter_text}%', f'%{filter_text}%', f'%{filter_text}%', f'%{filter_text}%'))
                else:
                    cursor.execute("""
                        SELECT id, accounttype, date, description, amount, merchant, category
                        FROM transactions
                        WHERE date BETWEEN ? AND ?
                        AND accounttype = ?
                        ORDER BY date DESC""", (start_date, end_date, account_type_id))
            
            data = cursor.fetchall()  # Use cursor instead of self.cursor

            conn.close()
            if data:
                return data

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))
