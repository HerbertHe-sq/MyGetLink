import json
import os

import win32api
import win32con
import win32ui

from PyQt5.QtGui import QIcon
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QFileDialog

from Form.QdmfConvertWin.QdmfConvertUi import Ui_QdmfConvertWin
from Function.QssHelper import QssHelper


class QdmfConvertWindow(QtWidgets.QMainWindow, Ui_QdmfConvertWin):
    def __init__(self,theme_str):
        super(QdmfConvertWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint);  # 窗体没有最大化最小化按钮
        self.setFixedSize(470, 150)  # 设置窗体的大小
        self.setWindowIcon(QIcon("./Image/Icon_GetSource.png"))

        # 加载样式
        self._SetControlProperty()
        self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format(theme_str)))
        self.btnSelPath.clicked.connect(self.BtnSelPath_Click)
        self.btnConvert.clicked.connect(self.BtnConvert_Click)

        self._InitSetUp()


    def ShowWindows(self):
        self.show()

    def _SetControlProperty(self):
        self.setProperty('name', 'QdmfConvertFrm')

    def _InitSetUp(self):
        self.allLink = []
        self.rbToQdmf.setChecked(True)
        self.cbFfmpeg.setChecked(True)

    def BtnSelPath_Click(self):
        if self.rbToQdmf.isChecked()!=True:
            filename_filter = "QDF文件|*.qdf|QDMF文件|*.qdmf|JSON文件|*.json||"
            tip_str = 'Please select the qdf file'
        else:
            filename_filter = "TXT文件|*.txt||"
            tip_str = 'Please select the tv file'
        dlg = win32ui.CreateFileDialog(1, None, '', 1, filename_filter, None)
        dlg.SetOFNTitle(tip_str)
        if dlg.DoModal() == 1:
            file_path = dlg.GetPathName()
            extension_name = os.path.splitext(file_path)[1]

            with open(file_path, 'r', encoding='utf-8') as f_read:
                if self.rbToQdmf.isChecked()!=True:
                    js_ele = json.loads(f_read.read())
                    if extension_name=='.json':
                        list_dat_t = js_ele['list']
                        for item in list_dat_t:
                            js_ele_t = json.loads(item['data'])
                            js_ele_video = json.loads(js_ele_t['videoUrl'])
                            dict_link = {
                                'FileName': js_ele_t['title'],
                                'FileLink': js_ele_video['hd'],
                                'BaseLink': '',
                                'CombMode': ''  # 合成模式
                            }
                            self.allLink.append(dict_link)
                    else:
                        count = int(js_ele['ItemCount'])

                        self.allLink.clear()
                        for i in range(0, count):
                            if extension_name == '.qdf':  # 兼容旧格式.qdf不存在合并模式
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
                                    'CombMode': js_ele['Item'][i]['CombMode']  # 合成模式
                                }
                            self.allLink.append(dict_link)

                    self.statusBar.showMessage('Resource Count:' + str(len(self.allLink)))
                else:
                    file_dat = f_read.read()
                    file_dat_arr = file_dat.split('\n')
                    if len(file_dat_arr)>0:
                        self.allLink.clear()
                        for i in range(0,len(file_dat_arr)):
                            file_dat_str_t = file_dat_arr[i].split(',')
                            dict_file_t = {
                                'FileName':file_dat_str_t[0],
                                'FileLink':file_dat_str_t[1],
                                'BaseLink':os.path.dirname(file_dat_str_t[1])+'/'
                            }
                            self.allLink.append(dict_file_t)
                        self.statusBar.showMessage('Resource Count:' + str(len(self.allLink)))
                    else:
                        self.statusBar.showMessage('Resource Count:fail!')


                self.txtQdmfPath.setText(file_path)

    def BtnConvert_Click(self):
        list_save_dialog = QFileDialog()
        try:
            if self.rbToQdmf.isChecked()!=True:
                file_filter = 'File Type (*.txt)|*.txt|'
            else:
                file_filter = 'File Type (*.qdmf)|*.qdmf|'
            save_path = list_save_dialog.getSaveFileName(self, caption="Please select save directory",filter=file_filter)[0]
            with open(save_path, 'w', encoding='utf-8') as f_write:
                js_str = ''
                if self.rbToQdmf.isChecked()!=True:
                    for item in self.allLink:
                        js_str += item['FileName'] + ','
                        js_str += item['FileLink'] + '\n'
                else:
                    js_str += '{ "ItemCount":"' + str(len(self.allLink)) + '","Item":['
                    for item in self.allLink:
                        js_str += '{"FileName":"' + item['FileName'] + '",'
                        js_str += '"FileLink":"' + item['FileLink'] + '",'
                        if self.cbAddAddr.isChecked():
                            js_str += '"BaseLink":"' + item['BaseLink'] + '",'
                        else:
                            js_str += '"BaseLink":"",'

                        if self.cbFfmpeg.isChecked():
                            js_str += '"CombMode":"0"},' #FFMpeg
                        else:
                            js_str += '"CombMode":"1"},'
                    js_str += ']}'
                    js_str = js_str.replace(',]}', ']}')
                f_write.write(js_str)
                win32api.MessageBox(0, 'Save success!', "Information", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        except Exception as msg:
            win32api.MessageBox(0, str(msg), "Error", win32con.MB_ICONERROR, win32con.MB_OK)