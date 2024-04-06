import sys
from PyQt5.Qt import *


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.resize(512, 512)
        #        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon("images/mp3-player.ico"))
        self.setWindowTitle("MP3-Player")

        self.image = QPixmap("lena.jpg")  # +++
        w = self.image.size().width()
        h = self.image.size().height()

        self.background_image = QLabel("<h2 style='color: blue'>lena.jpg</h2>", self)
        self.background_image.move(w - 240, h - 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.image)  # +++
        painter.setPen(QPen(Qt.red, 5))
        painter.drawLine(10, 10, 500, 500)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())