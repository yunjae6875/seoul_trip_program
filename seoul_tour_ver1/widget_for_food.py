import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from seoul_widget import *
# from PyQt5 import QtGui, QtCore, QtWidgets

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

        # Replace with the actual image path
        self.circular_image = self.circleImage(self.img_path)
        # self.imageLabel.setPixmap(circular_image)

        self.seoul_main = parent
        self.name_lab.setText(f"이 름 : {self.name}   평 점 : {self.rate}")
        self.type_lab.setText(f"메인 메뉴 : {self.main_dishes}   가 격 대 : {self.price}")
        self.location_lab.setText(f"주 소 : {self.address}")
        # self.img_label.setPixmap(QPixmap(f"{self.img_path}"))
        self.img_label.setPixmap(self.circular_image)

    def circleImage(self, imagePath):
        source = QtGui.QPixmap(imagePath)
        size = min(source.width(), source.height())

        target = QtGui.QPixmap(size, size)
        target.fill(QtCore.Qt.transparent)

        qp = QtGui.QPainter(target)
        qp.setRenderHints(qp.Antialiasing)
        path = QtGui.QPainterPath()
        path.addEllipse(0, 0, size, size)
        qp.setClipPath(path)

        sourceRect = QtCore.QRect(0, 0, size, size)
        sourceRect.moveCenter(source.rect().center())
        qp.drawPixmap(target.rect(), source, sourceRect)
        qp.end()

        return target

    def mousePressEvent(self, event):
        self.seoul_main.stackedWidget.setCurrentWidget(self.seoul_main.main_page_4)
        self.seoul_main.name_lab.setText(f"이 름 : {self.name}     평 점 : {self.rate}")
        self.seoul_main.type_lab.setText(f"메인 메뉴 : {self.main_dishes}     가 격 대 : {self.price}")
        self.seoul_main.location_lab.setText(f"주 소 : {self.address}")
        self.seoul_main.img_label.setPixmap(self.circular_image)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = SeoulForFood()
    myWindow.show()
    app.exec()

