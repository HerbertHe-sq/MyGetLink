import sys
import os

if hasattr(sys,'frozen'):
	os.environ['PATH']=sys._MEIPASS+";"+os.environ['PATH']

from PyQt5.QtWidgets import QApplication
from MainFrm import MainWindow

if __name__ == '__main__':
	    app = QApplication(sys.argv)
	    main_frm = MainWindow()
	    main_frm.ShowWindow()
	    sys.exit(app.exec_())
