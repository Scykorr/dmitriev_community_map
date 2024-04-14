#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from GUIpy import main_new_own, set_scale
from GUIpy.get_result import Ui_FormGetResult
from GUIpy.result_table import Ui_Form_muft_list
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMenu, QAction, qApp

from modules import imgView

first_window_muft_params = []
params_muft_after_click = []

class MyMainWindow(QtWidgets.QMainWindow, main_new_own.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.imageView = imgView.QImageView(window=self)
        self.setCentralWidget(self.imageView.centralWidget)
        self.createActions(self.imageView)
        self.createMenus()
        self.setWindowTitle('Построение оптического линейного тракта')
        self.get_result_window = WindowGetResult()

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
        self.get_result = QAction("&Произвести рассчет", self, triggered=self.getResult)
        self.scaling = QAction("&Масштабирование", self, enabled=False, triggered=view.scaling_img)

    def getResult(self):
        self.get_result_window.show()

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


class WindowGetResult(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_get_result = Ui_FormGetResult()
        self.ui_get_result.setupUi(self)
        self.get_hint()
        self.get_list_form = MuftList()
        self.ui_get_result.comboBox_5.currentTextChanged.connect(self.get_hint)
        self.ui_get_result.pushButton_get_muft_list.clicked.connect(self.show_muft_list)

    def get_hint(self):
        if self.ui_get_result.comboBox_5.currentText() == 'МТОК-А1/216-1KT3645-K-77':
            self.ui_get_result.comboBox_5.setToolTip('Усиленная муфта, отличающаяся высочайшей надежностью.')
        elif self.ui_get_result.comboBox_5.currentText() == 'МТОК-Б1/216-1KT3645-K-44':
            self.ui_get_result.comboBox_5.setToolTip('Муфта с транзитной петлёй.')
        elif self.ui_get_result.comboBox_5.currentText() == 'МТОК-В2/216-1KT3645-K-44':
            self.ui_get_result.comboBox_5.setToolTip('Муфта с транзитной петлёй. Механическая герметизация корпуса.')
        elif self.ui_get_result.comboBox_5.currentText() == 'МТОК-М6/144-1KT3645-K-44':
            self.ui_get_result.comboBox_5.setToolTip(
                'Бюджетный вариант – минимальная цена. Малогабаритная муфта. Механическая герметизация корпуса.')

    def show_muft_list(self):
        self.get_list_form.show()


class MuftList(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_get_list = Ui_Form_muft_list()
        self.ui_get_list.setupUi(self)

def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
