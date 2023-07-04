import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구',
                        '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구',
                        '관악구', '서초구', '강남구', '송파구', '강동구']

# def insert_values_in_gridlayout(grid):
#         # self.button_group = QButtonGroup()  # 버튼 그룹 생성
#         cnt = 0
#         for i in range(1, 6):
#             for j in range(1, 6):
#                 button = QPushButton(gu_list[cnt])  # 버튼 생성 및 이름 넣어줌
#                 button.setFixedSize(100, 100)  # 버튼의 크기 고정
#                 button.setCheckable(True)  # 선택할 수 있게 설정
#                 self.button_group.addButton(button)  # 버튼 그룹에 버튼 추가
#                 grid.addWidget(button, i, j)
#                 cnt += 1