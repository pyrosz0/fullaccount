import sqlite3
from PyQt6 import uic
import sqlite3
import datetime
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt, QDate
import utils, data
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

import a_spending_by_category as a_spending_by_category
import a_spending_by_category_mom as a_spending_by_category_mom
import transactions

currentTab = 'transactions'

class HomeSection(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('home.ui', self)

        self.getTransactionsBtn.clicked.connect(self.load_transactions)

        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.filtertext.textChanged.connect(self.filter_text_changed)
        self.filter_timer = QtCore.QTimer()
        self.filter_timer.timeout.connect(self.load_transactions)

        date_format = utils.loadDateFormat(self)

        self.dateFromFilter.setDisplayFormat(date_format)
        self.dateToFilter.setDisplayFormat(date_format)

        # Set dateFromFilter to the first day of the current month
        current_date = QDate.currentDate()
        self.dateFromFilter.setDate(QDate(current_date.year(), current_date.month(), 1))

        # Set dateToFilter to the last day of the current month
        self.dateToFilter.setDate(QDate(current_date.year(), current_date.month(), monthrange(current_date.year(), current_date.month())[1]))

        data.categories_list = utils.loadCategories(self)
        
        data.account_types = utils.loadAccountTypes(self)

        for account_type_id, name in data.account_types:
            self.accountsFilter.addItem(name, account_type_id)

        # Create all the tabs layouts
        self.transactionsTab.setLayout(QVBoxLayout())
        self.spending_by_category.setLayout(QVBoxLayout())
        self.spending_mom.setLayout(QVBoxLayout())

   
        self.load_transactions()
    

    def filter_text_changed(self, text):
        self.filter_timer.stop()
        self.filter_timer.setSingleShot(True)
        self.filter_timer.start(500)

    def tab_changed(self, index):
        tab_name = self.tabWidget.tabText(index).lower().replace(' ', '_')
        self.load_tabs(tab_name)

    def load_tabs(self, tab_name):
        global currentTab
        
        if tab_name == 'transactions':
            self.load_transactions_tab()
            currentTab = tab_name
        elif tab_name == 'spending_by_category':
             self.load_spending_by_category_tab()
             currentTab = tab_name
        elif tab_name == 'spending_month_over_month':
             self.load_spending_by_category_mom_tab()
             currentTab = tab_name
       
    def load_transactions_tab(self):

        transactionsWidget = transactions.Transactions()#(transaction_list, account_types)

        for i in reversed(range(self.transactionsTab.layout().count())): 
            self.transactionsTab.layout().itemAt(i).widget().setParent(None)

        self.transactionsTab.layout().addWidget(transactionsWidget) 
    
    def load_spending_by_category_tab(self):
        
        spending_by_category_widget = a_spending_by_category.ASpendingByCategory()

        for i in reversed(range(self.spending_by_category.layout().count())): 
            self.spending_by_category.layout().itemAt(i).widget().setParent(None)

        self.spending_by_category.layout().addWidget(spending_by_category_widget) 
    
    def load_spending_by_category_mom_tab(self):

        spending_by_category_mom_widget = a_spending_by_category_mom.ASpendingByCategoryMoM()

        for i in reversed(range(self.spending_mom.layout().count())): 
            self.spending_mom.layout().itemAt(i).widget().setParent(None)

        self.spending_mom.layout().addWidget(spending_by_category_mom_widget) 

  
    def load_transactions(self):
        date_format = utils.loadDateFormat(self)

        transactions = data.load_transactions(self, self.filtertext.text(),self.dateFromFilter.date().toString(date_format),self.dateToFilter.date().toString(date_format), self.accountsFilter.currentText())

        if transactions:
            data.transactions_list = transactions
            self.load_transactions_tab()
        #else:
        #    QMessageBox.information(self, "No Transactions", "No transactions found for the selected filter")
        
        self.load_tabs(currentTab)
