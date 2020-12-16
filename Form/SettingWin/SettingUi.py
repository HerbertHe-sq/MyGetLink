# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SettingUi.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SetWindow(object):
    def setupUi(self, SetWindow):
        SetWindow.setObjectName("SetWindow")
        SetWindow.resize(615, 184)
        self.centralwidget = QtWidgets.QWidget(SetWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 12, 91, 16))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.txtPath = QtWidgets.QTextEdit(self.centralwidget)
        self.txtPath.setGeometry(QtCore.QRect(110, 10, 401, 21))
        self.txtPath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtPath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtPath.setObjectName("txtPath")
        self.btnSelThPath = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelThPath.setGeometry(QtCore.QRect(520, 9, 81, 23))
        self.btnSelThPath.setObjectName("btnSelThPath")
        self.btnEnter = QtWidgets.QPushButton(self.centralwidget)
        self.btnEnter.setGeometry(QtCore.QRect(430, 130, 75, 23))
        self.btnEnter.setObjectName("btnEnter")
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget)
        self.btnCancel.setGeometry(QtCore.QRect(520, 130, 81, 23))
        self.btnCancel.setObjectName("btnCancel")
        self.txtPath2 = QtWidgets.QTextEdit(self.centralwidget)
        self.txtPath2.setGeometry(QtCore.QRect(110, 48, 401, 21))
        self.txtPath2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtPath2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtPath2.setObjectName("txtPath2")
        self.btnSelThPath2 = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelThPath2.setGeometry(QtCore.QRect(520, 47, 81, 23))
        self.btnSelThPath2.setObjectName("btnSelThPath2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 91, 16))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.cboThread = QtWidgets.QComboBox(self.centralwidget)
        self.cboThread.setGeometry(QtCore.QRect(110, 90, 69, 22))
        self.cboThread.setObjectName("cboThread")
        self.cboThread.addItem("")
        self.cboThread.addItem("")
        self.cboThread.addItem("")
        self.cboThread.addItem("")
        self.cboThread.addItem("")
        self.cboThread.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 91, 16))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        SetWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SetWindow)
        self.statusbar.setObjectName("statusbar")
        SetWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SetWindow)
        QtCore.QMetaObject.connectSlotsByName(SetWindow)

    def retranslateUi(self, SetWindow):
        _translate = QtCore.QCoreApplication.translate
        SetWindow.setWindowTitle(_translate("SetWindow", "Setting Window"))
        self.label.setText(_translate("SetWindow", "Thunder Path"))
        self.btnSelThPath.setText(_translate("SetWindow", "Select"))
        self.btnEnter.setText(_translate("SetWindow", "Confirm"))
        self.btnCancel.setText(_translate("SetWindow", "Cancel"))
        self.btnSelThPath2.setText(_translate("SetWindow", "Select"))
        self.label_2.setText(_translate("SetWindow", "PotPlayer Path"))
        self.cboThread.setItemText(0, _translate("SetWindow", "3"))
        self.cboThread.setItemText(1, _translate("SetWindow", "4"))
        self.cboThread.setItemText(2, _translate("SetWindow", "5"))
        self.cboThread.setItemText(3, _translate("SetWindow", "6"))
        self.cboThread.setItemText(4, _translate("SetWindow", "7"))
        self.cboThread.setItemText(5, _translate("SetWindow", "8"))
        self.label_3.setText(_translate("SetWindow", "Thread Count"))
