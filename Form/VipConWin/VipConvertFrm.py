import base64

import win32api
import win32con
import win32ui


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from Form.VipConWin.VipConUi import Ui_VipConWindow
from Function.NAnalysis import NationalAnalysis
from Function.QssHelper import QssHelper


class VConvertWindow(QtWidgets.QMainWindow, Ui_VipConWindow):
    def __init__(self,ini_file,theme_str):
        super(VConvertWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint);  # 窗体没有最大化最小化按钮
        self.setFixedSize(560, 240)  # 设置窗体的大小
        self.setWindowIcon(QIcon("./Image/Icon_GetSource.png"))
        # 加载样式
        self._SetControlProperty()
        self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format(theme_str)))

        self.setIniFile = ini_file
        self.btnConvert.clicked.connect(self.BtnConvert_Click)
        self.InitSetUp()


    def ShowWindows(self):
        self.show()

    def closeEvent(self, event):
        self.deleteLater()

    def _SetControlProperty(self):
        self.setProperty('name', 'VipConvertFrm')
        self.btnConvert.setProperty('name','btnConvert')

    def InitSetUp(self):
        # 直接联网获取
        self.nAnalysis = NationalAnalysis()
        self.nAnalysis.SetBaseUrl(str(self.setIniFile.GetIniValue('VipConverter', 'url')))
        self.dicEngine = self.nAnalysis.FindEngineUrl()
        if len(self.dicEngine) >0:
            for item in self.dicEngine:
                self.cboEngine.addItem(item['EngName'])
        else:
            win32api.MessageBox(0, "检索引擎失败!", "Exception", win32con.MB_ICONERROR, win32con.MB_OK)
            self.txtVideo.setEnabled(False)
            self.txtTagVideo.setEnabled(False)
            self.btnConvert.setEnabled(False)


    def BtnConvert_Click(self):
        tag_url = self.txtVideo.toPlainText()
        if len(tag_url)>0:
            self.statusbar.showMessage('Finding...')
            js_data = self.nAnalysis.EngineVip_1(tag_url)
            try:
                if not (js_data['url'].find('http') >= 0):
                    url = 'http:' + js_data['url']
                else:
                    url = js_data['url']
                self.txtTagVideo.setText(url)
                self.statusbar.showMessage('Finish!!!')
            except Exception as e:
                win32api.MessageBox(0, str(e), "Exception", win32con.MB_ICONERROR, win32con.MB_OK)
                self.statusbar.showMessage('Fail!!!')