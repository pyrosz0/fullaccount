import utils
import sqlite3
from PyQt6.QtWidgets import QMessageBox, QStatusBar


transactions_list = None
account_types = None
categories_list = None

def load_transactions(self, filter_text=None, start_date=None, end_date=None, account_type_id=None):

    date_format = utils.loadDateFormat(self)

    try:
        
        conn = sqlite3.connect('fullaccount.db')
        cursor = conn.cursor()

        start_date = utils.convert_custom_date_to_timestamp(self, start_date, date_format)

        end_date = utils.convert_custom_date_to_timestamp(self, end_date, date_format)
        print(start_date, end_date)
        #account_type_id = self.accountsFilter.currentText()

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
        else:
            return None

    except sqlite3.Error as e:
        QMessageBox.critical(self, "Database Error", str(e))
        
