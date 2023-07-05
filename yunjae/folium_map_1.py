# --- import modules
import io
import sqlite3
import sys

import folium
import pandas as pd
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from folium.plugins import MarkerCluster


class FoliumMap(QWidget):
    def __init__(self):
        super().__init__()

        # --- 윈도우창
        self.setWindowTitle('Seoul Folium Test')
        self.window_width, self.window_height = 700, 700
        self.setMinimumSize(self.window_width, self.window_height)
        self.setGeometry(300, 300, 1000, 600)

        # --- DB + Query
        self.conn = sqlite3.connect('00_db/seoul_db.db')
        self.cur = self.conn.cursor()

        # --- 판다스 리드
        self.df_tour = pd.read_sql('SELECT * FROM seoul_tourist', self.conn)  # --- 관광명소
        self.df_lodge = pd.read_sql('SELECT * FROM seoul_lodges', self.conn)  # --- 숙박업소
        self.df_food = pd.read_sql('SELECT * FROM food_list', self.conn)  # --- 음식점
        self.df_food_jongro = pd.read_sql('SELECT * FROM food_list WHERE gu_name = "종로구"', self.conn)

        # --- 판다스 옵션
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)

        # --- 레이아웃 & 버튼 & 웹엔진뷰
        self.layout = QVBoxLayout()
        self.button = QPushButton('뒤로가기(아직안됨)', self)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        # self.button.clicked.connect(self.button_clicked_event)

        # --- self.seoul_map 지도 설정
        self.latitude = 37.394946  # 위도
        self.longitude = 127.111104  # 경도
        self.titles = "http://mt0.google.com/vt/lyrs=m&hl=ko&x={x}&y={y}&z={z}"
        self.attr = "Google"
        # self.coordinate = (35.19475778198943, 126.8399771747554)

        # --- folium 맵 설정: 서울 전체 맵
        self.seoul_map = folium.Map(
            # tiles=self.titles,  # --- 배경지도 tiles에 대한 속성 (기본값: https://www.openstreetmap.org)
            # attr=self.attr,
            zoom_start=10,  # --- 화면 보여줄 거리 / 값이 적을수록 가까이 보여줌
            location=[self.latitude, self.longitude],  # --- 현재 화면에 보여줄 좌표 값
            control_scale=True,  # --- contol_scale: True 시 맵 좌측 하단에 배율을 보여줌
            # zoom_control = False,   # --- zoom_control: False 시 줌 컨트롤러가 사라집니다. (단, 마우스 휠 줌은 가능)
            # scrollWheelZoom = False,  # --- scrollWheelZoom: False 시 스크롤을 사용할 수 없음
            # dragging = False  # --- dragging: False 시 마우스 드래그를 사용할 수 없음
        )
        self.marker_cluster = MarkerCluster().add_to(self.seoul_map)  # --- 미리 만들어 둔 맵(self.seoul_map)을 변수에 저장합니다.

        # --- 실행부
        self.mapping_food_all_show()  # --- 마커+클러스터 맵에 표시
        self.load_map()  # --- 현재 폴더에 index.html 파일을 저장하고, 실제 위젯에 맵 불러오기

    # --- 메소드
    def mapping_tour_all_show(self):
        """DB의 관광지 목록을 맵에 마커 + 클러스트로 적용시킵니다"""
        for index, row in self.df_tour.iterrows():
            x_pos = row['x_pos']
            y_pos = row['y_pos']
            name = row['상호명']
            info = row['신주소'], row['전화번호']
            link = f"<a href={row['웹사이트']}>웹사이트 접속</a>"
            roadview = '<a href="https://www.google.com/maps?layer=c&cbll=' + str(x_pos) + ',' + str(y_pos) + '" target="_blank">GOOGLE STREET VIEW</a>'
            # popup = folium.Popup(name + f"({str(link)})" + "<br><br>" + str(info), min_width=500, max_width=500)
            popup = folium.Popup(name + f"({str(link)})" + "<br><br>" + str(info) + "<br><br>" + roadview, min_width=500, max_width=500)
            folium.Marker([x_pos, y_pos], tooltip=name, popup=popup, icon=folium.Icon(color="red")).add_to(self.marker_cluster)

    def mapping_lodges_all_show(self, ):
        """DB의 숙박지 목록을 맵에 마커 + 클러스트로 적용시킵니다"""
        for index, row in self.df_lodge.iterrows():
            x_pos = row['x_pos']
            y_pos = row['y_pos']
            name = row['사업장명']
            info = row['도로명주소'], row['전화번호']
            popup = folium.Popup(name + "<br>" + str(info), min_width=400, max_width=400)
            folium.Marker([x_pos, y_pos], tooltip=name, popup=popup, icon=folium.Icon(color="blue")).add_to(self.marker_cluster)

    def mapping_food_all_show(self, ):
        """DB의 음식점 목록을 맵에 마커 + 클러스트로 적용시킵니다"""
        for index, row in self.df_food.iterrows():
            x_pos = row['x_pos']
            y_pos = row['y_pos']
            name = row['name']
            info = row['address']
            img = row['img_path']
            popup = folium.Popup(f"<img src='{img}'>" + "<br><br>" + name + "<br><br>" + str(info), min_width=400, max_width=400)
            # folium.Marker([x_pos, y_pos], tooltip=name, popup=popup, icon=folium.Icon(color="green")).add_to(self.marker_cluster)
            folium.Marker([x_pos, y_pos], tooltip=name, popup=popup).add_to(self.marker_cluster)
            if index == 1000:
                break

    def load_map(self):
        """self.seoul_map을 index.html 파일로 저장하고, PyQt 레이아웃에 QWebEngineView를 추가합니다"""
        data = io.BytesIO()
        self.seoul_map.save('index.html', close_file=False)
        self.seoul_map.save(data, close_file=False)
        self.web = QWebEngineView()
        self.web.setHtml(data.getvalue().decode())
        self.layout.addWidget(self.web)

    def button_clicked_event(self):
        """뒤로가기 버튼"""
        print("def button_clicked_event")
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(''' QWidget { font-size: 35px; }''')
    run = FoliumMap()
    run.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
