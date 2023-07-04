import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from soyeon.test import *
from PyQt5.QtGui import *

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('seoul_main_page.ui')
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

        self.insert_values_in_gridlayout()

        # self.widget.setLayout(grid)

    # hover 하면 색 변하게 하기 (수정필요)
    def insert_values_in_gridlayout(self):
        # self.button_group = QButtonGroup()  # 버튼 그룹 생성
        cnt = 0
        for i in range(1, 6):
            for j in range(1, 6):
                button = QPushButton(gu_list[cnt])  # 버튼 생성 및 이름 넣어줌
                button.setFixedSize(100, 100)  # 버튼의 크기 고정
                button.setCheckable(True)  # 선택할 수 있게 설정
                button.setStyleSheet('''
                border-radius:15px;
                border: 1px solid black;
                background-color: rgb(255, 255, 255);
                ''')
                # self.button_group.addButton(button)  # 버튼 그룹에 버튼 추가
                self.gridLayout.addWidget(button, i, j)
                cnt += 1




if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./font/Pretendard-Medium.ttf')
    app.setFont(QFont('Pretendard Medium'))

    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )