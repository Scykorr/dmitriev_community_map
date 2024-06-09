#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QImage, QPixmap

from GUIpy import main_new_own, set_scale
from GUIpy.get_result import Ui_FormGetResult
from GUIpy.result_table import Ui_Form_muft_list
from GUIpy.main_result import Ui_Form_main_result
from GUIpy.cabels_list import Ui_Form_list_of_cables
from show_test_img import Window
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QFileDialog, QMessageBox, QLineEdit, QWidget, QVBoxLayout, \
    QHBoxLayout, QPushButton
from PyQt5.QtWidgets import QMenu, QAction, qApp
from math import ceil, sqrt, pow

from modules import imgView

first_window_muft_params = []


class MyMainWindow(QtWidgets.QMainWindow, main_new_own.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.points_list_for_len = None
        self.scale_value = 1
        self.setupUi(self)
        # self.imageView = imgView.QImageView(window=self)
        # self.setCentralWidget(self.imageView.centralWidget)
        # self.setFixedSize(1500, 1000)
        self.createActions()
        self.scaling = 1
        self.image = None
        self.points_list = self.get_coords_from_txt()
        self.open_img()
        self.new_win = Window(self.image, self.points_list)
        self.draw_flags()
        self.lbl_1 = QLineEdit(self)
        self.lbl_1.resize(100, 20)
        self.lbl_1.move(0, 0)
        self.add_button = QPushButton("Записать")
        self.add_button.clicked.connect(self.add_button_clicked)
        self.lbl_1.setText("100 100")
        self.layout = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.lbl_1)
        self.hbox.addWidget(self.add_button)
        self.layout.addWidget(self.new_win)
        self.layout.addLayout(self.hbox)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.createMenus()
        self.setWindowTitle('Построение оптического линейного тракта')

        self.lenght = 0
        self.get_lenght()
        self.get_result_window = WindowGetResult()

    def add_button_clicked(self):
        with open("coordinates.txt", "r", encoding="utf-8") as f:
            lines = [line for line in f]
            self.points_list_for_len = self.get_coords_from_txt()
            if "" in self.points_list_for_len:
                self.points_list_for_len.remove("")
            if len(self.points_list_for_len) != 10:
                with open("coordinates.txt", "a", encoding="utf-8") as f1:
                    f1.write(f'{self.lbl_1.text()}\n')

    def mouseMoveEvent(self, event):
        pos = QCursor.pos()
        self.lbl_1.setText(f'{pos.x()} {pos.y()}')

    def get_lenght(self):
        self.input_lenght = 0
        if "" in self.points_list:
            self.points_list.remove("")
        for el_num in range(0, len(self.points_list) - 1):
            new_el = self.points_list[el_num].split()
            new_el_next = self.points_list[el_num + 1].split()
            self.input_lenght += round(sqrt(
                pow(int(new_el_next[0]) - int(new_el[0]), 2) + pow(int(new_el_next[1]) - int(new_el[1]),
                                                                   2)) / 37.936267, 2)

    def draw_flags(self):
        if len(self.points_list) >= 10:
            for el in self.points_list:
                new_el = el.split()
                self.new_win.draw_flag(int(new_el[0]), int(new_el[1]))

    def get_coords_from_txt(self):
        with open('coordinates.txt', 'r') as f:
            temp = f.read().splitlines()

        return temp
        # self.new_win.draw_flag(30, 150)

    def open_img(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                       'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if self.fileName:
            self.image = QImage(self.fileName)
            if self.image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % self.fileName)
        self.image = QPixmap(self.fileName)

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.pressPos = event.pos()
            pos = QCursor.pos()
            # self.new_win.draw_flag(pos.x(), pos.y())
            self.lbl_1.setText(f'{pos.x()} {pos.y()}')

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.imageView.scrollArea.setWidgetResizable(fitToWindow)

        if not fitToWindow:
            self.imageView.normalSize()

        self.imageView.updateActions()

    def createActions(self):
        self.openAct = QAction("&Открыть", self, shortcut="Ctrl+O", triggered=self.fitToWindow)
        self.printAct = QAction("&Печать", self, shortcut="Ctrl+P", enabled=False, triggered=self.fitToWindow)
        # self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q", triggered=image.close)
        self.zoomInAct = QAction("&Увеличить (5%)", self, shortcut="Ctrl++", enabled=False, triggered=self.fitToWindow)
        self.zoomOutAct = QAction("&Уменьшить (5%)", self, shortcut="Ctrl+-", enabled=False, triggered=self.fitToWindow)
        self.normalSizeAct = QAction("&Нормальный размер", self, shortcut="Ctrl+S", enabled=False,
                                     triggered=self.fitToWindow)
        self.fitToWindowAct = QAction("&Вместить в окно", self,
                                      enabled=False, checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)
        self.addScale = QAction("&Масштаб карты", self,
                                enabled=True, checkable=True, triggered=self.get_img_scale)
        self.aboutAct = QAction("&О программе", self, triggered=self.fitToWindow)
        self.aboutQtAct = QAction("О &Qt", self, triggered=qApp.aboutQt)
        self.figures = QAction("&Фигуры", self, triggered=self.fitToWindow)
        self.add_flag = QAction("&Добавить точку", self, triggered=self.fitToWindow)
        self.get_result = QAction("&Произвести рассчет", self, triggered=self.getResult)

    def get_img_scale(self):
        scaling_value, ok = QtWidgets.QInputDialog.getText(None, "Введите масштаб",
                                                           "Масштаб в 1 см на карте : N км",
                                                           text="10")
        if ok:
            # self.scale_value = float(scaling_value) / 37.936267
            self.scale_value = float(scaling_value) / 1
            self.lenght = round(self.input_lenght * self.scale_value, 3)

    def getResult(self):
        self.get_result_window.ui_get_result.lineEdit.setText(f'{self.lenght}')
        self.get_result_window.show()

    def createMenus(self):
        self.fileMenu = QMenu("&Файл", self)
        # self.fileMenu.addAction(self.openAct)

        # self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.printAct)

        self.fileMenu.addSeparator()
        # self.fileMenu.addAction(self.exitAct)

        self.viewMenu = QMenu("&Вид", self)
        self.viewMenu.addAction(self.addScale)
        # self.viewMenu.addAction(self.zoomInAct)
        # self.viewMenu.addAction(self.zoomOutAct)
        # self.viewMenu.addAction(self.normalSizeAct)
        # self.viewMenu.addSeparator()
        # self.viewMenu.addAction(self.fitToWindowAct)

        self.toolMenu = QMenu("&Панель инструментов", self)
        # self.toolMenu.addAction(self.add_flag)
        # self.toolMenu.addAction(self.figures)
        self.toolMenu.addAction(self.get_result)

        # self.helpMenu = QMenu("&Помощь", self)
        # self.helpMenu.addAction(self.aboutAct)
        # self.helpMenu.addAction(self.aboutQtAct)
        #
        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.viewMenu)
        self.menuBar().addMenu(self.toolMenu)
        # self.menuBar().addMenu(self.helpMenu)


