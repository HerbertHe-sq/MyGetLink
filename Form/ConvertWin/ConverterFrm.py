import base64
import urllib

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QIcon
from Form.ConvertWin.ConverterUi import Ui_ConvertWindow
from Function.QssHelper import QssHelper


class ConverterWindow(QtWidgets.QMainWindow, Ui_ConvertWindow):
    myCloseSignal = QtCore.pyqtSignal(str)

    def __init__(self,theme_str):
        super(ConverterWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint);  # 窗体没有最大化最小化按钮
        self.setFixedSize(585, 185)  # 设置窗体的大小
        self.appPath = ""
        self.setWindowIcon(QIcon(self.appPath + "./Image/Icon_GetSource.png"))

        # 加载样式
        self._SetControlProperty()
        self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format(theme_str)))

        self.radioButton.setChecked(True)

        self.btnConvert.clicked.connect(self.BtnConvert_Click)

    def ShowWindows(self):
        self.show()


    def closeEvent(self, event):
        self.SendCloseMsg()

    def _SetControlProperty(self):
        self.setProperty('name', 'ConverterFrm')
        self.btnConvert.setProperty('name', 'btnConvert')

    def SendCloseMsg(self):
        self.myCloseSignal.emit("0")

    def BtnConvert_Click(self):
        tag_str = self.textEdit.toPlainText()
        result_str=""     #迅雷连接转换
        try:
            if self.radioButton.isChecked():
                result_str = 'AA' + tag_str + 'ZZ'
                result_str = "thunder://"+str(base64.b64encode(result_str.encode('utf-8')),'utf-8')
            else:
                tag_str = tag_str.replace("thunder://","")
                result_str = str(base64.b64decode(tag_str),'utf-8')
                result_str = urllib.parse.unquote(result_str[2:-2])

            self.textEdit_2.setText(result_str)
        except:
            pass