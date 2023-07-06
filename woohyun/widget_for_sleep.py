import sys
import folium
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from seoul_widget import *

class SeoulForSleep(QWidget, Ui_Form):
    def __init__(self, name, status, address, x_pos, y_pos, image_path,parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.name = name
        self.status = status
        self.address = address
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image_path = image_path
        self.seoul_main = parent

        self.name_lab.setText(f"이 름 : {self.name}")
        self.type_lab.setText(f"상 태 : {self.status}")
        self.location_lab.setText(f"주 소 : {self.address}")
        self.img_label.setPixmap(QPixmap(f"{self.image_path}"))

    def mousePressEvent(self, event):
        self.seoul_main.stackedWidget.setCurrentWidget(self.seoul_main.main_page_4)
        self.seoul_main.name_lab.setText(f"이 름 : {self.name}")
        self.seoul_main.type_lab.setText(f"상 태 : {self.status}")
        self.seoul_main.location_lab.setText(f"주 소 : {self.address}")
        self.seoul_main.img_label.setPixmap(QPixmap(f"{self.image_path}"))
        self.create_map()

    def create_map(self):
        map = folium.Map(location=[self.x_pos, self.y_pos], zoom_start=17, scrollWheelZoom=False,
                         zoom_control=False,  dragging=False)
        folium.Marker([self.x_pos, self.y_pos], tooltip=self.name, icon=folium.Icon(color="green")).add_to(
            map)
        map.save('map.html')
        self.loadPage()

    def loadPage(self):
        layout = self.seoul_main.map_widget.layout()
        layout.addWidget(self.seoul_main.webview)
        with open('map.html', 'r', encoding='UTF8') as f:
            html = f.read()
            self.seoul_main.webview.setHtml(html)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = SeoulForSleep()
    myWindow.show()
    app.exec()

