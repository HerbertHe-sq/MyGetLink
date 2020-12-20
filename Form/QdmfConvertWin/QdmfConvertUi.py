# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QdmfConvertUi.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_QdmfConvertWin(object):
    def setupUi(self, QdmfConvertWin):
        QdmfConvertWin.setObjectName("QdmfConvertWin")
        QdmfConvertWin.resize(470, 130)
        self.centralwidget = QtWidgets.QWidget(QdmfConvertWin)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 61, 20))
        self.label.setObjectName("label")
        self.txtQdmfPath = QtWidgets.QTextEdit(self.centralwidget)
        self.txtQdmfPath.setGeometry(QtCore.QRect(80, 20, 375, 21))
        self.txtQdmfPath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtQdmfPath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtQdmfPath.setObjectName("txtQdmfPath")
        self.btnConvert = QtWidgets.QPushButton(self.centralwidget)
        self.btnConvert.setGeometry(QtCore.QRect(370, 50, 85, 23))
        self.btnConvert.setObjectName("btnConvert")
        self.btnSelPath = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelPath.setGeometry(QtCore.QRect(270, 50, 85, 23))
        self.btnSelPath.setObjectName("btnSelPath")
        QdmfConvertWin.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(QdmfConvertWin)
        self.statusBar.setObjectName("statusBar")
        QdmfConvertWin.setStatusBar(self.statusBar)

        self.retranslateUi(QdmfConvertWin)
        QtCore.QMetaObject.connectSlotsByName(QdmfConvertWin)

    def retranslateUi(self, QdmfConvertWin):
        _translate = QtCore.QCoreApplication.translate
        QdmfConvertWin.setWindowTitle(_translate("QdmfConvertWin", "MainWindow"))
        self.label.setText(_translate("QdmfConvertWin", "QDMF File:"))
        self.btnConvert.setText(_translate("QdmfConvertWin", "Save As"))
        self.btnSelPath.setText(_translate("QdmfConvertWin", "Select File"))
