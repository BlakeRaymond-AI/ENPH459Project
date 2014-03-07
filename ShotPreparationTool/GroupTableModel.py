from ShotPreparationTool.VariableNameValildator import VariableNameValidator

__author__ = 'Blake & Jeff'

from PyQt4 import QtGui, QtCore
import numpy as np

EMPTY_ROW_STRING = '<Click to add row>'
NUMBER_OF_COLUMNS = 2
KEY_COLUMN_INDEX = 0
VALUE_COLUMN_INDEX = 1
SOURCE_EXPRESSION_ATTR_KEY = 'source_expression'


class GroupTableModel(QtCore.QAbstractTableModel):
    def __init__(self, group, parent):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.group = group
        self.addRow()

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.group.keys())

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 2

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=None):
        row = index.row()
        column = index.column()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if column == KEY_COLUMN_INDEX:
                return self.group.keys()[row]
            elif column == VALUE_COLUMN_INDEX:
                group = self.group.values()[row]
                if SOURCE_EXPRESSION_ATTR_KEY in group.attrs:
                    return group.attrs[SOURCE_EXPRESSION_ATTR_KEY]
                else:
                    value = group[()]
                    if isinstance(value, np.ndarray):
                        return str(list(value))
                    else:
                        return str(value)

    def setData(self, index, value, role=None):
        current = self.group.keys()[index.row()]
        new = str(value.toString())

        if not role == QtCore.Qt.EditRole:
            success = False
        elif index.column() == 0:
            success = self.tryChangeVariableName(current, new)
        elif index.column() == 1:
            success = self.tryChangeVariableValue(current, new)
        else:
            success = False

        if success:
            self.dataChanged.emit(index, index)
        return success

    def tryChangeVariableName(self, currentName, newName):
        if not currentName or newName == currentName:
            pass
        elif newName in self.group:
            self.warnUser('Duplicate variable name',
                          'Variable with name \"%s\" already exists for this device.' % newName)
        elif not VariableNameValidator.isValidVariableName(newName):
            self.warnUser('Invalid variable name',
                          'Variable name \"%s\" is not a valid Python variable name.' % newName)
        else:
            currentValue = self.group[currentName]
            self.group[newName] = currentValue
            del self.group[currentName]
            if EMPTY_ROW_STRING in currentName:  # Add another new row
                self.addRow()
            return True
        return False

    def tryChangeVariableValue(self, currentValue, newValue):
        if not newValue:
            pass
        else:
            try:
                newValueResult = eval(newValue)
            except Exception as expt:
                warningMessage = 'Could not evaluate expression: \"%s\"; error: \n\n%s' % (newValue, expt.message)
                self.warnUser('Invalid expression', warningMessage)
            else:
                del self.group[currentValue]
                self.group[currentValue] = newValueResult
                self.group[currentValue].attrs[SOURCE_EXPRESSION_ATTR_KEY] = newValue
                return True
        return False

    def removeRowByName(self, name):
        device = self.group
        if name in device:
            if not EMPTY_ROW_STRING in name:
                self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
                del device[name]
                self.endRemoveRows()
        else:
            raise KeyError('Cannot find key \'%s\' in device group' % name)

    def removeRows(self, position, rows, parent = None, *args, **kwargs):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
        self.endRemoveRows()

    def addRow(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        name = EMPTY_ROW_STRING
        if not name in self.group:
            self.group[name] = ''
        self.endInsertRows()

    def warnUser(self, title, message):
        message_box = QtGui.QMessageBox(None)
        message_box.warning(None, title, message)
