import sys
from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self, image, points_list, parent=None):
        super().__init__(parent)

        self.painter = None
        self.resize(1000, 1000)
        self.setWindowIcon(QIcon("images/mp3-player.ico"))
        self.setWindowTitle("MP3-Player")
        self.points_list = points_list
        self.image = image
        w = self.image.size().width()
        h = self.image.size().height()

        # self.background_image = QLabel("<h2 style='color: blue'>lena.jpg</h2>", self)
        # self.background_image.move(240, 100)



    def paintEvent(self, event):
        for el_num in range(0, len(self.points_list) - 1):
            painter = QPainter(self)
            painter.drawPixmap(QPoint(), self.image)  # +++
            painter.setPen(QPen(Qt.red, 5))
            new_el = self.points_list[el_num].split()
            new_el_next = self.points_list[el_num + 1].split()
            print(self.points_list)
            print(new_el, new_el_next)
            print(new_el[0], new_el[1], new_el_next[0], new_el_next[1])
            painter.drawLine(int(new_el[0]), int(new_el[1]), int(new_el_next[0], int(new_el_next[1])))

    def draw_flag(self, dx, dy):
        self.lbl = QLabel(self)
        self.pix = QPixmap("png-flag.png")
        self.lbl.setPixmap(self.pix)
        self.lbl.resize(100, 100)
        self.lbl.move(dx, dy)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())