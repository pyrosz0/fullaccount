from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QSizePolicy
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
import data

class ASpendingByCategory(QWidget):

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

        # Convert the transactions list to a DataFrame
        df = pd.DataFrame(self.transactions_list, columns=['id', 'accounttype', 'date', 'description', 'amount', 'merchant', 'category'])

        if not df.empty:
            # Filter the DataFrame based on selected categories
            if selected_categories is not None:
                df = df[df['category'].isin(selected_categories)]

            # Group by category and sum the amounts
            category_totals = df.groupby('category')['amount'].sum().reset_index()
            category_totals['amount'] = category_totals['amount'].round(2)  # Round to 2 decimal places

            # Calculate the total spending
            total_spending = category_totals['amount'].sum()
            total_spending = round(total_spending, 2)
            
            #print(category_totals)
            # Invert the values only if negative
            category_totals['amount'] = category_totals['amount'].apply(lambda x: -x if x < 0 else 0)

            category_totals = category_totals[category_totals['amount'] != 0]

            # Create the Matplotlib figure and axes
            fig = Figure(dpi=100)
            ax = fig.add_subplot(111)


            # Clear the previous chart
            ax.clear()

            # Create the horizontal bar chart
            ax.barh(category_totals['category'], category_totals['amount'])
            
            # Display total values on the chart
            for i, v in enumerate(category_totals['amount']):
                ax.text(v + 3, i, str(v), color='black', va='center')

            # Adjust the x-axis limits to accommodate the text
            max_value = category_totals['amount'].max()
            ax.set_xlim(0, max_value * 1.2)  # Increase the limit by 20%

            # Customize the layout
            ax.set_title('Spending by Category', color='black')
            ax.set_xlabel('Total Amount Spent', color='black')
            
            # Display the total spending at the top of the chart
            ax.text(0.5, 1.05, f'Total: ${total_spending}', transform=ax.transAxes, ha='center', va='bottom', color='white', fontsize=12)


            # Create a FigureCanvas to display the Matplotlib figure
            canvas = FigureCanvas(fig)
            canvas.draw()
            canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding) # make the canvas take up all available space
            canvas.setMinimumSize(100, 100) # set a minimum size
            
            # Add the canvas to the chartarea layout, clear it first

            global chartLayout
            
            for i in reversed(range(chartLayout.count())): 
                chartLayout.itemAt(i).widget().setParent(None)

            chartLayout.addWidget(canvas)



            
