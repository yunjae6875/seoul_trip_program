import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from seoul_widget import *

class SeoulForTour(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = SeoulForTour()
    myWindow.show()
    app.exec()

