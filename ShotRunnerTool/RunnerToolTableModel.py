__author__ = 'Jeff'

from PyQt4 import QtGui, QtCore
import JsonUtils

class RunnerToolTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.data = [{'1': 'one'}, {'2': 'two'}, {'3': 'three'},]

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.data)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 2

    def data(self, index, role=None):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            key = self.data[row].keys()
            data = self.data[row][key[0]]
            if column == 0:
                return key[0]
            if column == 1:
                return data

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role=None):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.EditRole:
            keyAsList = self.data[row].keys()
            key = keyAsList[0]
            if column == 0: #editting the KEYS for the json file
                tempData = self.data[row][key]
                self.data[row][value] = tempData
                del self.data[row][key]
            elif column == 1: #editting the DATA for the json file
                self.data[row][key] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertRows(QtCore.QModelIndex(), 0, rows + self.numberOfRows)
        for i in range(rows):
            pass
        self.endInsertRows()
        return True

    def addRow(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.endInsertRows()
        return True

    def saveDataToFileByPath(self, fileName):
        JsonUtils.JsonUtils.saveJsonFileByPath(fileName, self.data)

    def openDataByPath(self, fileName):
        self.data = JsonUtils.JsonUtils.getDataFromJsonFile(fileName)

if __name__ == '__main__':
    app = QtGui.QApplication([])

    table_view = QtGui.QTableView()
    table_model = RunnerToolTableModel()

    table_model.openDataByPath('test.json')

    table_view.setModel(table_model)
    table_view.show()

    app.exec_()
