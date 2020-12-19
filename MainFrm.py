import sys
import win32api
import win32con
import win32ui
import threading
import time
import os
import pyperclip

from PyQt5.QtCore import QStringListModel, Qt, pyqtSignal, QPoint, QTranslator
from PyQt5.QtGui import QIcon, QTextCursor, QImage, QPixmap, QCursor, QPainter
from PyQt5.QtWidgets import QMenu, QApplication, QStyleOption, QStyle, QMainWindow, QTextEdit, QSystemTrayIcon, QAction, \
    QPushButton

from MainUi import Ui_MainWindow
from PyQt5 import QtWidgets, QtCore, QtGui
from Function.CommonEng.GetLink import GetLink
from Function.CommonEng.GetLinkSec import GetLinkSec
from Function.CommonEng.GetLinkBt import GetLinkBt
from Function.CommonEng.GetLinkPan import GetLinkPan
from Function.CommonEng.GetLinkDy import GetLinkDy
from Function.CommonEng.GetLinkPanSo import GetLinkPanSo
from Function.CommonEng.GetLinkEs import GetLinkEs
from Function.CommonEng.GetLinkfNet import GetLinkfNet
from Function.CommonEng.GetLinkXplay import GetLinkXplay
from Function.CommonEng.GetLinkFfhk import GetLinkFfhk
from Function.CommonEng.GetLinkWlxf import GetLinkWlxf
from Function.CommonEng.GetLinkNfMov import GetLinkNfMov
from Function.CommonEng.GetLinkPiaoHua import GetLinkPiaoHua
from Function.CommonEng.GetLinkGj import GetLinkGj
from Function.HdEng.GetLinkHdHq import GetLinkHdHq
from Function.HdEng.GetLinkIqiyi import GetLinkIqiyi
from Function.HdEng.GetLinkTenv import GetLinkTenv
from Function.TvEng.GetLinkLiveSS import GetLinkLiveSS
from Function.TvEng.GetLinkLiveLS import GetLinkLiveLS
from Function.TvEng.GetLinkLiveIVI import GetLinkLiveIVI
from Function.TvEng.GetLinkLiveOtop import GetLinkLiveOtop
from Function.TvEng.GetLinkLiveQhtv import GetLinkLiveQhtv
from Function.TvEng.GetLinkLiveYsou import GetLinkLiveYsou
from Function.TvEng.GetLinkTvEye import GetLinkTvEye
from Function.BtEng.GetLinkZZS import GetLinkZZS
from Function.BtEng.GetLinkBtMov import GetLinkBtMov
from Function.StopThread import StopThread
from Function.OperateIniFile import OperateIniFile
from Form.ConvertWin.ConverterFrm import ConverterWindow
from Form.AboutWin.AboutFrm import AboutWindow
from Form.SettingWin.SettingFrm import SettingWindow
from Form.VipConWin.VipConvertFrm import VConvertWindow
from Form.VipDownWin.VipDownFrm import VDownWindow
from Form.BatchDownWin.BatchDownFrm import BatchDownWindow
from Form.BatchRenameWin.BatchRenameFrm import BatchRenameWindow
from Function.ApplicationList import AppList
from Function.QssHelper import QssHelper

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    signal = QtCore.pyqtSignal(str)     #txtMsg.append()
    signal2 = QtCore.pyqtSignal(str)    #txtMsg.setText()
    signal_list = QtCore.pyqtSignal()
    signal_list_hd = QtCore.pyqtSignal()
    signal_msg_hd = QtCore.pyqtSignal(str)  # txtMsg.setText()
    signal_msg_set_hd = QtCore.pyqtSignal(str)  # txtMsg.setText()

    signal_list_bt = QtCore.pyqtSignal()
    signal_msg_bt = QtCore.pyqtSignal(str)  # BT搜索
    signal_msg_set_bt = QtCore.pyqtSignal(str)

    signal_list_addr = QtCore.pyqtSignal()   #地区
    signal_list_tv = QtCore.pyqtSignal()     #台名
    signal_msg_tv = QtCore.pyqtSignal(str)  # txtMsg.setText()
    signal_msg_set_tv = QtCore.pyqtSignal(str)  # txtMsg.setText()


    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("My GetLink Tool")
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint|QtCore.Qt.WindowMinimizeButtonHint)  # 窗体没有最大化最小化按钮
        self.setFixedSize(860, 660)            #设置窗体的大小
        # self.appPath = self.GetAppPath()+"\\"  # 路径修改、调试可修改回来
        self.appPath = ""
        self.setWindowIcon(QIcon(self.appPath+"./Image/Icon_GetSource.png"))
        self._AddListContextMenu() #添加右键菜单
        self._AddTextContextMenu()

        self._ResisterEvent()      #注册事件

        self.seaEngines = []  #切换搜索引擎
        self.seaEnginesHd =[]
        self.seaEnginesTv = []
        self.seaEnginesBt = []
        self.gobalNameArr = []  # 默认参数
        self.gobalArr = []      # 默认参数
        self.gobalUrlArr = []   #存放网址
        self.downWinArr = []    #下载窗口对象
        self.downWinOFgArr = [0,0,0,0,0,0,0,0] # 下载窗口打开标志位
        self.ReadInitFile()
        self.cboList.addItems(self.gobalNameArr)

        #建立相应的对象
        self.CreateSearchEle()

        #清空列表
        self.qList = []
        self.qListHd=[]

        #直播源列表
        self.qListAddr = []
        self.qListTv = []

        #BT列表
        self.qListBt = []

        self.getLinkFlag = 0  # 获取标志位
        self.conOpenFg = 0    #窗体是否打开标志位
        self.vipDownOpenFg = 0

        self._BindingSignal() #绑定UI更新

        self.thGetLink = threading.Thread(target=self.MyGetLinkTask)
        self.thGetLink.setDaemon(False)
        self.thGetLink.start()

        self.CreateTraySystem() #创建最小化托盘

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Question, self.tr("提示"),self.tr("确定要退出吗？"), QtWidgets.QMessageBox.NoButton, self)
        btnExit = QPushButton("是的我要退出")
        btnExit.setProperty('name', 'btnTray')
        btnMin = QPushButton("最小化到托盘")
        btnMin.setProperty('name', 'btnTray')
        reply.addButton(btnExit, QtWidgets.QMessageBox.YesRole)
        reply.addButton(btnMin, QtWidgets.QMessageBox.NoRole)
        reply.exec_()
        if reply.clickedButton() == btnExit:
            event.accept()
            self.CloseThead()
            self.tray.deleteLater()
            QtWidgets.qApp.quit()
        else:
            event.ignore()
            self.hide()
            self.CloseForm(0, 0)


    def ShowWindow(self):
        self.show()

    def CreateTraySystem(self):
        self.tray = QSystemTrayIcon() #创建系统托盘对象
        self.tray.setToolTip("My GetLink Tool")
        self.tray.setIcon(QIcon(self.appPath+"./Image/Icon_GetSource.png"))
        self.trayMenu = QMenu(QApplication.desktop()) #创建菜单
        self.menuOpenTray = QAction('打开(O)', self, triggered=self.MenuOpenTray_Click) #添加一级菜单动作选项(还原主窗口)
        self.menuExitTray = QAction('退出(E)', self, triggered=self.MenuExitTray_Click) #添加一级菜单动作选项(退出程序)
        self.trayMenu.addAction(self.menuOpenTray) #为菜单添加动作
        self.trayMenu.addAction(self.menuExitTray)
        self.tray.setContextMenu(self.trayMenu) #设置系统托盘菜单
        self.tray.activated.connect(self.TrayIcon_Click)
        self.tray.show()

    def TrayIcon_Click(self,reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2:
            self.showNormal()
            self.activateWindow()
            self.CloseForm(0, 1)

    def MenuOpenTray_Click(self):
        self.showNormal()
        self.activateWindow()
        self.CloseForm(0, 1)

    def MenuExitTray_Click(self):
        self.tray.deleteLater()
        self.CloseThead()
        QtWidgets.qApp.quit()

    def CloseThead(self):
        if self.conOpenFg==1:
            self.conWin.close()
        if self.vipDownOpenFg==1:
            self.vipDownWin.close()

        try:
            StopThread(self.vipDownWin.thDownFile)  # 关闭爬取线程
            StopThread(self.vipDownWin.thDownTask1)  # 关闭爬取线程
            StopThread(self.vipDownWin.thDownTask2)  # 关闭爬取线程
            StopThread(self.vipDownWin.thDownTask3)  # 关闭爬取线程
            StopThread(self.vipDownWin.thDownTask4)  # 关闭爬取线程
            StopThread(self.vipDownWin.thDownTask5)  # 关闭爬取线程
            StopThread(self.vipDownWin.thDownTask6)  # 关闭爬取线程
            StopThread(self.vipDownWin.thDownTask7)  # 关闭爬取线程
            StopThread(self.vipDownWin.thDownTask8)  # 关闭爬取线程
        except Exception as msg:
            print(msg)
        StopThread(self.thGetLink)#关闭爬取线程

    def CloseForm(self,index,flag):
        try:
            for i in range(index,8):
                if i==0:
                    if flag==0:
                        self.aboutWin.hide()
                    else:
                        self.aboutWin.showNormal()
                        self.aboutWin.activateWindow()
                elif i==1:
                    if flag==0:
                        self.batchDownWin.hide()
                    else:
                        self.batchDownWin.showNormal()
                        self.batchDownWin.activateWindow()
                elif i == 2:
                    if flag == 0:
                        self.batRenameWin.hide()
                    else:
                        self.batRenameWin.showNormal()
                        self.batRenameWin.activateWindow()
                elif i == 3:
                    if flag == 0:
                        self.conWin.hide()
                    else:
                        self.conWin.showNormal()
                        self.conWin.activateWindow()
                elif i == 4:
                    if flag == 0:
                        self.setWin.hide()
                    else:
                        self.setWin.showNormal()
                        self.setWin.activateWindow()
                elif i == 5:
                    if flag == 0:
                        self.vipConWin.hide()
                    else:
                        self.vipConWin.showNormal()
                        self.vipConWin.activateWindow()
                elif i == 6:
                    if flag == 0:
                        self.vipDownWin.hide()
                    else:
                        self.vipDownWin.showNormal()
                        self.vipDownWin.activateWindow()
                elif i==7:
                    d_win_count = len(self.downWinArr)
                    for a_i in range(0, d_win_count):
                        if flag == 0:
                            self.downWinArr[a_i].hide()
                        else:
                            self.downWinArr[a_i].showNormal()
                            self.downWinArr[a_i].activateWindow()
                else:
                    pass
        except Exception as msg:
            self.CloseForm(index+1,flag)


    #注册事件
    def _ResisterEvent(self):
        self.btnGetLink.clicked.connect(self.BtnGetLink)
        self.btnSearchAll.clicked.connect(self.BtnSearchAll)
        self.btnSearchHd.clicked.connect(self.BtnSearchHd_Click)
        self.btnTvSearch.clicked.connect(self.BtnSerachTv_Click)
        self.btnSearchBt.clicked.connect(self.BtnSearchBt_Click)
        self.listView.clicked.connect(self.ListViewClick)
        self.listView_2.clicked.connect(self.ListViewHd_Click)
        self.listTvPlace.clicked.connect(self.ListViewAddr_Click)
        self.listTvLive.clicked.connect(self.ListViewLive_Click)
        self.listViewBt.clicked.connect(self.ListViewBt_Click)
        self.actionClear.triggered.connect(self.MenuClearClick)
        self.actionSave_As.triggered.connect(self.MenuSaveClick)
        self.actionThunder_Link.triggered.connect(self.MenuThLink_Click)
        self.actionPotPlayer.triggered.connect(self.MenuOpenPot_Click)
        self.actionThunder.triggered.connect(self.MenuOpenAppClick)
        self.actionDownload_Bt.triggered.connect(self.MenuDownBt_Click)
        self.actionAbout_Us.triggered.connect(self.MenuAboutUs_Click)
        self.actionSetting.triggered.connect(self.MenuSetting_Click)
        self.actionBatch_Rename.triggered.connect(self.MenuRename_Click)
        self.actionVip_Converter.triggered.connect(self.MenuVipCon_Click)
        self.actionVip_Downloader.triggered.connect(self.MenuVipDown_Click)
        self.actionGet_M3U8.triggered.connect(self.MenuGetM3U8_Click)
        self.actionRead_File.triggered.connect(self.MenuReadFile_Click)
        self.actionBatchDownloader.triggered.connect(self.MenuBatchDown_Click)
        self.actionLanguage1.triggered.connect(lambda: self.MenuLangChange(1))
        self.actionLanguage2.triggered.connect(lambda: self.MenuLangChange(2))
        self.actionLanguage3.triggered.connect(lambda: self.MenuLangChange(3))
        self.actionNative_Theme.triggered.connect(lambda: self.MenuTheme_Click(1))
        self.actionDark_Theme.triggered.connect(lambda: self.MenuTheme_Click(2))
        #self.txtMsgHd.grabKeyboard()

     #绑定信号
    def _BindingSignal(self):
        self.signal.connect(self.UpdateTextMsg)  # 主线程
        self.signal2.connect(self.SetTextMsg)
        self.signal_list.connect(self.UpdateListView)  # 更新ListView
        self.signal_list_hd.connect(self.UpdateListView_Hd)
        self.signal_msg_hd.connect(self.UpdateTextMsg_Hd)
        self.signal_msg_set_hd.connect(self.SetTextMsg_Hd)

        self.signal_list_addr.connect(self.UpdateListView_Addr)
        self.signal_list_tv.connect(self.UpdateListView_Tv)
        self.signal_msg_tv.connect(self.UpdateTextMsg_Tv)
        self.signal_msg_set_tv.connect(self.SetTextMsg_Tv)

        self.signal_list_bt.connect(self.UpdateListView_BT)
        self.signal_msg_bt.connect(self.UpdateTextMsg_Bt)
        self.signal_msg_set_bt.connect(self.SetTextMsg_Bt)

    #设置样式
    def _SetControlProperty(self):
        self.menu.setProperty('name', 'menu')

        self.btnGetLink.setProperty('name', 'btnGetLink')
        self.btnSearchAll.setProperty('name', 'btnSearchAll')
        self.btnSearchHd.setProperty('name', 'btnSearchHd')
        self.btnTvSearch.setProperty('name', 'btnTvSearch')
        self.btnSearchBt.setProperty('name', 'btnSearchBt')
        self.txtName.setProperty('name', 'txtName')
        self.txtMsg.setProperty('name', 'txtMsg')
        self.txtBtMsg.setProperty('name', 'txtBtMsg')
        self.txtBtKey.setProperty('name', 'txtBtKey')
        self.txtHdKey.setProperty('name', 'txtHdKey')
        self.txtMsgHd.setProperty('name', 'txtMsgHd')
        self.txtMsgTv.setProperty('name', 'txtMsgTv')
        self.cboList.setProperty('name', 'cboList')
        self.cboFind.setProperty('name', 'cboFind')
        self.cboHdEngine.setProperty('name', 'cboHdEngine')
        self.cboTvEngine.setProperty('name', 'cboTvEngine')
        self.cboBtEngine.setProperty('name', 'cboBtEngine')
        self.listView.setProperty('name', 'listView')
        self.listViewBt.setProperty('name', 'listViewBt')
        self.listTvLive.setProperty('name', 'listTvLive')
        self.listTvPlace.setProperty('name', 'listTvPlace')
        self.listView_2.setProperty('name', 'listView_2')
        self.tabWidget.setProperty('name', 'tabWidget')
        self.tab.setProperty('name', 'tab')
        self.tab_2.setProperty('name', 'tab_2')
        self.tab_3.setProperty('name', 'tab_3')
        self.tab_4.setProperty('name', 'tab_4')
        self.label.setProperty('name', 'label')
        self.label_2.setProperty('name', 'label_2')
        self.label_3.setProperty('name', 'label_3')
        self.label_4.setProperty('name', 'label_4')
        self.label_5.setProperty('name', 'label_5')
        self.groupBox.setProperty('name', 'groupBox')
        self.progressBar.setProperty('name', 'progressBar')
        self.pbBarBt.setProperty('name', 'pbBarBt')



    def _SettingTheme(self,flag):
        if flag==1:
            scroll_style_path = './Qss/{0}/ScrollBarStyle.qss'.format('NativeTheme')
            self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format('NativeTheme')))
        else:
            self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format('NightTheme')))
            scroll_style_path = './Qss/{0}/ScrollBarStyle.qss'.format('NightTheme')

        self.txtMsg.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.txtBtMsg.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.txtMsgHd.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.txtMsgTv.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listView.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listViewBt.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listTvLive.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listTvPlace.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listView_2.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))

        self.txtMsg.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.txtBtMsg.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.txtMsgHd.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.txtMsgTv.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listView.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listViewBt.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listTvLive.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listTvPlace.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))
        self.listView_2.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_style_path))



    #添加右键菜单
    def _AddListContextMenu(self):
        self.listTvLive.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listTvLive.customContextMenuRequested[QPoint].connect(self.listTvWidgetContext)

        self.listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listView.customContextMenuRequested[QPoint].connect(self.listComWidgetContext)

    def listTvWidgetContext(self, point):
        popMenu = QMenu()
        self.listTvMenuSave = popMenu.addAction("Save As List")
        self.listTvMenuSave.triggered.connect(lambda: self.Menu_ListTv_Click(self.listTvMenuSave))
        popMenu.exec_(QCursor.pos())

    def listComWidgetContext(self, point):
        popMenu = QMenu()
        self.listTvMenuSaveQdf = popMenu.addAction("Export QDF File")
        self.listTvMenuSaveQdf.triggered.connect(lambda: self.Menu_ListTv_Click(self.listTvMenuSaveQdf))
        popMenu.exec_(QCursor.pos())

    def _AddTextContextMenu(self):
        self.txtMsg.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.txtMsg.customContextMenuRequested[QPoint].connect(self.TxtMsgWidgetContext)

    def TxtMsgWidgetContext(self, point):
        popMenu = QMenu()
        self.txtMsgDown = popMenu.addAction("DownLoad Video")
        self.txtMsgDown.triggered.connect(lambda: self.MenuTxtDown_Click(self.txtMsgDown))

        self.tvChannel = popMenu.addAction("Save As List")
        self.tvChannel.triggered.connect(lambda: self.MenuTvChannel_Click(self.tvChannel))

        self.txtDownList = popMenu.addAction("Send Data To List")
        self.txtDownList.triggered.connect(lambda: self.MenuDownList_Click(self.txtDownList))
        popMenu.exec_(QCursor.pos())

    # 建立相应搜搜对象
    def CreateSearchEle(self):
        self.myGetLink = GetLink()

        self.myGetLinkSec = GetLinkSec()
        self.myGetLinkSec.SetBaseUrl(self.gobalUrlArr[2])

        self.myGetLinkBt = GetLinkBt()
        self.myGetLinkBt.SetBaseUrl(self.gobalUrlArr[3])

        self.myGetLinkPan = GetLinkPan()
        self.myGetLinkPan.SetBaseUrl(self.gobalUrlArr[4])

        self.myGetLinkDy = GetLinkDy()
        self.myGetLinkDy.SetBaseUrl(self.gobalUrlArr[5])

        self.myGetLinkPanSo = GetLinkPanSo()
        self.myGetLinkPanSo.SetBaseUrl(self.gobalUrlArr[6])

        self.myGetLinkEs = GetLinkEs()
        self.myGetLinkEs.SetBaseUrl(self.gobalUrlArr[7])
        self.myGetLinkEs.SetEleUrl(self.gobalUrlArr[8])

        self.myGetLinkfNet = GetLinkfNet()
        self.myGetLinkfNet.SetBaseUrl(self.gobalUrlArr[9])

        self.myGetLinkXplay = GetLinkXplay()
        self.myGetLinkXplay.SetBaseUrl(self.gobalUrlArr[10])

        self.myGetLinkHdHq = GetLinkHdHq()
        self.myGetLinkHdHq.SetBaseUrl(self.gobalUrlArr[11])

        self.myGetLinkFfhk = GetLinkFfhk()
        self.myGetLinkFfhk.SetBaseUrl(self.gobalUrlArr[20])

        self.myGetLinkWlxf = GetLinkWlxf()

        self.myGetLinkNfMov = GetLinkNfMov()
        self.myGetLinkNfMov.SetBaseUrl(self.gobalUrlArr[35])

        self.myGetLinkPiaoHua = GetLinkPiaoHua()
        self.myGetLinkPiaoHua.SetBaseUrl(self.gobalUrlArr[36])

        self.myGetLinkGj = GetLinkGj()
        self.myGetLinkGj.SetBaseUrl(self.gobalUrlArr[39])
        self.myGetLinkGj.SetSearchUrl(self.gobalUrlArr[38])

        #建立TV对象
        self.myGetLinkLiveSs = GetLinkLiveSS()
        self.myGetLinkLiveSs.SetBaseSeaUrl(self.gobalUrlArr[12])
        self.myGetLinkLiveSs.SetBaseUrl(self.gobalUrlArr[13])

        self.myGetLinkLiveLs = GetLinkLiveLS()
        self.myGetLinkLiveLs.SetBaseSeaUrl(self.gobalUrlArr[14])
        self.myGetLinkLiveLs.SetBaseUrl(self.gobalUrlArr[15])
        self.myGetLinkLiveLs.SetSigUrl(self.gobalUrlArr[16])

        self.myGetLinkLiveIVI = GetLinkLiveIVI()
        self.myGetLinkLiveIVI.SetBaseUrl(self.gobalUrlArr[19])

        self.myGetLinkLiveOtop = GetLinkLiveOtop()
        self.myGetLinkLiveOtop.SetBaseUrl(self.gobalUrlArr[22])

        self.myGetLinkLiveQhtv = GetLinkLiveQhtv()
        self.myGetLinkLiveQhtv.SetBaseUrl(self.gobalUrlArr[23])

        self.myGetLinkLiveYsou = GetLinkLiveYsou()
        self.myGetLinkLiveYsou.SetBaseUrl(self.gobalUrlArr[24])

        self.myGetLinkTvEye = GetLinkTvEye()
        self.myGetLinkTvEye.SetBaseUrl(self.gobalUrlArr[27])

        #建立BT对象
        self.myGetLinkZZS= GetLinkZZS()
        self.myGetLinkZZS.SetBaseUrl(self.gobalUrlArr[17])

        self.myGetLinkBtMov = GetLinkBtMov()
        self.myGetLinkBtMov.SetBaseUrl(self.gobalUrlArr[32])
        self.myGetLinkBtMov.SetRootUrl(self.gobalUrlArr[33])

        self.myGetLinkIqiyi = GetLinkIqiyi()
        self.myGetLinkIqiyi.SetBaseUrl(self.gobalUrlArr[26])

        self.myGetLinkTenv = GetLinkTenv()
        self.myGetLinkTenv.SetBaseUrl(self.gobalUrlArr[31])


    # 键盘某个键被按下时调用
    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key()==Qt.Key_F7:
            if self.tabWidget.currentIndex()==1:
                pyperclip.copy(self.txtMsgHd.textCursor().selectedText())
            elif self.tabWidget.currentIndex()==0:
                pyperclip.copy(self.txtMsg.textCursor().selectedText())
            else:
                pass


    #读取配置文件
    def ReadInitFile(self):
        self.setIniFile = OperateIniFile()
        self.setIniFile.SetResPath(self.appPath + 'SetInit.ini')

        self.gobalUrlArr.clear()
        self.gobalArr.clear()
        self.gobalNameArr.clear()
        self.seaEngines.clear()

        #设置初始化语言
        lang_index = int(self.setIniFile.GetIniValue('System','lang_flag'))
        self.transLang = QTranslator()
        if lang_index==1:
            self.transLang.load("./Language/zh_CN")
        elif lang_index==2:
            self.transLang.load("./Language/zh_HK")
        else:
            self.transLang.load("./Language/en_US")
        _app = QApplication.instance()
        _app.installTranslator(self.transLang)
        self.retranslateUi(self)

        tag_url_count = int(self.setIniFile.GetIniValue('TagetUrl','Url_Count'))+1
        for tag_i in range(1,tag_url_count):
            tag_str='Url_'+str(tag_i)
            temp_str = str(self.setIniFile.GetIniValue('TagetUrl', tag_str))
            self.gobalUrlArr.append(temp_str)

        t_count = int(self.setIniFile.GetIniValue('TypeName','T_Count'))+1
        for t_i in range(1,t_count):
            tag_str='TName_'+str(t_i)
            temp_str = str(self.setIniFile.GetIniValue('TypeName', tag_str))
            temp_str = temp_str.split(":")
            self.gobalArr.append(temp_str[0])
            self.gobalNameArr.append(temp_str[1])

        #common Engine
        item_count = int(self.setIniFile.GetIniValue('CboItem', 'item_count')) + 1
        for t_i in range(1, item_count):
            tag_str = 'item_' + str(t_i)
            temp_str = str(self.setIniFile.GetIniValue('CboItem', tag_str))
            self.seaEngines.append(temp_str)
        self.cboFind.addItems(self.seaEngines)
        self.cboFind.currentIndexChanged.connect(self.cboIndexChanged)

        self.searchNum = int(self.setIniFile.GetIniValue('System', 'SearchNum'))
        self.cboFind.setCurrentIndex(self.searchNum - 1)

        #hdEngine
        item_hd_count = int(self.setIniFile.GetIniValue('CboItem_HD', 'item_count')) + 1
        for t_i in range(1, item_hd_count):
            tag_str = 'item_' + str(t_i)
            temp_str = str(self.setIniFile.GetIniValue('CboItem_HD', tag_str))
            self.seaEnginesHd.append(temp_str)
        self.cboHdEngine.addItems(self.seaEnginesHd)
        self.cboHdEngine.currentIndexChanged.connect(self.CboHdIndexChanged)

        self.searchNumHd = int(self.setIniFile.GetIniValue('System', 'searchnumhd'))
        self.cboHdEngine.setCurrentIndex(self.searchNumHd - 1)

        #BTEngine
        item_bt_count = int(self.setIniFile.GetIniValue('CboItem_BT', 'item_count')) + 1
        for t_i in range(1, item_bt_count):
            tag_str = 'item_' + str(t_i)
            temp_str = str(self.setIniFile.GetIniValue('CboItem_BT', tag_str))
            self.seaEnginesBt.append(temp_str)
        self.cboBtEngine.addItems(self.seaEnginesBt)
        self.cboBtEngine.currentIndexChanged.connect(self.CboBtIndexChanged)

        self.searchNumBt = int(self.setIniFile.GetIniValue('System', 'searchnumbt'))
        self.cboBtEngine.setCurrentIndex(self.searchNumBt - 1)

        #TvLive
        item_tv_count = int(self.setIniFile.GetIniValue('CboItem_TV', 'item_count')) + 1
        for t_i in range(1, item_tv_count):
            tag_str = 'item_' + str(t_i)
            temp_str = str(self.setIniFile.GetIniValue('CboItem_TV', tag_str))
            self.seaEnginesTv.append(temp_str)
        self.cboTvEngine.addItems(self.seaEnginesTv)
        self.cboTvEngine.currentIndexChanged.connect(self.CboTvIndexChanged)

        self.searchNumTv = int(self.setIniFile.GetIniValue('System', 'searchnumtv'))
        self.cboTvEngine.setCurrentIndex(self.searchNumTv - 1)

        #加载样式
        self._SetControlProperty()
        self._SettingTheme(int(self.setIniFile.GetIniValue('System', 'theme')))

    #Common Engine Cbo
    def cboIndexChanged(self,index):
       if index==0:
           self.cboList.setEnabled(True)
           self.btnSearchAll.setEnabled(True)
           self.searchNum = 1
           self.setIniFile.SetIniValue('System', 'SearchNum', str(self.searchNum))
       elif index>=1:
           self.cboList.setEnabled(False)
           self.btnSearchAll.setEnabled(False)
           self.searchNum = index+1
           self.setIniFile.SetIniValue('System', 'SearchNum', str(self.searchNum))
       else:
           pass

    #HD Engine Cbo
    def CboHdIndexChanged(self,index):
        if (index >=0) and (index<3):
            self.searchNumHd = index+1
            self.setIniFile.SetIniValue('System', 'searchnumhd', str(self.searchNumHd))


    # Tv Engine Cbo
    def CboTvIndexChanged(self, index):
        if index>=0 and index<7:
            self.searchNumTv = index+1
            self.setIniFile.SetIniValue('System', 'searchnumtv', str(self.searchNumTv))


    #BT Engine
    def CboBtIndexChanged(self,index):
        if (index >= 0) and (index < 2):
            self.searchNumBt = index+1
            self.setIniFile.SetIniValue('System', 'searchnumbt', str(self.searchNumBt))

    def BtnSearchAll(self):
        self.getLinkFlag = 3
        self.statusbar.showMessage('Finding...')

    def BtnSearchHd_Click(self):
        self.getLinkFlag = 4
        self.statusbar.showMessage('Finding...')

    def BtnSerachTv_Click(self):
        self.getLinkFlag = 6
        self.statusbar.showMessage('Finding...')

    def BtnSearchBt_Click(self):
        self.getLinkFlag = 9
        self.statusbar.showMessage('Finding...')

    #执行线程
    def MyGetLinkTask(self):
        while True:
            try:
                if self.getLinkFlag==1:
                    self.getLinkFlag = 0
                    self.GetLinkFirst()    #普通搜索
                elif self.getLinkFlag==2:
                    self.getLinkFlag = 0
                    self.GetLinkList()     #全局搜索
                elif self.getLinkFlag==3:
                    self.getLinkFlag = 0
                    self.GetLinkSearchAll()
                elif self.getLinkFlag==4:
                    self.getLinkFlag = 0
                    self.GetLinkHdFirst()   #高清搜索
                elif self.getLinkFlag==5:
                    self.getLinkFlag = 0
                    self.GetLinkList_Hd()   #获取高清链接
                elif self.getLinkFlag==6:
                    self.getLinkFlag = 0
                    self.GetLinkLive_Place() #获取直播地区
                elif self.getLinkFlag==7:    #获取台列表
                    self.getLinkFlag = 0
                    self.GetLinkTvList()
                elif self.getLinkFlag==8:    #获取直播源
                    self.getLinkFlag = 0
                    self.GetLinkLiveLink()
                elif self.getLinkFlag==9:    #BT搜索
                    self.getLinkFlag=0
                    self.GetLinkBtSearchKey()
                elif self.getLinkFlag==10:
                    self.getLinkFlag = 0
                    self.GetLinkBtLink()
                elif self.getLinkFlag==11:  #批量保存文件
                    self.getLinkFlag = 0
                    self.SaveTvLiveToFile()
                elif self.getLinkFlag==12:
                    self.getLinkFlag = 0
                    self.SaveWlxfToFile(0)
                elif self.getLinkFlag==13:
                    self.getLinkFlag = 0
                    self.SaveWlxfToFile(1)
                else:
                    self.getLinkFlag = 0
            except:
                if self.getLinkFlag!=0:self.getLinkFlag=0
            time.sleep(2)

    #搜索全部
    def GetLinkSearchAll(self):
        self.qList.clear()
        self.signal_list.emit()#UpdateListView
        taget_name = self.txtName.toPlainText()

        #选择搜索引擎
        if self.cboFind.currentIndex()==0:
            self.allLink,self.allLinkTitle = self.myGetLink.SearchMasterKey(taget_name,self.gobalUrlArr[1])
        else:
            self.allLink,self.allLinkTitle = self.myGetLinkSec.SearchKey(taget_name)

        for i in range(0, len(self.allLink)):
            link_str = self.allLinkTitle[i]+'-'+self.allLink[i]
            self.qList.append(link_str)

        self.signal_list.emit()#UpdateListView
        self.statusbar.showMessage('Resource Count:'+str(len(self.allLink)))


    #获取连接函数
    def GetLinkFirst(self):
        taget = self.gobalArr[self.cboList.currentIndex()]
        taget_name = self.txtName.toPlainText()
        self.qList.clear()
        self.signal_list.emit()#UpdateListView

        if self.cboFind.currentIndex()==0:
            list_link,img = self.myGetLink.SearchKey(self.gobalUrlArr[0],taget,taget_name)
            self.signal2.emit("")
            self.ShowUrl(list_link)
            self.UpdateMovPicture(img,1)
        elif self.cboFind.currentIndex()==1:
            self.allLink,self.allLinkTitle = self.myGetLinkSec.SearchKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLinkTitle[i]+'-'+self.allLink[i]
                self.qList.append(link_str)
            self.signal_list.emit()#UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==2:
            self.allLink,self.allLinkTitle = self.myGetLinkBt.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLinkTitle[i]
                self.qList.append(link_str)
            self.signal_list.emit()#UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==3:
            self.allLink = self.myGetLinkPan.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['Title']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==4:
            self.allLink = self.myGetLinkDy.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['MovName']+'-'+self.allLink[i]['Notice']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==5:
            self.allLink=self.myGetLinkPanSo.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['Name']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==6:
            self.allLink = self.myGetLinkEs.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['MovName']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==7:
            self.allLink=self.myGetLinkfNet.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['BtName']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==8:
            self.allLink=self.myGetLinkXplay.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['MovieName']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==9:
            self.allLink = self.myGetLinkFfhk.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['MovName']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==10 or self.cboFind.currentIndex()==11:
            if self.cboFind.currentIndex()==10:
                self.myGetLinkWlxf.SetBaseUrl(self.gobalUrlArr[21])
                self.allLink = self.myGetLinkWlxf.SearchMasterKey()
            else:
                self.myGetLinkWlxf.SetBaseUrl(self.gobalUrlArr[34])
                self.allLink = self.myGetLinkWlxf.SearchMasterKey()
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['MovName']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==12:
            self.allLink = self.myGetLinkNfMov.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['MovName']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==13:
            self.allLink = self.myGetLinkPiaoHua.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['MovName']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboFind.currentIndex()==14:
            self.allLink = self.myGetLinkGj.SearchMasterKey(taget_name)
            self.qList.clear()
            for i in range(0, len(self.allLink)):
                link_str = self.allLink[i]['MovName']
                self.qList.append(link_str)
            self.signal_list.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        else:
            self.statusbar.showMessage('Resource Count:NULL')

    # 获取下载连接
    def GetLinkList(self):
        if self.qList:
            if self.cboFind.currentIndex()==0:
                html = 'http://'+self.allLink[self.qmodelRowIndex]
                list_link,img = self.myGetLink.SearchLink(html)
                self.signal2.emit("")
                self.ShowUrl(list_link)
                self.UpdateMovPicture(img,1)
            elif self.cboFind.currentIndex()==1:
                html = self.allLink[self.qmodelRowIndex]
                #搜索迅雷连接
                list1,list2,img = self.myGetLinkSec.SearchDownLink(html)
                #搜索百度连接
                pan_list1,pan_list2 = self.myGetLinkSec.SearchPanLink(html)
                self.signal2.emit("")
                self.UpdateMovPicture(img,1)
                if len(list1)>0 and len(list2)>0:
                    temp = ""
                    for i in range(0,len(list1)):
                        temp+=list1[i]+'\r\n\r\n'
                    for i in range(0,len(list2)):
                        temp+=list2[i]+'\r\n\r\n'
                    for i in range(0,len(pan_list2)):
                        temp +=pan_list1[i] + '\r\n' + pan_list2[i] + '\r\n\r\n'
                    self.signal.emit(temp)  # 子线程
                    self.statusbar.showMessage('Resource Count:' + str(len(list1)+len(pan_list1)))
            elif self.cboFind.currentIndex()==2:
                html = self.allLink[self.qmodelRowIndex]
                link,link2 = self.myGetLinkBt.SearchLinkBt(html)
                self.signal2.emit(link+'\r\n'+link2)
                self.statusbar.showMessage('Resource Count:1')
            elif self.cboFind.currentIndex()==3:
                js_pan_link = self.allLink[self.qmodelRowIndex]
                temp = js_pan_link['Link'] + '\r\n' + js_pan_link['BLink']+ '\r\n\r\n'
                self.signal2.emit(temp)  # 子线程
                self.statusbar.showMessage('Resource Count:1')
            elif self.cboFind.currentIndex()==4:
                self.signal2.emit("")
                html = self.allLink[self.qmodelRowIndex]['Link']
                dic_mov = self.myGetLinkDy.SearchLinkBt(html)
                img = self.myGetLinkDy.DownMovPicture(self.allLink[self.qmodelRowIndex]['Img'])
                self.UpdateMovPicture(img,1)
                temp_str = ""
                for item in dic_mov:
                    temp_str+=item['Name']+ '\r\n' + item['ThunderLink']+ '\r\n\r\n'
                self.signal2.emit(temp_str)
                self.statusbar.showMessage('Resource Count:1')
            elif self.cboFind.currentIndex()==5:
                self.signal2.emit("")
                html = self.allLink[self.qmodelRowIndex]['Link']
                link = self.myGetLinkPanSo.SearchPanLink(html)
                self.signal2.emit(link)
                self.statusbar.showMessage('Resource Count:1')
            elif self.cboFind.currentIndex()==6:
                self.signal2.emit("")
                data = self.allLink[self.qmodelRowIndex]
                dic_mov = self.myGetLinkEs.SearchLinkBt(data)
                temp_str = ""
                for item in reversed(dic_mov):
                    temp_str += item['Name'] + '\r\n' + item['ThunderLink'] + '\r\n\r\n'
                self.signal2.emit(temp_str)
                self.statusbar.showMessage('Resource Count:1')
                try:
                    img = self.myGetLinkEs.DownMovPicture('https:'+self.allLink[self.qmodelRowIndex]['Img'])
                    self.UpdateMovPicture(img,1)
                except:
                    pass
            elif self.cboFind.currentIndex()==7:
                self.signal2.emit("")
                data = self.allLink[self.qmodelRowIndex]['BtUrl']
                self.fnetDict = self.myGetLinkfNet.SearchLinkBt(data)
                self.fnetDict['BtName'] = self.allLink[self.qmodelRowIndex]['BtName']
                img = self.myGetLinkfNet.DownMovPicture(self.fnetDict['BtImg'])
                self.UpdateMovPicture(img,1)
                self.signal2.emit(self.fnetDict['BtUrl'])
                self.statusbar.showMessage('Resource Count:1')
            elif self.cboFind.currentIndex()==8:
                self.signal2.emit("")
                data = self.allLink[self.qmodelRowIndex]['Link']
                self.fDownDict,self.fPlayDict = self.myGetLinkXplay.SearchLinkBt(data)

                #打印播放链接
                temp_str='播放链接：\r\n'
                for item in self.fPlayDict:
                    temp_str = temp_str+item['MovieMode']+'\r\n'+item['PlayUrl']+'\r\n\r\n'

                #获取下载链接
                temp_str = temp_str+'迅雷链接：\r\n'
                for item in self.fDownDict:
                    temp_str = temp_str+item['MovName']+'\r\n'+item['DownUrl']+'\r\n\r\n'
                img = self.myGetLinkfNet.DownMovPicture(self.allLink[self.qmodelRowIndex]['Img'])
                self.UpdateMovPicture(img,1)
                self.signal2.emit(temp_str)
                self.statusbar.showMessage('Resource Count:'+str(len(self.fDownDict)))
            elif self.cboFind.currentIndex()==9:
                self.signal2.emit("")
                dict_data = self.allLink[self.qmodelRowIndex]
                link = self.myGetLinkFfhk.SearchLink(dict_data)
                temp_str = ""
                for item in link:
                    temp_str += item['Title'] + '\r\n' + item['PlayLink'] + '\r\n\r\n'
                self.signal2.emit(temp_str)
                self.statusbar.showMessage('Resource Count:'+str(len(link)))
            elif self.cboFind.currentIndex()==10 or self.cboFind.currentIndex()==11:
                self.signal2.emit("")
                dict_data = self.allLink[self.qmodelRowIndex]
                link = self.myGetLinkWlxf.SearchLink(dict_data)
                temp_str = dict_data['MovName'] + '\r\n' + link + '\r\n\r\n'
                img = self.myGetLinkWlxf.DownMovPicture(self.allLink[self.qmodelRowIndex]['MovImg'])
                self.UpdateMovPicture(img, 1)
                self.signal2.emit(temp_str)
                self.statusbar.showMessage('Resource Count:'+str(len(link)))
            elif self.cboFind.currentIndex()==12:
                self.signal2.emit("")
                dict_data = self.allLink[self.qmodelRowIndex]
                link = self.myGetLinkNfMov.SearchLink(dict_data)
                temp_str = ""
                for item in link:
                    temp_str += item['Title'] + '\r\n' + item['PlayLink'] + '\r\n\r\n'
                self.signal2.emit(temp_str)
                img = self.myGetLinkNfMov.DownMovPicture(self.allLink[self.qmodelRowIndex]['MovImg'])
                self.UpdateMovPicture(img, 1)
                self.statusbar.showMessage('Resource Count:' + str(len(link)))
            elif self.cboFind.currentIndex()==13:
                self.signal2.emit("")
                dict_data = self.allLink[self.qmodelRowIndex]
                link = self.myGetLinkPiaoHua.SearchLink(dict_data)
                temp_str = ""
                for item in link:
                    temp_str += item['Title'] + '\r\n' + item['PlayLink'] + '\r\n\r\n'
                self.signal2.emit(temp_str)
                img = self.myGetLinkPiaoHua.DownMovPicture(self.allLink[self.qmodelRowIndex]['MovImg'])
                self.UpdateMovPicture(img, 1)
                self.statusbar.showMessage('Resource Count:' + str(len(link)))
            elif self.cboFind.currentIndex()==14:
                self.signal2.emit("")
                dict_data = self.allLink[self.qmodelRowIndex]
                link = self.myGetLinkGj.SearchLink(dict_data)
                temp_str = ""
            else:
                self.statusbar.showMessage('Resource Count:NULL')

    def GetLinkHdFirst(self):
        master_key = self.txtHdKey.toPlainText()
        if len(master_key)>0:
            if self.cboHdEngine.currentIndex()==0:
                self.allLinkHd = self.myGetLinkHdHq.SearchMasterKey(master_key)
                self.qListHd.clear()
                for i in range(0, len(self.allLinkHd)):
                    self.qListHd.append(self.allLinkHd[i]['MovieName'])
                self.signal_list_hd.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkHd)))
            elif self.cboHdEngine.currentIndex()==1:
                self.allLinkHd = self.myGetLinkIqiyi.SearchMasterKey(master_key)
                self.qListHd.clear()
                for i in range(0, len(self.allLinkHd)):
                    self.qListHd.append(self.allLinkHd[i]['Title'])
                self.signal_list_hd.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkHd)))
            elif self.cboHdEngine.currentIndex()==2:
                self.allLinkHd = self.myGetLinkTenv.SearchMasterKey(master_key)
                self.qListHd.clear()
                for i in range(0, len(self.allLinkHd)):
                    self.qListHd.append(self.allLinkHd[i]['Title'])
                self.signal_list_hd.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkHd)))
            else:
                self.statusbar.showMessage('Resource Count:NULL')
        else:
            self.statusbar.showMessage('Resource Count:NULL')

    #获取HD链接
    def GetLinkList_Hd(self):
        if self.qListHd:
            if self.cboHdEngine.currentIndex()==0:
                tag_dict = self.allLinkHd[self.listHdRowIndex]
                dict_link = self.myGetLinkHdHq.SearchLinkBt(tag_dict['MovieLink'])
                if dict_link:
                    link_str = dict_link['MovName']+'\r\n\r\n'+dict_link['MovLink']
                    self.signal_msg_set_hd.emit("")
                    self.signal_msg_set_hd.emit(link_str)
                    img = self.myGetLinkHdHq.DownMovPicture(tag_dict['Img'])
                    self.UpdateMovPicture(img,2)
                    self.statusbar.showMessage('Resource Count:1')
                else:
                    self.statusbar.showMessage('Resource Count:None!')
            elif self.cboHdEngine.currentIndex()==1:
                tag_dict = self.allLinkHd[self.listHdRowIndex]
                link_str = tag_dict['Title']+'\r\n'
                self.signal_msg_set_hd.emit("")
                for item in tag_dict['List']:
                    link_str+=item['MovTitle']+'\r\n'+item['MovLink']+'\r\n\r\n'
                self.signal_msg_set_hd.emit(link_str)
                img =self.myGetLinkIqiyi.DownMovPicture(tag_dict['Img'])
                self.UpdateMovPicture(img, 2)
                self.statusbar.showMessage('Resource Count:'+str(len(tag_dict['List'])))
            elif self.cboHdEngine.currentIndex()==2:
                tag_dict = self.allLinkHd[self.listHdRowIndex]
                all_mov_link = self.myGetLinkTenv.SetMovLink(tag_dict)
                link_str = tag_dict['Title'] + '\r\n'
                self.signal_msg_set_hd.emit("")
                for item in all_mov_link:
                    link_str+='Episodes:'+item['MovTitle']+'\r\n'+item['MovLink']+'\r\n\r\n'
                self.signal_msg_set_hd.emit(link_str)
                self.statusbar.showMessage('Resource Count:' + str(len(all_mov_link)))
            else:
                pass

    #获取地方选项
    def GetLinkLive_Place(self):
        if self.cboTvEngine.currentIndex() == 0:
            self.allLinkAddr = self.myGetLinkLiveSs.SearchPlace()
            self.qListAddr.clear()
            self.qListTv.clear()
            self.signal_list_tv.emit()  # UpdateListView
            for i in range(0, len(self.allLinkAddr)):
                self.qListAddr.append(self.allLinkAddr[i]['AddrName'])
            self.signal_list_addr.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkAddr)))
        elif self.cboTvEngine.currentIndex()==1:
            self.allLinkAddr = self.myGetLinkLiveLs.SearchPlace()
            self.qListAddr.clear()
            self.qListTv.clear()
            self.signal_list_tv.emit()  # UpdateListView
            for i in range(0, len(self.allLinkAddr)):
                self.qListAddr.append(self.allLinkAddr[i]['AddrName'])
            self.signal_list_addr.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkAddr)))
        elif self.cboTvEngine.currentIndex()==2:
            self.allLinkAddr = self.myGetLinkLiveIVI.SearchMaster()

            self.qListAddr.clear()
            self.qListAddr.append('请看右边列表')
            self.signal_list_addr.emit()

            self.qListTv.clear()
            for i in range(0, len(self.allLinkAddr)):
                self.qListTv.append(self.allLinkAddr[i]['LiveTitle'])
            self.signal_list_tv.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkAddr)))
        elif self.cboTvEngine.currentIndex() == 3:
            self.allLinkAddr = self.myGetLinkLiveOtop.SearchMaster()

            self.qListAddr.clear()
            self.qListAddr.append('请看右边列表')
            self.signal_list_addr.emit()

            self.qListTv.clear()
            for i in range(0, len(self.allLinkAddr)):
                self.qListTv.append(self.allLinkAddr[i]['LiveLink'])
            self.signal_list_tv.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkAddr)))
        elif self.cboTvEngine.currentIndex()==4:
            self.allLinkAddr = self.myGetLinkLiveQhtv.SearchPlace()
            self.qListAddr.clear()
            self.qListTv.clear()
            self.signal_list_tv.emit()  # UpdateListView
            for i in range(0, len(self.allLinkAddr)):
                self.qListAddr.append(self.allLinkAddr[i]['PlaceName'])
            self.signal_list_addr.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkAddr)))
        elif self.cboTvEngine.currentIndex()==5:
            self.allLinkAddr = self.myGetLinkLiveYsou.SearchPlace()
            self.qListAddr.clear()
            self.qListTv.clear()
            self.signal_list_tv.emit()  # UpdateListView
            for i in range(0, len(self.allLinkAddr)):
                self.qListAddr.append(self.allLinkAddr[i]['PlaceName'])
            self.signal_list_addr.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkAddr)))
        elif self.cboTvEngine.currentIndex()==6:
            self.allLinkAddr = self.myGetLinkTvEye.SearchPlace()
            self.qListAddr.clear()
            self.qListTv.clear()
            self.signal_list_tv.emit()  # UpdateListView
            for i in range(0, len(self.allLinkAddr)):
                self.qListAddr.append(self.allLinkAddr[i]['PlaceName'])
            self.signal_list_addr.emit()  # UpdateListView
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkAddr)))
        else:
            self.statusbar.showMessage('Resource Count:NULL')

    #获取电视台列表
    def GetLinkTvList(self):
        if self.qListAddr:
            if self.cboTvEngine.currentIndex()==0:
                dict_temp = self.allLinkAddr[self.listAddrRowIndex]
                self.allLinkProgram = self.myGetLinkLiveSs.SearchTvProgram(dict_temp)
                self.qListTv.clear()
                for i in range(0, len(self.allLinkProgram)):
                    self.qListTv.append(self.allLinkProgram[i]['LiveTitle'])
                self.signal_list_tv.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkProgram)))
            elif self.cboTvEngine.currentIndex() == 1:
                dict_temp = self.allLinkAddr[self.listAddrRowIndex]
                self.allLinkProgram = self.myGetLinkLiveLs.SearchTvProgram(dict_temp)
                self.qListTv.clear()
                for i in range(0, len(self.allLinkProgram)):
                    self.qListTv.append(self.allLinkProgram[i]['LiveTitle'])
                self.signal_list_tv.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkProgram)))
            elif self.cboTvEngine.currentIndex() == 4:
                dict_temp = self.allLinkAddr[self.listAddrRowIndex]
                self.allLinkProgram = self.myGetLinkLiveQhtv.SearchTvProgram(dict_temp)
                self.qListTv.clear()
                for i in range(0, len(self.allLinkProgram)):
                    self.qListTv.append(self.allLinkProgram[i]['LiveTitle'])
                self.signal_list_tv.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkProgram)))
            elif self.cboTvEngine.currentIndex() == 5:
                dict_temp = self.allLinkAddr[self.listAddrRowIndex]
                self.allLinkProgram = self.myGetLinkLiveYsou.SearchTvProgram(dict_temp)
                self.qListTv.clear()
                for i in range(0, len(self.allLinkProgram)):
                    self.qListTv.append(self.allLinkProgram[i]['LiveTitle'])
                self.signal_list_tv.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkProgram)))
            elif self.cboTvEngine.currentIndex() == 6:
                self.allLinkProgram = self.allLinkAddr[self.listAddrRowIndex]['LiveList']
                self.qListTv.clear()
                for i in range(0, len(self.allLinkProgram)):
                    self.qListTv.append(self.allLinkProgram[i]['LiveTitle'])
                self.signal_list_tv.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkProgram)))
            else:
                pass

    def GetLinkLiveLink(self):
        if self.qListTv:
            if self.cboTvEngine.currentIndex()==0:
                dict_temp = self.allLinkProgram [self.listTvRowIndex]
                self.allLinkLive = self.myGetLinkLiveSs.SearchTvLink(dict_temp)
                self.signal_msg_set_tv.emit("")
                link_str=''
                for item in self.allLinkLive:
                    link_str = link_str+item['LiveTitle']+'\r\n'+item['LiveLink']+'\r\n\r\n'
                self.signal_msg_set_tv.emit(link_str)
                img = self.myGetLinkLiveSs.DownPicture(dict_temp['LiveIcon'])
                self.UpdateMovPicture(img,3)
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkLive)))
            elif self.cboTvEngine.currentIndex()==1:
                dict_temp = self.allLinkProgram[self.listTvRowIndex]
                self.allLinkLive = self.myGetLinkLiveLs.SearchTvLink(dict_temp)
                self.signal_msg_set_tv.emit("")
                link_str = ''
                for item in self.allLinkLive:
                    link_str = link_str+item['LiveTitle']+'\r\n'+item['LiveLink']+'\r\n\r\n'
                self.signal_msg_set_tv.emit(link_str)
                # img = self.myGetLinkLiveSs.DownPicture(dict_temp['LiveIcon'])
                # self.UpdateMovPicture(img,3)
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkLive)))
            elif self.cboTvEngine.currentIndex()==2:
                dict_temp = self.allLinkAddr[self.listTvRowIndex]
                self.signal_msg_set_tv.emit("")
                link_str =dict_temp['LiveTitle']+'\r\nPC端'+dict_temp['PCLink']+'\r\n\r\n'+'移动端'+dict_temp['MobileLink']
                self.signal_msg_set_tv.emit(link_str)
                self.statusbar.showMessage('Resource Count:2')
            elif self.cboTvEngine.currentIndex()==3:
                dict_temp = self.allLinkAddr[self.listTvRowIndex]
                self.signal_msg_set_tv.emit("")
                live_name = dict_temp['LiveLink'][dict_temp['LiveLink'].rfind('/'):].replace('.htm','').replace('/','').upper()
                link_str = self.myGetLinkLiveOtop.GetM3U8Link(dict_temp)
                self.signal_msg_set_tv.emit(live_name+'\r\n'+link_str+'\r\n')
                img = self.myGetLinkLiveSs.DownPicture(dict_temp['LiveImg'])
                self.UpdateMovPicture(img,3)
                self.statusbar.showMessage('Resource Count:1')
            elif self.cboTvEngine.currentIndex()==4:
                dict_temp = self.allLinkProgram[self.listTvRowIndex]
                self.allLinkLive = self.myGetLinkLiveQhtv.GetM3U8Link(dict_temp)
                self.signal_msg_set_tv.emit("")
                link_str = ''
                link_str = link_str + dict_temp['LiveTitle'] + '\r\n'
                for item in self.allLinkLive:
                    link_str = link_str + item['Title'] + '\r\n' + item['Link'] + '\r\n\r\n'
                    if (not '.flv' in item['Link']) and '.m3u8' in item['Link']:
                        m3u8_link = self.myGetLinkLiveQhtv.ExplainM3U8File(item['Link'])
                        for i in range(len(m3u8_link)):
                            temp_str = '{0}-源{1}:\r\n'.format(item['Title'],str(i+1))
                            link_str = link_str+temp_str+m3u8_link[i]+'\r\n\r\n'
                        self.statusbar.showMessage('Resource Count:' + str(len(m3u8_link)))
                    else:
                        self.statusbar.showMessage('Resource Count:1')
                self.signal_msg_set_tv.emit(link_str)
            elif self.cboTvEngine.currentIndex()==5:
                dict_temp = self.allLinkProgram[self.listTvRowIndex]
                self.allLinkLive = self.myGetLinkLiveYsou.GetM3U8Link(dict_temp)
                self.signal_msg_set_tv.emit("")
                link_str = ''
                link_str = link_str + dict_temp['LiveTitle'] + '\r\n' + self.allLinkLive + '\r\n\r\n'
                self.signal_msg_set_tv.emit(link_str)
                self.statusbar.showMessage('Resource Count:1')
            elif self.cboTvEngine.currentIndex()==6:
                dict_temp = self.allLinkProgram[self.listTvRowIndex]
                self.allLinkLive = dict_temp['LiveLink']
                self.signal_msg_set_tv.emit("")
                link_str = ''
                if '#' in self.allLinkLive:
                    link_str = link_str + dict_temp['LiveTitle'] + '\r\n\r\n'
                    temp_arr = self.allLinkLive.split('#')
                    for item in temp_arr:
                        link_str+=item + '\r\n\r\n'
                    self.statusbar.showMessage('Resource Count:'+str(len(temp_arr)))
                else:
                    link_str = link_str + dict_temp['LiveTitle'] + '\r\n' + self.allLinkLive + '\r\n\r\n'
                    self.statusbar.showMessage('Resource Count:1')
                self.signal_msg_set_tv.emit(link_str)
            else:
                self.statusbar.showMessage('Resource Count:NULL')

    #获取BT种子列表
    def GetLinkBtSearchKey(self):
        master_key = self.txtBtKey.toPlainText()
        if len(master_key) > 0:
            if self.cboBtEngine.currentIndex() == 0:
                self.allLinkBt = self.myGetLinkZZS.SearchMasterKey(master_key)
                self.qListBt.clear()
                for i in range(0, len(self.allLinkBt)):
                    self.qListBt.append(self.allLinkBt[i]['BtName'])
                self.signal_list_bt.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkBt)))
            elif self.cboBtEngine.currentIndex()==1:
                self.allLinkBt = self.myGetLinkBtMov.SearchMasterKey(master_key)
                self.qListBt.clear()
                for i in range(0, len(self.allLinkBt)):
                    self.qListBt.append(self.allLinkBt[i]['BtName'])
                self.signal_list_bt.emit()  # UpdateListView
                self.statusbar.showMessage('Resource Count:' + str(len(self.allLinkBt)))
            else:
                self.statusbar.showMessage('Resource Count:NULL')
        else:
            self.statusbar.showMessage('Resource Count:NULL')

    def GetLinkBtLink(self):
        if self.qListBt:
            if self.cboBtEngine.currentIndex()==0:
                dict = self.allLinkBt[self.listBtRowIndex]
                list_link = self.myGetLinkZZS.SearchLink(dict)
                self.signal_msg_set_bt.emit(list_link)
                self.statusbar.showMessage('Resource Count:1')
            elif self.cboBtEngine.currentIndex()==1:
                dict = self.allLinkBt[self.listBtRowIndex]
                list_link = self.myGetLinkBtMov.SearchLink(dict)
                self.signal_msg_set_bt.emit(list_link)
                self.statusbar.showMessage('Resource Count:1')
            else:
                self.statusbar.showMessage('Resource Count:NULL')

    #搜索+定位获取链接
    def BtnGetLink(self):
        self.getLinkFlag=1
        self.statusbar.showMessage('Finding...')

    #多链接选择
    def ListViewClick(self,qModelIndex):
        self.qmodelRowIndex = qModelIndex.row()
        self.getLinkFlag = 2
        self.statusbar.showMessage('Finding...')

    def ListViewHd_Click(self,qModelIndex):
        self.listHdRowIndex = qModelIndex.row()
        self.getLinkFlag = 5
        self.statusbar.showMessage('Finding...')

    def ListViewAddr_Click(self,qModelIndex):
        self.listAddrRowIndex = qModelIndex.row()
        self.getLinkFlag = 7
        self.statusbar.showMessage('Finding...')

    def ListViewLive_Click(self, qModelIndex):
        self.listTvRowIndex = qModelIndex.row()
        self.getLinkFlag = 8
        self.statusbar.showMessage('Finding...')

    def ListViewBt_Click(self,qModelIndex):
        self.listBtRowIndex = qModelIndex.row()
        self.getLinkFlag = 10
        self.statusbar.showMessage('Finding...')

    #打开迅雷下载
    def MenuOpenAppClick(self):
        thunder_path =r'"{0}"'.format(str(self.setIniFile.GetIniValue('Thunder','Path')))
        try:
            win32api.ShellExecute(0, 'open', thunder_path, '', '', 0)
        except Exception as msg:
            self.statusbar.showMessage('Error:'+str(msg))

    #打开PotPlayer
    def MenuOpenPot_Click(self):
        pot_path = r'"{0}"'.format(str(self.setIniFile.GetIniValue('PotPlayer', 'Path')))
        try:
            win32api.ShellExecute(0, 'open', pot_path, '', '', 0)
        except Exception as msg:
            self.statusbar.showMessage('Error:'+str(msg))

    def MenuThLink_Click(self):
        if self.conOpenFg==0:
            theme = int(self.setIniFile.GetIniValue('System', 'theme'))
            theme_str = 'NativeTheme'
            if theme == 1:
                theme_str = 'NativeTheme'
            else:
                theme_str = 'NightTheme'
            self.conWin = ConverterWindow(theme_str)
            self.conWin.myCloseSignal.connect(self.ConWinClose_Event)
            self.conWin.ShowWindows()
            self.conWin.retranslateUi(self.conWin)
            self.conOpenFg = 1

    def ConWinClose_Event(self):
        self.conOpenFg = 0
        self.conWin.deleteLater()

    #右键菜单，保存文件
    def Menu_ListTv_Click(self,menu_item):
        if 'Save As List' ==menu_item.text():
            filename_filter = "*.txt|文件类型 (*.txt)"
            dlg = win32ui.CreateFileDialog(0, None, None, 1, filename_filter, None)
            dlg.SetOFNInitialDir("C:")
            if dlg.DoModal() == 1:
                self.saveLivePath = dlg.GetPathName()
                self.getLinkFlag = 11                #执行保存操作
        elif 'Export QDF File' ==menu_item.text():
            filename_filter = "*.qdf|文件类型 (*.qdf)"
            dlg = win32ui.CreateFileDialog(0, None, None, 1, filename_filter, None)
            dlg.SetOFNInitialDir("C:")
            if dlg.DoModal() == 1:
                self.saveLivePath = dlg.GetPathName()
                self.getLinkFlag = 13  # 执行保存操作
        else:
            pass

    #实现菜单
    def MenuTxtDown_Click(self,menu_item):
        if self.cboFind.currentIndex()==10:
            if 'DownLoad Video'==menu_item.text():
                self.OpenDownWin(2,'')
                temp_str = self.txtMsg.toPlainText()
                if len(temp_str)>0:
                    data = temp_str.split('\n')
                    self.vipDownWin.SetUrlText(data[1]) #设置url
                    self.vipDownWin.btnGetUrl.click()   #模拟按钮点击
                    pyperclip.copy(data[0])             #将数据复制到粘贴板

    def MenuTvChannel_Click(self,menu_item):
        if self.cboFind.currentIndex()==10:
            if 'Save As List' == menu_item.text():
                filename_filter = "*.txt|文件类型 (*.txt)"
                dlg = win32ui.CreateFileDialog(0, None, None, 1, filename_filter, None)
                dlg.SetOFNInitialDir("C:")
                if dlg.DoModal() == 1:
                    self.saveWlxfPath = dlg.GetPathName()
                    self.getLinkFlag = 12
                    self.statusbar.showMessage('Saving...')

    def MenuDownList_Click(self,menu_item):
        if self.cboFind.currentIndex()==10:
            if 'Send Data To List' == menu_item.text():
                try:
                    temp_str = self.txtMsg.toPlainText()
                    if len(temp_str) > 0:
                        data = temp_str.split('\n')
                        data[0] = data[0].replace(' ','_')          #防止shell出错
                        self.batchDownWin.UpdateTextBox(1, data[0])  # 设置url
                        self.batchDownWin.UpdateTextBox(2,data[1])  # 设置url
                        self.batchDownWin.UpdateTextBox(3, '')  # 模拟点击
                except Exception as msg:
                    win32api.MessageBox(0, str(msg), "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)

    def SaveWlxfToFile(self,flag):
        if flag==0:
            with open(self.saveWlxfPath + '.txt','w',encoding='utf-8') as f_write:
                for item in self.allLink:
                   link = self.myGetLinkWlxf.SearchLink(item)
                   if '_' in item['MovName']:
                        name = item['MovName'].split('_')[1]
                   else:
                        name = item['MovName']
                   f_write.write(name+','+link+'\n')
        else:
            with open(self.saveLivePath + '.qdf','w',encoding='utf-8') as f_write:
                js_str = '{ "ItemCount":"' + str(len(self.allLink)) + '","Item":['
                for i in range(0,len(self.allLink)):
                    try:
                        link = self.myGetLinkWlxf.SearchLink(self.allLink[i])
                        js_str += '{"FileName":"' + self.allLink[i]['MovName'] + '",'
                        js_str += '"FileLink":"' + link + '",'
                        js_str += '"BaseLink":""},'
                        self.signal.emit(self.allLink[i]['MovName']+' Saved!')
                    except Exception as msg:
                        i-=1
                        self.signal.emit(self.allLink[i]['MovName'] + ' Resaveding...')
                js_str += ']}'
                js_str = js_str.replace(',]}', ']}')
                f_write.write(js_str)
        self.statusbar.showMessage('Save success!')
        win32api.MessageBox(0, 'Save success!', "Information", win32con.MB_ICONINFORMATION, win32con.MB_OK)

    #保存直播源到文件内
    def SaveTvLiveToFile(self):
        if self.cboTvEngine.currentIndex()==2:
            temp_str = ''
            for item in self.allLinkAddr:
                temp_str = temp_str+item['LiveTitle']+','+item['MobileLink']+'\n'
            with open(self.saveLivePath + '.txt', "w",encoding='utf-8') as f_create:
                f_create.write(temp_str)
            win32api.MessageBox(0, 'Output data successful!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        elif self.cboTvEngine.currentIndex()==0:
            self.signal_msg_set_tv.emit('')
            with open(self.saveLivePath + '.txt', "w", encoding='utf-8') as f_create:
                temp_str = ''
                for item in self.allLinkProgram:
                    try:
                        all_link = self.myGetLinkLiveSs.SearchTvLink(item)
                        temp_str += item['LiveTitle'] + ','
                        cnt = 0
                        for i in range(len(all_link)):
                            if not 'rtmp' in all_link[i]['LiveLink']:
                                if 'id=http' in all_link[i]['LiveLink']:
                                    temp_link ='http'+all_link[i]['LiveLink'].split('id=http')[1]
                                else:
                                    temp_link = all_link[i]['LiveLink']
                                if i < len(all_link) - 1:
                                    temp_str += temp_link+ '#'
                                else:
                                    temp_str += temp_link
                                cnt+=1
                        if cnt==0:
                            temp_str = temp_str.replace(item['LiveTitle']+',','')
                        else:
                            temp_str += '\n'
                    except Exception as msg:
                        self.signal_msg_tv.emit(item['LiveTitle'] + 'find url failed!\r\n')
                f_create.write(temp_str)
            win32api.MessageBox(0, 'Output data successful!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        elif self.cboTvEngine.currentIndex()==1:
            self.signal_msg_set_tv.emit('')
            with open(self.saveLivePath + '.txt', "w", encoding='utf-8') as f_create:
                temp_str = ''
                for item in self.allLinkProgram:
                    try:
                        all_link = self.myGetLinkLiveLs.SearchTvLink(item)
                        temp_str+=item['LiveTitle']+','
                        cnt = 0
                        for i in range(len(all_link)):
                            if not 'rtmp' in all_link[i]['LiveLink']:
                                if i<len(all_link)-1:
                                    temp_str+=all_link[i]['LiveLink'] + '#'
                                else:
                                    temp_str += all_link[i]['LiveLink']
                                cnt+=1
                        if cnt==0:
                            temp_str = temp_str.replace(item['LiveTitle']+',','')
                        else:
                            temp_str +='\n'
                    except Exception as msg:
                        self.signal_msg_tv.emit(item['LiveTitle'] + 'find url failed!\r\n')
                f_create.write(temp_str)
            win32api.MessageBox(0, 'Output data successful!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        elif self.cboTvEngine.currentIndex()==3:
            # self.signal_msg_set_tv.emit('')
            # with open(self.saveLivePath + '.txt', "w", encoding='utf-8') as f_create:
            #     temp_str = ''
            #     f_create.write(temp_str)
            #     win32api.MessageBox(0, 'Output data successful!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
            pass
        elif self.cboTvEngine.currentIndex()==4:
            self.signal_msg_set_tv.emit('')
            with open(self.saveLivePath + '.txt', "w", encoding='utf-8') as f_create:
                    temp_str = ''
                    for item in self.allLinkProgram:
                        try:
                            link = self.myGetLinkLiveQhtv.GetM3U8Link(item)
                            temp_str += item['LiveTitle']+','+link+'\n'
                        except Exception as msg:
                            self.signal_msg_tv.emit(item['LiveTitle']+'find url failed!\r\n')
                    f_create.write(temp_str)
            win32api.MessageBox(0, 'Output data successful!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        elif self.cboTvEngine.currentIndex()==5:
            self.signal_msg_set_tv.emit('')
            with open(self.saveLivePath + '.txt', "w", encoding='utf-8') as f_create:
                temp_str = ''
                for item in self.allLinkProgram:
                    try:
                        link = self.myGetLinkLiveYsou.GetM3U8Link(item)
                        if ('http' in link) or ('rtmp' in link):
                            temp_str += item['LiveTitle'] + ',' + link + '\n'
                        else:
                            self.signal_msg_tv.emit(item['LiveTitle'] + ' find url failed! '+link+'\r\n')
                        self.signal_msg_tv.emit('.')
                    except Exception as msg:
                        self.signal_msg_tv.emit(item['LiveTitle'] + 'find url failed!\r\n')
                f_create.write(temp_str)
            win32api.MessageBox(0, 'Output data successful!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        elif self.cboTvEngine.currentIndex()==6:
            self.signal_msg_set_tv.emit('')
            with open(self.saveLivePath + '.txt', "w", encoding='utf-8') as f_create:
                temp_str = ''
                for item in self.allLinkProgram:
                    temp_str += item['LiveTitle'] + ',' + item['LiveLink'] + '\n'
                    self.signal_msg_tv.emit('.')
                f_create.write(temp_str)
            win32api.MessageBox(0, 'Output data successful!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        else:
            pass

    #清空消息框
    def MenuClearClick(self):
        self.txtMsg.setText("")

    def MenuSaveClick(self):
        filename_filter = "*.txt|文件类型 (*.txt)"
        dlg = win32ui.CreateFileDialog(0,None, None, 1, filename_filter, None)
        dlg.SetOFNInitialDir("C:")
        flag = dlg.DoModal()
        if flag==1:
           path = dlg.GetPathName()
           with open(path+'.txt',"w") as f_create:
               f_create.write(self.txtMsg.toPlainText())

    #下载BT种子
    def MenuDownBt_Click(self):
        if self.cboFind.currentIndex()==7:
            if len(self.txtMsg.toPlainText())>0:
                file_name = self.fnetDict['BtName'].replace('/','_')
                filename_filter = "文件类型 (*.torrent)|*.torrent||"
                dlg = win32ui.CreateFileDialog(0, None, file_name, 1, filename_filter, None)
                dlg.SetOFNInitialDir("C:")
                dlg.SetOFNTitle("Please select the save dir")
                flag = dlg.DoModal()
                if flag == 1:
                    path = dlg.GetPathName()
                    try:
                        self.myGetLinkfNet.DownLoadTor(path,self.txtMsg.toPlainText(),self.ReportHook)
                        self.progressBar.setValue(100)
                    except Exception as msg:
                        print(msg)

    #关于我们
    def MenuAboutUs_Click(self):
        ver_str =str(self.setIniFile.GetIniValue('System', 'verstr'))
        theme = int(self.setIniFile.GetIniValue('System', 'theme'))
        theme_str = 'NativeTheme'
        if theme==1:
            theme_str = 'NativeTheme'
        else:
            theme_str = 'NightTheme'
        self.aboutWin = AboutWindow(theme_str)
        self.aboutWin.ShowWindows()
        self.aboutWin.retranslateUi(self.aboutWin)
        self.aboutWin.SetAuthorData(ver_str)

    #设置菜单
    def MenuSetting_Click(self):
        #打开设置窗口
        theme = int(self.setIniFile.GetIniValue('System', 'theme'))
        theme_str = 'NativeTheme'
        if theme == 1:
            theme_str = 'NativeTheme'
        else:
            theme_str = 'NightTheme'
        self.setWin = SettingWindow(self.setIniFile,theme_str)
        self.setWin.ShowWindows()
        self.setWin.retranslateUi(self.setWin)

    #批量重命名
    def MenuRename_Click(self):
        theme = int(self.setIniFile.GetIniValue('System', 'theme'))
        theme_str = 'NativeTheme'
        if theme == 1:
            theme_str = 'NativeTheme'
        else:
            theme_str = 'NightTheme'
        self.batRenameWin = BatchRenameWindow(theme_str)
        self.batRenameWin.ShowWindows()
        self.batRenameWin.retranslateUi(self.batRenameWin)


    #VIP转换通道
    def MenuVipCon_Click(self):
        theme = int(self.setIniFile.GetIniValue('System', 'theme'))
        theme_str = 'NativeTheme'
        if theme == 1:
            theme_str = 'NativeTheme'
        else:
            theme_str = 'NightTheme'
        self.vipConWin = VConvertWindow(self.setIniFile,theme_str)
        self.vipConWin.ShowWindows()
        self.vipConWin.retranslateUi(self.vipConWin)

    def MenuVipDown_Click(self):
        if self.vipDownOpenFg == 0:
            theme = int(self.setIniFile.GetIniValue('System', 'theme'))
            theme_str = 'NativeTheme'
            if theme == 1:
                theme_str = 'NativeTheme'
            else:
                theme_str = 'NightTheme'
            self.vipDownWin = VDownWindow(self.setIniFile,theme_str)
            self.vipDownWin.myCloseSignal.connect(self.VipDownWinClose_Event)
            self.vipDownWin.ShowWindows()
            self.vipDownWin.retranslateUi(self.vipDownWin)
            self.vipDownOpenFg = 1

    def VipDownWinClose_Event(self):
        self.vipDownOpenFg = 0
        self.vipDownWin.deleteLater()

    def VipDownWinTaskClose_Event(self,index):
        self.downWinArr[index] = 0
        self.downWinArr[index].deleteLater()

    #打开下载窗口
    def OpenDownWin(self,flag,path):
        if self.vipDownOpenFg == 0:
            theme = int(self.setIniFile.GetIniValue('System', 'theme'))
            theme_str = 'NativeTheme'
            if theme == 1:
                theme_str = 'NativeTheme'
            else:
                theme_str = 'NightTheme'
            self.vipDownWin = VDownWindow(self.setIniFile,theme_str)
            self.vipDownWin.myCloseSignal.connect(self.VipDownWinClose_Event)
            self.vipDownWin.ShowWindows()
            self.vipDownWin.retranslateUi(self.vipDownWin)
            self.vipDownWin.SetM3U8Init(flag, path)
            self.vipDownOpenFg = 1

    #多任务下载窗口
    def OpenTaskDownWin(self,flag,path,task_count):
        m_task_list = []
        theme = int(self.setIniFile.GetIniValue('System', 'theme'))
        theme_str = 'NativeTheme'
        if theme == 1:
            theme_str = 'NativeTheme'
        else:
            theme_str = 'NightTheme'
        if len(self.downWinArr)==0:
            for i in range(0,task_count):
                self.downWinArr.append(VDownWindow(self.setIniFile,theme_str))
                m_task_list.append([])

        #分拆任务
        task_avg_count = int(len(path)/task_count)
        if len(path)%task_count==0:
            for i in range(0,task_count):
                for a_i in range(0,task_avg_count):
                    m_task_list[i].append(path[(i*task_avg_count)+a_i])
        else:
            for i in range(0, task_count):
                count = task_avg_count
                if i<task_count-1:
                    count = task_avg_count
                else:
                    count = task_avg_count+(len(path)%task_count)
                for a_i in range(0, count):
                    if ((i * task_avg_count) + a_i) < len(path):
                        m_task_list[i].append(path[(i * task_avg_count) + a_i])


        for item in range(0,task_count):
            if self.downWinOFgArr[item]==0:
                vip_down_win_t = self.downWinArr[item]
                vip_down_win_t.myCloseSignal.connect(lambda: self.VipDownWinTaskClose_Event(item))
                vip_down_win_t.ShowWindows()
                vip_down_win_t.retranslateUi(vip_down_win_t)
                vip_down_win_t.setWindowTitle(vip_down_win_t.windowTitle()+ ' Task->' + str((item+1)))
                vip_down_win_t.SetM3U8Init(flag, m_task_list[item])
                self.downWinOFgArr[item] = 1

    def MenuGetM3U8_Click(self):
        self.OpenDownWin(2,'')

    def MenuReadFile_Click(self):
        filename_filter = "文件类型 (*.m3u8)|*.m3u8||"
        dlg = win32ui.CreateFileDialog(1, None,'', 1, filename_filter, None)
        dlg.SetOFNInitialDir("C:")
        dlg.SetOFNTitle("Please select the m3u8 file")
        if dlg.DoModal() == 1:
            self.OpenDownWin(1,dlg.GetPathName())

    #批量下载
    def MenuBatchDown_Click(self):
        theme = int(self.setIniFile.GetIniValue('System', 'theme'))
        theme_str = 'NativeTheme'
        if theme == 1:
            theme_str = 'NativeTheme'
        else:
            theme_str = 'NightTheme'
        self.batchDownWin = BatchDownWindow(self,theme_str)
        self.batchDownWin.show()
        self.batchDownWin.retranslateUi(self.batchDownWin)

    #下载所有
    def DownloadAllLink(self,all_link,flag,task_count):
        if task_count==0:
            if self.vipDownOpenFg == 0:
                if flag==3: # 多线程下载
                    self.OpenDownWin(6, all_link)
                elif flag==2:# 单线程下载
                    self.OpenDownWin(7, all_link)
                else:        #M3U8
                    self.OpenDownWin(4, all_link)
            else:
                if flag==3:
                    self.vipDownWin.SetM3U8Init(6, all_link)
                elif flag == 2:
                    self.vipDownWin.SetM3U8Init(7, all_link)
                else:
                    self.vipDownWin.SetM3U8Init(4, all_link)
        else:
            if flag == 3:  # 多线程下载
                self.OpenTaskDownWin(6, all_link,task_count)
            elif flag == 2:  # 单线程下载
                self.OpenTaskDownWin(7, all_link,task_count)
            else:  # M3U8
                self.OpenTaskDownWin(4, all_link,task_count)

        #关闭窗体
        self.batchDownWin.CloseWindow()

    #语言切换
    def MenuLangChange(self,lan_index):
        #  翻译家
        self.transLang = QTranslator()
        if lan_index==1:   #简体中文
            self.transLang.load("./Language/zh_CN")
        elif lan_index==2: #繁体中文
            self.transLang.load("./Language/zh_HK")
        else:              #默认英文
            self.transLang.load("./Language/en_US")

        self.setIniFile.SetIniValue('System','lang_flag',str(lan_index))
        _app = QApplication.instance()
        _app.installTranslator(self.transLang)
        self.retranslateUi(self)

    def MenuTheme_Click(self,t_index):
        exe_path = r'"{0}"'.format(os.getcwd() + '\\MyApp.exe')
        if t_index==1:
            self.setIniFile.SetIniValue('System', 'theme', str(t_index))
            win32api.MessageBox(0, 'The theme will not take effect until it is restarted', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
            try:
                win32api.ShellExecute(0, 'open', exe_path, '', '', 0)
                self.close()
            except Exception as msg:
                self.statusbar.showMessage('Error:' + str(msg))
        elif t_index==2:
            self.setIniFile.SetIniValue('System', 'theme', str(t_index))
            win32api.MessageBox(
                0,
                'The theme will not take effect until it is restarted',
                "Tip",
                win32con.MB_ICONINFORMATION,
                win32con.MB_OK)
            try:
                win32api.ShellExecute(0, 'open', exe_path, '', '', 0)
                self.close()
            except Exception as msg:
                self.statusbar.showMessage('Error:' + str(msg))
        else:
            pass


    #显示连接
    def ShowUrl(self,link_arr):
        find_str = 'ahundr：'
        for item in link_arr:
            for i in range(0, len(item)):
                split_str = item[i].split("$")
                for myitem in split_str:
                    myitem = str(myitem)
                    if myitem.find(find_str)!=-1:
                        myitem = myitem.replace(find_str,'thunder:')
                    self.signal.emit(myitem)
                    #self.txtMsg.append(myitem)
                self.signal.emit("")
        self.statusbar.showMessage('Resource Count:' + str(len(link_arr)))
                #self.txtMsg.append("")

    def GetAppPath(self):
        list_path = sys.argv
        index = list_path[0].rfind('\\')
        return list_path[0][0:index]

    #更新列表
    def UpdateListView(self):
        slm = QStringListModel()       # 实例化列表模型，添加数据
        slm.setStringList(self.qList)  # 设置模型列表视图，加载数据列表
        self.listView.setModel(slm)    # 设置列表视图的模型

    def UpdateListView_Hd(self):
        slm = QStringListModel()  # 实例化列表模型，添加数据
        slm.setStringList(self.qListHd)  # 设置模型列表视图，加载数据列表
        self.listView_2.setModel(slm)  # 设置列表视图的模型

    #TV列表
    def UpdateListView_Addr(self):
        slm = QStringListModel()  # 实例化列表模型，添加数据
        slm.setStringList(self.qListAddr)  # 设置模型列表视图，加载数据列表
        self.listTvPlace.setModel(slm)  # 设置列表视图的模型

    def UpdateListView_Tv(self):
        slm = QStringListModel()  # 实例化列表模型，添加数据
        slm.setStringList(self.qListTv)  # 设置模型列表视图，加载数据列表
        self.listTvLive.setModel(slm)  # 设置列表视图的模型

    def UpdateListView_BT(self):
        slm = QStringListModel()  # 实例化列表模型，添加数据
        slm.setStringList(self.qListBt)  # 设置模型列表视图，加载数据列表
        self.listViewBt.setModel(slm)  # 设置列表视图的模型

    #更新图片
    def UpdateMovPicture(self,img,flag):
        if len(img)>0:
            image = QImage.fromData(img)
            pixmap = QPixmap.fromImage(image)
            if flag==1:
                pixmap = pixmap.scaled(130, 150, aspectRatioMode=Qt.KeepAspectRatio)
                self.imgMovie.setPixmap(pixmap)
            elif flag==2:
                pixmap = pixmap.scaled(180, 190, aspectRatioMode=Qt.KeepAspectRatio)
                self.labHdImg.setPixmap(pixmap)
            elif flag==3:
                pixmap = pixmap.scaled(250, 250, aspectRatioMode=Qt.KeepAspectRatio)
                self.labTvImg.setPixmap(pixmap)
            else:
                pass


    #更新数据
    def UpdateTextMsg(self,str):
        self.txtMsg.append(str)

    def SetTextMsg(self,str):
        self.txtMsg.setText(str)

    def UpdateTextMsg_Hd(self, str):
        self.txtMsgHd.append(str)

    def SetTextMsg_Hd(self, str):
        self.txtMsgHd.setText(str)

    def UpdateTextMsg_Tv(self, str):
        self.txtMsgTv.append(str)

    def SetTextMsg_Tv(self, str):
        self.txtMsgTv.setText(str)

    def UpdateTextMsg_Bt(self, str):
        self.txtBtMsg.append(str)

    def SetTextMsg_Bt(self, str):
        self.txtBtMsg.setText(str)

    # 及时更新进度
    def ReportHook(self, data, datas, file_size):
        """
        显示下载进度
        :param data: 已经下载的数据块
        :param datas: 数据块的大小
        :param file_size: 远程文件大小
        :return: None
        """
        self.progressBar.setValue((data * datas * 100.0 / file_size))
        # print("\rdownloading: %5.1f%%" % (a * b * 100.0 / c), end="")