from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPen, QColor
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QFileDialog, QWidget, QHBoxLayout
from PyQt5.Qt import QPoint, QPainter


class QImageView(QWidget):
    def __init__(self, window=None):
        super().__init__()

        self.fileName = None
        self.image_height = None
        self.image_width = None
        self.window = window
        self.printer = QPrinter()
        self.scaleFactor = 0.0

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.scrollArea.setVisible(False)

        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.centralWidget = QWidget()
        self.layout = QHBoxLayout(self.centralWidget)
        self.layout.addWidget(self.scrollArea)

        self.scrollArea.mouseMoveEvent = self.mouseMoveEvent
        self.scrollArea.mousePressEvent = self.mousePressEvent
        self.scrollArea.mouseReleaseEvent = self.mouseReleaseEvent
        self.scrollArea.wheelEvent = self.wheelEvent

        self.imageLabel.setCursor(Qt.OpenHandCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.fileName)
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(QColor("red"))
        pen.setWidth(10)
        painter.setPen(pen)
        painter.drawLine(0, 0, 1000, 1000)

    def mousePressEvent(self, event):
        self.pressed = True
        self.imageLabel.setCursor(Qt.ClosedHandCursor)
        self.initialPosX = self.scrollArea.horizontalScrollBar().value() + event.pos().x()
        self.initialPosY = self.scrollArea.verticalScrollBar().value() + event.pos().y()
        self.update()

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.imageLabel.setCursor(Qt.OpenHandCursor)
        self.initialPosX = self.scrollArea.horizontalScrollBar().value()
        self.initialPosY = self.scrollArea.verticalScrollBar().value()

    def mouseMoveEvent(self, event):
        if self.pressed:
            self.scrollArea.horizontalScrollBar().setValue(self.initialPosX - event.pos().x())
            self.scrollArea.verticalScrollBar().setValue(self.initialPosY - event.pos().y())

    def wheelEvent(self, event) -> None:
        wheel_val = event.angleDelta().y()
        if wheel_val > 0:
            self.zoomIn()
        elif wheel_val < 0:
            self.zoomOut()

    def open_img(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if self.fileName:
            print(self.fileName)
            self.image = QImage(self.fileName)
            if self.image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % self.fileName)
                return
            # px = QPixmap.fromImage(self.image)
            px = QPixmap(self.fileName)

            painter = QPainter(self)
            pixmap = QPixmap(self.get_img_path())
            painter.drawPixmap(self.rect(), pixmap)
            pen = QPen(QColor("red"))
            pen.setWidth(10)
            painter.setPen(pen)
            painter.drawLine(0, 0, 1000, 1000)

            self.imageLabel.setPixmap(px)
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.window.printAct.setEnabled(True)
            self.window.fitToWindowAct.setEnabled(True)
            self.window.scaling.setEnabled(True)
            self.updateActions()

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def print_img(self):
        dialog = QPrintDialog(self.printer, self)
        if dialog.exec_():
            painter = QPainter(self.printer)
            rect = painter.viewport()
            size = self.imageLabel.pixmap().size()
            size.scale(rect.size(), Qt.KeepAspectRatio)
            painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            painter.setWindow(self.imageLabel.pixmap().rect())
            painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    def zoomIn(self):
        self.scaleImage(1.05)


    def zoomOut(self):
        self.scaleImage(0.95)



    def normalSize(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def about(self):
        QMessageBox.about(self, "Название программы",
                          "<p> <b>Название программы</b> </p>"
                          "<p>1</p>")

    def updateActions(self):
        self.window.zoomInAct.setEnabled(not self.window.fitToWindowAct.isChecked())
        self.window.zoomOutAct.setEnabled(not self.window.fitToWindowAct.isChecked())
        self.window.normalSizeAct.setEnabled(not self.window.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.window.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.window.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def scaling_img(self):
        print('Hello!')

    def get_img_path(self):
        return self.fileName


