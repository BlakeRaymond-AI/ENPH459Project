__author__ = 'Jeff'

import os

from PyQt4 import QtGui, QtCore

import JsonUtils


EMPTY_ROW_KEY = '<Click to add row>'

SCRIPT_FILE_KEY = 'scriptFileName'
SCRIPT_PATH_KEY = 'scriptFilePath'
SETTINGS_FILE_KEY = 'settingsFileName'
SETTINGS_PATH_KEY = 'settingsFilePath'

SCRIPT_FILE_EXTENSION = '*.py'
SETTINGS_FILE_EXTENSION = '*.h5'

DEFAULT_ENTRY = {SCRIPT_FILE_KEY: EMPTY_ROW_KEY, SCRIPT_PATH_KEY: '',
                 SETTINGS_FILE_KEY: '',
                 SETTINGS_PATH_KEY: ''}  #store an empty list for the data until it is loaded from the json file


class ShotRunnerToolTableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent=None):
        QtCore.QAbstractTableModel.__init__(self, None)
        self.fileData = []
        self.fileData.append(dict(DEFAULT_ENTRY))
        self.headerLabels = ['Script Files', 'Settings Files']
        self.workAroundQtBugFlag = False

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.fileData)

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 2

    def data(self, index, role=None):
        row = index.row()
        column = index.column()
        if role == QtCore.Qt.EditRole:
            if self.workAroundQtBugFlag:
                self.getShotFilesFromUser(index)
            self.workAroundQtBugFlag = not (
            self.workAroundQtBugFlag)  #Qt has a weird bug were it will call data with the edit role twice. This is a work around for that bug
            if column == 0:
                return self.fileData[row][SCRIPT_FILE_KEY]
            if column == 1:
                return self.fileData[row][SETTINGS_FILE_KEY]
        if role == QtCore.Qt.DisplayRole:
            if column == 0:
                return self.fileData[row][SCRIPT_FILE_KEY]
            if column == 1:
                return self.fileData[row][SETTINGS_FILE_KEY]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    def getShotFilesFromUser(self, index):
        row = index.row()
        column = index.column()
        if column == 0:  #editing the script file name
            addNewRow = False
            if self.fileData[row][SCRIPT_FILE_KEY] == EMPTY_ROW_KEY: addNewRow = True
            value = str(self.getFilenameFromDialogBox(SCRIPT_FILE_EXTENSION))
            if value:  #if the value is not None, False or an empty string
                self.fileData[row][SCRIPT_PATH_KEY] = value
                self.fileData[row][SCRIPT_FILE_KEY] = self.__parseFilenameFromDialogBox(value)
                if addNewRow: self.addRow()
        elif column == 1:  #editing the settings file name (should be h5 files)
            value = str(self.getFilenameFromDialogBox(SETTINGS_FILE_EXTENSION))
            if value:
                self.fileData[row][SETTINGS_PATH_KEY] = value
                self.fileData[row][SETTINGS_FILE_KEY] = self.__parseFilenameFromDialogBox(value)
        self.dataChanged.emit(index, index)
        return

    def addRow(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        self.fileData.append(dict(DEFAULT_ENTRY))
        self.endInsertRows()
        return True

    def removeRowByRowNumber(self, row):
        if self.fileData[row][SCRIPT_FILE_KEY] != EMPTY_ROW_KEY:
            self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
            self.fileData.pop(row)
            self.endRemoveRows()

    def saveDataToFileByPath(self, fileName):
        output = list(self.fileData)
        for eachRow in output:
            if eachRow[SCRIPT_FILE_KEY] == EMPTY_ROW_KEY: output.remove(eachRow)
        JsonUtils.JsonUtils.saveJsonFileByPath(fileName, output)

    def openDataByPath(self, fileName):
        tempData = JsonUtils.JsonUtils.getDataFromJsonFile(fileName)
        if not self.__validateFileData(fileName, tempData):
            return
        else:
            self.beginResetModel()
            self.fileData = tempData
            self.fileData.append(dict(DEFAULT_ENTRY))
            self.endResetModel()
            return

    @staticmethod
    def __validateFileData(fileName, tempData):
        for data in tempData:
            if (not (SCRIPT_FILE_KEY in data.keys()) or not (SCRIPT_PATH_KEY in data.keys()) or not (
                SCRIPT_FILE_KEY in data.keys())
                or not (SCRIPT_PATH_KEY in data.keys())):
                raise Exception, "The file \"%s\" is either corrupt or in the wrong format" % (fileName)
            return True

    def getFilenameFromDialogBox(self, fileSuffixFilter='*.*'):
        fileDialog = QtGui.QFileDialog()
        dialogReturn = fileDialog.getOpenFileName(directory=str(os.getcwd()), filter=fileSuffixFilter)
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0), self.columnCount(0)))
        return dialogReturn

    @staticmethod
    def __parseFilenameFromDialogBox(value):
        return os.path.basename(value)

    def close(self):
        self.beginResetModel()
        self.fileData = []
        self.fileData.append(dict(DEFAULT_ENTRY))
        self.endResetModel()

    def getScriptsAndSettingsFilePaths(self):
        filteredFileData = filter(lambda x: (x[SCRIPT_FILE_KEY] != EMPTY_ROW_KEY and x[SCRIPT_FILE_KEY]), self.fileData)
        scripts = [shot[SCRIPT_PATH_KEY] for shot in filteredFileData]
        settings = [shot[SETTINGS_PATH_KEY] for shot in filteredFileData]
        return scripts, settings

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            return self.headerLabels[section]
        return QtCore.QAbstractTableModel.headerData(self, section, orientation, role)

    def moveCurrentShotUp(self, row):
        if row > 0:  #check so that it wont try to swap rows out of bounds
            self.beginResetModel()
            self.__swapRows(row, row - 1)
            self.endResetModel()

    def moveCurrentShotDown(self, row):
        if row < (len(self.fileData)):  #check so that it wont try to swap rows out of bounds
            self.beginResetModel()
            self.__swapRows(row, row + 1)
            self.endResetModel()

    def __swapRows(self, row, row2):
        if self.fileData[row][SCRIPT_FILE_KEY] == EMPTY_ROW_KEY or self.fileData[row2][
            SCRIPT_FILE_KEY] == EMPTY_ROW_KEY:
            #make sure not moving the empty row
            return
        else:
            self.fileData[row], self.fileData[row2] = self.fileData[row2], self.fileData[row]


if __name__ == '__main__':
    app = QtGui.QApplication([])

    table_view = QtGui.QTableView()
    table_model = ShotRunnerToolTableModel()
    table_view.setModel(table_model)
    table_view.show()

    app.exec_()
