import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from soyeon.test import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('seoul_main_page.ui')
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)


        # self.widget.setLayout(grid)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )