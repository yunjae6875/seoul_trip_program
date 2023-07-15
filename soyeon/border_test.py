from PyQt5.QtWidgets import QApplication, QMainWindow

app = QApplication([])

class CustomMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom MainWindow")
        self.setGeometry(100, 100, 400, 300)  # Example window geometry

        self.setStyleSheet(
            "QMainWindow {"
            "   background-color: #f0f0f0;"  # Example background color
            "   border-radius: 10px;"
            "   border: 2px solid #000000;"  # Example border color and width
            "}"
        )

window = CustomMainWindow()
window.show()

app.exec()
