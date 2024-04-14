import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

from GUIpy import result_table


class SetScale(QtWidgets.QWidget, result_table.Ui_Form_muft_list):
    def __init__(self):
        super().__init__()
        self.setupUi(self)



def main():
    app = QApplication(sys.argv)
    main_window = SetScale()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
