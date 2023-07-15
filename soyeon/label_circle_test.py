import sys
from PyQt5 import QtGui, QtCore, QtWidgets


def circleImage(imagePath):
    """이미지 경로를 받아 둥글게 만드는 함수"""
    source = QtGui.QPixmap(imagePath)  # imagePath를 이용하여 이미지를 QPixmap 객체로 로드
    size = min(source.width(), source.height())  # 이미지의 너비와 높이 중 작은 값을 선택하여 정사각형으로 만들어준다.

    target = QtGui.QPixmap(size, size)  # 원형 이미지를 그릴 캔버스
    target.fill(QtCore.Qt.transparent)  # 투명하게 채움

    qp = QtGui.QPainter(target)  # QPainter 객체를 생성하여 target 위에 그릴 수 있도록 설정
    qp.setRenderHints(qp.Antialiasing)  # 안티앨리어싱(render hint)을 설정하여 부드럽게 그릴 수 있도록 함
    path = QtGui.QPainterPath()  # path라는 QPainterPath 객체를 생성하여 원형 모양의 경로를 정의
    path.addEllipse(0, 0, size, size)
    qp.setClipPath(path)  # qp의 클리핑 경로로 path를 설정 -> 이렇게 하면 이미지는 원형 내부에만 그려짐

    # sourceRect를 생성하여 원본 이미지에서 원형 영역을 잘라내기 위한 영역을 설정
    sourceRect = QtCore.QRect(0, 0, size, size)
    sourceRect.moveCenter(source.rect().center())
    # qp.drawPixmap을 사용하여 원본 이미지에서 sourceRect의 부분만을 target에 그림
    qp.drawPixmap(target.rect(), source, sourceRect)
    qp.end()  # qp를 닫기

    return target  # target 반환


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create a QLabel to display the circular image
        self.imageLabel = QtWidgets.QLabel()
        self.setCentralWidget(self.imageLabel)

        # Load the image and set it to the QLabel
        image_path = "../img/background.png"  # Replace with the actual image path
        circular_image = circleImage(image_path)
        self.imageLabel.setPixmap(circular_image)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
