import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from seoul_widget import *

class SeoulForSleep(QWidget, Ui_Form):
    def __init__(self, name, status, address, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.name = name
        self.status = status
        self.address = address
        self.seoul_main = parent

        self.name_lab.setText(f"이 름 : {self.name}")
        self.type_lab.setText(f"상 태 : {self.status}")
        self.location_lab.setText(f"주 소 : {self.address}")
        # self.img_label.setPixmap(QPixmap(f"{self.img_path}"))

    def mousePressEvent(self, event):
        self.seoul_main.stackedWidget.setCurrentWidget(self.seoul_main.main_page_4)
        self.seoul_main.name_lab.setText(f"이 름 : {self.name}")
        self.seoul_main.type_lab.setText(f"상 태 : {self.status}")
        self.seoul_main.location_lab.setText(f"주 소 : {self.address}")
        # self.seoul_main.img_label.setPixmap(QPixmap(f"{self.img_path}"))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = SeoulForSleep()
    myWindow.show()
    app.exec()

