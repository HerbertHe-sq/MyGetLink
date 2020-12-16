# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VipConUi.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_VipConWindow(object):
    def setupUi(self, VipConWindow):
        VipConWindow.setObjectName("VipConWindow")
        VipConWindow.resize(560, 240)
        self.centralwidget = QtWidgets.QWidget(VipConWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnConvert = QtWidgets.QPushButton(self.centralwidget)
        self.btnConvert.setGeometry(QtCore.QRect(470, 50, 81, 23))
        self.btnConvert.setObjectName("btnConvert")
        self.txtVideo = QtWidgets.QTextEdit(self.centralwidget)
        self.txtVideo.setGeometry(QtCore.QRect(10, 50, 448, 71))
        self.txtVideo.setObjectName("txtVideo")
        self.txtTagVideo = QtWidgets.QTextEdit(self.centralwidget)
        self.txtTagVideo.setGeometry(QtCore.QRect(10, 130, 448, 71))
        self.txtTagVideo.setObjectName("txtTagVideo")
        self.cboEngine = QtWidgets.QComboBox(self.centralwidget)
        self.cboEngine.setGeometry(QtCore.QRect(70, 10, 483, 20))
        self.cboEngine.setObjectName("cboEngine")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 50, 20))
        self.label.setMaximumSize(QtCore.QSize(50, 16777215))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        VipConWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(VipConWindow)
        self.statusbar.setObjectName("statusbar")
        VipConWindow.setStatusBar(self.statusbar)

        self.retranslateUi(VipConWindow)
        QtCore.QMetaObject.connectSlotsByName(VipConWindow)

    def retranslateUi(self, VipConWindow):
        _translate = QtCore.QCoreApplication.translate
        VipConWindow.setWindowTitle(_translate("VipConWindow", "Vip Converter"))
        self.btnConvert.setText(_translate("VipConWindow", "Convert"))
        self.label.setText(_translate("VipConWindow", "Engine"))
