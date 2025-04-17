import sqlite3
import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QMessageBox

from categories_edit import CategoryEditorDialog

class Categories(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('categories.ui', self)
        
        self.addCategoryBtn.clicked.connect(self.add_category)
        self.listWidget.itemDoubleClicked.connect(self.edit_category)
        self.load_categories()

    def load_categories(self):
        try:
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM categories")
            categories = cursor.fetchall()  # Fixed typo here
            self.listWidget.clear()
            
            for category_id, name in categories:
                item = QtWidgets.QListWidgetItem(name)
                item.setData(Qt.ItemDataRole.UserRole, category_id)  # Store ID in item data
                self.listWidget.addItem(item)
                
            conn.close()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def add_category(self):
        name = self.categorynameinput.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Category name cannot be empty!")
            return

        try:
            conn = sqlite3.connect('fullaccount.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name,))
            conn.commit()
            conn.close()
            self.categorynameinput.clear()
            self.load_categories()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Database Error", str(e))

    def edit_category(self, item):
        category_id = item.data(Qt.ItemDataRole.UserRole)
        dialog = CategoryEditorDialog(category_id=category_id, parent=self)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.load_categories()