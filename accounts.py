import sqlite3
import sys
from PyQt6 import QtWidgets, uic, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMessageBox, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout

class Accounts(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('accounts.ui', self)
        
        self.listWidget.itemDoubleClicked.connect(self.edit_account)
        self.addAccountBtn.clicked.connect(self.add_account)
        
        
        self.load_acounts()

    def load_acounts(self):
        try:
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM accounts")
            accounts = cursor.fetchall()  # Fixed typo here
            self.listWidget.clear()
            
            for account_id, name in accounts:
                item = QtWidgets.QListWidgetItem(name)
                item.setData(Qt.ItemDataRole.UserRole, account_id)  # Store ID in item data
                self.listWidget.addItem(item)
                
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def add_account(self):
        name = self.accountnameinput.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Account name cannot be empty!")
            return

        try:
            conn = sqlite3.connect('fullaccount.db')  
            cursor = conn.cursor()  

            # Check if the account name already exists
            cursor.execute("SELECT name FROM accounts WHERE name = ?", (name,))
            existing_account = cursor.fetchone()

            if existing_account:
                QMessageBox.warning(self, "Error", "Account name already exists!")
            else:
                cursor.execute("INSERT INTO accounts (name) VALUES (?)", (name,))
                conn.commit()

            conn.close()  
            self.accountnameinput.clear()
            self.load_acounts()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))
    
    def edit_account(self, item):
        account_id = item.data(Qt.ItemDataRole.UserRole)
        account_name = item.text()

        dialog = self.AccountEditorDialog(account_id=account_id, account_name=account_name, parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.load_acounts()

    class AccountEditorDialog(QDialog):
        def __init__(self, account_id, account_name, parent=None):
            super().__init__(parent)
            self.account_id = account_id
            self.setWindowTitle("Edit Account")
            self.setFixedWidth(300)

            layout = QVBoxLayout(self)

            # Account Name Label and Input
            layout.addWidget(QLabel("Account Name:"))
            self.account_name_input = QLineEdit(account_name)
            layout.addWidget(self.account_name_input)

            # Button Layout
            button_layout = QHBoxLayout()

            # Save Button
            self.save_button = QPushButton("Save")
            self.save_button.clicked.connect(self.save_changes)
            button_layout.addWidget(self.save_button)

            # Delete Button
            self.delete_button = QPushButton("Delete")
            self.delete_button.clicked.connect(self.delete_account)
            button_layout.addWidget(self.delete_button)

            # Cancel Button
            self.cancel_button = QPushButton("Cancel")
            self.cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(self.cancel_button)

            layout.addLayout(button_layout)

        def save_changes(self):
            new_account_name = self.account_name_input.text().strip()
            if not new_account_name:
                QMessageBox.warning(self, "Error", "Account name cannot be empty!")
                return

            try:
                conn = sqlite3.connect('fullaccount.db')
                cursor = conn.cursor()

                # Check if the new account name already exists (excluding the current account)
                cursor.execute("SELECT name FROM accounts WHERE name = ? AND id != ?", (new_account_name, self.account_id))
                existing_account = cursor.fetchone()

                if existing_account:
                    QMessageBox.warning(self, "Error", "Account name already exists!")
                    conn.close()
                    return

                # Update transactions with the new account name
                cursor.execute("""
                    UPDATE transactions
                    SET accounttype = ?
                    WHERE accounttype = ?
                """, (new_account_name, self.parent().listWidget.item(self.parent().listWidget.currentRow()).text()))

                # Update the account name
                cursor.execute("UPDATE accounts SET name = ? WHERE id = ?", (new_account_name, self.account_id))
                conn.commit()
                conn.close()
                self.accept()
            except sqlite3.Error as e:
                QMessageBox.critical(self, "Database Error", str(e))

        def delete_account(self):
            reply = QMessageBox.question(self, "Delete Account", 
                                        "Are you sure you want to delete this account?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                try:
                    conn = sqlite3.connect('fullaccount.db')
                    cursor = conn.cursor()

                    # Check if the account is used in transactions
                    cursor.execute("SELECT COUNT(*) FROM transactions WHERE accounttype = (SELECT name FROM accounts WHERE id = ?)", (self.account_id,))
                    transaction_count = cursor.fetchone()[0]

                    if transaction_count > 0:
                        QMessageBox.warning(self, "Error", "This account is used in transactions and cannot be deleted.")
                        conn.close()
                        return

                    # Delete the account
                    cursor.execute("DELETE FROM accounts WHERE id = ?", (self.account_id,))
                    conn.commit()
                    conn.close()
                    self.accept()
                except sqlite3.Error as e:
                    QMessageBox.critical(self, "Database Error", str(e))



    
