#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QPixmap, QPainter, QImage, QColor, QPalette
from PyQt5.QtPrintSupport import QPrinter

from GUIpy import main_new_own
from PyQt5.QtWidgets import QApplication, QMessageBox, QFileDialog, QLabel, QSizePolicy, QScrollArea, QWidget, \
    QHBoxLayout
from PyQt5.QtWidgets import QMenu, QAction, qApp

from modules import imgView


class MyMainWindow(QtWidgets.QMainWindow, main_new_own.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.fileName = None
        self.image_height = None
        self.image_width = None
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
        self.createActions()
        self.createMenus()

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.imageView.scrollArea.setWidgetResizable(fitToWindow)

        if not fitToWindow:
            self.imageView.normalSize()

        self.imageView.updateActions()

    def createActions(self):
        self.openAct = QAction("&Открыть", self, shortcut="Ctrl+O", triggered=self.open_img)
        self.printAct = QAction("&Печать", self, shortcut="Ctrl+P", enabled=False, triggered=self.pass_func)
        # self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=image.close)
        self.zoomInAct = QAction("&Увеличить (5%)", self, shortcut="Ctrl++", enabled=False, triggered=self.pass_func)
        self.zoomOutAct = QAction("&Уменьшить (5%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.pass_func)
        self.normalSizeAct = QAction("&Нормальный размер", self, shortcut="Ctrl+S", enabled=False,
                                     triggered=self.pass_func)
        self.fitToWindowAct = QAction("&Вместить в окно", self,
                                      enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.pass_func)
        self.aboutAct = QAction("&О программе", self, triggered=self.pass_func)
        self.aboutQtAct = QAction("О &Qt", self, triggered=qApp.aboutQt)
        self.figures = QAction("&Фигуры", self, triggered=self.pass_func)
        self.scaling = QAction("&Масштабирование", self, enabled=False, triggered=self.pass_func)

    def pass_func(self):
        pass

    def open_img(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        self.fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if self.fileName:
            self.image = QImage(self.fileName)
            if self.image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % self.fileName)
                return

            self.imageLabel.setPixmap(QPixmap.fromImage(self.image))
            self.scaleFactor = 1.0

            self.scrollArea.setVisible(True)
            self.printAct.setEnabled(True)
            self.fitToWindowAct.setEnabled(True)
            self.updateActions()

            if not self.fitToWindowAct.isChecked():
                self.imageLabel.adjustSize()


    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     pixmap = QPixmap("test.bmp")
    #     painter.drawPixmap(self.rect(), pixmap)
    #     pen = QPen(QColor("red"))
    #     pen.setWidth(10)
    #     painter.setPen(pen)
    #     painter.drawLine(0, 0, 1000, 1000)

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

        self.toolMenu = QMenu("&Панель инструментов", self)
        self.toolMenu.addAction(self.figures)
        self.toolMenu.addAction(self.scaling)

        self.helpMenu = QMenu("&Помощь", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.toolMenu)
        self.menuBar().addMenu(self.helpMenu)

    def get_img_path(self):
        return self.fileName

    def updateActions(self):
        self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def zoomIn(self):
        self.scaleImage(1.05)

    def zoomOut(self):
        self.scaleImage(0.95)

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

        self.zoomInAct.setEnabled(self.scaleFactor < 3.0)
        self.zoomOutAct.setEnabled(self.scaleFactor > 0.333)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))


    def wheelEvent(self, event) -> None:
        wheel_val = event.angleDelta().y()
        if wheel_val > 0:
            self.zoomIn()
        elif wheel_val < 0:
            self.zoomOut()


def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
