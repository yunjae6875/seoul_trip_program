import io
import random
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
from widget_for_graph import *
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
        # 레이아웃에 있는 객체를 지움
        if self.verticalLayout_17.count():
            self.verticalLayout_17.takeAt(0)

        # 유저가 검색한 내용을 가져옴
        user_text = self.map_lineEdit.text()
        print("유저가 선택한 동은", user_text)

        # 사용자가 검색을 하지 않은 경우
        if user_text == "":
            if user_idx == 0:
                self.map_obj.mapping_food_all_show()  # 서울의 모든 음식점을 보여줌
            elif user_idx == 1:
                self.map_obj.mapping_lodges_all_show()  # 서울의 모든 숙박업소를 보여줌
            else:
                self.map_obj.mapping_tour_all_show()  # 서울의 모든 명소를 보여줌

        # 사용자가 구 검색을 한 경우
        else:
            if user_idx == 0:
                self.map_obj.mapping_food_guname_show(user_text)
            elif user_idx == 1:
                self.map_obj.mapping_lodges_guname_show(user_text)
            else:
                self.map_obj.mapping_tour_guname_show(user_text)

        # 레이아웃에 맵 객체를 리턴받아서 로드해 줌
        self.verticalLayout_17.addWidget(self.map_obj.load_map())
        del self.map_obj  # map 클래스 객체를 지우고
        self.map_obj = FoliumMap()  # 다시 생성
        print("객체 지움")  # 확인용

    def what_do_you_want_to_know(self, choice):
        """
        뭘 알고 싶니
        :return:
        """
        self.stackedWidget.setCurrentWidget(self.main_page_2)
        self.gu_btn_clicked(choice)

    # 구 버튼 클릭이벤트
    def gu_btn_clicked(self, choice):
        """유저가 선택한 버튼에 따라 라벨의 내용을 변경해 줌"""
        if choice == 'food':
            self.frame_20.setStyleSheet('background-color:#FFEFB5;border-radius:20px;')
            text = '가고싶은 서울의 장소를 선택하세요!\n인기있는 음식점들만 소개해 드립니다.'
            self.main_2_title_lab.setText(text)
            for idx, btn in enumerate(self.gu_btn_list):
                btn.clicked.connect(lambda event, idx=idx: self.gu_btn_for_food(self.gu_btn_list[idx]))
        elif choice == 'sleep':
            self.frame_20.setStyleSheet('background-color:#B0DAFF;border-radius:20px;')
            text = '가고싶은 서울의 장소를 선택하세요!\n최고의 숙박시설을 소개해 드립니다.'
            self.main_2_title_lab.setText(text)
            for idx, btn in enumerate(self.gu_btn_list):
                btn.clicked.connect(lambda event, idx=idx: self.gu_btn_for_sleep(self.gu_btn_list[idx]))

    # 구 버튼 클릭하면 무슨일이 일어날까
    def gu_btn_for_food(self, btn):
        """구 버튼을 클릭하면 스크롤 영역에 음식점 리스트를 넣어줌"""
        region = btn.text()
        food_text = f"{region}의 유명한 음식점을 안내해드려요!"
        self.main_3_title_lab.setText(food_text)
        self.main_4_title_lab.setText(food_text)
        datas = self.cur.execute(f'select * from food_list where gu_name = "{region}";')
        self.stackedWidget.setCurrentWidget(self.main_page_3)
        self.clear_scroll_area()
        self.set_data_of_food_in_scrollarea(datas)
        self.scrollArea.ensureVisible(0, 0)

    def gu_btn_for_sleep(self, btn):
        """구 버튼을 클릭하면 스크롤 영역에 숙박업소 리스트를 넣어줌"""
        region = btn.text()
        sleep_text = f'{region}의 최고의 숙박시설을 안내해드려요!'
        self.main_3_title_lab.setText(sleep_text)
        self.main_4_title_lab.setText(sleep_text)
        datas = self.cur.execute(
            f'select 사업장명, 영업상태명, 도로명주소, x_pos, y_pos, img_path from seoul_lodges where 지번주소 like "%{region}%";')
        self.stackedWidget.setCurrentWidget(self.main_page_3)
        self.clear_scroll_area()
        self.set_data_of_sleep_in_scrollarea(datas)
        self.scrollArea.ensureVisible(0, 0)

    def tour_btn_click(self):
        """스크롤 영역에 명소리스트를 넣어줌"""
        self.frame_20.setStyleSheet('background-color:#caffbf; border-radius:20px;')
        self.back_3_btn_clicked = True
        tour_text = '서울시의 유명한 명소를 소개해드려요!'
        self.main_3_title_lab.setText(tour_text)
        self.main_4_title_lab.setText(tour_text)
        self.stackedWidget.setCurrentWidget(self.main_page_3)
        self.clear_scroll_area()
        self.set_data_of_tour_in_scrollarea()
        self.scrollArea.ensureVisible(0, 0)

    # 스크롤 위젯에 데이터 심기
    def set_data_of_food_in_scrollarea(self, datas):
        """스크롤 영역에 음식점 데이터 심기"""
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
        """스크롤 영역에 숙박업소 리스트 심기"""
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
        """스크롤 영역에 명소 리스트 심기"""
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
            layout.addWidget(
                SeoulForTour(name, address, working_day, working_time, holiday, x_pos, y_pos, image_path, self))

    def clear_scroll_area(self):
        """스크롤 영역 위젯 비워주기"""
        while self.scrollAreaWidgetContents.layout().count():
            item = self.scrollAreaWidgetContents.layout().takeAt(0)
            widget = item.widget()
            self.scrollAreaWidgetContents.layout().removeWidget(widget)

    def insert_values_in_gridlayout(self):
        """그리드 영역에 버튼 생성해서 넣어주기"""
        self.gu_btn_list = list()
        cnt = 0
        for i in range(1, 6):
            for j in range(1, 6):
                button = QPushButton(gu_list[cnt])  # 버튼 생성 및 이름 넣어줌
                button.setFixedSize(100, 100)  # 버튼의 크기 고정
                button.setStyleSheet('''
                border-radius:15px;
                border: 1px solid black;
                ''')
                self.gridLayout.addWidget(button, i, j)
                self.gu_btn_list.append(button)
                cnt += 1

    # 날씨관련
    def wheather_crawling(self):
        """날씨를 크롤링해와서 메인 화면에 지정함"""
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://weather.naver.com/today/09140104?cpName=KMA")

        temperature = self.driver.find_element(By.CSS_SELECTOR,
                                               '#now > div > div.weather_area > div.weather_now > div > strong')
        wheather = self.driver.find_element(By.CSS_SELECTOR,
                                            '#now > div > div.weather_area > div.weather_now > p > span.weather')
        self.temp_label.setText(f"{temperature.text[-5:]} ")
        self.temp_label_2.setText(f'{wheather.text}')
        self.set_wheather_icon(wheather.text)
        self.driver.close()

    # 날씨 셋업
    def set_wheather_icon(self, wheather):
        """날씨 아이콘을 설정함"""
        wheather_icon_path = {
            '맑음': '../img/wheather_icon/shiny',
            '구름많음': '../img/wheather_icon/cloud',
            '흐림': '../img/wheather_icon/overcast',
            '비': '../img/wheather_icon/rainy'
        }
        idx = wheather_icon_path.get(wheather)
        self.wheather_icon.setPixmap(QPixmap(idx))

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
        if self.check_name() and self.check_len_phone_number(self.lineEdit_2.text()):
            self.stackedWidget.setCurrentWidget(self.main_page_1)
            self.main_sub_title.setText(f"{self.lineEdit.text()}님, \n서울 여행을 준비하세요.")
            personal_info = (self.lineEdit, self.lineEdit_2, self.dateEdit)
            # self.cur.execute("insert into {테이블이름넣으셈} values (?, ?, ?);",personal_info)
            # self.conn.commit()
        else:
            print("썸띵이즈롱")

    # 이름체크
    def check_name(self):
        name = self.lineEdit.text()
        if len(name) == 0:
            self.user_name_label.setText('이름을 입력해주세요.')
            self.user_name_label.setStyleSheet('color:red;')
            return False
        elif len(name) > 6:
            self.user_name_label.setText('이름이 너무 깁니다.')
            self.user_name_label.setStyleSheet('color:red;')
            return False
        else:
            self.user_name_label.setText(f'{name}님 안녕하세요.')
            self.user_name_label.setStyleSheet('color:blue;')
            print('트루탐')
            return True

    # 연락처 체크
    # 번호에 숫자이외의 썸띵이 들어가는지
    def check_letter_in_number(self, number):
        # number = self.lineEdit_2.text()
        # check_number = self.check_len_phone_number(number)
        for num in number:
            num = ord(num)
            if 47 < num < 58:
                return True
                pass
            else:
                self.user_number_label('숫자만 입력하실 수 잇습니다.')
                self.user_number_label.setStyleSheet('color:red;')
                return False
        return True

    # 폰 번호 길이체크
    def check_len_phone_number(self, number):

        if len(number) == 11:
            if self.check_letter_in_number(number):
                return True
        else:
            self.user_number_label.setText('형식에 맞게 핸드폰 번호를 입력해주세요.')
            self.user_number_label.setStyleSheet('color:red;')
            return False

    ######################################################################
    # 그래프 관련 작업 코드
    def set_graph_widget(self):
        layout = self.frame_22.layout()
        row = 0
        column = 0
        for name, img_path, desc in zip(self.graph_name_list, self.graph_imgpath_list, self.graph_desc_list):
            layout.addWidget(SeoulforGraph(name, img_path, desc, self), row, column)
            column += 1
            if column == 2:
                row += 1
                column = 0
    ######################################################################
    # 기능 이니트
    def function_init(self):

        # 날씨 크롤링
        self.wheather_crawling()

        # 버튼에 따라 다른 조건으로 이동
        self.food_btn.clicked.connect(lambda: self.what_do_you_want_to_know('food'))
        self.sleep_btn.clicked.connect(lambda: self.what_do_you_want_to_know('sleep'))
        self.tour_btn.clicked.connect(self.tour_btn_click)

        # 라벨 클릭하면 오픈 페이지로 이동
        self.label.mousePressEvent = lambda event: self.stackedWidget.setCurrentWidget(self.login_page)
        # 버튼 클릭하면 특정 페이지로 이동
        self.back_2_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.main_page_1))
        self.back_3_btn.clicked.connect(self.back_3_btn_click_event)
        self.back_4_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.main_page_3))
        self.back_5_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.main_page_1))
        self.all_show_btn.clicked.connect(lambda x: self.stackedWidget.setCurrentWidget(self.main_page_5))
        self.admit_btn.clicked.connect(self.input_personal_information)

        # db 활성화
        self.activate_DB()

        # 자동완성 기능 추가
        completer = QCompleter(gu_list)
        self.map_lineEdit.setCompleter(completer)

        # 지도버튼 시그널 연결
        map_btn_list = [self.map_food_btn, self.map_lodge_btn, self.map_place_btn]
        for idx, btn in enumerate(map_btn_list):
            btn.clicked.connect(lambda x, y=idx: self.show_map_as_search(y))

        # 하단 버튼 시그널 연결
        menu_btn_frame = [self.menu_btns_frame_1, self.menu_btns_frame_2, self.menu_btns_frame_3,
                          self.menu_btns_frame_4]  # 메뉴 버튼 담긴 프레임
        menu_btns = [frame.findChildren(QPushButton) for frame in menu_btn_frame]  # 해당 프레임에 있는 버튼들 가져오기

        # 버튼에 따라 이동해야 할 페이지
        button_mapping = {
            'menu_home_btn': self.main_page_1,
            'menu_map_btn': self.main_page_5,
            'menu_menu_btn': self.main_page_6,
            # 여기에 4번째 버튼 연결할 것 있으면 추가
        }

        # 버튼에 따라 다른 페이지로 이동(위 button_mapping 딕셔너리 참고)
        for btn_list in menu_btns:
            for btn in btn_list:
                for object_name, widget in button_mapping.items():
                    if object_name in btn.objectName():
                        btn.clicked.connect(lambda checked, widget=widget: self.stackedWidget.setCurrentWidget(widget))
                        break

        # 그래프 페이지 시그널 연결
        self.set_graph_widget()
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
        """스타일시트 관련"""
        # 스크롤에어리어 레이아웃 넣기
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint)  # Qt.WindowType.WindowStaysOnTopHint 프레임 지우기 / 윈도우가 다른 창 위에 항상 최상위로 유지되도록 함
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게 함

        v_layout = QVBoxLayout(self)
        self.scrollAreaWidgetContents.setLayout(v_layout)

        # 오픈 페이지 랜덤 지정
        self.stackedWidget.setCurrentWidget(self.open_page)
        random_num = random.randint(1, 4)

        # 라벨에 이미지 넣어주기
        self.label.setPixmap(QPixmap(f'../img/qt_img/background_{random_num}.png'))
        self.back_2_btn.setIcon(QIcon('../img/qt_img/back.png'))
        self.back_3_btn.setIcon(QIcon('../img/qt_img/back.png'))
        self.back_4_btn.setIcon(QIcon('../img/qt_img/back.png'))
        self.back_5_btn.setIcon(QIcon('../img/qt_img/back.png'))


        # 웹엔진뷰
        self.webview = QWebEngineView()
        webview_layout = QVBoxLayout(self)
        self.map_widget.setLayout(webview_layout)

        self.map_lineEdit.returnPressed.connect(self.show_map_as_search)

        # 그래프 레이아웃 설정
        graph_layout = QGridLayout(self)
        self.frame_22.setLayout(graph_layout)

    def var_init(self):
        """관광버튼 눌렀는지 확인하기"""
        self.back_3_btn_clicked = False
        self.graph_imgpath_list = ['../img/graph_img/map_1', '../img/graph_img/map_2', '../img/graph_img/map_3'
            , '../img/graph_img/map_4', '../img/graph_img/map_5']
        self.graph_name_list = ['월별_서울방문비교', '연령별_서울방문비교', '목적별_서울방문비교', '국가별_서울방문비교',
                                '자치구별 호텔 비율']
        self.graph_desc_list = ['- 이 데이터는 2022년을 기준으로 수집되었습니다.'
                                '- 월별(1~12월)로 어느 시점에 사람들이 서울을 여행지를 선택하여 방문했는지 시각화 했습니다.',
                                '- 이 데이터는 2022년을 기준으로 수집되었습니다.'
                                '- 연령대(15~20세/21~30세/31~40세/41~50세/51~60세)별로 서울을 여행지로 선택하여 방문했는지 시각화 했습니다.',
                                '- 이 데이터는 2022년을 기준으로 수집되었습니다.'
                                '- 서울을 방문하는 사람들이 어떤 목적을 가지고 방문 했는지 시각화 했습니다.',
                                '- 이 데이터는 2022년을 기준으로 수집되었습니다.'
                                '- 서울을 방문한 외국인들의 국적 비율을 시각화 했습니다.',
                                '- 서울의 각 구별 호텔 비율을 설명합니다.']


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('../font/Pretendard-Medium.ttf') # 폰트 지정
    app.setFont(QFont('Pretendard Medium'))

    myWindow = WindowClass()
    myWindow.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
