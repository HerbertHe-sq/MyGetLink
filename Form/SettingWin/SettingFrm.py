import base64

import win32api
import win32con
import win32ui


from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from Form.SettingWin.SettingUi import Ui_SetWindow
from Function.QssHelper import QssHelper


class SettingWindow(QtWidgets.QMainWindow, Ui_SetWindow):
    def __init__(self,ini_file,theme_str):
        super(SettingWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint);  # 窗体没有最大化最小化按钮
        self.setFixedSize(615, 185)  # 设置窗体的大小
        self.setWindowIcon(QIcon("./Image/Icon_GetSource.png"))

        # 加载样式
        self._SetControlProperty()
        self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format(theme_str)))

        self.btnSelThPath.clicked.connect(self.BtnSelThPath_Click)
        self.btnSelThPath2.clicked.connect(self.BtnSelThPath2_Click)
        self.btnEnter.clicked.connect(self.BtnEnter_Click)
        self.btnCancel.clicked.connect(self.BtnCancel_Click)
        self.setIniFile = ini_file
        self.txtPath.setText(str(self.setIniFile.GetIniValue('Thunder','Path')))
        self.txtPath2.setText(str(self.setIniFile.GetIniValue('PotPlayer', 'Path')))
        self.cboThread.setCurrentIndex(int(self.setIniFile.GetIniValue('System','thread_count')))

    def ShowWindows(self):
        self.show()

    def closeEvent(self, event):
        self.deleteLater()

    def _SetControlProperty(self):
        self.setProperty('name', 'SettingFrm')
        self.btnCancel.setProperty('name','btnCancel')
        self.btnEnter.setProperty('name', 'btnEnter')
        self.btnSelThPath.setProperty('name', 'btnSelThPath')
        self.btnSelThPath2.setProperty('name', 'btnSelThPath2')

    def BtnSelThPath_Click(self):
        dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
        dlg.SetOFNInitialDir('E:/Python')  # 设置打开文件对话框中的初始显示目录
        dlg.DoModal()

        filename = dlg.GetPathName()  # 获取选择的文件名称
        self.txtPath.setText(filename)

    def BtnSelThPath2_Click(self):
        dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
        dlg.SetOFNInitialDir('E:/Python')  # 设置打开文件对话框中的初始显示目录
        dlg.DoModal()

        filename = dlg.GetPathName()  # 获取选择的文件名称
        self.txtPath2.setText(filename)


    def BtnEnter_Click(self):
        if len(self.txtPath.toPlainText())>0:

            th_count = self.cboThread.currentIndex()
            self.setIniFile.SetIniValue('System', 'thread_count', str(th_count))
            self.setIniFile.SetIniValue('Thunder', 'Path', self.txtPath.toPlainText())
            self.setIniFile.SetIniValue('PotPlayer', 'Path', self.txtPath2.toPlainText())
            win32api.MessageBox(0, "Write Path Success", "Tip",win32con.MB_OK)
            self.close()

    def BtnCancel_Click(self):
        self.close()