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
        self.setFixedSize(470, 130)  # 设置窗体的大小
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

    def BtnSelPath_Click(self):
        filename_filter = "QDF文件|*.qdf|QDMF文件|*.qdmf||"
        dlg = win32ui.CreateFileDialog(1, None, '', 1, filename_filter, None)
        dlg.SetOFNTitle("Please select the qdf file")
        if dlg.DoModal() == 1:
            file_path = dlg.GetPathName()
            extension_name = os.path.splitext(file_path)[1]

            with open(file_path, 'r', encoding='utf-8') as f_read:
                js_ele = json.loads(f_read.read())
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
                self.txtQdmfPath.setText(file_path)

    def BtnConvert_Click(self):
        list_save_dialog = QFileDialog()
        try:
            save_path = list_save_dialog.getSaveFileName(self, caption="Please select save directory",filter='File Type (*.txt)|*.txt|')[0]
            with open(save_path, 'w', encoding='utf-8') as f_write:
                js_str = ''
                for item in self.allLink:
                    js_str += item['FileName'] + ','
                    js_str += item['FileLink'] + '\n'
                f_write.write(js_str)
                win32api.MessageBox(0, 'Save success!', "Information", win32con.MB_ICONINFORMATION, win32con.MB_OK)
        except Exception as msg:
            win32api.MessageBox(0, str(msg), "Error", win32con.MB_ICONERROR, win32con.MB_OK)