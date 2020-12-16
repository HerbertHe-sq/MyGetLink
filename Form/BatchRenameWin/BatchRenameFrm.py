import os

import win32api
import win32con
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QStringListModel, QFileInfo
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileDialog

from Form.BatchRenameWin.BatchRenameUi import Ui_BatchRenameWin
from Function.QssHelper import QssHelper


class BatchRenameWindow(QtWidgets.QMainWindow, Ui_BatchRenameWin):
    signal_list = QtCore.pyqtSignal()

    def __init__(self,theme_str):
        super(BatchRenameWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint);  # 窗体没有最大化最小化按钮
        self.setFixedSize(492, 554)  # 设置窗体的大小
        self.appPath = ""
        self.setWindowIcon(QIcon(self.appPath + "./Image/Icon_GetSource.png"))

        # 加载样式
        self._SetControlProperty(theme_str)
        self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format(theme_str)))
        self.InitSetUp()

    def ShowWindows(self):
        self.show()

    def closeEvent(self, event):
        self.deleteLater()

    def _SetControlProperty(self,theme_str):
        self.setProperty('name','BatchRenameFrm')
        self.listView.verticalScrollBar().setStyleSheet(QssHelper.ReadQss("./Qss/{0}/ScrollBarStyle.qss".format(theme_str)))
        self.listView.horizontalScrollBar().setStyleSheet(QssHelper.ReadQss("./Qss/{0}/ScrollBarStyle.qss".format(theme_str)))
        self.btnChange.setProperty('name', 'btnChange')
        self.btnSelect.setProperty('name', 'btnSelect')
        self.btnSelectFolder.setProperty('name', 'btnSelectFolder')

    def InitSetUp(self):
        # 清空列表
        self.qList = []
        self.fileList = []
        self.signal_list.connect(self.UpdateListView) #更新ListView

        self.btnSelect.clicked.connect(self.BtnSelectFile_Click)
        self.btnSelectFolder.clicked.connect(self.BtnSelectFolder_Click)
        self.btnChange.clicked.connect(self.BtnChange_Click)

    #选择文件夹
    def BtnSelectFolder_Click(self):
        file_dialog = QFileDialog()
        file_folder = file_dialog.getExistingDirectory(self, "Please select file directory", '')
        self.fileList.clear()
        for file in os.listdir(file_folder):
            temp_file = QFileInfo(file)
            self.qList.append(temp_file.fileName())
            self.fileList.append(file_folder+'/'+file)
        self.signal_list.emit()

    #选择文件
    def BtnSelectFile_Click(self):
        files, file_type = QFileDialog.getOpenFileNames(self, "Please Select File", "/", "所有文件 (*.*);;所有文件 (*)")
        self.fileList.clear()
        for file in files:
            temp_file = QFileInfo(file)
            self.qList.append(temp_file.fileName())
            self.fileList.append(file)
        self.signal_list.emit()

    def BtnChange_Click(self):
        tag_str = self.txtFirst.toPlainText()
        rep_str = self.txtSecond.toPlainText()
        path_list = []
        name_list = []

        if len(self.fileList)>0:
            for i in range(0,len(self.fileList)):
                name = self.fileList[i][self.fileList[i].rfind('/'):]
                path = self.fileList[i][:self.fileList[i].rfind('/')]
                path_list.append(path)
                name_list.append(name.replace(tag_str,rep_str))

            for i in range(0,len(self.fileList)):
                desc_path = path_list[i]+name_list[i]
                if self.fileList[i]!=desc_path:
                    os.rename(self.fileList[i],desc_path)
                    self.fileList[i] = desc_path
                    self.qList[i] = name_list[i].replace('/','')
            win32api.MessageBox(0, "Rename successful!", "Tip", win32con.MB_ICONINFORMATION, win32con.MB_OK)
            self.signal_list.emit()


    # 更新列表
    def UpdateListView(self):
        slm = QStringListModel()  # 实例化列表模型，添加数据
        slm.setStringList(self.qList)  # 设置模型列表视图，加载数据列表
        self.listView.setModel(slm)  # 设置列表视图的模型