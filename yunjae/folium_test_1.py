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
        self.setWindowTitle('Seoul Folium Test')  # 타이틀 설정
        self.window_width, self.window_height = 700, 400  # 창 가로, 세로길이 설정
        self.setMinimumSize(self.window_width, self.window_height)  # 최소크기 가로, 세로크기로 설정함
        self.setGeometry(300, 300, 1000, 600)  # 창 크기 설정

        # ----- 좌표: 위도 경도
        latitude = 37.394946  # 위도
        longitude = 127.111104  # 경도
        # coordinate = (35.19475778198943, 126.8399771747554)  # 현재 보여줄 좌표 위치

        # ----- Pandas / DataFrame
        # df = pd.read_csv('00_db/_csv/seoul_tourist.csv')
        con = sqlite3.connect('00_db/seoul_db.sqlite')  # seoul_db 연결 및 con 객체에 담는다.
        cur = con.cursor()  # 커서 객체 생성
        df = pd.read_sql('SELECT * FROM seoul_tourist', con)  # con db에서 참조한 - seoul_tourlist 테이블에서 모든 값을 가져와 df에 담는다.
        lod_df = pd.read_sql('SELECT * FROM seoul_lodges',
                             con)  # con db에서 참조한 - seoul_lodges 테이블에서 모든 값을 가져와 lod_df에 담는다.

        # ----- Pandas Option
        pd.set_option("display.max_columns", None)  # 열값 모두 표시
        pd.set_option("display.max_rows", None)  # 행값 모두 표시

        # ----- Sub DataFrame
        sub_df = df.loc[df['map_select'].isin([1])]  # df 데이터프레임에서 'map_select' 열 값이 1인 행만 선택하여 sub_df에 할당한다.
        third_df = lod_df.loc[lod_df['select'].isin([1])]  # lod_df 데이터프레임에서 'select' 열 값이 1인 행만 선택하여 third_df에 할당한다.

        # ----- Layout & Button
        layout = QVBoxLayout()  # 수직 상자 레이아웃(QVBoxLayout) 객체를 생성
        button = QPushButton('test', self)  # 'test'라는 텍스트를 갖는 QPushButton 객체를 생성
        layout.addWidget(button)  # button을 수직 상자 레이아웃에 추가
        self.setLayout(layout)  # 위에서 생성한 수직 상자 레이아웃을 현재 위젯의 레이아웃으로 설정

        # ----- folium map 설정
        # folium.Map 함수를 사용하여 지도 객체 m을 생성
        m = folium.Map(
            tiles='OpenStreetMap',  # 배경지도 tiles에 대한 속성 => 타이틀명 아님
            zoom_start=10,  # 화면 보여줄 거리 => 값이 적을수록 가까이 보여줌
            location=[latitude, longitude],  # 현재 화면에 보여줄 좌표 값
            # zoom_control = False,
            # scrollWheelZoom = False,
            # dragging = False
        )

        # ----- folium Marker => 마커 찍기
        # 주어진 좌표에 마커를 생성
        folium.Marker([latitude, longitude],
                      radius=30,  # radius 인자: 마커의 크기를 설정
                      tooltip="윤재 집",  # tooltip 인자: 마커에 대한 툴팁을 설정
                      # popup 인자: 마커를 클릭했을 때 표시되는 팝업을 설정
                      popup='<iframe width="560" height="315" src="https://www.youtube.com/embed/dpwTOQri42s" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>',
                      icon=folium.Icon(color="red", icon="info-sign")  # icon 인자: 마커의 아이콘 스타일을 설정
                      ).add_to(m)  # 생성된 마커를 m 지도 객체에 추가

        # ----- folium MarkerCluster
        # folium.MarkerCluster를 사용하여 여러 개의 마커를 클러스터링하는 객체 marker_cluster를 생성
        matching = sub_df[['x_pos', 'y_pos']]  # sub_df 데이터프레임에서 'x_pos'와 'y_pos' 열을 추출하여 matching에 저장
        marker_cluster = MarkerCluster().add_to(m)
        for lat, long in zip(matching['x_pos'], matching['y_pos']):  # matching의 좌표 값을 순회하면서 folium.Marker 함수를 사용하여 각 좌표에 마커를 생성
            folium.Marker([lat, long],
                          tooltip="",
                          icon=folium.Icon(color="red") # 빨간 아이콘 스타일을 설정
                          ).add_to(marker_cluster)  # 생성된 마커는 앞서 생성한 marker_cluster에 추가

        # save map data to data object
        # 지도 데이터를 바이트 스트림으로 저장하기 위해 io.BytesIO 객체인 data를 생성
        data = io.BytesIO()
        m.save(data, close_file=False)  # m 지도 객체를 data에 저장한다.
        webView = QWebEngineView()  # QWebEngineView를 생성하고
        webView.setHtml(data.getvalue().decode())  # setHtml 메서드를 사용하여 data에 저장된 지도 데이터를 로드한다.
        layout.addWidget(webView)  # webView를 수직 상자 레이아웃(vbox)에 추가


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(''' QWidget { font-size: 35px; }''')
    run = MyApp()
    run.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
