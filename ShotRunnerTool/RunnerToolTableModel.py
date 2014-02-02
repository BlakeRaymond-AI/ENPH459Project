__author__ = 'Jeff'

from PyQt4 import QtGui, QtCore

class RunnerToolTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.testData = [{'1': 'one'}, {'2': 'two'}, {'3': 'three'},]

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.testData)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 2

    def data(self, index, role=None):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            key = self.testData[row].keys()
            data = self.testData[row][key[0]]
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
            keyAsList = self.testData[row].keys()
            key = keyAsList[0]
            if column == 0: #editting the KEYS for the json file
                tempData = self.testData[row][key]
                self.testData[row][value] = tempData
                del self.testData[row][key]
            elif column == 1: #editting the DATA for the json file
                self.testData[row][key] = value
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


if __name__ == '__main__':
    app = QtGui.QApplication([])

    table_view = QtGui.QTableView()
    table_model = RunnerToolTableModel()

    table_view.setModel(RunnerToolTableModel())
    table_view.show()

    app.exec_()
