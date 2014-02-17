__author__ = 'Jeff'

from PyQt4 import QtGui, QtCore
import JsonUtils
import os

#TODOS:

#fix the dialogbox. Right now it opens AFTER enter has been pressed. It should open on select.
    #might need to modify: the role (editrole) or maybe can't even edit it in setData, might need a new function (select data?)

class RunnerToolTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractListModel.__init__(self, None)
        self.fileData = [{'scriptFileName': '', 'scriptFilePath' : '',
                      'settingsFileName' : '', 'settingsFilePath' : ''}] #store an empty list for the data until it is loaded from the json file

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.fileData)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 2

    def data(self, index, role=None):
        row = index.row()
        column = index.column()
        debuggingData = self.fileData #easier to view with the debugger
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if column == 0:
                return self.fileData[row]['scriptFileName']
            if column == 1:
                return self.fileData[row]['settingsFileName']
        if role == 'removeRowRoll' :
            return row
        if role == QtCore.Qt.EditRole:
            print "editing"

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable #|QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled

    def setData(self, index, value, role=None):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.EditRole:
            if column == 0:    #editing the script file name
                value = str(self.getFilenameFromDialogBox('*.py'))
                self.fileData[row]['scriptFilePath'] = value
                self.fileData[row]['scriptFileName'] = self.__parseFilenameFromDialogBox(value)
            elif column == 1: #editing the settings file name (should be h5 files)
                value = str(self.getFilenameFromDialogBox('*.h5'))
                self.fileData[row]['settingsFilePath'] = value
                self.fileData[row]['settingsFileName'] = self.__parseFilenameFromDialogBox(value)
            self.dataChanged.emit(index, index)
            return True
        return False

    def insertRows(self, position, rows, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertRows(QtCore.QModelIndex(), 0, rows + self.numberOfRows)
        self.endInsertRows()
        return True

    def addRow(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.fileData.append({'scriptFileName': '', 'scriptFilePath' : '',
                      'settingsFileName' : '', 'settingsFilePath' : ''})
        self.endInsertRows()
        return True

    def removeRowByRowNumber(self, row):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
        self.fileData.pop(row)
        self.endRemoveRows()

    def removeRows(self, position, rows, parent = None, *args, **kwargs):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
        self.endRemoveRows()

    def saveDataToFileByPath(self, fileName):
        JsonUtils.JsonUtils.saveJsonFileByPath(fileName, self.fileData)

    def openDataByPath(self, fileName):
        tempData = JsonUtils.JsonUtils.getDataFromJsonFile(fileName)
        if not self.__validateFileData(fileName, tempData):
            return
        else:
            self.beginResetModel()
            self.fileData = tempData
            self.endResetModel()
            return

    def __validateFileData(self, fileName, tempData):
        for data in tempData:
            if ( not('settingsFileName' in data.keys()) or not('scriptFilePath' in data.keys()) or not('scriptFileName' in data.keys())
                 or not('settingsFilePath' in data.keys())):
                raise Exception, "The file \"%s\" is either corrupt or in the wrong format" %(fileName)
            return True


    def getFilenameFromDialogBox(self, fileSuffixFilter=None):
        fileDialog = QtGui.QFileDialog()
        if fileSuffixFilter == None:
            dialogReturn = fileDialog.getOpenFileName(directory=str(os.getcwd()), filter='*.*')
        else:
            dialogReturn = fileDialog.getOpenFileName(directory=str(os.getcwd()), filter=fileSuffixFilter)
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        return dialogReturn

    def __parseFilenameFromDialogBox(self, value):
        return os.path.basename(value)

    def close(self):
        self.beginResetModel()
        self.fileData = [{'scriptFileName': '', 'scriptFilePath' : '',
                      'settingsFileName' : '', 'settingsFilePath' : ''}]
        self.endResetModel()

if __name__ == '__main__':
    app = QtGui.QApplication([])

    table_view = QtGui.QTableView()
    table_model = RunnerToolTableModel()
    table_view.setModel(table_model)
    table_view.show()

    app.exec_()
    table_model.saveDataToFileByPath('debugging.json')
