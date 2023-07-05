import sqlite3

from selenium import webdriver
from selenium.webdriver.common.by import By
from seoul_tour_ver1.seoul_main_page import *
from widget_for_food import *
from widget_for_sleep import *
from widget_for_tour import *

gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구',
                        '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구',
                        '관악구', '서초구', '강남구', '송파구', '강동구']
class WindowClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)
        self.var_init()
        self.Ui_init()
        self.insert_values_in_gridlayout()
        self.function_init()


        # self.widget.setLayout(grid)


    def what_do_you_want_to_know(self, choice):
        """
        뭘 알고 싶니
        :return:
        """
        self.stackedWidget.setCurrentWidget(self.main_page_2)
        self.gu_btn_clicked(choice)


    # 구 버튼 클릭이벤트
    def gu_btn_clicked(self, choice):
        if choice == 'food':
            text = '가고싶은 서울의 장소를 선택하세요!\n인기있는 음식점들만 소개해 드립니다.'
            self.main_2_title_lab.setText(text)
            for idx, btn in enumerate(self.gu_btn_list):
                btn.clicked.connect(lambda event, idx = idx : self.gu_btn_for_food(self.gu_btn_list[idx]))
        elif choice == 'sleep':
            text = '가고싶은 서울의 장소를 선택하세요!\n최고의 숙박시설을 소개해 드립니다.'
            self.main_2_title_lab.setText(text)
            for idx, btn in enumerate(self.gu_btn_list):
                btn.clicked.connect(lambda event, idx = idx : self.gu_btn_for_sleep(self.gu_btn_list[idx]))

    # 구 버튼 클릭하면 무슨일이 일어날까
    def gu_btn_for_food(self, btn):
        region = btn.text()
        self.main_3_title_lab.setText(f"{region}의 유명한 음식점을 안내해드려요!")
        self.main_4_title_lab.setText(f"{region}의 유명한 음식점을 안내해드려요!")
        datas = self.cur.execute(f'select * from food_list where gu_name = "{region}";')
        self.stackedWidget.setCurrentWidget(self.main_page_3)
        self.clear_scroll_area()
        self.set_data_of_food_in_scrollarea(datas)
        self.scrollArea.ensureVisible(0, 0)

    def gu_btn_for_sleep(self, btn):
        region = btn.text()
        self.main_3_title_lab.setText(f"{region}의 최고의 숙박시설을 안내해드려요!")
        self.main_4_title_lab.setText(f"{region}의 최고의 숙박시설을 안내해드려요!")
        datas = self.cur.execute(f'select 사업장명, 영업상태명, 도로명주소, img_path from seoul_lodges where 지번주소 like "%{region}%";')
        self.stackedWidget.setCurrentWidget(self.main_page_3)
        self.clear_scroll_area()
        self.set_data_of_sleep_in_scrollarea(datas)
        self.scrollArea.ensureVisible(0,0)

    def tour_btn_click(self):
        self.back_3_btn_clicked = True
        self.main_3_title_lab.setText(f"서울시의 유명한 명소를 소개해드려요!")
        self.main_4_title_lab.setText(f"서울시의 유명한 명소를 소개해드려요!")
        self.stackedWidget.setCurrentWidget(self.main_page_3)
        self.clear_scroll_area()
        self.set_data_of_tour_in_scrollarea()
        self.scrollArea.ensureVisible(0, 0)
    # 스크롤 위젯에 데이터 심기
    def set_data_of_food_in_scrollarea(self, datas):
        layout = self.scrollAreaWidgetContents.layout()
        for data in datas:
            name = data[2]
            rate = data[3]
            address = data[4]
            main_dishes = data[-3]
            price = data[-2]
            img_path = data[-1]
            layout.addWidget(SeoulForFood(name, rate, address, main_dishes, price, img_path, self))

    def set_data_of_sleep_in_scrollarea(self, datas):
        layout = self.scrollAreaWidgetContents.layout()
        for data in datas:
            name = data[0]
            status = data[1]
            address = data[2]
            image_path = data[-1]
            layout.addWidget(SeoulForSleep(name, status, address, image_path,self))

    def set_data_of_tour_in_scrollarea(self):
        layout = self.scrollAreaWidgetContents.layout()
        datas = self.cur.execute('select 상호명, 신주소, 운영요일, 운영시간, 휴무일, img_path from seoul_tourist;')
        for data in datas:
            name = data[0]
            address = data[1]
            working_day = data[2]
            working_time = data[3]
            holiday = data[4]
            image_path = data[-1]
            layout.addWidget(SeoulForTour(name, address, working_day, working_time, holiday, image_path,self))
    # 스크롤 에어리어 위젯비우기
    def clear_scroll_area(self):
        while self.scrollAreaWidgetContents.layout().count():
            item = self.scrollAreaWidgetContents.layout().takeAt(0)
            widget = item.widget()
            self.scrollAreaWidgetContents.layout().removeWidget(widget)

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

    ######################################
    #날씨관련
    def wheather_crawling(self):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://weather.naver.com/today/09140104?cpName=KMA")

        temperature = self.driver.find_element(By.CSS_SELECTOR, '#now > div > div.weather_area > div.weather_now > div > strong')
        wheather = self.driver.find_element(By.CSS_SELECTOR, '#now > div > div.weather_area > div.weather_now > p > span.weather')
        self.temp_label.setText(f"{temperature.text[-5:]} {wheather.text}")
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
    ######################################

    # 디비디비
    def activate_DB(self):
        self.conn = sqlite3.connect('../database/seoul_db.db')
        self.cur = self.conn.cursor()

    # 기능 이니트
    def function_init(self):
        self.wheather_crawling() # 날씨 크롤링
        self.food_btn.clicked.connect(lambda :self.what_do_you_want_to_know('food'))
        self.sleep_btn.clicked.connect(lambda :self.what_do_you_want_to_know('sleep'))
        self.tour_btn.clicked.connect(self.tour_btn_click)
        # 라벨 클릭하면 오픈 페이지로 이동
        self.label.mousePressEvent = lambda event: self.stackedWidget.setCurrentWidget(self.main_page_1)
        self.back_2_btn.clicked.connect(lambda x : self.stackedWidget.setCurrentWidget(self.main_page_1))
        self.back_3_btn.clicked.connect(self.back_3_btn_click_event)
        self.back_4_btn.clicked.connect(lambda x : self.stackedWidget.setCurrentWidget(self.main_page_3))
        self.activate_DB()

    def back_3_btn_click_event(self):
        if not self.back_3_btn_clicked:
            self.stackedWidget.setCurrentWidget(self.main_page_2)
        else:
            self.back_3_btn_clicked = False
            self.stackedWidget.setCurrentWidget(self.main_page_1)
    def Ui_init(self):
        #스크롤에어리어 레이아웃 넣기
        v_layout = QVBoxLayout(self)
        self.scrollAreaWidgetContents.setLayout(v_layout)
        #########
        self.stackedWidget.setCurrentWidget(self.open_page)

        self.label.setPixmap(QPixmap('../img/background.png'))
        self.back_2_btn.setIcon(QIcon('../img/back.png'))
        self.back_3_btn.setIcon(QIcon('../img/back.png'))
        self.back_4_btn.setIcon(QIcon('../img/back.png'))

    def var_init(self):
        self.back_3_btn_clicked = False # 관광버튼 눌렀는지 안눌렀느닞

if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('../font/Pretendard-Medium.ttf')
    app.setFont(QFont('Pretendard Medium'))

    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )