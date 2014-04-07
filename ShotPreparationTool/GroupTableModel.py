import numpy
from PyQt4 import QtGui, QtCore
from ShotPreparationTool import VariableNameValidator


EMPTY_ROW_STRING = '<Click to add row>'
NUMBER_OF_COLUMNS = 2
KEY_COLUMN_INDEX = 0
VALUE_COLUMN_INDEX = 1
SOURCE_EXPRESSION_ATTR_KEY = 'source_expression'


class GroupTableModel(QtCore.QAbstractTableModel):
    def __init__(self, group, parent):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.group = group
        self._addRow()

    def rowCount(self, *args, **kwargs):
        return len(self.group.keys())

    def columnCount(self, *args, **kwargs):
        return NUMBER_OF_COLUMNS

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
                    if isinstance(value, getattr(numpy, 'ndarray')):  # pylint reports this as an error otherwise
                        return str(list(value))
                    else:
                        return str(value)

    def setData(self, index, value, role=None):
        current = self.group.keys()[index.row()]
        new = str(value.toString())

        if not role == QtCore.Qt.EditRole:
            success = False
        elif index.column() == KEY_COLUMN_INDEX:
            success = self._tryChangeVariableName(current, new)
        elif index.column() == VALUE_COLUMN_INDEX:
            success = self._tryChangeVariableValue(current, new)
        else:
            success = False

        if success:
            self.dataChanged.emit(index, index)
        return success

    def _tryChangeVariableName(self, currentName, newName):
        if not currentName or newName == currentName:
            pass
        elif newName in self.group:
            self._warnUser('Duplicate variable name',
                          'A variable with name \"%s\" already exists for this device.' % newName)
        elif not VariableNameValidator.isValidVariableName(newName):
            self._warnUser('Invalid variable name',
                          'The name \"%s\" is not a valid Python variable name.' % newName)
        else:
            currentValue = self.group[currentName]
            self.group[newName] = currentValue
            del self.group[currentName]
            if EMPTY_ROW_STRING in currentName:  # Add another new row
                self._addRow()
            return True
        return False

    def _tryChangeVariableValue(self, currentValue, newValue):
        if not newValue:
            pass
        else:
            try:
                newValueResult = eval(newValue)
            except (SyntaxError, NameError, TypeError):
                warningMessage = "The expression \"%s\" could not be evaluated as a Python expression.  \
                                  String values must be escaped with quotation marks." % newValue
                self._warnUser('Invalid expression', warningMessage)
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

    def _addRow(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        name = EMPTY_ROW_STRING
        if not name in self.group:
            self.group[name] = ''
        self.endInsertRows()

    @staticmethod
    def _warnUser(title, message):
        message_box = QtGui.QMessageBox(None)
        message_box.warning(None, title, message)
