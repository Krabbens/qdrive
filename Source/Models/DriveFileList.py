from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt, pyqtSlot


class DriveFileList(QAbstractListModel):
    col1 = QtCore.Qt.UserRole + 1
    col2 = QtCore.Qt.UserRole + 2
    col3 = QtCore.Qt.UserRole + 3
    col4 = QtCore.Qt.UserRole + 4
    col5 = QtCore.Qt.UserRole + 5
    col6 = QtCore.Qt.UserRole + 6
    col7 = QtCore.Qt.UserRole + 7
    col8 = QtCore.Qt.UserRole + 8

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = []

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()
        if index.isValid() and 0 <= row < self.rowCount():
            if role == DriveFileList.col1:
                return self.items[row]["name"]
            if role == DriveFileList.col2:
                return self.items[row]["type"]
            if role == DriveFileList.col3:
                return self.items[row]["id"]
            if role == DriveFileList.col4:
                return self.items[row]["parentId"]
            if role == DriveFileList.col5:
                return self.items[row]["size"]
            if role == DriveFileList.col6:
                return self.items[row]["icon"]
            if role == DriveFileList.col7:
                return self.items[row]["date"]
            if role == DriveFileList.col8:
                return self.items[row]["parts"]

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.items)

    def roleNames(self):
        return {
            DriveFileList.col1: b"name",
            DriveFileList.col2: b"type",
            DriveFileList.col3: b"id",
            DriveFileList.col4: b"parentId",
            DriveFileList.col5: b"size",
            DriveFileList.col6: b"icon",
            DriveFileList.col7: b"date",
            DriveFileList.col8: b"parts",
        }

    @pyqtSlot(int, result="QVariant")
    def get(self, row):
        if 0 <= row < self.rowCount():
            return self.items[row]

    def add_items(self, items):
        self.beginResetModel()
        for i in items:
            self.items.append(i)
        self.endResetModel()

    def clear_items(self):
        self.beginResetModel()
        self.items = []
        self.endResetModel()
