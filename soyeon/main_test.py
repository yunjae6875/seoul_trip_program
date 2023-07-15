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
        super().__init__()
        self.setupUi(self)

        self.insert_values_in_gridlayout() # 그리드 레이아웃에 값 넣기

        # 라벨 클릭하면 오픈 페이지로 이동
        self.opening_page_img_lab.mousePressEvent = lambda event: self.stackedWidget.setCurrentWidget(self.main_page_1)


    def insert_values_in_gridlayout(self):
        """그리드 레이아웃에 값 넣기"""
        btn_style = '''
        border-radius:15px;
        border: 1px solid black;
        background-color: rgb(255, 255, 255);
        '''
        for i, gu in enumerate(gu_list, start=1):
            button = QPushButton(gu)  # 버튼 생성 및 이름 넣어줌
            button.setFixedSize(100, 100)  # 버튼의 크기 고정
            button.setStyleSheet(btn_style)  # 버튼 스타일 설정
            self.gridLayout.addWidget(button, (i - 1) // 5 + 1, (i - 1) % 5 + 1)  # 그리드 레이아웃에 버튼 위치 설정 (행위치 / 열위치)
            # print((i - 1) // 5 + 1, (i - 1) % 5 + 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./font/Pretendard-Medium.ttf')
    app.setFont(QFont('Pretendard Medium'))

    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
