import os
import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from seoul_main_page import *
gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구',
                        '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구',
                        '관악구', '서초구', '강남구', '송파구', '강동구']
class WindowClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

        self.insert_values_in_gridlayout()
        self.wheather_crawling()
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

    def set_wheather_icon(self, wheather):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('../font/Pretendard-Medium.ttf')
    app.setFont(QFont('Pretendard Medium'))

    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )