import base64
import subprocess
import threading
import time

import win32api
import win32con
import win32ui
import os.path
import re
import pyperclip
import urllib

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QStringListModel, QFileInfo, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog
from Crypto.Cipher import AES

from Function.QssHelper import QssHelper
from Function.ReadM3U8File import ReadM3U8File
from Function import StopThread
from Function.VipdEng.VipChangeSoe import VipChangeSoe
from Function.VipdEng.VipChange8090 import VipChange8090
from Function.VipdEng.VipChangeOsCloud import VipChangeOsCloud
from Form.VipDownWin.VipDownUi import Ui_VDownWindow


class VDownWindow(QtWidgets.QMainWindow, Ui_VDownWindow):
    myCloseSignal = QtCore.pyqtSignal(str)
    signal_url_set = QtCore.pyqtSignal(str)
    signal_list_vipd = QtCore.pyqtSignal()          # VIP视频搜索转换
    signal_msg_append_vipd = QtCore.pyqtSignal(str)
    signal_msg_set_vipd = QtCore.pyqtSignal(str)
    signal_pb_set = QtCore.pyqtSignal(int)
    signal_cbo_sel = QtCore.pyqtSignal(int)

    signal_msg_append = QtCore.pyqtSignal(str)
    signal_msg_set = QtCore.pyqtSignal(str)
    signal_btn_stop_set = QtCore.pyqtSignal(int)


    def __init__(self,ini_file,theme_str):
        super(VDownWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint);  # 窗体没有最大化最小化按钮
        self.setFixedSize(660, 550)  # 设置窗体的大小
        self.setWindowIcon(QIcon("./Image/Icon_GetSource.png"))
        # 加载样式
        self._SetControlProperty(theme_str)
        self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format(theme_str)))

        self.setIniFile = ini_file

        #绑定事件
        self._EventBinding()

        #初始化设置
        self._InitSetUp()


    def ShowWindows(self):
        self.show()

    def closeEvent(self, event):
        self.SendCloseMsg()

    def _SetControlProperty(self,theme_str):
        scroll_path = './Qss/{0}/ScrollBarStyle.qss'.format(theme_str)
        self.setProperty('name', 'VipDownFrm')
        self.btnGetUrl.setProperty('name','btnGetUrl')
        self.btnMerge.setProperty('name', 'btnMerge')
        self.btnDownMerge.setProperty('name', 'btnDownMerge')
        self.btnDown.setProperty('name', 'btnDown')
        self.listView.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_path))
        self.listView.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_path))
        self.txtMsg.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_path))
        self.txtLink.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_path))
        self.txtUrl.verticalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_path))
        self.txtMsg.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_path))
        self.txtLink.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_path))
        self.txtUrl.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss(scroll_path))


    def SendCloseMsg(self):
        self.myCloseSignal.emit("0")

    #事件绑定
    def _EventBinding(self):
        self.btnGetUrl.clicked.connect(self.BtnGetUrl_Click)
        self.btnDown.clicked.connect(self.BtnDown_Click)
        self.btnDownMerge.clicked.connect(self.BtnDownMerge_Click)
        self.btnMerge.clicked.connect(self.BtnMerge_Click)
        self.btnStop.clicked.connect(self.BtnStop_Click)
        self.actionClear_List.triggered.connect(self.MenuClearList_Click)
        self.actionShow_in_Explorer.triggered.connect(self.MenuShowExplorer_Click)


    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key()==Qt.Key_F7:
            self.txtUrl.setText(pyperclip.paste())
            self.btnGetUrl.click()
        elif qKeyEvent.key()==Qt.Key_F8:
           pyperclip.copy(self.txtLink.textCursor().selectedText())
           self.txtLink.textCursor()
        elif qKeyEvent.key()==Qt.Key_F6:
            pyperclip.copy(self.txtLink.toPlainText())
        else:
            pass


    #初始化设置
    def _InitSetUp(self):
        #开启线程任务总数
        self.THREAD_TASK_COUNT = int(self.setIniFile.GetIniValue('System', 'thread_count')) + 3
        self.MUTLI_MIN_LEN = 1024*1024

        self.seaEnginesVipd = []
        self.qListVipd = []
        self.combineFiles = []  #合并文件对象

        #多线程下载任务列表-八线程下载
        self.dTaskList1 = []
        self.dTaskList2 = []
        self.dTaskList3 = []
        self.dTaskList4 = []
        self.dTaskList5 = []
        self.dTaskList6 = []
        self.dTaskList7 = []
        self.dTaskList8 = []

        #任务线程标志位
        self.dRunFlag = 0
        self.dTaskFlag = [0,0,0,0,0,0,0,0]

        self.dErrFlag=[0,0,0,0,0,0,0,0]

        #任务进度
        self.dTaskProcUpFlag = 0
        self.dTaskProcIndex = [0,0,0,0,0,0,0,0]

        #任务下载总路径
        self.dTaskAllPath = []

        #获取下载时间
        self.startDownTime = 0
        self.endDownTime = 0

        #批量下载标志位
        self.batchDownFlag = 0
        self.batchDownIndex = 0

        #暂停继续下载标志位
        self.pauseFlag = 0

        #是否应用AES-128解密
        self.aesFlag = 0
        self.aesKey = ''


        # VIP Change Engine
        item_vipd_count = int(self.setIniFile.GetIniValue('CboItem_VipDown', 'item_count')) + 1
        for t_i in range(1, item_vipd_count):
            tag_str = 'item_' + str(t_i)
            temp_str = str(self.setIniFile.GetIniValue('CboItem_VipDown', tag_str))
            self.seaEnginesVipd.append(temp_str)
        self.cboExEng.addItems(self.seaEnginesVipd)
        self.cboExEng.currentIndexChanged.connect(self.CboExEngIndexChanged)

        #设置初始状态
        self.vipdownch = int(self.setIniFile.GetIniValue('System', 'vipdownch'))
        self.cboExEng.setCurrentIndex(self.vipdownch - 1)

        #信号绑定
        self.signal_list_vipd.connect(self.UpdateListView_Vipd)
        self.signal_msg_append_vipd.connect(self.UpdateTextMsg_Vipd)
        self.signal_msg_set_vipd.connect(self.SetTextMsg_Vipd)

        self.signal_msg_append.connect(self.UpdateTextMsg)
        self.signal_msg_set.connect(self.SetTextMsg)

        self.signal_pb_set.connect(self.UpdateProgBar)
        self.signal_url_set.connect(self.SetUrlText)

        self.signal_cbo_sel.connect(self.SetCboIndex)

        self.signal_btn_stop_set.connect(self.SetBtnStopSta)


        self.myVipChangeSoe = VipChangeSoe()
        tag_url = str(self.setIniFile.GetIniValue('TagetUrl', 'url_19'))
        self.myVipChangeSoe.SetBaseUrl(tag_url)

        self.myVipChange8090 = VipChange8090()
        self.myVipChange8090.SetBaseUrl(str(self.setIniFile.GetIniValue('TagetUrl', 'url_30')))
        self.myVipChange8090.SetRootUrl(str(self.setIniFile.GetIniValue('TagetUrl', 'url_29')))
        self.myVipChange8090.SetInterFace(str(self.setIniFile.GetIniValue('TagetUrl', 'url_31')))

        self.myVipChangeOsCloud = VipChangeOsCloud()
        self.myVipChangeOsCloud.SetBaseUrl(str(self.setIniFile.GetIniValue('TagetUrl', 'url_38')))

        #普通线程
        self.thDownFile = threading.Thread(target=self.MyDownFileTask)
        self.thDownFile.setDaemon(True)
        self.thDownFile.start()

        #建立下载线程-3线程同时下载
        self.thDownTask1 = threading.Thread(target=self.MyDownTask1)
        self.thDownTask1.setDaemon(True)
        self.thDownTask1.start()

        self.thDownTask2 = threading.Thread(target=self.MyDownTask2)
        self.thDownTask2.setDaemon(True)
        self.thDownTask2.start()

        self.thDownTask3 = threading.Thread(target=self.MyDownTask3)
        self.thDownTask3.setDaemon(True)
        self.thDownTask3.start()

        self.thDownTask4 = threading.Thread(target=self.MyDownTask4)
        self.thDownTask4.setDaemon(True)
        self.thDownTask4.start()

        self.thDownTask5 = threading.Thread(target=self.MyDownTask5)
        self.thDownTask5.setDaemon(True)
        self.thDownTask5.start()

        self.thDownTask6 = threading.Thread(target=self.MyDownTask6)
        self.thDownTask6.setDaemon(True)
        self.thDownTask6.start()

        self.thDownTask7 = threading.Thread(target=self.MyDownTask7)
        self.thDownTask7.setDaemon(True)
        self.thDownTask7.start()

        self.thDownTask8 = threading.Thread(target=self.MyDownTask8)
        self.thDownTask8.setDaemon(True)
        self.thDownTask8.start()

        #初始化RB设置
        self.rbFfmpeg.setChecked(True)
        self.rbNormally.setChecked(False)

    #Cbo 选择事件
    def CboExEngIndexChanged(self,index):
        if index >=0 and index<=5:
            self.vipdownch = index+1
            self.setIniFile.SetIniValue('System', 'vipdownch', str(self.vipdownch))
        else:
            pass

    #设置M3U8
    def SetM3U8Init(self,mode,list):
        if mode==1:
            self.cboExEng.setCurrentIndex(1)
            read_m3u8 = ReadM3U8File(list)
            flag,data = read_m3u8.ReadFile()
            if flag:
                self.listTs = read_m3u8.GetM3U8FromList(data)
                self.qListVipd.clear()
                for item in self.listTs:
                    self.qListVipd.append(item['MovName'])
                self.signal_list_vipd.emit()
                self.statusbar.showMessage('Resource Count:' + str(len(self.listTs)))
        elif mode==2:
            self.cboExEng.setCurrentIndex(1)
        elif mode==3:
            read_m3u8 = ReadM3U8File('')      #从网址中获取M3U8资源
            data,key_url,mov_url = read_m3u8.GetUrlFile(list)

            if 'base64,' in key_url:#base64进行视频解码
                self.v_base_head =base64.b64decode(key_url.replace('base64,',''))
                self.aesFlag = 2
            elif key_url!='':    #获取AES秘钥
                self.aesKey = read_m3u8.GetAesKey(os.path.dirname(list)+'/'+key_url)
                self.aesFlag = 1
            else:
                self.aesKey = ''
                self.aesFlag = 0

            self.listTs = read_m3u8.GetM3U8FromList(data)
            if not 'http' in self.listTs[0]['MovPath']:
                self.signal_url_set.emit('')
                self.signal_msg_append.emit('Please add root url!\r\n')
                self.signal_msg_append.emit(mov_url+'\r\n')
                self.signal_msg_set_vipd.emit(mov_url)
            self.qListVipd.clear()
            for item in self.listTs:
                self.qListVipd.append(item['MovName'])
            self.signal_list_vipd.emit()
            self.statusbar.showMessage('Resource Count:' + str(len(self.listTs)))
        elif mode==4:#批量下载
            self.cboExEng.setCurrentIndex(1)
            self.allDownLink = list
            self.batchDownFlag = 1
            self.batchDownIndex = 0
            self.RunDownList(self.batchDownIndex)
            self.statusbar.showMessage('Start download list...')
        elif mode==5:
            read_m3u8 = ReadM3U8File('')
            data,key_url,mov_url = read_m3u8.GetUrlFile(list['FileLink'])

            if 'base64,' in key_url:  # base64进行视频解码
                self.v_base_head = base64.b64decode(key_url.replace('base64,', ''))
                self.aesFlag = 2
            elif key_url != '':  # 获取AES秘钥
                self.aesKey = read_m3u8.GetAesKey(os.path.dirname(list['FileLink'])+'/'+key_url)
                self.aesFlag = 1
            else:
                self.aesKey = ''
                self.aesFlag = 0

            self.listTs = read_m3u8.GetM3U8FromList(data)
            if not 'http' in self.listTs[0]['MovPath']:
                self.signal_url_set.emit(list['BaseLink'])
            self.qListVipd.clear()
            for item in self.listTs:
                self.qListVipd.append(item['MovName'])
            self.signal_list_vipd.emit()
            self.statusbar.showMessage('Resource Count:' + str(len(self.listTs)))
        elif mode==6:  #多线程批量下
            self.cboExEng.setCurrentIndex(4)
            self.allDownLink = list
            self.batchDownFlag = 1
            self.batchDownIndex = 0
            self.RunMulitList(self.batchDownIndex)
            self.statusbar.showMessage('Start download list...')
        elif mode==7:#单线程批量下载
            self.cboExEng.setCurrentIndex(2)
            self.allDownLink = list
            self.dRunFlag=6
            self.statusbar.showMessage('Start download list...')
        else:
            pass

    #循环执行  批量进行下载
    def RunDownList(self,index):
        link = self.allDownLink[index]['FileLink']
        base_link = self.allDownLink[index]['BaseLink']

        #获取列表
        self.signal_url_set.emit(link)
        if base_link=='':
            self.SetM3U8Init(3,link)
        else:
            self.SetM3U8Init(5, self.allDownLink[index])#加入源地址进行下载

        #准备下载
        self.savePath = self.allDownLink[index]['FileName']
        if self.allDownLink[index]['CombMode']=='0':
            self.rbFfmpeg.setChecked(True)
        elif self.allDownLink[index]['CombMode']=='1':
            self.rbNormally.setChecked(True)
        else:
            pass

        self.DownMovFile()

    def RunMulitList(self,index):
        link = self.allDownLink[index]['FileLink']
        if 'thunder' in link:
            link = self.ThunderLink(link)
        self.masterKey = link
        # 获取列表
        self.signal_url_set.emit(link)

        #准备下载
        self.savePath = self.allDownLink[index]['FileName']
        self._StartDownFile()


    #按钮点击事件
    #获取链接事件
    def BtnGetUrl_Click(self):
        self.masterKey = self.txtUrl.toPlainText()
        self.dRunFlag = 1
        self.statusbar.showMessage('Finding...')


    #下载所有视频
    def BtnDown_Click(self):
        filename_filter = "文件类型 (*.mkv)|*.mkv||"
        dlg = win32ui.CreateFileDialog(0, None, '', 1, filename_filter, None)
        dlg.SetOFNInitialDir("C:")
        dlg.SetOFNTitle("Please select the save dir")
        flag = dlg.DoModal()
        if flag == 1:
            self.savePath = dlg.GetPathName()
            if (self.cboExEng.currentIndex()!=2) and (self.cboExEng.currentIndex()!=4) :
                self.dRunFlag = 2
            else:
                self.masterKey = self.txtUrl.toPlainText()
                if 'thunder' in self.masterKey:
                    self.masterKey = self.ThunderLink(self.masterKey)
                self.dRunFlag = 4   #单一文件下载
            self.statusbar.showMessage('Downloading...')

    #迅雷链接转换为普通链接
    def ThunderLink(self,link):
        result_str=""
        link = link.replace("thunder://", "")
        result_str = str(base64.b64decode(link), 'utf-8')
        result_str = urllib.parse.unquote(result_str[2:-2])
        return result_str

    #选择文件
    def BtnDownMerge_Click(self):
        files, file_type = QFileDialog.getOpenFileNames(self, "Please Select File", "/", "TS文件 (*.ts);;所有文件 (*)")
        for file in files:
            temp_file = QFileInfo(file)
            self.qListVipd.append(temp_file.fileName())
            self.combineFiles.append(file)
        self.signal_list_vipd.emit()

    #单独合并视频
    def BtnMerge_Click(self):
        filename_filter = "文件类型 (*.mkv)|*.mkv||"
        dlg = win32ui.CreateFileDialog(0, None, '', 1, filename_filter, None)
        dlg.SetOFNInitialDir("C:")
        dlg.SetOFNTitle("Please select the save dir")
        flag = dlg.DoModal()
        if flag == 1:
            savePath = dlg.GetPathName()
            self.dRunFlag = 3
            self._RunFfmpegImport(savePath)

    #暂停目前下载的任务
    def BtnStop_Click(self):
        if self.pauseFlag == 0:
            self.pauseFlag = 1
        else:
            self.pauseFlag = 0
        self.SetBtnStopSta(self.pauseFlag)

    #设置状态
    def SetBtnStopSta(self,flag):
        pause_str = ''
        if flag == 1:
            if self.btnDown.text()=='下载':pause_str = '暂停'
            elif self.btnDown.text()=='下載':pause_str = '暫停'
            else:pause_str = 'Task Pause'
        else:
            if self.btnDown.text()=='下载':pause_str = '开始'
            elif self.btnDown.text()=='下載':pause_str = '開始'
            else:pause_str = 'Task Start'
        self.signal_msg_append.emit(pause_str+'!')
        self.btnStop.setText(pause_str)


    #清空列表
    def MenuClearList_Click(self):
        self.qListVipd.clear()
        self.combineFiles.clear()
        self.signal_list_vipd.emit()

    #打开文件夹
    def MenuShowExplorer_Click(self):
        try:
            os.system('start explorer '+os.path.dirname(self.savePath))
        except Exception as msg:
            self.signal_msg_append.emit('\n\nError:'+str(msg))


    def MyDownFileTask(self):
        while True:
            try:
                if self.dRunFlag==1:
                    self.dRunFlag = 0
                    self.FindFileList()
                elif self.dRunFlag==2:   #下载文件
                    self.dRunFlag=0
                    self.DownMovFile()
                elif self.dRunFlag==3:
                    self._GetFfmpegMsg()
                elif self.dRunFlag==4:
                    self.dRunFlag = 0
                    if self.vipdownch==3:
                        self._RunSingleDown() #下载单一文件
                    elif self.vipdownch==5:
                        self._StartDownFile()#多线程下载文件
                elif self.dRunFlag==5:
                    self.dRunFlag=0
                    self._CombineDownFile()
                elif self.dRunFlag==6:   #单线程批量下载文件
                    self.dRunFlag = 0
                    self._RunSingleDownList()
                else:
                    self.dRunFlag = 0
                if self.dTaskProcUpFlag==1:
                    if self.vipdownch!=5:
                        self._CalcProb(1)
                    else:
                        self._CalcProb(2)
            except:
                if self.dRunFlag!=0:
                    self.dRunFlag = 0
            time.sleep(2)

    #利用多线程并行下载
    def MyDownTask1(self):
        while True:
            if self.dTaskFlag[0]==1:
                self.dTaskFlag[0] = 0
                self.DownFileTask(1,1)
            elif self.dTaskFlag[0]==2:
                self.dTaskFlag[0] = 0
                self.DownFileTask(1,2)
            time.sleep(1)#休眠

    def MyDownTask2(self):
        while True:
            if self.dTaskFlag[1]==1:
                self.dTaskFlag[1] = 0
                self.DownFileTask(2,1)
            elif self.dTaskFlag[1] == 2:
                self.dTaskFlag[1] = 0
                self.DownFileTask(2,2)
            time.sleep(1)  # 休眠

    def MyDownTask3(self):
        while True:
            if self.dTaskFlag[2]==1:
                self.dTaskFlag[2] = 0
                self.DownFileTask(3,1)
            elif self.dTaskFlag[2] == 2:
                self.dTaskFlag[2] = 0
                self.DownFileTask(3,2)
            time.sleep(1)  # 休眠

    def MyDownTask4(self):
        while True:
            if self.dTaskFlag[3]==1:
                self.dTaskFlag[3] = 0
                self.DownFileTask(4,1)
            elif self.dTaskFlag[3] == 2:
                self.dTaskFlag[3] = 0
                self.DownFileTask(4,2)
            time.sleep(1)  # 休眠

    def MyDownTask5(self):
        while True:
            if self.dTaskFlag[4]==1:
                self.dTaskFlag[4] = 0
                self.DownFileTask(5,1)
            elif self.dTaskFlag[4] == 2:
                self.dTaskFlag[4] = 0
                self.DownFileTask(5,2)
            time.sleep(1)  # 休眠

    def MyDownTask6(self):
        while True:
            if self.dTaskFlag[5]==1:
                self.dTaskFlag[5] = 0
                self.DownFileTask(6,1)
            elif self.dTaskFlag[5] == 2:
                self.dTaskFlag[5] = 0
                self.DownFileTask(6,2)
            time.sleep(1)  # 休眠

    def MyDownTask7(self):
        while True:
            if self.dTaskFlag[6]==1:
                self.dTaskFlag[6] = 0
                self.DownFileTask(7,1)
            elif self.dTaskFlag[6] == 2:
                self.dTaskFlag[6] = 0
                self.DownFileTask(7,2)
            time.sleep(1)  # 休眠

    def MyDownTask8(self):
        while True:
            if self.dTaskFlag[7]==1:
                self.dTaskFlag[7] = 0
                self.DownFileTask(8,1)
            elif self.dTaskFlag[7] == 2:
                self.dTaskFlag[7] = 0
                self.DownFileTask(8,2)
            time.sleep(1)  # 休眠

    #寻找所有的TS文件
    def FindFileList(self):
        if self.cboExEng.currentIndex()==0:    #618G
            self.qListVipd.clear()
            self.allLink,self.tagUrl = self.myVipChangeSoe.SearchMasterUrl(self.masterKey)
            for item in self.allLink:
                self.qListVipd.append(item['MovName'])
            self.signal_list_vipd.emit()
            self.signal_msg_set_vipd.emit(self.tagUrl)
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboExEng.currentIndex()==1: #M3u8
            self.SetM3U8Init(3,self.masterKey)
        elif self.cboExEng.currentIndex()==3: #8090
            self.allLink,self.tagUrl = self.myVipChange8090.SearchMaster(self.masterKey)
            if len(self.allLink) >0:
                for item in self.allLink:
                    self.qListVipd.append(item['MovName'])
                self.signal_list_vipd.emit()
            else:
                self.signal_url_set.emit(self.tagUrl)
                self.signal_cbo_sel.emit(2)
            self.signal_msg_set_vipd.emit(self.tagUrl)
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))
        elif self.cboExEng.currentIndex() == 5:  # 1717Cloud
            self.allLink, self.tagUrl = self.myVipChangeOsCloud.SearchMaster(self.masterKey)
            self.signal_msg_set_vipd.emit(self.tagUrl)
        else:
            self.statusbar.showMessage('Resource Count:None')

    #计算进度条
    def _CalcProb(self,flag):
        sum = len(self.dTaskList1)+len(self.dTaskList2)+len(self.dTaskList3)+len(self.dTaskList4)+len(self.dTaskList5)+len(self.dTaskList6)+len(self.dTaskList7)+len(self.dTaskList8)
        cur = self.dTaskProcIndex[0]+self.dTaskProcIndex[1]+self.dTaskProcIndex[2]+self.dTaskProcIndex[3]+self.dTaskProcIndex[4]+self.dTaskProcIndex[5]+self.dTaskProcIndex[6]+self.dTaskProcIndex[7]
        if cur==sum:
            self.dTaskProcUpFlag=0

            #计算总下载时间
            self.endDownTime = time.time()
            sum_time = self.endDownTime - self.startDownTime

            self.signal_msg_append.emit('\r\nSum download Time:' + str(int(sum_time))+'s')
            self.signal_msg_append.emit('\r\nTask assigned successfully!')
            self.statusbar.showMessage('Download success!')

            #执行合成
            if flag==1:
                if self.rbFfmpeg.isChecked():
                    self.dRunFlag = 3
                    self._RunFfmpeg('')
                else:
                    self._CombineDownFileM3U8() #普通流式合成
            elif flag==2:
                self.dRunFlag = 5
            else:
                pass
        temp_val = cur*100/sum
        self.signal_pb_set.emit(temp_val)

    #下载文件
    def DownMovFile(self):
        tag_dir = self.savePath[:self.savePath.rfind('\\')]
        if os.path.isdir(tag_dir):
            #建立缓存路径
            self.dTaskAllPath.clear()
            temp_ts_folder = self.savePath+'_ts'
            if not os.path.isdir(temp_ts_folder):
                os.mkdir(temp_ts_folder)

            self.dTaskAllPath.append(temp_ts_folder)

            temp_path_1 = temp_ts_folder+'\\hls_1'
            if not os.path.isdir(temp_path_1):
                os.mkdir(temp_path_1)
            self.dTaskAllPath.append(temp_path_1)

            temp_path_2 = temp_ts_folder + '\\hls_2'
            if not os.path.isdir(temp_path_2):
                os.mkdir(temp_path_2)
            self.dTaskAllPath.append(temp_path_2)

            temp_path_3 = temp_ts_folder + '\\hls_3'
            if not os.path.isdir(temp_path_3):
                os.mkdir(temp_path_3)
            self.dTaskAllPath.append(temp_path_3)

            if self.THREAD_TASK_COUNT>=4:                 #控制线程数量
                temp_path_4 = temp_ts_folder + '\\hls_4'
                if not os.path.isdir(temp_path_4):
                    os.mkdir(temp_path_4)
                self.dTaskAllPath.append(temp_path_4)

            if self.THREAD_TASK_COUNT >= 5:
                temp_path_5 = temp_ts_folder + '\\hls_5'
                if not os.path.isdir(temp_path_5):
                    os.mkdir(temp_path_5)
                self.dTaskAllPath.append(temp_path_5)

            if self.THREAD_TASK_COUNT >= 6:
                temp_path_6 = temp_ts_folder + '\\hls_6'
                if not os.path.isdir(temp_path_6):
                    os.mkdir(temp_path_6)
                self.dTaskAllPath.append(temp_path_6)

            if self.THREAD_TASK_COUNT >= 7:
                temp_path_7 = temp_ts_folder + '\\hls_7'
                if not os.path.isdir(temp_path_7):
                    os.mkdir(temp_path_7)
                self.dTaskAllPath.append(temp_path_7)

            if self.THREAD_TASK_COUNT >= 8:
                temp_path_8 = temp_ts_folder + '\\hls_8'
                if not os.path.isdir(temp_path_8):
                    os.mkdir(temp_path_8)
                self.dTaskAllPath.append(temp_path_8)

            #清空任务列
            self.dTaskList1.clear()
            self.dTaskList2.clear()
            self.dTaskList3.clear()
            self.dTaskList4.clear()
            self.dTaskList5.clear()
            self.dTaskList6.clear()
            self.dTaskList7.clear()
            self.dTaskList8.clear()

            if self.vipdownch ==1 or self.vipdownch ==4:
                #分配下载任务
                link_count = len(self.allLink)
                single_len = link_count/self.THREAD_TASK_COUNT

                for i in range(0,link_count):
                    url_path = self.allLink[i]['MovLink']
                    if i<(single_len*1):
                        file_name = temp_path_1 + '\\'+str(i)+'_'+ self.allLink[i]['MovName'].replace('-','_')
                        dict_detail = {
                            'UrlPath': url_path,
                            'FileName': file_name
                        }
                        self.dTaskList1.append(dict_detail)
                    elif i>=(single_len*1) and i<(single_len*2):
                        file_name = temp_path_2 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                        dict_detail = {
                            'UrlPath': url_path,
                            'FileName': file_name
                        }
                        self.dTaskList2.append(dict_detail)
                    elif i>=(single_len*2) and i<(single_len*3):
                        file_name = temp_path_3 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                        dict_detail = {
                            'UrlPath': url_path,
                            'FileName': file_name
                        }
                        self.dTaskList3.append(dict_detail)
                    elif i >= (single_len * 3) and i < (single_len * 4):
                        if self.THREAD_TASK_COUNT>=4:                    #控制线程数量
                            file_name = temp_path_4 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList4.append(dict_detail)
                        else:
                            if i<=(link_count-1):
                                file_name = temp_path_3 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                                dict_detail = {
                                    'UrlPath': url_path,
                                    'FileName': file_name
                                }
                                self.dTaskList3.append(dict_detail)
                    elif i >= (single_len * 4) and i < (single_len * 5):
                        if self.THREAD_TASK_COUNT >= 5:
                            file_name = temp_path_5 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList5.append(dict_detail)
                        else:
                            if i<=(link_count-1):
                                file_name = temp_path_4 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                                dict_detail = {
                                    'UrlPath': url_path,
                                    'FileName': file_name
                                }
                                self.dTaskList4.append(dict_detail)
                    elif i >= (single_len * 5) and i < (single_len * 6):
                        if self.THREAD_TASK_COUNT >= 6:
                            file_name = temp_path_6 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList6.append(dict_detail)
                        else:
                            if i<=(link_count-1):
                                file_name = temp_path_5 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                                dict_detail = {
                                    'UrlPath': url_path,
                                    'FileName': file_name
                                }
                                self.dTaskList5.append(dict_detail)
                    elif i >= (single_len * 6) and i < (single_len * 7):
                        if self.THREAD_TASK_COUNT >= 7:
                            file_name = temp_path_7 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList7.append(dict_detail)
                        else:
                            if i<=(link_count-1):
                                file_name = temp_path_6 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                                dict_detail = {
                                    'UrlPath': url_path,
                                    'FileName': file_name
                                }
                                self.dTaskList6.append(dict_detail)
                    else:
                        if self.THREAD_TASK_COUNT >= 8:
                            file_name = temp_path_8 + '\\'+str(i)+'_' + self.allLink[i]['MovName'].replace('-','_')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList8.append(dict_detail)
            elif self.vipdownch==2:
                base_tag_url = self.txtUrl.toPlainText()
                # 分配下载任务
                link_count = len(self.listTs)
                single_len = link_count / self.THREAD_TASK_COUNT

                for i in range(0, link_count):
                    url_path=''
                    if not 'http' in self.listTs[i]['MovPath']:
                        url_path =base_tag_url+ self.listTs[i]['MovPath']
                    else:
                        url_path = self.listTs[i]['MovPath']
                    if i < (single_len * 1):
                        file_name = temp_path_1 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                        dict_detail = {
                            'UrlPath': url_path,
                            'FileName': file_name
                        }
                        self.dTaskList1.append(dict_detail)
                    elif i >= (single_len * 1) and i < (single_len * 2):
                        file_name = temp_path_2 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                        dict_detail = {
                            'UrlPath': url_path,
                            'FileName': file_name
                        }
                        self.dTaskList2.append(dict_detail)
                    elif i >= (single_len * 2) and i < (single_len * 3):
                        file_name = temp_path_3 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                        dict_detail = {
                            'UrlPath': url_path,
                            'FileName': file_name
                        }
                        self.dTaskList3.append(dict_detail)
                    elif i >= (single_len * 3) and i < (single_len * 4):
                        if self.THREAD_TASK_COUNT >= 4:  # 控制线程数量
                            file_name = temp_path_4 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList4.append(dict_detail)
                        else:
                            if i <= (link_count - 1):
                                file_name = temp_path_3 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                                dict_detail = {
                                    'UrlPath': url_path,
                                    'FileName': file_name
                                }
                                self.dTaskList3.append(dict_detail)
                    elif i >= (single_len * 4) and i < (single_len * 5):
                        if self.THREAD_TASK_COUNT >= 5:  # 控制线程数量
                            file_name = temp_path_5 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList5.append(dict_detail)
                        else:
                            if i <= (link_count - 1):
                                file_name = temp_path_4 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                                dict_detail = {
                                    'UrlPath': url_path,
                                    'FileName': file_name
                                }
                                self.dTaskList4.append(dict_detail)
                    elif i >= (single_len * 5) and i < (single_len * 6):
                        if self.THREAD_TASK_COUNT >= 6:  # 控制线程数量
                            file_name = temp_path_6 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList6.append(dict_detail)
                        else:
                            if i <= (link_count - 1):
                                file_name = temp_path_5 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                                dict_detail = {
                                    'UrlPath': url_path,
                                    'FileName': file_name
                                }
                                self.dTaskList5.append(dict_detail)
                    elif i >= (single_len * 6) and i < (single_len * 7):
                        if self.THREAD_TASK_COUNT >= 7:  # 控制线程数量
                            file_name = temp_path_7 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList7.append(dict_detail)
                        else:
                            if i <= (link_count - 1):
                                file_name = temp_path_6 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                                dict_detail = {
                                    'UrlPath': url_path,
                                    'FileName': file_name
                                }
                                self.dTaskList6.append(dict_detail)
                    else:
                        if self.THREAD_TASK_COUNT >= 8:  # 控制线程数量
                            file_name = temp_path_8 + '\\' + self.listTs[i]['MovName'].replace('-','_').replace('.ts','_'+str(i)+'.ts')
                            dict_detail = {
                                'UrlPath': url_path,
                                'FileName': file_name
                            }
                            self.dTaskList8.append(dict_detail)
            else:
                return
            self.signal_msg_append.emit('\r\nTask assigned successfully!')
            self.statusbar.showMessage('Task assigned successfully!')

            self.dTaskProcUpFlag = 1
            for i in range(0,8):
                if i <self.THREAD_TASK_COUNT:
                    self.dTaskProcIndex[i] = 0
                    self.dTaskFlag[i] = 1
                else:
                    self.dTaskProcIndex[i] = 0
                    self.dTaskFlag[i] = 0

            self.startDownTime = time.time()

            #设置暂停状态
            self.pauseFlag=1
            self.signal_btn_stop_set.emit(self.pauseFlag)

            self.signal_msg_append.emit('\r\nTask start!')
            self.signal_msg_append.emit('\r\nStart download Time:'+str(int(self.startDownTime))+'s')
            if self.batchDownFlag!=1:
                self.statusbar.showMessage('Task start!')
            else:
                self.statusbar.showMessage('Task start!  Downloading...({0})'.format(os.path.basename(self.allDownLink[self.batchDownIndex]['FileName'])))

    #多线程进行下载任务
    def DownFileTask(self,flag,mutli_flag):
        if flag==1:
            if self.dTaskList1:
                dtask_i1 = 0
                while dtask_i1<len(self.dTaskList1):
                    if self.pauseFlag==1:
                        try:
                            if mutli_flag==1:
                                #M3U8
                                self._SaveFile(self.dTaskList1[dtask_i1]['FileName'],self.dTaskList1[dtask_i1]['UrlPath'])
                            else:
                                #多线程
                                self._SaveMutliFile(self.masterKey, self.dTaskList1[dtask_i1]['MovName'],self.dTaskList1[dtask_i1]['MovRange'], flag)
                            self.signal_msg_append.emit('\r\nTaskList1 TS File {0} download finish!'.format(dtask_i1))
                            dtask_i1 = dtask_i1+1
                            self.dTaskProcIndex[0] = dtask_i1  #提示进度条
                        except:
                            if dtask_i1 != self.dErrFlag[0]:
                                #dtask_i1=dtask_i1-1
                                self.dErrFlag[0]=dtask_i1
                                self.signal_msg_append.emit('\r\nTaskList1 TS File {0} redownloading...'.format(dtask_i1))
                    else:
                        time.sleep(1)
        elif flag==2:
            if self.dTaskList2:
                dtask_i2 = 0
                while dtask_i2 < len(self.dTaskList2):
                    if self.pauseFlag == 1:
                        try:
                            if mutli_flag==1:
                                #M3U8
                                self._SaveFile(self.dTaskList2[dtask_i2]['FileName'], self.dTaskList2[dtask_i2]['UrlPath'])
                            else:
                                # 多线程
                                self._SaveMutliFile(self.masterKey, self.dTaskList2[dtask_i2]['MovName'],self.dTaskList2[dtask_i2]['MovRange'], flag)
                            self.signal_msg_append.emit('\r\nTaskList2 TS File {0} download finish!'.format(dtask_i2))
                            dtask_i2 = dtask_i2 + 1
                            self.dTaskProcIndex[1] = dtask_i2
                        except:
                            if dtask_i2!=self.dErrFlag[1]:
                                #dtask_i2 = dtask_i2 - 1
                                self.dErrFlag[1] = dtask_i2
                                self.signal_msg_append.emit('\r\nTaskList2 TS File {0} redownloading...'.format(dtask_i2))
                    else:
                        time.sleep(1)
        elif flag==3:
            if self.dTaskList3:
                dtask_i3 = 0
                while dtask_i3 < len(self.dTaskList3):
                    if self.pauseFlag == 1:
                        try:
                            if mutli_flag==1:
                                #M3U8
                                self._SaveFile(self.dTaskList3[dtask_i3]['FileName'], self.dTaskList3[dtask_i3]['UrlPath'])
                            else:
                                # 多线程
                                self._SaveMutliFile(self.masterKey, self.dTaskList3[dtask_i3]['MovName'],self.dTaskList3[dtask_i3]['MovRange'], flag)
                            self.signal_msg_append.emit('\r\nTaskList3 TS File {0} download finish!'.format(dtask_i3))
                            dtask_i3 = dtask_i3 + 1
                            self.dTaskProcIndex[2] = dtask_i3
                        except:
                            if dtask_i3 != self.dErrFlag[2]:
                                #dtask_i3 = dtask_i3 - 1
                                self.dErrFlag[2] = dtask_i3
                                self.signal_msg_append.emit('\r\nTaskList3 TS File {0} redownloading...'.format(dtask_i3))
                    else:
                        time.sleep(1)
        elif flag==4:
            if self.dTaskList4:
                dtask_i4 = 0
                while dtask_i4 < len(self.dTaskList4):
                    if self.pauseFlag == 1:
                        try:
                            if mutli_flag==1:
                                #M3U8
                                self._SaveFile(self.dTaskList4[dtask_i4]['FileName'], self.dTaskList4[dtask_i4]['UrlPath'])
                            else:
                                # 多线程
                                self._SaveMutliFile(self.masterKey, self.dTaskList4[dtask_i4]['MovName'],self.dTaskList4[dtask_i4]['MovRange'], flag)
                            self.signal_msg_append.emit('\r\nTaskList4 TS File {0} download finish!'.format(dtask_i4))
                            dtask_i4 = dtask_i4 + 1
                            self.dTaskProcIndex[3] = dtask_i4
                        except:
                            if dtask_i4 != self.dErrFlag[3]:
                                #dtask_i3 = dtask_i3 - 1
                                self.dErrFlag[3] = dtask_i4
                                self.signal_msg_append.emit('\r\nTaskList4 TS File {0} redownloading...'.format(dtask_i4))
                    else:
                        time.sleep(1)
        elif flag == 5:
            if self.dTaskList5:
                dtask_i5 = 0
                while dtask_i5 < len(self.dTaskList5):
                    if self.pauseFlag == 1:
                        try:
                            if mutli_flag==1:
                                #M3U8
                                self._SaveFile(self.dTaskList5[dtask_i5]['FileName'], self.dTaskList5[dtask_i5]['UrlPath'])
                            else:
                                # 多线程
                                self._SaveMutliFile(self.masterKey, self.dTaskList5[dtask_i5]['MovName'],self.dTaskList5[dtask_i5]['MovRange'], flag)
                            self.signal_msg_append.emit('\r\nTaskList5 TS File {0} download finish!'.format(dtask_i5))
                            dtask_i5 = dtask_i5 + 1
                            self.dTaskProcIndex[4] = dtask_i5
                        except:
                            if dtask_i5 != self.dErrFlag[4]:
                                #dtask_i3 = dtask_i3 - 1
                                self.dErrFlag[4] = dtask_i5
                                self.signal_msg_append.emit('\r\nTaskList5 TS File {0} redownloading...'.format(dtask_i5))
                    else:
                        time.sleep(1)
        elif flag == 6:
            if self.dTaskList6:
                dtask_i6 = 0
                while dtask_i6 < len(self.dTaskList6):
                    if self.pauseFlag == 1:
                        try:
                            if mutli_flag==1:
                                #M3U8
                                self._SaveFile(self.dTaskList6[dtask_i6]['FileName'], self.dTaskList6[dtask_i6]['UrlPath'])
                            else:
                                # 多线程
                                self._SaveMutliFile(self.masterKey, self.dTaskList6[dtask_i6]['MovName'],self.dTaskList6[dtask_i6]['MovRange'], flag)
                            self.signal_msg_append.emit('\r\nTaskList6 TS File {0} download finish!'.format(dtask_i6))
                            dtask_i6 = dtask_i6 + 1
                            self.dTaskProcIndex[5] = dtask_i6
                        except:
                            if dtask_i6 != self.dErrFlag[5]:
                                #dtask_i3 = dtask_i3 - 1
                                self.dErrFlag[5] = dtask_i6
                                self.signal_msg_append.emit('\r\nTaskList6 TS File {0} redownloading...'.format(dtask_i6))
                    else:
                        time.sleep(1)
        elif flag == 7:
            if self.dTaskList7:
                dtask_i7 = 0
                while dtask_i7 < len(self.dTaskList7):
                    if self.pauseFlag == 1:
                        try:
                            if mutli_flag==1:
                                #M3U8
                                self._SaveFile(self.dTaskList7[dtask_i7]['FileName'], self.dTaskList7[dtask_i7]['UrlPath'])
                            else:
                                # 多线程
                                self._SaveMutliFile(self.masterKey, self.dTaskList7[dtask_i7]['MovName'],self.dTaskList7[dtask_i7]['MovRange'], flag)
                            self.signal_msg_append.emit('\r\nTaskList7 TS File {0} download finish!'.format(dtask_i7))
                            dtask_i7 = dtask_i7 + 1
                            self.dTaskProcIndex[6] = dtask_i7
                        except:
                            if dtask_i7 != self.dErrFlag[6]:
                                #dtask_i3 = dtask_i3 - 1
                                self.dErrFlag[6] = dtask_i7
                                self.signal_msg_append.emit('\r\nTaskList7 TS File {0} redownloading...'.format(dtask_i7))
                    else:
                        time.sleep(1)
        else:
            if self.dTaskList8:
                dtask_i8 = 0
                while dtask_i8 < len(self.dTaskList8):
                    if self.pauseFlag == 1:
                        try:
                            if mutli_flag==1:
                                #M3U8
                                self._SaveFile(self.dTaskList8[dtask_i8]['FileName'], self.dTaskList8[dtask_i8]['UrlPath'])
                            else:
                                # 多线程
                                self._SaveMutliFile(self.masterKey, self.dTaskList8[dtask_i8]['MovName'],self.dTaskList8[dtask_i8]['MovRange'], flag)
                            self.signal_msg_append.emit('\r\nTaskList8 TS File {0} download finish!'.format(dtask_i8))
                            dtask_i8 = dtask_i8 + 1
                            self.dTaskProcIndex[7] = dtask_i8
                        except:
                            if dtask_i8 != self.dErrFlag[7]:
                                #dtask_i3 = dtask_i3 - 1
                                self.dErrFlag[7] = dtask_i8
                                self.signal_msg_append.emit('\r\nTaskList8 TS File {0} redownloading...'.format(dtask_i8))
                    else:
                        time.sleep(1)


    #保存文件
    def _SaveFile(self,file_name,url):
        with open(file_name, 'wb') as f_write:
            req = self.myVipChangeSoe.GetUrlFile(url)
            if req.status_code == 200:
                if self.aesFlag == 0:
                    f_write.write(req.content)
                elif self.aesFlag == 2:
                    #base64视频解码
                    v_data = req.content
                    f_write.write(v_data)
                else:
                    #AES解密
                    cryptor = AES.new(self.aesKey.encode('utf-8'), AES.MODE_CBC)
                    f_write.write(cryptor.decrypt(req.content))
            else:
                print(req.status_code)


    #移除所有文件
    def _RemoveAllFile(self):
        all_count = len(self.dTaskAllPath)
        for i in range(1,all_count):
            if os.path.isdir(self.dTaskAllPath[i]):
                file_list = os.listdir(self.dTaskAllPath[i])
                for item in file_list:
                    path = self.dTaskAllPath[i]+'\\'+item
                    if os.path.isfile(path):  # 判断该文件是否为文件或者文件夹
                        os.remove(path)
                os.rmdir(self.dTaskAllPath[i])
                self.signal_msg_append.emit('Remove '+self.dTaskAllPath[i] +' successful!\r\n\r\n')
        os.rmdir(self.dTaskAllPath[0])
        self.signal_msg_append.emit('Remove ' + self.dTaskAllPath[0] + ' successful!\r\n\r\n')

    def _RunFfmpegImport(self,path):
        temp_path = path + '.mkv'
        try:
            with open('file_list.txt','w') as f_write:
                for item in self.combineFiles:
                    temp_str = item.replace('/','\\\\')
                    f_write.writelines('file \''+temp_str+'\'\n')
            cmd = '.\\Ffmpeg\\ffmpeg.exe -f concat -safe 0 -i file_list.txt -c copy -bsf:a aac_adtstoasc -movflags +faststart '+temp_path

            sub = subprocess.Popen(
                cmd,
               shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)
            self.subOut, err = sub.communicate()
            self.signal_msg_append.emit('Start convert...')
        except Exception as msg:
            win32api.MessageBox(0, str(msg), "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
            print(msg)

    #运行Ffmpeg
    def _RunFfmpeg(self,cmd):
        temp_path = self.savePath+'.mkv'
        try:
            with open('file_list.txt','w') as f_write:
                for item in self.dTaskList1:
                    temp_str = item['FileName'].replace('\\','\\\\')
                    f_write.writelines('file \''+temp_str+'\'\n')
                for item in self.dTaskList2:
                    temp_str = item['FileName'].replace('\\', '\\\\')
                    f_write.writelines('file \''+temp_str+'\'\n')
                for item in self.dTaskList3:
                    temp_str = item['FileName'].replace('\\', '\\\\')
                    f_write.writelines('file \''+temp_str+'\'\n')
                if self.THREAD_TASK_COUNT>=4:
                    for item in self.dTaskList4:
                        temp_str = item['FileName'].replace('\\', '\\\\')
                        f_write.writelines('file \'' + temp_str + '\'\n')
                if self.THREAD_TASK_COUNT >= 5:
                    for item in self.dTaskList5:
                        temp_str = item['FileName'].replace('\\', '\\\\')
                        f_write.writelines('file \'' + temp_str + '\'\n')
                if self.THREAD_TASK_COUNT >= 6:
                    for item in self.dTaskList6:
                        temp_str = item['FileName'].replace('\\', '\\\\')
                        f_write.writelines('file \'' + temp_str + '\'\n')
                if self.THREAD_TASK_COUNT >= 7:
                    for item in self.dTaskList7:
                        temp_str = item['FileName'].replace('\\', '\\\\')
                        f_write.writelines('file \'' + temp_str + '\'\n')
                if self.THREAD_TASK_COUNT >= 8:
                    for item in self.dTaskList8:
                        temp_str = item['FileName'].replace('\\', '\\\\')
                        f_write.writelines('file \'' + temp_str + '\'\n')
            cmd = '.\\Ffmpeg\\ffmpeg.exe -f concat -safe 0 -i file_list.txt -c copy -bsf:a aac_adtstoasc -movflags +faststart '+temp_path

            sub = subprocess.Popen(
                cmd,
               shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
               stderr=subprocess.PIPE)
            self.subOut, err = sub.communicate()
            self.signal_msg_append.emit('Start convert...')
        except Exception as msg:
            win32api.MessageBox(0, str(msg), "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
            print(msg)

    #接收回调
    def _GetFfmpegMsg(self):
        try:
            msg = self.subOut.decode()
            self.signal_msg_append.emit(str(msg))

            #移除文件
            if os.path.exists('file_list.txt'):
                os.remove('file_list.txt')

            self._RemoveAllFile()
            self.signal_msg_append.emit(msg)
            self.signal_msg_append.emit('Convert Finish!')
            if self.batchDownFlag!=1:
                win32api.MessageBox(0, 'Convert Success!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
                self.dRunFlag = 0
            else:
                self.batchDownIndex+=1
                if self.batchDownIndex<len(self.allDownLink):
                    self.dRunFlag = 0
                    self.RunDownList(self.batchDownIndex)
                else:
                    win32api.MessageBox(0, 'Download Finish!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
                    self.dRunFlag = 0
        except:
            self.dRunFlag = 3

    #按照普通方式合成流文件
    def _CombineDownFileM3U8(self):
        # 合并文件
        with open(self.savePath + '.mkv', 'wb+') as f_write:
            if self.aesFlag==2:
                f_write.write(self.v_base_head)
            for item in self.dTaskList1:
                with open(item['FileName'], 'rb') as f_read:
                    data = f_read.read()
                    f_write.write(data)
                if os.path.isfile(item['FileName']):
                    os.remove(item['FileName'])
            for item in self.dTaskList2:
                with open(item['FileName'], 'rb') as f_read:
                    data = f_read.read()
                    f_write.write(data)
                if os.path.isfile(item['FileName']):
                    os.remove(item['FileName'])
            for item in self.dTaskList3:
                with open(item['FileName'], 'rb') as f_read:
                    data = f_read.read()
                    f_write.write(data)
                if os.path.isfile(item['FileName']):
                    os.remove(item['FileName'])
            if self.THREAD_TASK_COUNT >= 4:
                for item in self.dTaskList4:
                    with open(item['FileName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['FileName']):
                        os.remove(item['FileName'])
            if self.THREAD_TASK_COUNT >= 5:
                for item in self.dTaskList5:
                    with open(item['FileName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['FileName']):
                        os.remove(item['FileName'])
            if self.THREAD_TASK_COUNT >= 6:
                for item in self.dTaskList6:
                    with open(item['FileName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['FileName']):
                        os.remove(item['FileName'])
            if self.THREAD_TASK_COUNT >= 7:
                for item in self.dTaskList7:
                    with open(item['FileName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['FileName']):
                        os.remove(item['FileName'])
            if self.THREAD_TASK_COUNT >= 8:
                for item in self.dTaskList8:
                    with open(item['FileName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['FileName']):
                        os.remove(item['FileName'])
        #删除个文件夹
        self._RemoveAllFile()
        self.signal_msg_append.emit('Convert Finish!')
        if self.batchDownFlag != 1:
            win32api.MessageBox(0, 'Convert Success!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
            self.dRunFlag = 0
        else:
            self.batchDownIndex += 1
            if self.batchDownIndex < len(self.allDownLink):
                self.dRunFlag = 0
                self.RunDownList(self.batchDownIndex)
            else:
                win32api.MessageBox(0, 'Download Finish!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
                self.dRunFlag = 0

    #下载单一文件
    def _RunSingleDown(self):
        self.signal_msg_append.emit('Start File Download...')
        startDownTime = time.time()
        self._StreamDown(self.masterKey,self.savePath+'.mkv')
        # 计算总下载时间
        endDownTime = time.time()
        sum_time = endDownTime - startDownTime
        self.signal_msg_append.emit('\r\nSum download Time:' + str(int(sum_time)) + 's')
        self.signal_msg_append.emit('\r\nTask assigned successfully!')
        self.statusbar.showMessage('Download success!')

    #批量下载
    def _RunSingleDownList(self):
        start_list_time = time.time()
        for item in self.allDownLink:
            startDownTime = time.time()
            self.signal_msg_append.emit('\r\nFile '+os.path.basename(item['FileName'])+' start download...')
            self.statusbar.showMessage('File '+os.path.basename(item['FileName'])+' downloading...')
            link = item['FileLink']
            if 'thunder' in link:
                link = self.ThunderLink(link)
            self.signal_url_set.emit(link)

            self._StreamDown(link, item['FileName'] + '.mkv')

            endDownTime = time.time()
            sum_time = endDownTime - startDownTime
            self.signal_msg_append.emit('\r\nFile download Time:' + str(int(sum_time)) + 's')
            self.signal_msg_append.emit('\r\nFile download successfully!')
        sum_list_time = time.time() - start_list_time
        self.signal_msg_append.emit('\r\nSum download Time:' + str(int(sum_list_time)) + 's')
        self.signal_msg_append.emit('\r\nFile list download successfully!')
        self.statusbar.showMessage('Download success!')

    #流式下载单个文件
    def _StreamDown(self,url,file_path='',chunk_size=1024):
        req = self.myVipChangeSoe.GetStreamReq(url)
        # 获取文件总大小
        size = int(req.headers['Content-Length'])
        self.signal_msg_append.emit('\r\nFile Length->'+str(size)+'bytes')
        temp_size = 0
        self.signal_msg_append.emit('\r\nDownloading...')
        with open(file_path, 'wb') as f:
            for chunk in req.iter_content(chunk_size=chunk_size):
                if chunk:
                    temp_size += len(chunk)
                    # 写入文件及刷新
                    f.write(chunk)
                    f.flush()
                    current_size = ((temp_size*100)/size)
                    self.signal_pb_set.emit(current_size)

    #开启多线程下载文件
    def _StartDownFile(self):
        tag_dir = self.savePath[:self.savePath.rfind('\\')]
        if os.path.isdir(tag_dir):
            # 建立缓存路径
            self.dTaskAllPath.clear()
            temp_ts_folder = self.savePath + '_ts'
            if not os.path.isdir(temp_ts_folder):
                os.mkdir(temp_ts_folder)

        self.dTaskAllPath.append(temp_ts_folder)
        # 清空任务列
        self.dTaskList1.clear()
        self.dTaskList2.clear()
        self.dTaskList3.clear()
        self.dTaskList4.clear()
        self.dTaskList5.clear()
        self.dTaskList6.clear()
        self.dTaskList7.clear()
        self.dTaskList8.clear()

        if self.vipdownch==5:
            #获取文件总长度
            req_msg = self.myVipChangeSoe.GetStreamReqMsg(self.masterKey)
            file_len = int(req_msg.headers['Content-Length'])
            data_len = int(file_len/self.MUTLI_MIN_LEN)

            #获取所有连接
            all_down_list = []
            if file_len%self.MUTLI_MIN_LEN==0:
                for i in range(0,data_len):
                    dict_data = {
                        'MovName':self.savePath + '_ts\\MovTempStream'+str(i)+'.ts',
                        'MovRange':'bytes='+str(i*self.MUTLI_MIN_LEN)+'-'+str(((i+1)*self.MUTLI_MIN_LEN)-1),
                        'MovSPos': str(i*self.MUTLI_MIN_LEN),
                        'MovLen':str(self.MUTLI_MIN_LEN)
                    }
                    all_down_list.append(dict_data)
            else:
                for i in range(0,data_len):
                    dict_data = {
                        'MovName':self.savePath + '_ts\\MovTempStream'+str(i)+'.ts',
                        'MovRange':'bytes='+str(i*self.MUTLI_MIN_LEN)+'-'+str(((i+1)*self.MUTLI_MIN_LEN)-1),
                        'MovSPos': str(i*self.MUTLI_MIN_LEN),
                        'MovLen':str(self.MUTLI_MIN_LEN)
                    }
                    all_down_list.append(dict_data)
                dict_data = {
                    'MovName': self.savePath + '_ts\\MovTempStream' + str(data_len) + '.ts',
                    'MovRange': 'bytes=' + str(data_len * self.MUTLI_MIN_LEN) + '-' + str(file_len - 1),
                    'MovSPos': str(data_len * self.MUTLI_MIN_LEN),
                    'MovLen': str(file_len-(data_len * self.MUTLI_MIN_LEN))
                }
                all_down_list.append(dict_data)

            #根据任务线程数量分配任务
            avg_task_len = len(all_down_list)/self.THREAD_TASK_COUNT
            for i in range(0,len(all_down_list)):
                if (i>=0) and (i<avg_task_len*1):
                    self.dTaskList1.append(all_down_list[i])
                elif (i>=avg_task_len*1) and (i<avg_task_len*2):
                    self.dTaskList2.append(all_down_list[i])
                elif (i >= avg_task_len * 2) and (i < avg_task_len * 3):
                    self.dTaskList3.append(all_down_list[i])
                elif (i >= avg_task_len * 3) and (i < avg_task_len * 4):
                    if self.THREAD_TASK_COUNT >= 4:  # 控制线程数量
                        self.dTaskList4.append(all_down_list[i])
                    else:
                        self.dTaskList3.append(all_down_list[i])
                elif (i >= avg_task_len * 4) and (i < avg_task_len * 5):
                    if self.THREAD_TASK_COUNT >= 5:  # 控制线程数量
                        self.dTaskList5.append(all_down_list[i])
                    else:
                        self.dTaskList4.append(all_down_list[i])
                elif (i >= avg_task_len * 5) and (i < avg_task_len * 6):
                    if self.THREAD_TASK_COUNT >= 6:  # 控制线程数量
                        self.dTaskList6.append(all_down_list[i])
                    else:
                        self.dTaskList5.append(all_down_list[i])
                elif (i >= avg_task_len * 6) and (i < avg_task_len * 7):
                    if self.THREAD_TASK_COUNT >= 7:  # 控制线程数量
                        self.dTaskList7.append(all_down_list[i])
                    else:
                        self.dTaskList6.append(all_down_list[i])
                else:
                    self.dTaskList8.append(all_down_list[i])

        self.signal_msg_append.emit('\r\nTask assigned successfully!')
        self.statusbar.showMessage('Task assigned successfully!')

        self.dTaskProcUpFlag = 1
        for i in range(0, 8):
            if i < self.THREAD_TASK_COUNT:
                self.dTaskProcIndex[i] = 0
                self.dTaskFlag[i] = 2
            else:
                self.dTaskProcIndex[i] = 0
                self.dTaskFlag[i] = 0

        self.startDownTime = time.time()

        # 设置暂停状态
        self.pauseFlag = 1
        self.signal_btn_stop_set.emit(self.pauseFlag)

        self.signal_msg_append.emit('\r\nTask start!')
        self.signal_msg_append.emit('\r\nStart download Time:' + str(int(self.startDownTime)) + 's')

    #保存数据文件
    def _SaveMutliFile(self,url,save_path,range,flag,chunk_size=1024):
        headers = {
            #'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Range':range
        }
        req = self.myVipChangeSoe.GetStreamReqHeader(self.masterKey,headers)
        with open(save_path, 'wb') as f:
            f.write(req.content)

    #合并文件
    def _CombineDownFile(self):
        #合并文件
        with open(self.savePath+'.mkv','wb+') as f_write:
            for item in self.dTaskList1:
                f_write.seek(int(item['MovSPos']))
                with open(item['MovName'],'rb') as f_read:
                    data = f_read.read()
                    f_write.write(data)
                if os.path.isfile(item['MovName']):
                    os.remove(item['MovName'])
            for item in self.dTaskList2:
                f_write.seek(int(item['MovSPos']))
                with open(item['MovName'], 'rb') as f_read:
                    data = f_read.read()
                    f_write.write(data)
                if os.path.isfile(item['MovName']):
                    os.remove(item['MovName'])
            for item in self.dTaskList3:
                f_write.seek(int(item['MovSPos']))
                with open(item['MovName'], 'rb') as f_read:
                    data = f_read.read()
                    f_write.write(data)
                if os.path.isfile(item['MovName']):
                    os.remove(item['MovName'])
            if self.THREAD_TASK_COUNT >= 4:
                for item in self.dTaskList4:
                    f_write.seek(int(item['MovSPos']))
                    with open(item['MovName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['MovName']):
                        os.remove(item['MovName'])
            if self.THREAD_TASK_COUNT >= 5:
                for item in self.dTaskList5:
                    f_write.seek(int(item['MovSPos']))
                    with open(item['MovName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['MovName']):
                        os.remove(item['MovName'])
            if self.THREAD_TASK_COUNT >= 6:
                for item in self.dTaskList6:
                    f_write.seek(int(item['MovSPos']))
                    with open(item['MovName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['MovName']):
                        os.remove(item['MovName'])
            if self.THREAD_TASK_COUNT >= 7:
                for item in self.dTaskList7:
                    f_write.seek(int(item['MovSPos']))
                    with open(item['MovName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['MovName']):
                        os.remove(item['MovName'])
            if self.THREAD_TASK_COUNT >= 8:
                for item in self.dTaskList8:
                    f_write.seek(int(item['MovSPos']))
                    with open(item['MovName'], 'rb') as f_read:
                        data = f_read.read()
                        f_write.write(data)
                    if os.path.isfile(item['MovName']):
                        os.remove(item['MovName'])
        #删除相应的文件夹
        os.rmdir(self.savePath + '_ts')

        self.signal_msg_append.emit('\r\nCombine file successfully!')
        self.statusbar.showMessage('Combine file success!')
        if self.batchDownFlag != 1:
            win32api.MessageBox(0, 'Convert Success!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
            self.dRunFlag = 0
        else:
            self.batchDownIndex += 1
            if self.batchDownIndex < len(self.allDownLink):
                self.dRunFlag = 0
                self.RunMulitList(self.batchDownIndex)
            else:
                win32api.MessageBox(0, 'Download Finish!', "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
                self.dRunFlag = 0

    #UI更新函数
    def UpdateListView_Vipd(self):
        slm = QStringListModel()  # 实例化列表模型，添加数据
        slm.setStringList(self.qListVipd)  # 设置模型列表视图，加载数据列表
        self.listView.setModel(slm)  # 设置列表视图的模型

    def UpdateTextMsg_Vipd(self, str):
        self.txtLink.append(str)

    def SetTextMsg_Vipd(self, str):
        self.txtLink.setText(str)

    def UpdateTextMsg(self, str):
        self.txtMsg.append(str)

    def SetTextMsg(self, str):
        self.txtMsg.setText(str)

    def SetUrlText(self, str):
        self.txtUrl.setText(str)

    def SetCboIndex(self,index):
        self.cboExEng.setCurrentIndex(index)

    #更新进度条
    def UpdateProgBar(self,val):
        self.pbDownBar.setValue(val)