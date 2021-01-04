import base64
import json
import os
import win32api
import win32con
import win32ui
import pyperclip


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QStringListModel, QPoint
from PyQt5.QtGui import QIcon, QPixmap, QCursor
from PyQt5.QtWidgets import QFileDialog, QMenu, QAbstractItemView
from Form.BatchDownWin.BatchDownUi import Ui_BatDownWindow
from Function.QssHelper import QssHelper


class BatchDownWindow(QtWidgets.QMainWindow, Ui_BatDownWindow):
    signal_list = QtCore.pyqtSignal()

    def __init__(self,main_frm,theme_str):
        super(BatchDownWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint);  # 窗体没有最大化最小化按钮
        self.setFixedSize(678, 560)  # 设置窗体的大小
        self.setWindowIcon(QIcon("./Image/Icon_GetSource.png"))

        # 加载样式
        self._SetControlProperty(theme_str)
        self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format(theme_str)))

        self.mainWin = main_frm

        self._AddListContextMenu()
        #注册事件
        self._ResigterEvent()

        #初始化设置
        self._InitSetUp()

    def ShowWindows(self):
        self.show()

    def CloseWindow(self):
        self.close()

    def closeEvent(self, event):
        self.deleteLater()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_F8:   #模拟ctrl+v
            win32api.keybd_event(0x11, 0, 0, 0)
            win32api.keybd_event(0x56, 0, 0, 0)
            win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
            win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
        elif event.key()==Qt.Key_F6:
            data_str = pyperclip.paste()
            self.txtLink.setText(data_str)
            self.txtBaseLink.setText(os.path.dirname(data_str)+'/')
            file_name_len = len(self.allLink)
            if file_name_len >0:
               file_name_str = self.allLink[file_name_len-1]['FileName']
               index = int(file_name_str[(len(file_name_str)-2):len(file_name_str)])+1
               if index<10:
                   self.txtFileName.setText(file_name_str[:len(file_name_str) - 2] +'0'+ str(index))
               else:
                   self.txtFileName.setText(file_name_str[:len(file_name_str)-2]+str(index))
               self.AddLinkToList()
        else:
            pass

    # 为所有控件设置setProperty
    def _SetControlProperty(self,theme_str):
        self.setProperty('name','BatchDownFrm')
        self.btnAddLink.setProperty('name', 'btnAddLink')
        self.btnDownList.setProperty('name', 'btnDownList')
        self.btnSelectPath.setProperty('name', 'btnSelectPath')
        self.listView.verticalScrollBar().setStyleSheet(QssHelper.ReadQss("./Qss/{0}/ScrollBarStyle.qss".format(theme_str)))
        self.listView.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss("./Qss/{0}/ScrollBarStyle.qss".format(theme_str)))

    #初始化设置
    def _InitSetUp(self):
        self.saveFolderPath = ''  #保存路径
        self.qDownList = []
        self.allLink = []
        self.saveQdmfPath = ''
        self.taskCountArr = ['1','2','3','4','5','6','7','8']
        self.fileNameIndex = 0
        self.txtSavePath.setReadOnly(True)
        self.rb1.setChecked(True)
        self.radioButton.setChecked(True)
        self.cboTaskCount.addItems(self.taskCountArr)


    def _AddListContextMenu(self):
        self.listView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listView.customContextMenuRequested[QPoint].connect(self.ListWidgetContext)

    def ListWidgetContext(self, point):
        popMenu = QMenu()
        self.menuListDelItem = popMenu.addAction("Delete Item")
        self.menuListDelItem.triggered.connect(lambda: self.MenuDelItem_Click(self.menuListDelItem))

        self.menuListClear= popMenu.addAction("Clear List")
        self.menuListClear.triggered.connect(lambda: self.MenuListClear_Click(self.menuListClear))

        self.menuListItemUp = popMenu.addAction("Move Up")
        self.menuListItemUp.triggered.connect(lambda: self.MenuListItemMove_Click(self.menuListItemUp,1))

        self.menuListItemDown = popMenu.addAction("Move Down")
        self.menuListItemDown.triggered.connect(lambda: self.MenuListItemMove_Click(self.menuListItemDown,2))
        popMenu.exec_(QCursor.pos())

    #事件注册
    def _ResigterEvent(self):
        self.btnSelectPath.clicked.connect(self.BtnSelectPath_Click)
        self.btnAddLink.clicked.connect(self.BtnAddLink_Click)
        self.btnDownList.clicked.connect(self.BtnDownList_Click)
        self.actionList_Save_As.triggered.connect(self.MenuSaveAs_Click)
        self.actionImport_List.triggered.connect(self.Menu_ImportList_Click)
        self.actionSave.triggered.connect(self.MenuSave_Click)
        self.listView.clicked.connect(self.ListView_Click)
        self.listView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.signal_list.connect(self.UpdateListView)

    #保存列表
    def MenuSaveAs_Click(self):
        list_save_dialog = QFileDialog()
        try:
            save_path = list_save_dialog.getSaveFileName(self, caption="Please select save directory", filter='File Type (*.qdmf)|*.qdmf|')[0]
            with open(save_path,'w',encoding='utf-8') as f_write:
                js_str='{ "ItemCount":"'+str(len(self.allLink))+'","Item":['
                for item in self.allLink:
                    js_str+='{"FileName":"'+item['FileName']+'",'
                    js_str += '"FileLink":"'+item['FileLink']+'",'
                    js_str += '"BaseLink":"'+item['BaseLink']+'",'
                    js_str += '"CombMode":"' + item['CombMode'] + '"},'
                js_str+=']}'
                js_str = js_str.replace(',]}',']}')
                f_write.write(js_str)
                win32api.MessageBox(0, 'Save success!', "Information", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        except Exception as msg:
            win32api.MessageBox(0, str(msg), "Error", win32con.MB_ICONERROR, win32con.MB_OK)

    #读取文件
    def Menu_ImportList_Click(self):
        filename_filter = "QDF文件|*.qdf|QDMF文件|*.qdmf||"
        dlg = win32ui.CreateFileDialog(1, None, '', 1, filename_filter, None)
        dlg.SetOFNTitle("Please select the qdf file")
        if dlg.DoModal() == 1:
            file_path = dlg.GetPathName()
            self.saveQdmfPath = file_path
            extension_name =  os.path.splitext(file_path)[1]

            with open(file_path,'r',encoding='utf-8') as f_read:
                js_ele = json.loads(f_read.read())
                count = int(js_ele['ItemCount'])

                self.qDownList.clear()
                self.allLink.clear()
                for i in range(0,count):
                    if extension_name == '.qdf':  #兼容旧格式.qdf不存在合并模式
                        dict_link = {
                            'FileName': js_ele['Item'][i]['FileName'],
                            'FileLink': js_ele['Item'][i]['FileLink'],
                            'BaseLink': js_ele['Item'][i]['BaseLink'],
                            'CombMode': 'NULL'
                        }
                    else:
                        dict_link = {
                            'FileName': js_ele['Item'][i]['FileName'],
                            'FileLink': js_ele['Item'][i]['FileLink'],
                            'BaseLink': js_ele['Item'][i]['BaseLink'],
                            'CombMode': js_ele['Item'][i]['CombMode']   #合成模式
                        }
                    self.qDownList.append(dict_link['FileName'])
                    self.allLink.append(dict_link)
            self.signal_list.emit()
            self.statusbar.showMessage('Resource Count:' + str(len(self.allLink)))

    def MenuSave_Click(self):
        save_path = ''
        try:
            if self.saveQdmfPath=='':
                list_save_dialog = QFileDialog()
                save_path = list_save_dialog.getSaveFileName(self, caption="Please select save directory",
                                                                 filter='File Type (*.qdmf)|*.qdmf|')[0]
            else:
                save_path = self.saveQdmfPath
            with open(save_path, 'w', encoding='utf-8') as f_write:
                js_str = '{ "ItemCount":"' + str(len(self.allLink)) + '","Item":['
                for item in self.allLink:
                    js_str += '{"FileName":"' + item['FileName'] + '",'
                    js_str += '"FileLink":"' + item['FileLink'] + '",'
                    js_str += '"BaseLink":"' + item['BaseLink'] + '",'
                    js_str += '"CombMode":"' + item['CombMode'] + '"},'
                js_str += ']}'
                js_str = js_str.replace(',]}', ']}')
                f_write.write(js_str)
                win32api.MessageBox(0, 'Save success!', "Information", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        except Exception as msg:
            win32api.MessageBox(0, str(msg), "Error", win32con.MB_ICONERROR, win32con.MB_OK)



    #列表单击事件
    def ListView_Click(self,qModelIndex):
        index = qModelIndex.row()
        self.txtFileName.setText(self.allLink[index]['FileName'])
        self.txtLink.setText(self.allLink[index]['FileLink'])
        self.txtBaseLink.setText(self.allLink[index]['BaseLink'])
        if self.allLink[index]['CombMode']!='NULL':
            if self.allLink[index]['CombMode']=='0':
                self.radioButton.setChecked(True)
            else:
                self.radioButton_2.setChecked(True)

    #选择保存文件夹
    def BtnSelectPath_Click(self):
        file_dialog = QFileDialog()
        self.saveFolderPath = file_dialog.getExistingDirectory(self, "Please select save directory", '')
        self.txtSavePath.setText(self.saveFolderPath)

    #添加到列表内
    def BtnAddLink_Click(self):
        self.AddLinkToList()

    #添加链接到列表
    def AddLinkToList(self):
        if self.CheckText():
            file_name = self.txtFileName.toPlainText()
            link = self.txtLink.toPlainText()
            base_link = self.txtBaseLink.toPlainText()
            com_flag = '0'
            if self.radioButton.isChecked():
                com_flag = '0'  #FFmpeg
            else:
                com_flag = '1' #Compision
            dict_link = {
                'FileName':file_name,
                'FileLink':link,
                'BaseLink':base_link,
                'CombMode':com_flag
            }
            self.qDownList.append(file_name)
            self.allLink.append(dict_link)
            self.signal_list.emit()

            #清空输入框
            #self.txtFileName.setText('')
            #self.txtLink.setText('')


    def BtnDownList_Click(self):
        if not len(self.saveFolderPath)>0:
            file_dialog = QFileDialog()
            self.saveFolderPath = file_dialog.getExistingDirectory(self, "Please select save directory", '')
            self.txtSavePath.setText(self.saveFolderPath)
        if len(self.saveFolderPath)>0:
            for item in self.allLink:
                item['FileName'] = self.saveFolderPath.replace('/','\\')+'\\'+item['FileName']
            if self.cbSwTask.isChecked():
                task_count = self.cboTaskCount.currentIndex()+1
                self.mainWin.DownloadAllLink(self.allLink,1,task_count) #多任务进行
            else:
                if self.rb1.isChecked():
                    self.mainWin.DownloadAllLink(self.allLink,1,0)   #弹出下载框-M3u8
                elif self.rb2.isChecked():
                    self.mainWin.DownloadAllLink(self.allLink, 2,0)  # 弹出下载框-单线程
                elif self.rb3.isChecked():
                    self.mainWin.DownloadAllLink(self.allLink, 3,0)  # 弹出下载框-多线程
                else:
                    self.mainWin.DownloadAllLink(self.allLink, 1,0)  # 弹出下载框-M3u8



    def MenuDelItem_Click(self,menu_item):
        if menu_item.text()=='Delete Item':
            for item in self.listView.selectedIndexes():
                temp = item.data()
                for i in range(0,len(self.qDownList)):
                    if self.qDownList[i]==temp:
                        del self.qDownList[i]
                        break
                for i in range(0,len(self.allLink)):
                    if self.allLink[i]['FileName']==temp:
                        del self.allLink[i]
                        break
            self.signal_list.emit()

    #清空列表
    def MenuListClear_Click(self,menu_item):
        self.qDownList.clear()
        self.allLink.clear()
        self.signal_list.emit()

    #移动项目
    def MenuListItemMove_Click(self,menu_item,index):
        if index==1:
            for item in self.listView.selectedIndexes():
                sel_index = item.row()
                if sel_index>0:
                    temp = self.qDownList[sel_index]
                    self.qDownList[sel_index] = self.qDownList[sel_index-1]
                    self.qDownList[sel_index - 1] = temp

                    dict_temp = self.allLink[sel_index]
                    self.allLink[sel_index] = self.allLink[sel_index-1]
                    self.allLink[sel_index - 1] = dict_temp
            self.signal_list.emit()
        elif index==2:
            for item in self.listView.selectedIndexes():
                sel_index = item.row()
                if sel_index <(len(self.qDownList)-1):
                    temp = self.qDownList[sel_index]
                    self.qDownList[sel_index] = self.qDownList[sel_index + 1]
                    self.qDownList[sel_index + 1] = temp

                    dict_temp = self.allLink[sel_index]
                    self.allLink[sel_index] = self.allLink[sel_index + 1]
                    self.allLink[sel_index + 1] = dict_temp
            self.signal_list.emit()
        else:
            pass


    #检测输入之数据是否正确
    def CheckText(self):
        file_name = self.txtFileName.toPlainText()
        link = self.txtLink.toPlainText()

        if len(file_name)<=0:return False
        if len(link)<=0:return False
        if not (('http' in link) or ('thunder' in link)):return False
        return True

    def UpdateListView(self):
        slm = QStringListModel()  # 实例化列表模型，添加数据
        slm.setStringList(self.qDownList)  # 设置模型列表视图，加载数据列表
        self.listView.setModel(slm)  # 设置列表视图的模型

    def UpdateTextBox(self,flag,temp):
        if flag==1:
            self.txtFileName.setText(temp)
        elif flag==2:
            self.txtLink.setText(temp)
        elif flag==3:
            self.btnAddLink.click()
        else:
            pass