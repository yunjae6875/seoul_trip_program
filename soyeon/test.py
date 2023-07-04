import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic


# def insert_values_in_gridlayout()
#     genres_kor_list = list(genres_dict.keys())  # 20개
#             self.button_group = QButtonGroup()  # 버튼 그룹 생성
#             grid = QGridLayout(self.scrollAreaWidgetContents)
#             cnt = 0
#             for i in range(1, 6):
#                 for j in range(1, 5):
#                     button = QPushButton(genres_kor_list[cnt])  # 버튼 생성 및 이름 넣어줌
#                     button.setFixedSize(150, 75)  # 버튼의 크기 고정
#                     button.setCheckable(True)  # 선택할 수 있게 설정
#                     self.button_group.addButton(button)  # 버튼 그룹에 버튼 추가
#                     grid.addWidget(button, i, j)
#                     cnt += 1