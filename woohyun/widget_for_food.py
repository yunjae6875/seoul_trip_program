import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from seoul_widget import *

class SeoulForFood(QWidget, Ui_Form):
    def __init__(self, name, rate, address, main_dishes, price, img_path, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.name = name
        self.rate = rate
        self.address = address
        self.main_dishes = main_dishes
        self.price = price
        self.img_path = img_path

        self.parent_seoul = parent
        self.name_lab.setText(f"이 름 : {self.name}   평 점 : {self.rate}")
        self.type_lab.setText(f"메인 메뉴 : {self.main_dishes}   가 격 대 : {self.price}")
        self.location_lab.setText(f"주 소 : {self.address}")
        self.img_label.setPixmap(QPixmap(f"{self.img_path}"))

    def mousePressEvent(self, event):
        self.parent_seoul.stackedWidget.setCurrentWidget(self.parent_seoul.main_page_4)
        self.parent_seoul.name_lab.setText(f"이 름 : {self.name}     평 점 : {self.rate}")
        self.parent_seoul.type_lab.setText(f"메인 메뉴 : {self.main_dishes}     가 격 대 : {self.price}")
        self.parent_seoul.location_lab.setText(f"주 소 : {self.address}")
        self.parent_seoul.img_label.setPixmap(QPixmap(f"{self.img_path}"))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = SeoulForFood()
    myWindow.show()
    app.exec()

