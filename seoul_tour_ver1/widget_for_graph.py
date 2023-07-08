import sys
import folium
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from map_widget import *

class SeoulforGraph(QWidget, Ui_Form):
    def __init__(self, name, img_path, desc, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.graph_name = name
        self.img_path = img_path
        self.desc = desc
        self.seoul_main = parent

        self.map_lab.setPixmap(QPixmap(f"{self.img_path}"))
        self.map_info.setText(f"{self.graph_name}")

    def mousePressEvent(self, event):
        self.seoul_main.stackedWidget.setCurrentWidget(self.seoul_main.main_page_7)
        self.seoul_main.graph_img_lab.setPixmap(QPixmap(f"{self.img_path}"))
        self.seoul_main.graph_info_lab.setText(f"{self.desc}")
        self.seoul_main.grahp_title_lab.setText(f'{self.graph_name}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = SeoulforGraph()
    myWindow.show()
    app.exec()
