import os
import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMainWindow,QVBoxLayout
from PyQt6.QtCore import QSettings, QSize

#import qdarktheme

import home
import settings
import setupdb


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        DATABASE_NAME = 'fullaccount.db'
        if not os.path.exists(DATABASE_NAME):
            setupdb.create_database()

        # Load the main UI file
        uic.loadUi('main.ui', self)

        self.layout = QVBoxLayout(self.contentBox)

        self.setMinimumWidth(800)

        self.settings = QSettings("FullAccount", "FullAccount")

        #theme = self.settings.value("theme", "dark")
        #qdarktheme.setup_theme(theme)

        self.resize(self.settings.value("size", QSize(800, 800)))

        self.load_home()

        self.homeBtn.clicked.connect(self.load_home)
        self.settingsBtn.clicked.connect(self.load_settings)

        self.statusBar.showMessage("Welcome to FullAccount", 5000)

        


    def closeEvent(self, event):
        # Save settings before closing
        self.save_settings()
        event.accept()

   
    def save_settings(self):
        # Save window size and position
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())

##############################################

    def clearLayout(self):
        for i in reversed(range(self.layout.count())): 
            widget_to_remove = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

    def load_home(self):
        home_widget = home.HomeSection()
        self.clearLayout()
        self.layout.addWidget(home_widget)
        self.contentBox.setLayout(self.layout)


    def load_settings(self):
        settings_widget = settings.Settings()
        self.clearLayout()
        self.layout.addWidget(settings_widget)
        self.contentBox.setLayout(self.layout)

    

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
