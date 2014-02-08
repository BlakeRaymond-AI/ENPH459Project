__author__ = 'Jeff'

from PyQt4 import QtGui, QtCore
import JsonUtils
import os

#TODOS:

#fix the dialogbox. Right now it opens AFTER enter has been pressed. It should open on select.
    #might need to modify: the role (editrole) or maybe can't even edit it in setData, might need a new function (select data?)

#gold plating: enable dragging and dropping files for inputting in filenames
#restructure the json files: have different keys: i.e. scriptFile (just the name, for displaying to the user), fullScriptPath (fullname w/path)
    #dataFile, fullDataFilePath (same logic as the script datas)
    # --this wasn't done before because I didn't think that there was a need. There is because the path names are too long


class RunnerToolTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self)
        self.data = [{'': ''}]        #store an empty list for the data until it is loaded from the json file

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
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable #|QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled

    def setData(self, index, value, role=None):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.EditRole:
            keyAsList = self.data[row].keys()
            key = keyAsList[0]
            if column == 0:    #editting the KEYS for the json file
                value = str(self.getFilenameFromDialogBox('*.py'))
                tempData = self.data[row][key]
                self.data[row][value] = tempData
                del self.data[row][key]
            elif column == 1: #editting the DATA for the json file
                value = str(self.getFilenameFromDialogBox('*.json'))
                self.data[row][key] = value
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertRows(QtCore.QModelIndex(), 0, rows + self.numberOfRows)
        self.endInsertRows()
        return True

    def addRow(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.endInsertRows()
        return True

    def removeRowByName(self, name):
        try:
            if name in self.data:
                self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
                #del self.data[name] #this part not completed yet
                self.endRemoveRows()
        except:
            raise KeyError('Cannot find key \'%s\' in device group' % name)

    def removeRows(self, position, rows, parent = None, *args, **kwargs):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
        self.endRemoveRows()

    def saveDataToFileByPath(self, fileName):
        JsonUtils.JsonUtils.saveJsonFileByPath(fileName, self.data)

    def openDataByPath(self, fileName):
        self.data = JsonUtils.JsonUtils.getDataFromJsonFile(fileName)

    def getFilenameFromDialogBox(self, fileSuffixFilter=None):
        fileDialog = QtGui.QFileDialog()
        if fileSuffixFilter == None:
            dialogReturn = fileDialog.getOpenFileName(directory=str(os.getcwd()), filter='*.*')
        else:
            dialogReturn = fileDialog.getOpenFileName(directory=str(os.getcwd()), filter=fileSuffixFilter)
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        return dialogReturn

if __name__ == '__main__':
    app = QtGui.QApplication([])

    table_view = QtGui.QTableView()
    table_model = RunnerToolTableModel()
    table_view.setModel(table_model)
    table_view.show()

    table_model.openDataByPath('test.json')

    app.exec_()
