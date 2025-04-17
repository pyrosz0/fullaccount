from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QSizePolicy
from PyQt6.QtCore import QDate
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as mticker
import pandas as pd
import calendar
import data

from datetime import datetime
from collections import defaultdict

class ASpendingByCategoryMoM(QWidget):

    chartLayout = None

    def __init__(self):
        super().__init__()
        uic.loadUi('a_spending_by_category.ui', self)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) # make the widget take up all available space
        self.categoriesWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) # make the widget take up all available space
        
        
       
        self.checkboxes = []  # Store references to checkboxes

        self.settings = QSettings("FullAccount", "FullAccount") # load settings

        global chartLayout
        chartLayout = QVBoxLayout()
        
        self.chartWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.chartWidget.setLayout(chartLayout)
        
        self.load_categories()
        self.display_chart()
        
    def load_categories(self):

        if data.categories_list is not None:
            self.categories_list = data.categories_list
        else:
            self.categories_list = []
        
        # Create checkboxes for each category
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        for category in self.categories_list:
            checkbox = QCheckBox(category)
            if category.lower() == 'income':
                checkbox.setChecked(False)
            else:
                checkbox.setChecked(True)  # Initially check all categories
            
            checkbox.stateChanged.connect(self.update_chart)  # Connect checkbox state change
            layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)  # Store checkbox reference
            
        self.categoriesWidget.setContentsMargins(0, 0, 0, 0)
        self.categoriesWidget.setLayout(layout)

    def update_chart(self):
        # Update the chart based on the selected checkboxes
        selected_categories = [cb.text() for cb in self.checkboxes if cb.isChecked()]
        self.display_chart(selected_categories)

    def display_chart(self, selected_categories=None):

        if data.transactions_list is not None:
            self.transactions_list = data.transactions_list
            
        else:
            self.transactions_list = []
        
        # Filter transactions based on selected categories
        if selected_categories:
            self.transactions_list_filtered = [transaction for transaction in self.transactions_list if transaction[6] in selected_categories]
        else:
            self.transactions_list_filtered = self.transactions_list

        # Remove positive values
        self.transactions_list_filtered = [transaction for transaction in self.transactions_list_filtered if transaction[4] < 0]

        # Invert the values only if negative
        self.transactions_list_filtered = [
            (t[0], t[1], t[2], t[3], -t[4], t[5], t[6]) if t[4] < 0 else t
            for t in self.transactions_list_filtered
        ]

        monthly_totals = defaultdict(lambda: defaultdict(float))

        # Process each transaction
        for transaction in self.transactions_list_filtered:
            # Extract timestamp (index 2), amount (index 4), and category (index 6)
            timestamp = transaction[2]
            amount = transaction[4]
            category = transaction[6]

            # Convert Unix timestamp to datetime object
            dt_object = datetime.fromtimestamp(timestamp)

            # Format to get YYYY-Month string (e.g., "2025-March")
            month_number = dt_object.month
            month_name = calendar.month_name[month_number]
            month_year_str = dt_object.strftime(f"%Y-{month_name}")

            # Add the amount to the total for that category in that month
            monthly_totals[month_year_str][category] += amount
            

            monthly_totals[month_year_str][category] = round(monthly_totals[month_year_str][category], 2)

        # Sort the months chronologically
        sorted_months = sorted(monthly_totals.keys())

        # Extracting data for the bar chart
        months = list(monthly_totals.keys())
        categories = set()  # To hold unique categories across all months

        # Collect all unique categories
        for month in months:
            categories.update(monthly_totals[month].keys())

        categories = list(categories)  # Convert to list for indexing
        values = {month: [] for month in months}  # Dictionary to hold values for each month

        # Fill the values for each month
        for month in months:
            for category in categories:
                values[month].append(monthly_totals[month].get(category, 0.0))

        # Creating the bar chart
        fig, ax = plt.subplots()
        bar_width = 0.2  # Width of the bars
        x = range(len(categories))  # X locations for the groups

        # Plotting each month's data
        for i, month in enumerate(months):
            ax.bar(
                [pos + bar_width * i for pos in x],
                values[month],
                width=bar_width,
                label=month,
            )

        ax.set_xlabel('Categories', color='black')
        ax.set_ylabel('Values', color='black')
        ax.set_title('Spending by Category Month Over Month', color='black')
        ax.set_xticks([pos + bar_width * (len(months) - 1) / 2 for pos in x])
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.axhline(0, color='black', linewidth=0.8)  # Add a line at y=0 for reference
        ax.legend()

        global chartLayout
            
        for i in reversed(range(chartLayout.count())): 
            chartLayout.itemAt(i).widget().setParent(None)

        canvas = FigureCanvas(fig)
        chartLayout.addWidget(canvas)

            
