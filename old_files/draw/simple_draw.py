import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap  # для машинки
from PyQt5.QtGui import QPainter  # для геометрических фигур


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.qp = QPainter()
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 100, 400, 400)
        self.setWindowTitle('Рисование')
        self.pixmap = QPixmap("car2.png")
        self.lbl = QLabel(self)
        self.lbl.setPixmap(self.pixmap)
        self.show()

    def paintEvent(self, event):
        self.qp.begin(self)
        coords = [[100, 200], [200, 300], [300, 100]]
        self.qp.setPen(Qt.red)
        self.qp.drawLine(*coords[0], *coords[1])
        self.qp.drawLine(*coords[1], *coords[2])
        self.qp.drawLine(*coords[2], *coords[0])
        self.qp.drawEllipse(*[250, 250], 20, 20)
        self.qp.drawRect(*[170, 170], *[20, 20])
        self.qp.end()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())