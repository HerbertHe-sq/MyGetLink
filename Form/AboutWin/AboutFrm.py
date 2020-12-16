import base64

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication

from Form.AboutWin.AboutUi import Ui_AboutWindow
from Function.QssHelper import QssHelper


class AboutWindow(QtWidgets.QMainWindow, Ui_AboutWindow):
    def __init__(self,theme_str):
        super(AboutWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint);  # 窗体没有最大化最小化按钮
        self.setFixedSize(390, 325)  # 设置窗体的大小
        self.setWindowIcon(QIcon("./Image/Icon_GetSource.png"))

        # 加载样式
        self._SetControlProperty()
        self.setStyleSheet(QssHelper.ReadQss("./Qss/{0}/MainFrmStyle.qss".format(theme_str)))

        pixmap = QPixmap("./Image/Icon_Search.png")
        pixmap = pixmap.scaled(130, 130, aspectRatioMode=Qt.KeepAspectRatio)
        self.labImg.setPixmap(pixmap)

    def ShowWindows(self):
        self.show()

    def closeEvent(self, event):
        self.deleteLater()

    # 为所有控件设置setProperty
    def _SetControlProperty(self):
        self.label.setProperty('name', 'label')
        self.label_2.setProperty('name', 'label_2')

    def SetAuthorData(self,ver_str):
        self.label.setText('Software Name:\r\nMyGetLink Tool\r\n\r\nVersion:' + ver_str + '\r\nAnthor:Herbert He')
        self.label_2.setText('本系统只为内部交流学习，不以盈利为目的!!!!\r\n所有资源均来源第三方资源，并不提供影片资源存储，\r\n录制、上传相关视频等，视频版权归属其合法持有人\r\n所有,本站不对使用者的行为负担任何法律责任'+
                            '如果有\r\n因为本站而导致您的权益受到损害，请与我们联系，\r\n我们将理性对待，协助你解决相关问题。')