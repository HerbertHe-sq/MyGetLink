# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainUi.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(861, 660)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 861, 615))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.imgMovie = QtWidgets.QLabel(self.tab)
        self.imgMovie.setGeometry(QtCore.QRect(710, 10, 131, 151))
        self.imgMovie.setText("")
        self.imgMovie.setObjectName("imgMovie")
        self.listView = QtWidgets.QListView(self.tab)
        self.listView.setGeometry(QtCore.QRect(10, 70, 691, 91))
        self.listView.setObjectName("listView")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(9, 9, 691, 51))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.btnGetLink = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnGetLink.setObjectName("btnGetLink")
        self.gridLayout.addWidget(self.btnGetLink, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.cboList = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cboList.setObjectName("cboList")
        self.gridLayout.addWidget(self.cboList, 0, 1, 1, 1)
        self.txtName = QtWidgets.QTextEdit(self.gridLayoutWidget)
        self.txtName.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtName.setObjectName("txtName")
        self.gridLayout.addWidget(self.txtName, 1, 1, 1, 1)
        self.btnSearchAll = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btnSearchAll.setObjectName("btnSearchAll")
        self.gridLayout.addWidget(self.btnSearchAll, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.cboFind = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.cboFind.setObjectName("cboFind")
        self.gridLayout.addWidget(self.cboFind, 0, 3, 1, 2)
        self.gridLayout.setColumnMinimumWidth(2, 150)
        self.gridLayout.setColumnMinimumWidth(3, 50)
        self.gridLayout.setColumnMinimumWidth(4, 100)
        self.txtMsg = QtWidgets.QTextEdit(self.tab)
        self.txtMsg.setGeometry(QtCore.QRect(10, 170, 831, 371))
        self.txtMsg.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txtMsg.setObjectName("txtMsg")
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setGeometry(QtCore.QRect(10, 550, 831, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_3 = QtWidgets.QLabel(self.tab_2)
        self.label_3.setGeometry(QtCore.QRect(10, 11, 54, 16))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.txtHdKey = QtWidgets.QTextEdit(self.tab_2)
        self.txtHdKey.setGeometry(QtCore.QRect(60, 10, 301, 21))
        self.txtHdKey.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtHdKey.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtHdKey.setObjectName("txtHdKey")
        self.btnSearchHd = QtWidgets.QPushButton(self.tab_2)
        self.btnSearchHd.setGeometry(QtCore.QRect(514, 10, 131, 23))
        self.btnSearchHd.setObjectName("btnSearchHd")
        self.listView_2 = QtWidgets.QListView(self.tab_2)
        self.listView_2.setGeometry(QtCore.QRect(10, 40, 641, 161))
        self.listView_2.setObjectName("listView_2")
        self.txtMsgHd = QtWidgets.QTextEdit(self.tab_2)
        self.txtMsgHd.setGeometry(QtCore.QRect(10, 210, 831, 371))
        self.txtMsgHd.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txtMsgHd.setObjectName("txtMsgHd")
        self.labHdImg = QtWidgets.QLabel(self.tab_2)
        self.labHdImg.setGeometry(QtCore.QRect(660, 10, 180, 190))
        self.labHdImg.setText("")
        self.labHdImg.setObjectName("labHdImg")
        self.cboHdEngine = QtWidgets.QComboBox(self.tab_2)
        self.cboHdEngine.setGeometry(QtCore.QRect(370, 10, 131, 22))
        self.cboHdEngine.setObjectName("cboHdEngine")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.pbBarBt = QtWidgets.QProgressBar(self.tab_4)
        self.pbBarBt.setGeometry(QtCore.QRect(10, 550, 841, 23))
        self.pbBarBt.setProperty("value", 0)
        self.pbBarBt.setObjectName("pbBarBt")
        self.listViewBt = QtWidgets.QListView(self.tab_4)
        self.listViewBt.setGeometry(QtCore.QRect(10, 10, 571, 351))
        self.listViewBt.setObjectName("listViewBt")
        self.txtBtMsg = QtWidgets.QTextEdit(self.tab_4)
        self.txtBtMsg.setGeometry(QtCore.QRect(10, 365, 838, 181))
        self.txtBtMsg.setObjectName("txtBtMsg")
        self.groupBox = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox.setGeometry(QtCore.QRect(590, 10, 261, 111))
        self.groupBox.setObjectName("groupBox")
        self.txtBtKey = QtWidgets.QTextEdit(self.groupBox)
        self.txtBtKey.setGeometry(QtCore.QRect(50, 20, 201, 21))
        self.txtBtKey.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtBtKey.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtBtKey.setObjectName("txtBtKey")
        self.cboBtEngine = QtWidgets.QComboBox(self.groupBox)
        self.cboBtEngine.setGeometry(QtCore.QRect(50, 50, 201, 22))
        self.cboBtEngine.setObjectName("cboBtEngine")
        self.btnSearchBt = QtWidgets.QPushButton(self.groupBox)
        self.btnSearchBt.setGeometry(QtCore.QRect(140, 80, 111, 23))
        self.btnSearchBt.setObjectName("btnSearchBt")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(5, 20, 41, 20))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(5, 52, 41, 16))
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.cboTvEngine = QtWidgets.QComboBox(self.tab_3)
        self.cboTvEngine.setGeometry(QtCore.QRect(580, 10, 181, 22))
        self.cboTvEngine.setObjectName("cboTvEngine")
        self.txtMsgTv = QtWidgets.QTextEdit(self.tab_3)
        self.txtMsgTv.setGeometry(QtCore.QRect(6, 310, 845, 271))
        self.txtMsgTv.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.txtMsgTv.setObjectName("txtMsgTv")
        self.listTvPlace = QtWidgets.QListView(self.tab_3)
        self.listTvPlace.setGeometry(QtCore.QRect(6, 10, 151, 291))
        self.listTvPlace.setObjectName("listTvPlace")
        self.listTvLive = QtWidgets.QListView(self.tab_3)
        self.listTvLive.setGeometry(QtCore.QRect(165, 10, 401, 291))
        self.listTvLive.setObjectName("listTvLive")
        self.btnTvSearch = QtWidgets.QPushButton(self.tab_3)
        self.btnTvSearch.setGeometry(QtCore.QRect(770, 10, 81, 23))
        self.btnTvSearch.setObjectName("btnTvSearch")
        self.labTvImg = QtWidgets.QLabel(self.tab_3)
        self.labTvImg.setGeometry(QtCore.QRect(580, 40, 261, 261))
        self.labTvImg.setText("")
        self.labTvImg.setObjectName("labTvImg")
        self.tabWidget.addTab(self.tab_3, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 861, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuOpen_Thunder = QtWidgets.QMenu(self.menu)
        self.menuOpen_Thunder.setObjectName("menuOpen_Thunder")
        self.menuConverter = QtWidgets.QMenu(self.menubar)
        self.menuConverter.setObjectName("menuConverter")
        self.menuM3U8_Downloader = QtWidgets.QMenu(self.menuConverter)
        self.menuM3U8_Downloader.setObjectName("menuM3U8_Downloader")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuTheme = QtWidgets.QMenu(self.menuAbout)
        self.menuTheme.setObjectName("menuTheme")
        self.menuLanguage = QtWidgets.QMenu(self.menubar)
        self.menuLanguage.setObjectName("menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_As = QtWidgets.QAction(MainWindow)
        self.actionSave_As.setObjectName("actionSave_As")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.actionThunder_Link = QtWidgets.QAction(MainWindow)
        self.actionThunder_Link.setObjectName("actionThunder_Link")
        self.actionDownload_Bt = QtWidgets.QAction(MainWindow)
        self.actionDownload_Bt.setObjectName("actionDownload_Bt")
        self.actionAbout_Us = QtWidgets.QAction(MainWindow)
        self.actionAbout_Us.setObjectName("actionAbout_Us")
        self.actionSetting = QtWidgets.QAction(MainWindow)
        self.actionSetting.setObjectName("actionSetting")
        self.actionVip_Converter = QtWidgets.QAction(MainWindow)
        self.actionVip_Converter.setObjectName("actionVip_Converter")
        self.actionPotPlayer = QtWidgets.QAction(MainWindow)
        self.actionPotPlayer.setObjectName("actionPotPlayer")
        self.actionThunder = QtWidgets.QAction(MainWindow)
        self.actionThunder.setObjectName("actionThunder")
        self.actionVip_Downloader = QtWidgets.QAction(MainWindow)
        self.actionVip_Downloader.setObjectName("actionVip_Downloader")
        self.actionRead_File = QtWidgets.QAction(MainWindow)
        self.actionRead_File.setObjectName("actionRead_File")
        self.actionGet_M3U8 = QtWidgets.QAction(MainWindow)
        self.actionGet_M3U8.setObjectName("actionGet_M3U8")
        self.actionBatchDownloader = QtWidgets.QAction(MainWindow)
        self.actionBatchDownloader.setObjectName("actionBatchDownloader")
        self.actionLanguage1 = QtWidgets.QAction(MainWindow)
        self.actionLanguage1.setObjectName("actionLanguage1")
        self.actionLanguage2 = QtWidgets.QAction(MainWindow)
        self.actionLanguage2.setObjectName("actionLanguage2")
        self.actionLanguage3 = QtWidgets.QAction(MainWindow)
        self.actionLanguage3.setObjectName("actionLanguage3")
        self.actionBatch_Rename = QtWidgets.QAction(MainWindow)
        self.actionBatch_Rename.setObjectName("actionBatch_Rename")
        self.actionDark_Theme = QtWidgets.QAction(MainWindow)
        self.actionDark_Theme.setObjectName("actionDark_Theme")
        self.actionNative_Theme = QtWidgets.QAction(MainWindow)
        self.actionNative_Theme.setObjectName("actionNative_Theme")
        self.menuOpen_Thunder.addAction(self.actionPotPlayer)
        self.menuOpen_Thunder.addAction(self.actionThunder)
        self.menu.addAction(self.actionSave_As)
        self.menu.addAction(self.actionClear)
        self.menu.addAction(self.menuOpen_Thunder.menuAction())
        self.menu.addAction(self.actionDownload_Bt)
        self.menu.addAction(self.actionSetting)
        self.menu.addAction(self.actionBatch_Rename)
        self.menuM3U8_Downloader.addAction(self.actionRead_File)
        self.menuM3U8_Downloader.addAction(self.actionGet_M3U8)
        self.menuM3U8_Downloader.addAction(self.actionBatchDownloader)
        self.menuConverter.addAction(self.actionThunder_Link)
        self.menuConverter.addAction(self.actionVip_Converter)
        self.menuConverter.addAction(self.actionVip_Downloader)
        self.menuConverter.addAction(self.menuM3U8_Downloader.menuAction())
        self.menuTheme.addAction(self.actionDark_Theme)
        self.menuTheme.addAction(self.actionNative_Theme)
        self.menuAbout.addAction(self.actionAbout_Us)
        self.menuAbout.addAction(self.menuTheme.menuAction())
        self.menuLanguage.addAction(self.actionLanguage1)
        self.menuLanguage.addAction(self.actionLanguage2)
        self.menuLanguage.addAction(self.actionLanguage3)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuConverter.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnGetLink.setText(_translate("MainWindow", "Search"))
        self.label_2.setText(_translate("MainWindow", "Name"))
        self.btnSearchAll.setText(_translate("MainWindow", "Search All"))
        self.label.setText(_translate("MainWindow", "Type"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Common Engine"))
        self.label_3.setText(_translate("MainWindow", "Name"))
        self.btnSearchHd.setText(_translate("MainWindow", "Search"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "HD Engine"))
        self.groupBox.setTitle(_translate("MainWindow", "Search"))
        self.btnSearchBt.setText(_translate("MainWindow", "Search"))
        self.label_4.setText(_translate("MainWindow", "Key"))
        self.label_5.setText(_translate("MainWindow", "Engine"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "BT Engine"))
        self.btnTvSearch.setText(_translate("MainWindow", "Search"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Live TV source"))
        self.menu.setTitle(_translate("MainWindow", "Operation"))
        self.menuOpen_Thunder.setTitle(_translate("MainWindow", "Open Application"))
        self.menuConverter.setTitle(_translate("MainWindow", "Converter"))
        self.menuM3U8_Downloader.setTitle(_translate("MainWindow", "M3U8 Downloader"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.menuTheme.setTitle(_translate("MainWindow", "Theme"))
        self.menuLanguage.setTitle(_translate("MainWindow", "Language(语言)"))
        self.actionSave_As.setText(_translate("MainWindow", "Save As"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))
        self.actionThunder_Link.setText(_translate("MainWindow", "Thunder Link"))
        self.actionDownload_Bt.setText(_translate("MainWindow", "Download Bt"))
        self.actionAbout_Us.setText(_translate("MainWindow", "About Us"))
        self.actionSetting.setText(_translate("MainWindow", "Setting"))
        self.actionVip_Converter.setText(_translate("MainWindow", "Vip Converter"))
        self.actionPotPlayer.setText(_translate("MainWindow", "PotPlayer"))
        self.actionThunder.setText(_translate("MainWindow", "Thunder"))
        self.actionVip_Downloader.setText(_translate("MainWindow", "Vip Downloader"))
        self.actionRead_File.setText(_translate("MainWindow", "Read M3U8 File"))
        self.actionGet_M3U8.setText(_translate("MainWindow", "Get M3U8"))
        self.actionBatchDownloader.setText(_translate("MainWindow", "Batch Downloader"))
        self.actionLanguage1.setText(_translate("MainWindow", "简体中文"))
        self.actionLanguage2.setText(_translate("MainWindow", "繁體中文"))
        self.actionLanguage3.setText(_translate("MainWindow", "English"))
        self.actionBatch_Rename.setText(_translate("MainWindow", "Batch Rename"))
        self.actionDark_Theme.setText(_translate("MainWindow", "Dark Theme"))
        self.actionNative_Theme.setText(_translate("MainWindow", "Native Theme"))
