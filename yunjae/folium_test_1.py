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

        # ----- 좌표: 위도 경도
        latitude = 37.394946  # 위도
        longitude = 127.111104  # 경도
        # coordinate = (35.19475778198943, 126.8399771747554)  # 현재 보여줄 좌표 위치

        # ----- Pandas / DataFrame
        # df = pd.read_csv('00_db/_csv/seoul_tourist.csv')
        con = sqlite3.connect('00_db/seoul_db.sqlite')
        cur = con.cursor()
        df = pd.read_sql('SELECT * FROM seoul_tourist', con)
        lod_df = pd.read_sql('SELECT * FROM seoul_lodges', con)

        # ----- Pandas Option
        pd.set_option("display.max_columns", None)
        pd.set_option("display.max_rows", None)

        # ----- Sub DataFrame
        sub_df = df.loc[df['map_select'].isin([1])]
        third_df = lod_df.loc[lod_df['select'].isin([1])]

        # ----- Layout & Button
        layout = QVBoxLayout()
        button = QPushButton('test', self)
        layout.addWidget(button)
        self.setLayout(layout)

        # ----- folium map 설정
        m = folium.Map(
            tiles='OpenStreetMap',  # 배경지도 tiles에 대한 속성 => 타이틀명 아님
            zoom_start=10,  # 화면 보여줄 거리 => 값이 적을수록 가까이 보여줌
            location=[latitude, longitude],  # 현재 화면에 보여줄 좌표 값
            # zoom_control = False,
            # scrollWheelZoom = False,
            # dragging = False
        )

        # ----- folium Marker => 마커 찍기
        folium.Marker([latitude, longitude],
                      radius=30,
                      tooltip="윤재 집",
                      popup='<iframe width="560" height="315" src="https://www.youtube.com/embed/dpwTOQri42s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                      icon=folium.Icon(color="red", icon="info-sign")
                      ).add_to(m)

        # ----- folium MarkerCluster
        matching = sub_df[['x_pos', 'y_pos']]
        marker_cluster = MarkerCluster().add_to(m)
        for lat, long in zip(matching['x_pos'], matching['y_pos']):
            folium.Marker([lat, long],
                          tooltip="",
                          icon=folium.Icon(color="red")
                          ).add_to(marker_cluster)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(''' QWidget { font-size: 35px; }''')
    run = MyApp()
    run.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
