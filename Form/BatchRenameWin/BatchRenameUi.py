# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BatchRenameUi.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_BatchRenameWin(object):
    def setupUi(self, BatchRenameWin):
        BatchRenameWin.setObjectName("BatchRenameWin")
        BatchRenameWin.resize(492, 554)
        self.centralwidget = QtWidgets.QWidget(BatchRenameWin)
        self.centralwidget.setObjectName("centralwidget")
        self.btnSelect = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelect.setGeometry(QtCore.QRect(10, 10, 91, 23))
        self.btnSelect.setObjectName("btnSelect")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(10, 50, 471, 351))
        self.listView.setObjectName("listView")
        self.btnSelectFolder = QtWidgets.QPushButton(self.centralwidget)
        self.btnSelectFolder.setGeometry(QtCore.QRect(110, 10, 91, 23))
        self.btnSelectFolder.setObjectName("btnSelectFolder")
        self.btnChange = QtWidgets.QPushButton(self.centralwidget)
        self.btnChange.setGeometry(QtCore.QRect(394, 470, 91, 23))
        self.btnChange.setObjectName("btnChange")
        self.txtFirst = QtWidgets.QTextEdit(self.centralwidget)
        self.txtFirst.setGeometry(QtCore.QRect(90, 410, 391, 21))
        self.txtFirst.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtFirst.setObjectName("txtFirst")
        self.txtSecond = QtWidgets.QTextEdit(self.centralwidget)
        self.txtSecond.setGeometry(QtCore.QRect(90, 440, 391, 21))
        self.txtSecond.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtSecond.setObjectName("txtSecond")
        self.lab1 = QtWidgets.QLabel(self.centralwidget)
        self.lab1.setGeometry(QtCore.QRect(20, 410, 61, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.lab1.setFont(font)
        self.lab1.setObjectName("lab1")
        self.lab2 = QtWidgets.QLabel(self.centralwidget)
        self.lab2.setGeometry(QtCore.QRect(20, 440, 61, 21))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        self.lab2.setFont(font)
        self.lab2.setObjectName("lab2")
        BatchRenameWin.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(BatchRenameWin)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 492, 23))
        self.menubar.setObjectName("menubar")
        self.menuOperation = QtWidgets.QMenu(self.menubar)
        self.menuOperation.setObjectName("menuOperation")
        BatchRenameWin.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(BatchRenameWin)
        self.statusbar.setObjectName("statusbar")
        BatchRenameWin.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuOperation.menuAction())

        self.retranslateUi(BatchRenameWin)
        QtCore.QMetaObject.connectSlotsByName(BatchRenameWin)

    def retranslateUi(self, BatchRenameWin):
        _translate = QtCore.QCoreApplication.translate
        BatchRenameWin.setWindowTitle(_translate("BatchRenameWin", "Batch Rename"))
        self.btnSelect.setText(_translate("BatchRenameWin", "Select File"))
        self.btnSelectFolder.setText(_translate("BatchRenameWin", "Select Folder"))
        self.btnChange.setText(_translate("BatchRenameWin", "Batch Rename"))
        self.lab1.setText(_translate("BatchRenameWin", "Target"))
        self.lab2.setText(_translate("BatchRenameWin", "Replace"))
        self.menuOperation.setTitle(_translate("BatchRenameWin", "Operation"))
