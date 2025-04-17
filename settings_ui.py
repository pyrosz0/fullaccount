# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'settings.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(463, 604)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setMaximumSize(QSize(16777215, 30))
        font = QFont()
        font.setFamilies([u"Arial"])
        font.setPointSize(14)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)

        self.verticalLayout.addWidget(self.label)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 100))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        self.groupBox.setFont(font1)
        self.importFormatBtn = QPushButton(self.groupBox)
        self.importFormatBtn.setObjectName(u"importFormatBtn")
        self.importFormatBtn.setGeometry(QRect(10, 60, 171, 23))
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 20, 281, 31))
        font2 = QFont()
        font2.setPointSize(10)
        self.label_2.setFont(font2)
        self.label_2.setWordWrap(True)

        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_3 = QGroupBox(Form)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setMinimumSize(QSize(0, 100))
        self.groupBox_3.setFont(font2)
        self.setDateFormatBtn = QPushButton(self.groupBox_3)
        self.setDateFormatBtn.setObjectName(u"setDateFormatBtn")
        self.setDateFormatBtn.setGeometry(QRect(10, 60, 121, 23))
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(10, 20, 311, 31))
        self.label_4.setFont(font2)
        self.label_4.setWordWrap(True)

        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox_2 = QGroupBox(Form)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMinimumSize(QSize(0, 75))
        self.groupBox_2.setFont(font2)
        self.manageCategoriesBtn = QPushButton(self.groupBox_2)
        self.manageCategoriesBtn.setObjectName(u"manageCategoriesBtn")
        self.manageCategoriesBtn.setGeometry(QRect(10, 30, 121, 23))

        self.verticalLayout.addWidget(self.groupBox_2)

        self.groupBox_4 = QGroupBox(Form)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setMinimumSize(QSize(0, 75))
        self.groupBox_4.setFont(font2)
        self.manageAccountsBtn = QPushButton(self.groupBox_4)
        self.manageAccountsBtn.setObjectName(u"manageAccountsBtn")
        self.manageAccountsBtn.setGeometry(QRect(10, 30, 121, 23))

        self.verticalLayout.addWidget(self.groupBox_4)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(0, 25))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.resetDatabaseBtn = QPushButton(self.widget)
        self.resetDatabaseBtn.setObjectName(u"resetDatabaseBtn")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.resetDatabaseBtn.sizePolicy().hasHeightForWidth())
        self.resetDatabaseBtn.setSizePolicy(sizePolicy)
        self.resetDatabaseBtn.setMinimumSize(QSize(100, 0))

        self.horizontalLayout.addWidget(self.resetDatabaseBtn)

        self.horizontalSpacer = QSpacerItem(237, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.widget)

        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 15))
        self.label_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.verticalLayout.addWidget(self.label_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"FullAccount", None))
        self.label.setText(QCoreApplication.translate("Form", u"Settings", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"CSV File Import", None))
        self.importFormatBtn.setText(QCoreApplication.translate("Form", u"CSV Import Format Builder", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"The import format changes how the CSV files from your bank are loaded into the system.", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Form", u"Date Format", None))
        self.setDateFormatBtn.setText(QCoreApplication.translate("Form", u"Set Date Format", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Make sure you set the date format to be the same as what your bank uses.", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Form", u"Categories", None))
        self.manageCategoriesBtn.setText(QCoreApplication.translate("Form", u"Manage Categories", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("Form", u"Accounts", None))
        self.manageAccountsBtn.setText(QCoreApplication.translate("Form", u"Manage Accounts", None))
        self.resetDatabaseBtn.setText(QCoreApplication.translate("Form", u"Reset Database", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Version 0.1.1", None))
    # retranslateUi

