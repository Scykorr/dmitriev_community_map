#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from GUIpy import main_new_own, set_scale
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu, QAction, qApp

from modules import imgView






class MyMainWindow(QtWidgets.QMainWindow, main_new_own.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.imageView = imgView.QImageView(window=self)
        self.setCentralWidget(self.imageView.centralWidget)
        self.createActions(self.imageView)
        self.createMenus()
        self.setWindowTitle('Построение оптического линейного тракта')

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.imageView.scrollArea.setWidgetResizable(fitToWindow)

        if not fitToWindow:
            self.imageView.normalSize()

        self.imageView.updateActions()

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
        self.addScale = QAction("&Масштаб карты", self,
                                enabled=True, checkable=True, shortcut="Ctrl+Q", triggered=self.fitToWindow)
        self.aboutAct = QAction("&О программе", self, triggered=view.about)
        self.aboutQtAct = QAction("О &Qt", self, triggered=qApp.aboutQt)
        self.figures = QAction("&Фигуры", self, triggered=view.paintEvent)
        self.add_flag = QAction("&Добавить точку", self, triggered=view.paintEvent)
        self.get_result = QAction("&Произвести рассчет", self, triggered=view.paintEvent)
        self.scaling = QAction("&Масштабирование", self, enabled=False, triggered=view.scaling_img)




    def createMenus(self):
        self.fileMenu = QMenu("&Файл", self)
        self.fileMenu.addAction(self.openAct)

        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAct)

        self.fileMenu.addSeparator()
        # self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&Вид", self)
        self.viewMenu.addAction(self.addScale)
        self.viewMenu.addAction(self.zoomInAct)
        self.viewMenu.addAction(self.zoomOutAct)
        self.viewMenu.addAction(self.normalSizeAct)
        self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.fitToWindowAct)

        self.toolMenu = QMenu("&Панель инструментов", self)
        self.toolMenu.addAction(self.add_flag)
        self.toolMenu.addAction(self.figures)
        self.toolMenu.addAction(self.scaling)
        self.toolMenu.addAction(self.get_result)


        self.helpMenu = QMenu("&Помощь", self)
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.toolMenu)
        self.menuBar().addMenu(self.helpMenu)


def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
