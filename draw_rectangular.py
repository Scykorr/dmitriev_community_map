import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


# from time import sleep


class Drawer(QWidget):
    def __init__(self, width, height, parent=None):
        QWidget.__init__(self, parent)
        self.setAttribute(Qt.WA_StaticContents)
        self.pen_width = 3
        self.pen_color = Qt.black
        self.image = QImage(width, height, QImage.Format_RGB32)
        self.path = QPainterPath()
        self.clear()

    def clear(self):
        self.path = QPainterPath()
        self.image.fill(Qt.white)
        self.update()

    def save_image(self, fileName, fileFormat):
        self.image.save(fileName, fileFormat)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(event.rect(), self.image, self.rect())

    def draw_rect(self, x, y, szx, szy, color=None, width=None):
        p = QPainter(self.image)

        p.setPen(QPen(color if color else self.pen_color,
                      width if width else self.pen_width,
                      Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

        p.drawRect(x, y, szx, szy)
        p.end()
        self.update()


def on_timeout():  # +++
    # Удаляю все рисунки
    drawer.clear()
    # Рисую второй прямоугольнки который и оторажается в конце
    drawer.draw_rect(0, 0, 30, 30)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = QWidget()
    win.resize(900, 900)

    drawer = Drawer(500, 500)

    win.setLayout(QVBoxLayout())
    win.layout().addWidget(drawer)

    # Рисую прямоугольник который не получается отобразить
    drawer.draw_rect(0, 10, 200, 100)
    #    win.show()
    #    sleep(3)

    QTimer.singleShot(3000, on_timeout)  # +++
    # Удаляю все рисунки
    #    drawer.clear()
    # Рисую второй прямоугольнки который и оторажается в конце
    #    drawer.draw_rect(0, 0, 30, 30)

    win.show()
    sys.exit(app.exec_())