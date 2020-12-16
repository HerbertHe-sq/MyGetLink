# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ConverterUi.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConvertWindow(object):
    def setupUi(self, ConvertWindow):
        ConvertWindow.setObjectName("ConvertWindow")
        ConvertWindow.resize(584, 192)
        self.centralwidget = QtWidgets.QWidget(ConvertWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 10, 401, 51))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 80, 401, 51))
        self.textEdit_2.setObjectName("textEdit_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(420, 10, 151, 81))
        self.groupBox.setObjectName("groupBox")
        self.radioButton = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 20, 131, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 50, 131, 16))
        self.radioButton_2.setObjectName("radioButton_2")
        self.btnConvert = QtWidgets.QPushButton(self.centralwidget)
        self.btnConvert.setGeometry(QtCore.QRect(420, 100, 151, 31))
        self.btnConvert.setObjectName("btnConvert")
        ConvertWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ConvertWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 584, 23))
        self.menubar.setObjectName("menubar")
        self.menuOperation = QtWidgets.QMenu(self.menubar)
        self.menuOperation.setObjectName("menuOperation")
        ConvertWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ConvertWindow)
        self.statusbar.setObjectName("statusbar")
        ConvertWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuOperation.menuAction())

        self.retranslateUi(ConvertWindow)
        QtCore.QMetaObject.connectSlotsByName(ConvertWindow)

    def retranslateUi(self, ConvertWindow):
        _translate = QtCore.QCoreApplication.translate
        ConvertWindow.setWindowTitle(_translate("ConvertWindow", "Converter Window"))
        self.groupBox.setTitle(_translate("ConvertWindow", "Converter"))
        self.radioButton.setText(_translate("ConvertWindow", "ToThunder"))
        self.radioButton_2.setText(_translate("ConvertWindow", "ToLink"))
        self.btnConvert.setText(_translate("ConvertWindow", "Convert"))
        self.menuOperation.setTitle(_translate("ConvertWindow", "Operation"))
