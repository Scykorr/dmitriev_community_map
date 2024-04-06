from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import sys
from socket import *
import json
from GUIpy.main_form import Ui_MainWindow
from random import shuffle
import time
import sqlite3 as sql


class MyMainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.view_img_map()
        # self.ui_main_window.pushButton.clicked.connect(self.attachImage)
        self.attach_image()
        self.ui.open_action.triggered.connect(self.open_new_file)


    def open_new_file(self):
        options = QFileDialog.Options()
        # fileName = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                  'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
        if fileName:
            print(fileName)
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Ошибка!", "Невозможно загрузить %s." % fileName)
                return

            lay = QtWidgets.QVBoxLayout(self.ui.scrollAreaWidgetContents)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.addWidget(self.ui.map_jpg)
            path = fileName
            pix_map = QtGui.QPixmap(path)
            # pix_map.scroll(10, 10, pixmap.rect(), exposed)
            self.ui.map_jpg.setPixmap(pix_map)
            self.ui.map_jpg.setScaledContents(True)
            self.ui.scrollArea.setWidgetResizable(True)
            self.ui.map_jpg.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


    def view_img_map(self):
        pixmap = QPixmap('maps/карта-7920-4320.bmp')
        self.ui.map_jpg.setPixmap(pixmap)

    def attach_image(self):
        # qdialog
        lay = QtWidgets.QVBoxLayout(self.ui.scrollAreaWidgetContents)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(self.ui.map_jpg)
        path = "maps/карта-7920-4320.bmp"
        pix_map = QtGui.QPixmap(path)
        # pix_map.scroll(10, 10, pixmap.rect(), exposed)
        self.ui.map_jpg.setPixmap(pix_map)
        self.ui.map_jpg.setScaledContents(True)
        self.ui.scrollArea.setWidgetResizable(True)
        self.ui.map_jpg.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)


def main():
    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
