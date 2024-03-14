from PyQt5 import QtWidgets, QtCore, QtQuickWidgets, QtPositioning
from PyQt5.QtWidgets import QApplication, QWidget
import uf
import sys, os


class MarkerModel(QtCore.QAbstractListModel):
    PositionRole, SourceRole = range(QtCore.Qt.UserRole, QtCore.Qt.UserRole + 2)

    def __init__(self, parent=None):
        super(MarkerModel, self).__init__(parent)
        self._markers = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._markers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount():
            if role == MarkerModel.PositionRole:
                return self._markers[index.row()]["position"]
            elif role == MarkerModel.SourceRole:
                return self._markers[index.row()]["source"]
        return QtCore.QVariant()

    def roleNames(self):
        return {MarkerModel.PositionRole: b"position_marker", MarkerModel.SourceRole: b"source_marker"}

    def appendMarker(self, marker):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()


class MapWidget(QtQuickWidgets.QQuickWidget):
    def __init__(self, parent=None):
        super(MapWidget, self).__init__(parent,
                                        resizeMode=QtQuickWidgets.QQuickWidget.SizeRootObjectToView)
        self.model = MarkerModel(self)
        self.rootContext().setContextProperty("markermodel", self.model)
        qml_path = os.path.join(os.path.dirname(__file__), "Untitled-1.qml")
        self.setSource(QtCore.QUrl.fromLocalFile(qml_path))

    def place_marks(self, positions):
        urls = ["http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_gray.png",
                "http://maps.gstatic.com/mapfiles/ridefinder-images/mm_20_red.png"]
        for c, u in zip(positions, urls):
            coord = QtPositioning.QGeoCoordinate(*c)
            source = QtCore.QUrl(u)
            self.model.appendMarker({"position": coord, "source": source})


class Window(QtQuickWidgets.QQuickWidget):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = uf.Ui_Form()
        self.ui.setupUi(self)
        self.a = MapWidget()
        self.ui.gridLayout.addWidget(self.a)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())