class WindowGetResult(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.main_lenght = None
        self.ui_get_result = Ui_FormGetResult()
        self.ui_get_result.setupUi(self)
        self.params_muft_area = []
        self.get_hint()
        self.set_area_params()
        self.get_list_form = MuftList()
        self.ui_get_result.comboBox_5.currentTextChanged.connect(self.get_hint)
        self.ui_get_result.pushButton_get_muft_list.clicked.connect(self.show_muft_list)
        self.ui_get_result.comboBox_6.currentTextChanged.connect(self.set_area_params)
        self.ui_get_result.pushButton.clicked.connect(self.get_result)
        self.get_main_result = MainResult()
        self.cabels_list = CabelsList()
        self.ui_get_result.pushButton_get_cables_list.clicked.connect(self.get_cabels_list)
        self.lenght = None
        self.get_true_cable_lenght()
        self.ui_get_result.lineEdit.textChanged.connect(self.get_true_cable_lenght)
        self.ui_get_result.lineEdit_2.textChanged.connect(self.get_true_cable_lenght)

    def get_true_cable_lenght(self):
        if self.ui_get_result.lineEdit_2.text() == '':
            self.ui_get_result.lineEdit_2.setText('0')
        if self.ui_get_result.lineEdit.text() == '':
            self.ui_get_result.lineEdit.setText('0')
        self.ui_get_result.lineEdit_3.setText(
            f'{round(float(self.ui_get_result.lineEdit.text()) * float(self.ui_get_result.lineEdit_2.text()), 2)}')
        self.ui_get_result.lineEdit_4.setText(f'{ceil(float(self.ui_get_result.lineEdit.text()) / 6000 + 2)}')

    def get_cabels_list(self):
        self.cabels_list.show()

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

    def set_area_params(self):
        self.params_muft_area.clear()
        if self.ui_get_result.comboBox_6.currentText() == 'Под водой' or self.ui_get_result.comboBox_6.currentText() == 'Болото':
            self.ui_get_result.lineEdit_5.setText('Муфта чугунная защитная (МЧЗ)')
            self.ui_get_result.lineEdit_7.setText('23')
            self.ui_get_result.lineEdit_8.setText('4882.0')
            self.ui_get_result.lineEdit_9.setText('130104-00034')
            self.params_muft_area.append('Муфта чугунная защитная (МЧЗ)')
            self.params_muft_area.append(23)
            self.params_muft_area.append(4882.0)
            self.params_muft_area.append('130104-00034')
        elif self.ui_get_result.comboBox_6.currentText() == 'Прочие грунты':
            self.ui_get_result.lineEdit_5.setText('Муфта пластмассовая защитная (МПЗ)')
            self.ui_get_result.lineEdit_7.setText('2.3')
            self.ui_get_result.lineEdit_8.setText('2014.28')
            self.ui_get_result.lineEdit_9.setText('130104-00015')
            self.params_muft_area.append('Муфта пластмассовая защитная (МПЗ)')
            self.params_muft_area.append(2.3)
            self.params_muft_area.append(2014.28)
            self.params_muft_area.append('130104-00015')

    def get_result(self):
        self.main_lenght = float(self.ui_get_result.lineEdit.text())

        muft_weight = round(float(self.ui_get_result.lineEdit_4.text()) * 3.2, 2)
        muft_price = 6177
        muft_common_price = round(int(self.ui_get_result.lineEdit_4.text()) * muft_price, 2)

        guard_muft_weight = round(
            float(self.ui_get_result.lineEdit_4.text()) * float(self.ui_get_result.lineEdit_7.text()), 2)
        guard_muft_price = float(self.ui_get_result.lineEdit_8.text())
        guard_muft_price_common = round(int(self.ui_get_result.lineEdit_4.text()) * guard_muft_price, 2)

        cable_weight = round(float(self.ui_get_result.lineEdit_3.text()) * 228.3, 2)
        cable_price = 59.975
        cable_price_common = round(cable_price * 1000 * float(self.ui_get_result.lineEdit_3.text()), 2)

        marker_weight = 1
        marker_price = 948
        marker_price_common = 948

        germetic_wheight = 1.6
        germetic_price = 1100
        germetic_price_common = 1100

        column_amount = ceil(self.main_lenght / 0.2)
        column_weight = column_amount * 2
        column_price = 387.29
        column_price_common = column_amount * column_price

        sign_amount = column_amount
        sign_weight = sign_amount * 0.6
        sign_price = 406.87
        sign_price_common = sign_price * sign_amount

        ankers_amount = column_amount
        ankers_weight = ankers_amount * 0.2
        ankers_price = 33.59
        ankers_price_common = ankers_amount * ankers_price

        tapes_amount = ceil(self.main_lenght / 0.5)
        tapes_weight = tapes_amount * 3.68
        tapes_price = 999.1
        tapes_price_common = tapes_price * tapes_amount

        common_price = muft_common_price + guard_muft_price_common + cable_price_common + marker_price_common + germetic_price_common + column_price_common + sign_price_common + ankers_price_common + tapes_price_common
        common_weight = muft_weight + guard_muft_weight + cable_weight + marker_weight + germetic_wheight + column_weight + sign_weight + ankers_weight + tapes_weight

        self.get_main_result.ui_get_main_result.tableWidget.setItem(0, 1, QTableWidgetItem('Муфта'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(0, 2, QTableWidgetItem('МТОК-А1/216-1KT3645-K-77'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(0, 3, QTableWidgetItem('130103-00071'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(0, 4, QTableWidgetItem('ООО «Связьстройдеталь»'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(0, 5, QTableWidgetItem('шт.'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(0, 6, QTableWidgetItem(
            self.ui_get_result.lineEdit_4.text()))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(0, 7, QTableWidgetItem(
            f'{muft_weight}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(0, 8, QTableWidgetItem(f'{muft_price}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(0, 9, QTableWidgetItem(f'{muft_common_price}'))

        self.get_main_result.ui_get_main_result.tableWidget.setItem(1, 1, QTableWidgetItem('Муфта защитная'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(1, 2, QTableWidgetItem(
            f'{self.ui_get_result.lineEdit_5.text()}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(1, 3, QTableWidgetItem(
            f'{self.ui_get_result.lineEdit_9.text()}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(1, 4, QTableWidgetItem('ООО «Связьстройдеталь»'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(1, 5, QTableWidgetItem('шт.'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(1, 6, QTableWidgetItem(
            self.ui_get_result.lineEdit_4.text()))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(1, 7, QTableWidgetItem(
            f'{guard_muft_weight}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(1, 8, QTableWidgetItem(f'{guard_muft_price}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(1, 9,
                                                                    QTableWidgetItem(f'{guard_muft_price_common}'))

        self.get_main_result.ui_get_main_result.tableWidget.setItem(2, 1, QTableWidgetItem('Кабель'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(2, 2,
                                                                    QTableWidgetItem('ВО ДПС – П– 16А (4х4) – 7 кН'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(2, 3, QTableWidgetItem('130905-00179'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(2, 4, QTableWidgetItem('ООО «ОптикТорг»'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(2, 5, QTableWidgetItem('м'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(2, 6, QTableWidgetItem(
            f'{float(self.ui_get_result.lineEdit_3.text()) * 1000}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(2, 7, QTableWidgetItem(
            f'{cable_weight}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(2, 8, QTableWidgetItem(f'{cable_price}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(2, 9,
                                                                    QTableWidgetItem(f'{cable_price_common}'))

        self.get_main_result.ui_get_main_result.tableWidget.setItem(3, 1, QTableWidgetItem('Маркер Scotchmark'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(3, 2, QTableWidgetItem('1401-XR'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(3, 3, QTableWidgetItem('130104-00041'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(3, 4, QTableWidgetItem('ООО «Связьстройдеталь»'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(3, 5, QTableWidgetItem('шт.'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(3, 6, QTableWidgetItem('1'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(3, 7, QTableWidgetItem(f'{marker_weight}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(3, 8, QTableWidgetItem(f'{marker_price}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(3, 9,
                                                                    QTableWidgetItem(f'{marker_price_common}'))

        self.get_main_result.ui_get_main_result.tableWidget.setItem(4, 1, QTableWidgetItem(
            'Герметик для крепления МЗ с базовой муфтой'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(4, 2, QTableWidgetItem('КтГМЗ'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(4, 3, QTableWidgetItem('130104-00006'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(4, 4, QTableWidgetItem('ООО «Связьстройдеталь»'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(4, 5, QTableWidgetItem('шт.'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(4, 6, QTableWidgetItem('1'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(4, 7, QTableWidgetItem(f'{germetic_wheight}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(4, 8, QTableWidgetItem(f'{germetic_price}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(4, 9,
                                                                    QTableWidgetItem(f'{germetic_price_common}'))

        self.get_main_result.ui_get_main_result.tableWidget.setItem(5, 1, QTableWidgetItem(
            'Столбик опознавательный для подземных кабельных линий связи 2,5 м'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(5, 2, QTableWidgetItem('СОС'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(5, 3, QTableWidgetItem('110501-00005'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(5, 4, QTableWidgetItem('ЗАО «Связьстройдеталь»'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(5, 5, QTableWidgetItem('шт.'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(5, 6,
                                                                    QTableWidgetItem(f'{column_amount}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(5, 7, QTableWidgetItem(f'{column_weight}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(5, 8, QTableWidgetItem(f'{column_price}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(5, 9,
                                                                    QTableWidgetItem(f'{column_price_common}'))

        self.get_main_result.ui_get_main_result.tableWidget.setItem(6, 1, QTableWidgetItem(
            'Табличка металлическая односторонняя'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(6, 2, QTableWidgetItem('300х400х0,8'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(6, 3, QTableWidgetItem('110501-00009'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(6, 4, QTableWidgetItem('ЗАО «Связьстройдеталь»'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(6, 5, QTableWidgetItem('шт.'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(6, 6,
                                                                    QTableWidgetItem(f'{sign_amount}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(6, 7, QTableWidgetItem(f'{sign_weight}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(6, 8, QTableWidgetItem(f'{sign_price}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(6, 9,
                                                                    QTableWidgetItem(f'{sign_price_common}'))

        self.get_main_result.ui_get_main_result.tableWidget.setItem(7, 1, QTableWidgetItem(
            'Анкерное крепление для опознавательных столбов'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(7, 2, QTableWidgetItem('АК'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(7, 3, QTableWidgetItem('110712-00169'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(7, 4, QTableWidgetItem('ЗАО «Связьстройдеталь»'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(7, 5, QTableWidgetItem('шт.'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(7, 6,
                                                                    QTableWidgetItem(f'{ankers_amount}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(7, 7, QTableWidgetItem(f'{ankers_weight}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(7, 8, QTableWidgetItem(f'{ankers_price}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(7, 9,
                                                                    QTableWidgetItem(f'{ankers_price_common}'))

        self.get_main_result.ui_get_main_result.tableWidget.setItem(8, 1, QTableWidgetItem(
            'Лента сигнальная 70мм*500м *100мкм'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(8, 2, QTableWidgetItem('ЛСО-70'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(8, 3, QTableWidgetItem('120808-00022'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(8, 4, QTableWidgetItem('ЗАО «Связьстройдеталь»'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(8, 5, QTableWidgetItem('шт.'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(8, 6,
                                                                    QTableWidgetItem(f'{tapes_amount}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(8, 7, QTableWidgetItem(f'{tapes_weight}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(8, 8, QTableWidgetItem(f'{tapes_price}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(8, 9,
                                                                    QTableWidgetItem(f'{tapes_price_common}'))

        self.get_main_result.ui_get_main_result.tableWidget.setItem(9, 7,
                                                                    QTableWidgetItem(f'{round(common_weight, 3)}'))
        self.get_main_result.ui_get_main_result.tableWidget.setItem(9, 9, QTableWidgetItem(f'{round(common_price, 3)}'))

        self.get_main_result.show()


class MuftList(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_get_list = Ui_Form_muft_list()
        self.ui_get_list.setupUi(self)


class MainResult(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_get_main_result = Ui_Form_main_result()
        self.ui_get_main_result.setupUi(self)


class CabelsList(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui_get_cabels_list = Ui_Form_list_of_cables()
        self.ui_get_cabels_list.setupUi(self)


def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
