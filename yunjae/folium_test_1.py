import io
import sys

import folium
import pandas as pd
import sqlite3
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import *
from folium.plugins import MarkerCluster


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # ----- 윈도우창
        self.setWindowTitle('Seoul Folium Test')
        self.window_width, self.window_height = 700, 400
        self.setMinimumSize(self.window_width, self.window_height)
        self.setGeometry(300, 300, 1000, 600)

        # ----- Pandas / DataFrame
        # df = pd.read_csv('00_db/_csv/seoul_tourist.csv')
        con = sqlite3.connect('00_db/seoul_db.sqlite')
        cur = con.cursor()
        self.df_tour = pd.read_sql('SELECT * FROM seoul_tourist', con)
        self.df_sleep = pd.read_sql('SELECT * FROM seoul_sleep', con)

        # ----- Pandas Option
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)

        # ----- Layout & Button
        self.layout = QVBoxLayout()
        self.button = QPushButton('test', self)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # ----- self.seoul_map 좌표 설정
        latitude = 37.394946  # 위도
        longitude = 127.111104  # 경도
        # coordinate = (35.19475778198943, 126.8399771747554)  # 현재 보여줄 좌표 위치

        # ----- self.seoul_map
        self.seoul_map = folium.Map(
            tiles='OpenStreetMap',  # 배경지도 tiles에 대한 속성 => 타이틀명 아님
            zoom_start=10,  # 화면 보여줄 거리 => 값이 적을수록 가까이 보여줌
            location=[latitude, longitude],  # 현재 화면에 보여줄 좌표 값
            # zoom_control = False,
            # scrollWheelZoom = False,
            # dragging = False
        )

        # # ----- folium Marker => 마커 찍기 테스트
        # folium.Marker([latitude, longitude],
        #               radius=30,
        #               tooltip="윤재 집",
        #               popup='<iframe width="560" height="315" src="https://www.youtube.com/embed/dpwTOQri42s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
        #               icon=folium.Icon(color="red", icon="info-sign")
        #               ).add_to(m)

        # ----- folium MarkerCluster / Sub DataFrame
        sub_df = self.df_tour.loc[self.df_tour['map_select'].isin([1])]
        matching = sub_df[['x_pos', 'y_pos']]


        self.marker_cluster = MarkerCluster().add_to(self.seoul_map)
        self.mapping_tour_all_show()

        # ----- 다른 방법
        # for lat, long in zip(matching['x_pos'], matching['y_pos']):
        #     folium.Marker([lat, long],
        #                   tooltip="",
        #                   icon=folium.Icon(color="red")
        #                   ).add_to(marker_cluster)

        print("왔나?ffdddd")
        data = io.BytesIO()
        self.seoul_map.save('index.html', close_file=False)
        self.seoul_map.save(data, close_file=False)
        self.web = QWebEngineView()
        self.web.setHtml(data.getvalue().decode())
        self.layout.addWidget(self.web)

        # self.seoul_map.save('seoul_tour.html', close_file=False)
        # self.seoul_map.save('seoul_map.html', close_file=False)
        # self.loadPage()

    def mapping_tour_all_show(self):
        for index, row in self.df_tour.iterrows():
            tour_x_pos = row['x_pos']
            tour_y_pos = row['y_pos']
            tour_name = row['상호명']
            tour_info = row['신주소'], row['전화번호']
            folium.Marker([tour_x_pos, tour_y_pos], tooltip=tour_name, popup=tour_info, icon=folium.Icon(color="red")).add_to(self.marker_cluster)

    def mapping_sleep_all_show(self):
        for index, row in self.df_sleep.iterrows():
            sleep_x_pos = row['x_pos']
            sleep_y_pos = row['y_pos']
            sleep_name = row['사업장명']
            sleep_info = row['도로명주소'], row['전화번호']
            folium.Marker([sleep_x_pos, sleep_y_pos], tooltip=sleep_name, popup=sleep_info, icon=folium.Icon(color="blue")).add_to(self.marker_cluster)

    def loadPage(self):
        with open('seoul_map.html', 'r') as f:
            html = f.read()
            self.web.setHtml(html)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(''' QWidget { font-size: 35px; }''')
    run = MyApp()
    run.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
