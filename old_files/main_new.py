#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QPainter
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from PyQt5.QtWidgets import QLabel, QSizePolicy, QScrollArea, QMessageBox, QMainWindow, QMenu, QAction, \
    qApp, QFileDialog, QWidget, QHBoxLayout


class QImageViewSync(QWidget):
    def __init__(self, window=None):
        super().__init__()

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

    def mousePressEvent(self, event):
        self.pressed = True
        self.imageLabel.setCursor(Qt.ClosedHandCursor)
        self.initialPosX = self.scrollArea.horizontalScrollBar().value() + event.pos().x()
        self.initialPosY = self.scrollArea.verticalScrollBar().value() + event.pos().y()

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

    def open(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            print(fileName)
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))

            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.window.printAct.setEnabled(True)
            self.window.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.window.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()

    def open_img(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            print(fileName)
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(image))
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.window.printAct.setEnabled(True)
            self.window.fitToWindowAct.setEnabled(True)
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.imageViewSync = QImageViewSync(window=self)
        self.setCentralWidget(self.imageViewSync.centralWidget)

        self.createActions(self.imageViewSync)
        self.createMenus()

        self.setWindowTitle("Название программы")
        self.resize(1200, 600)



    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.imageViewSync.scrollArea.setWidgetResizable(fitToWindow)

        if not fitToWindow:
            self.imageViewSync.normalSize()

        self.imageViewSync.updateActions()

    def createActions(self, view):
        self.openAct = QAction("&Открыть", self, shortcut="Ctrl+O", triggered=view.open_img)
        self.printAct = QAction("&Печать", self, shortcut="Ctrl+P", enabled=False, triggered=view.print_img)
        # self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=image.close)
        self.zoomInAct = QAction("&Увеличить (5%)", self, shortcut="Ctrl++", enabled=False, triggered=view.zoomIn)
        self.zoomOutAct = QAction("&Уменьшить (5%)", self, shortcut="Ctrl+-", enabled=False, triggered=view.zoomOut)
        self.normalSizeAct = QAction("&Нормальный размер", self, shortcut="Ctrl+S", enabled=False,
                                     triggered=view.normalSize)
        self.fitToWindowAct = QAction("&Вместить в окно", self,
                                      enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
        self.aboutAct = QAction("&О программе", self, triggered=view.about)
        self.aboutQtAct = QAction("О &Qt", self, triggered=qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = QMenu("&Файл", self)
        self.fileMenu.addAction(self.openAct)

        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAct)

        self.fileMenu.addSeparator()
        # self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&Вид", self)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.helpMenu = QMenu("&Помощь", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.helpMenu)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
