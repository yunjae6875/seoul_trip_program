import io
import sqlite3
import folium
import sys
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from seoul_main_page import *
from widget_for_food import *
from widget_for_sleep import *
from widget_for_tour import *

# 윤재 코드 병합중(main_copy로 이어서 진행)
from map_file import *

gu_list = ['종로구', '중구', '용산구', '성동구', '광진구', '동대문구', '중랑구', '성북구', '강북구', '도봉구',
           '노원구', '은평구', '서대문구', '마포구', '양천구', '강서구', '구로구', '금천구', '영등포구', '동작구',
           '관악구', '서초구', '강남구', '송파구', '강동구']


class WindowClass(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.map_obj = FoliumMap()
        self.setupUi(self)
        self.var_init()
        self.Ui_init()
        self.insert_values_in_gridlayout()
        self.function_init()

    def show_map_as_search(self, user_idx):
        """검색한 값에 따라 자료들이 출력됨"""
        if self.verticalLayout_17.count():
            self.verticalLayout_17.takeAt(0)
        print('여길 탑니다')
        print('유저의 선택은', user_idx)
        user_text = self.map_lineEdit.text()
        print("유저가 선택한 동은", user_text)
        if user_text == "": # 사용자가 검색을 하지 않은 경우
            if user_idx == 0:
                self.map_obj.mapping_food_all_show()
            elif user_idx == 1:
                self.map_obj.mapping_lodges_all_show()
            else:
                self.map_obj.mapping_tour_all_show()
        else:
            print('검색창에 친 경우')
            if user_idx == 0:
                self.map_obj.mapping_food_guname_show(user_text)
            elif user_idx == 1:
                self.map_obj.mapping_lodges_guname_show(user_text)
            else:
                self.map_obj.mapping_tour_guname_show(user_text)

        # while self.verticalLayout_17.count():
        #     child = self.verticalLayout_17.takeAt(0)
        #     if child.widget():
        #         child.widget().deleteLater()

        self.verticalLayout_17.addWidget(self.map_obj.load_map())
        del self.map_obj
        self.map_obj = FoliumMap()
        print("객체 지움")


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
                btn.clicked.connect(lambda event, idx=idx: self.gu_btn_for_food(self.gu_btn_list[idx]))
        elif choice == 'sleep':
            text = '가고싶은 서울의 장소를 선택하세요!\n최고의 숙박시설을 소개해 드립니다.'
            self.main_2_title_lab.setText(text)
            for idx, btn in enumerate(self.gu_btn_list):
                btn.clicked.connect(lambda event, idx=idx: self.gu_btn_for_sleep(self.gu_btn_list[idx]))

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
        #
        # MyApp(self).show()

    def gu_btn_for_sleep(self, btn):
        region = btn.text()
        self.main_3_title_lab.setText(f"{region}의 최고의 숙박시설을 안내해드려요!")
        self.main_4_title_lab.setText(f"{region}의 최고의 숙박시설을 안내해드려요!")
        datas = self.cur.execute(f'select 사업장명, 영업상태명, 도로명주소, x_pos, y_pos, img_path from seoul_lodges where 지번주소 like "%{region}%";')
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
            x_pos = data[5]
            y_pos = data[6]
            main_dishes = data[-3]
            price = data[-2]
            img_path = data[-1]
            layout.addWidget(SeoulForFood(name, rate, address, main_dishes, price, x_pos, y_pos, img_path, self))

    def set_data_of_sleep_in_scrollarea(self, datas):
        layout = self.scrollAreaWidgetContents.layout()
        for data in datas:
            name = data[0]
            status = data[1]
            address = data[2]
            x_pos = data[3]
            y_pos = data[4]
            image_path = data[-1]
            layout.addWidget(SeoulForSleep(name, status, address, x_pos, y_pos, image_path, self))

    def set_data_of_tour_in_scrollarea(self):
        layout = self.scrollAreaWidgetContents.layout()
        datas = self.cur.execute('select 상호명, 신주소, 운영요일, 운영시간, 휴무일, x_pos, y_pos, img_path from seoul_tourist;')
        for data in datas:
            name = data[0]
            address = data[1]
            working_day = data[2]
            working_time = data[3]
            holiday = data[4]
            x_pos = data[-3]
            y_pos = data[-2]
            image_path = data[-1]
            layout.addWidget(SeoulForTour(name, address, working_day, working_time, holiday, x_pos, y_pos, image_path,self))
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
                button.setStyleSheet('''
                border-radius:15px;
                border: 1px solid black;
                background-color: rgb(255, 255, 255);
                ''')
                # self.button_group.addButton(button)  # 버튼 그룹에 버튼 추가
                self.gridLayout.addWidget(button, i, j)
                self.gu_btn_list.append(button)
                cnt += 1

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
        wheather_icon_path = ['../img/wheather_icon/shiny', '../img/wheather_icon/cloud', '../img/wheather_icon/overcast',
                              '../img/wheather_icon/rainy']
        idx = None
        if wheather == '맑음':
            idx = 0
        elif wheather == '구름많음':
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

    def back_3_btn_click_event(self):
        if not self.back_3_btn_clicked:
            self.stackedWidget.setCurrentWidget(self.main_page_2)
        else:
            self.back_3_btn_clicked = False
            self.stackedWidget.setCurrentWidget(self.main_page_1)
    ######################################################################
    # 로그인 페이지 작업 -> 생년월일 창
    def input_personal_information(self):
        self.check_name()
        self.check_phone_number()

        if self.check_name() and self.check_phone_number() :
            self.stackedWidget.setCurrentWidget(self.main_page_1)
            personal_info = (self.lineEdit, self.lineEdit_2, self.lineEdit_3)
            # self.cur.execute("insert into {테이블이름넣으셈} values (?, ?, ?);",personal_info)
            # self.conn.commit()
        else:
            print("썸띵이즈롱")

    # 이름체크
    def check_name(self):
        name = self.lineEdit.text()
        if len(name) > 6:
            print("너는 이름이 왤케 기니?")
            return False
        else:
            return True

    # 연락처 체크
    def check_phone_number(self):
        number = self.lineEdit_2.text()
        check_number = self.check_len_phone_number(number)

    # 번호에 숫자이외의 썸띵이 들어가는지
    def check_letter_in_number(self, number):
        for num in number:
            num = ord(num)
            if 47 < num < 58:
                pass
            else :
                print("숫자외는 입력을 못한단다")
                return False
        return True

    # 폰 번호 길이체크
    def check_len_phone_number(self, number):
        if len(number) == 11:
            if self.check_letter_in_number(number):
                return True
        else:
            return False

    ######################################################################

    # 기능 이니트
    def function_init(self):
        # self.wheather_crawling() # 날씨 크롤링
        self.food_btn.clicked.connect(lambda :self.what_do_you_want_to_know('food'))
        self.sleep_btn.clicked.connect(lambda :self.what_do_you_want_to_know('sleep'))
        self.tour_btn.clicked.connect(self.tour_btn_click)

        # 라벨 클릭하면 오픈 페이지로 이동
        self.label.mousePressEvent = lambda event: self.stackedWidget.setCurrentWidget(self.main_page_1)
        self.back_2_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.main_page_1))
        self.back_3_btn.clicked.connect(self.back_3_btn_click_event)
        self.back_4_btn.clicked.connect(lambda x : self.stackedWidget.setCurrentWidget(self.main_page_3))
        self.all_show_btn.clicked.connect(lambda x : self.stackedWidget.setCurrentWidget(self.main_page_5))


        #         # self.admit_btn.clicked.connect(self.input_personal_information)
        self.activate_DB()

        # 자동완성 기능 추가
        completer = QCompleter(gu_list)
        self.map_lineEdit.setCompleter(completer)

        # 지도버튼 시그널 연결
        map_btn_list = [self.map_food_btn, self.map_lodge_btn, self.map_place_btn]
        for idx, btn in enumerate(map_btn_list):
            btn.clicked.connect(lambda x, y= idx: self.show_map_as_search(y))


    # def show_whole_map(self):
    #     """전체 지도를 보여줍니다"""
    #     self.stackedWidget.setCurrentWidget(self.main_page_5)
    #     print(self.verticalLayout_17)
    #     self.map_obj.mapping_tour_all_show() # 모든 관광명소를 지도에 마커+클러스터로 표시함
    #     self.verticalLayout_17.addWidget(self.map_obj.load_map())


    # def back_3_btn_click_event(self):
    #     if not self.back_3_btn_clicked:
    #         self.stackedWidget.setCurrentWidget(self.main_page_2)
    #     else:
    #         self.back_3_btn_clicked = False
    #         self.stackedWidget.setCurrentWidget(self.main_page_1)

    def Ui_init(self):
        # 스크롤에어리어 레이아웃 넣기
        v_layout = QVBoxLayout(self)
        self.scrollAreaWidgetContents.setLayout(v_layout)
        #########
        self.stackedWidget.setCurrentWidget(self.open_page)

        self.label.setPixmap(QPixmap('../img/background.png'))
        self.back_2_btn.setIcon(QIcon('../img/back.png'))
        self.back_3_btn.setIcon(QIcon('../img/back.png'))
        self.back_4_btn.setIcon(QIcon('../img/back.png'))
        # 웹엔진뷰
        self.webview = QWebEngineView()
        webview_layout = QVBoxLayout(self)
        self.map_widget.setLayout(webview_layout)

    def var_init(self):
        self.back_3_btn_clicked = False  # 관광버튼 눌렀는지 안눌렀는지


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('./font/Pretendard-Medium.ttf')
    app.setFont(QFont('Pretendard Medium'))

    myWindow = WindowClass()
    myWindow.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
    # app.exec_()
