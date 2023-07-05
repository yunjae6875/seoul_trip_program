import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from seoul_widget import *

class SeoulWidget(QWidget, Ui_Form):
    def __init__(self, name, address, main_dishes, img_path, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.name = name
        self.address = address
        self.main_dishes = main_dishes
        self.img_path = img_path

        self.parent_seoul = parent

        self.name_lab.setText(f"이 름 : {self.name}")
        self.type_lab.setText(f"메인 메뉴 : {self.main_dishes}")
        self.location_lab.setText(f"주 소 : {self.address}")
        self.img_label.setPixmap(QPixmap(f"{self.img_path}"))

    def mousePressEvent(self, event):
        self.parent_seoul.stackedWidget.setCurrentWidget(self.parent_seoul.main_page_4)
        self.parent_seoul.name_lab.setText(f"이 름 : {self.name}")
        self.parent_seoul.type_lab.setText(f"메인 메뉴 : {self.main_dishes}")
        self.parent_seoul.location_lab.setText(f"주 소 : {self.address}")
        self.parent_seoul.img_label.setPixmap(QPixmap(f"{self.img_path}"))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = SeoulWidget()
    myWindow.show()
    app.exec()

