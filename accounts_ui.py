# Form implementation generated from reading ui file 'h:\development\python\fullaccount\venv\accounts.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(500, 616)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_5.addWidget(self.label)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.accountnameinput = QtWidgets.QLineEdit(parent=Form)
        self.accountnameinput.setObjectName("accountnameinput")
        self.horizontalLayout_2.addWidget(self.accountnameinput)
        self.addAccountBtn = QtWidgets.QPushButton(parent=Form)
        self.addAccountBtn.setObjectName("addAccountBtn")
        self.horizontalLayout_2.addWidget(self.addAccountBtn)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.listWidget = QtWidgets.QListWidget(parent=Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_5.addWidget(self.listWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Accounts"))
        self.label.setText(_translate("Form", "Accounts"))
        self.addAccountBtn.setText(_translate("Form", "Add Account"))
