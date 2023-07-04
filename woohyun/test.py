import os
import sqlite3
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from seoul_main_page import *
from widget_test import *

gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구',
                        '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구',
                        '관악구', '서초구', '강남구', '송파구', '강동구']
class WindowClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.Ui_init()
        self.insert_values_in_gridlayout()
        self.function_init()

        # self.widget.setLayout(grid)

    def food_btn_click_event(self):
        self.stackedWidget.setCurrentWidget(self.main_page_2)

    # 구 버튼 클릭이벤트
    def gu_btn_clicked(self):
        for idx, btn in enumerate(self.gu_btn_list):
            btn.clicked.connect(lambda event, idx = idx : self.what_if_gu_btn_click(self.gu_btn_list[idx]))

    # 구 버튼 클릭하면 무슨일이 일어날까
    def what_if_gu_btn_click(self, btn):
        region = btn.text()
        datas = self.cur.execute(f'select * from food_list where gu_name = "{region}";')
        self.stackedWidget.setCurrentWidget(self.main_page_3)
        self.set_data_of_food_in_scrollarea(datas)

    # 스크롤 위젯에 데이터 심기
    def set_data_of_food_in_scrollarea(self, datas):
        layout = self.scrollAreaWidgetContents.layout()
        for data in datas:
            name = data[2]
            rate = data[3]
            address = data[4]
            main_dishes = data[-3]
            img_path = data[-1]
            layout.addWidget(SeoulWidget(name,address,main_dishes,img_path, self))

    # hover 하면 색 변하게 하기 (수정필요)
    def insert_values_in_gridlayout(self):
        self.gu_btn_list = list()
        # self.button_group = QButtonGroup()  # 버튼 그룹 생성
        cnt = 0
        for i in range(1, 6):
            for j in range(1, 6):
                button = QPushButton(gu_list[cnt])  # 버튼 생성 및 이름 넣어줌
                button.setFixedSize(100, 100)  # 버튼의 크기 고정
                # button.setCheckable(True)  # 선택할 수 있게 설정
                button.setStyleSheet('''
                border-radius:15px;
                border: 1px solid black;
                background-color: rgb(255, 255, 255);
                ''')
                # self.button_group.addButton(button)  # 버튼 그룹에 버튼 추가
                self.gridLayout.addWidget(button, i, j)
                self.gu_btn_list.append(button)
                cnt += 1

    def wheather_crawling(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(options=options)
        # self.driver = webdriver.Chrome()
        self.driver.get("https://weather.naver.com/today/09140104?cpName=KMA")

        temperature = self.driver.find_element(By.CSS_SELECTOR, '#now > div > div.weather_area > div.weather_now > div > strong')
        wheather = self.driver.find_element(By.CSS_SELECTOR, '#now > div > div.weather_area > div.weather_now > p > span.weather')
        self.temp_label.setText(f"{temperature.text[-5:]}")
        self.set_wheather_icon(wheather.text)
        self.driver.close()

    # 날씨 셋업
    def set_wheather_icon(self, wheather):
        wheather_icon_path = ['../img/wheather_icon/shiny', '../img/wheather_icon/cloudy', '../img/wheather_icon/overcast',
                              '../img/wheather_icon/rainy']
        idx = None
        if wheather == '맑음':
            idx = 0
        elif wheather == '구름 낀':
            idx = 1
        elif wheather == '흐림':
            idx = 2
        elif wheather == '비':
            idx = 3

        self.wheather_icon.setPixmap(QPixmap(wheather_icon_path[idx]))

    # 디비디비
    def activate_DB(self):
        self.conn = sqlite3.connect('../database/food.db')
        self.cur = self.conn.cursor()

    # 기능 이니트
    def function_init(self):
        self.wheather_crawling() # 날씨 크롤링
        self.food_btn.clicked.connect(self.food_btn_click_event)
        self.gu_btn_clicked()
        self.activate_DB()

    def Ui_init(self):
        v_layout = QVBoxLayout(self)
        self.scrollAreaWidgetContents.setLayout(v_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('../font/Pretendard-Medium.ttf')
    app.setFont(QFont('Pretendard Medium'))

    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )