import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(30, 30, 500, 300)

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     pixmap = QPixmap("test_img.bmp")
    #     painter.drawPixmap(self.rect(), pixmap)
    #     painter.setPen((QPen(QColor("red"))))
    #     painter.drawLine(0, 0, 1000, 1000)


    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap("test_img.bmp")
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(QColor("red"))
        pen.setWidth(10)
        painter.setPen(pen)
        painter.drawLine(0, 0, 1000, 1000)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.showMaximized()
    sys.exit(app.exec_())
