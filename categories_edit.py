import sqlite3
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt

class CategoryEditorDialog(QtWidgets.QDialog):
    def __init__(self, category_id=None, parent=None):
        super().__init__(parent)
        uic.loadUi("category_edit.ui", self)
        self.category_id = category_id
        self.db_connection = sqlite3.connect('fullaccount.db')
        
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setup_connections()
        self.load_category_data()
        
        self.keywordinput.setPlaceholderText("Enter keyword...")
        self.categoryName.setPlaceholderText("Category name...")

    def setup_connections(self):
        self.keywordinput.returnPressed.connect(self.add_keyword)
        self.addKeyword.clicked.connect(self.add_keyword)
        self.deleteCategoryBtn.clicked.connect(self.delete_category)
        self.saveCategoryChangesBtn.clicked.connect(self.save_changes)
        self.cancelCategoryChangesBtn.clicked.connect(self.reject)
        self.categoryKeywords.itemDoubleClicked.connect(self.remove_keyword)
        self.categoryKeywords.setDragDropMode(QtWidgets.QAbstractItemView.DragDropMode.InternalMove)

    def add_keyword(self):
        """Handle both button click and Enter key press"""
        keyword = self.keywordinput.text().strip().lower()
        if not keyword:
            return
        
        if self.keyword_exists(keyword):
            return
            
        self.categoryKeywords.addItem(keyword)
        self.keywordinput.clear()
        self.keywordinput.setFocus()  # Maintain focus for rapid entry

    def remove_keyword(self, item):
        confirm = QtWidgets.QMessageBox.question(
            self,
            "Remove Keyword",
            f"Remove '{item.text()}' from keywords?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            row = self.categoryKeywords.row(item)
            self.categoryKeywords.takeItem(row)

    def load_category_data(self):
        if self.category_id:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("SELECT name, keywords FROM categories WHERE id = ?", (self.category_id,))
                result = cursor.fetchone()
                
                if result:
                    self.categoryName.setText(result[0])
                    keywords = result[1].split(',') if result[1] else []
                    keywords = [keyword.strip().lower() for keyword in keywords]
                    self.categoryKeywords.addItems(keywords)
            except sqlite3.Error as e:
                self.show_error(f"Database error: {str(e)}")

    def keyword_exists(self, keyword):
        return any(self.categoryKeywords.item(i).text() == keyword 
                 for i in range(self.categoryKeywords.count()))

    def delete_category(self):
        confirm = QtWidgets.QMessageBox.question(
            self, "Delete Category", 
            "Are you sure you want to delete this category?",
            QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
        )
        
        if confirm == QtWidgets.QMessageBox.StandardButton.Yes:
            try:
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM categories WHERE id = ?", (self.category_id,))
                self.db_connection.commit()
                self.accept()
            except sqlite3.Error as e:
                self.show_error(f"Delete failed: {str(e)}")

    def save_changes(self):
        name = self.categoryName.text().strip()
        keywords = [self.categoryKeywords.item(i).text() 
                  for i in range(self.categoryKeywords.count())]
        
        if not name:
            self.show_error("Category name cannot be empty!")
            return
            
        try:
            cursor = self.db_connection.cursor()
            if self.category_id:  # Update existing
                cursor.execute("""
                    UPDATE categories 
                    SET name = ?, keywords = ?
                    WHERE id = ?
                """, (name, ','.join(keywords), self.category_id))
            else:  # Create new
                cursor.execute("""
                    INSERT INTO categories (name, keywords)
                    VALUES (?, ?)
                """, (name, ','.join(keywords)))
                self.category_id = cursor.lastrowid
            
            self.db_connection.commit()
            self.accept()
            
        except sqlite3.Error as e:
            self.show_error(f"Save failed: {str(e)}")
            self.db_connection.rollback()

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(
            self, "Error", message,
            QtWidgets.QMessageBox.StandardButton.Ok
        )

    def closeEvent(self, event):
        self.db_connection.close()
        super().closeEvent(event)
