__author__ = 'Blake & Jeff'

import os
import os.path

from PyQt4 import QtGui, QtCore
import h5py
import numpy as np

class GroupTableModel(QtCore.QAbstractTableModel):
    def __init__(self, h5file, group_name, parent, empty_row_string='<Click to add row>'):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.h5file = h5file
        self.group_name = group_name
        self.empty_row_string = empty_row_string
        self.addRow()

    def __group(self):
        return self.h5file[self.group_name]

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.__group().keys())

    def columnCount(self, QModelIndex_parent=None, *args, **kwargs):
        return 2

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def data(self, index, role=None):
        row = index.row()
        column = index.column()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if column == 0:
                return self.__group().keys()[row]
            elif column == 1:
                group = self.__group().values()[row]
                if 'source_expression' in group.attrs:
                    return group.attrs['source_expression']
                else:
                    value = group[()]
                    if isinstance(value, np.ndarray):
                        return str(list(value))
                    else:
                        return str(value)

    def setData(self, index, value, role=None):
        #refactor this to use f.copy instead of making a new one and then copying over.
        if role == QtCore.Qt.EditRole:
            name = self.__group().keys()[index.row()]
            current_name = self.group_name + '/' + name

            if index.column() == 0:
                new_name = self.group_name + '/' + str(value.toString())
                current_group = self.h5file[current_name]

                if '<remove>' in new_name:
                    self.removeRows(index, index.row)
                    del self.h5file[current_name]
                    return True

                if not str(value.toString()) or new_name == current_name:
                    return False

                try:
                    self.h5file[new_name] = current_group
                    del self.h5file[current_name]
                except RuntimeError as expt:
                    message_box = QtGui.QMessageBox(None)
                    message_box.warning(None, '', 'Unable to create constant with key \"%s\". Can not have duplicate keys.' %value.toString())

                if self.empty_row_string in current_name:
                    return self.addRow()

            elif index.column() == 1:
                # change value
                new_value_string = str(value.toString())
                if not new_value_string:
                    return False
                try:
                    new_value = eval(new_value_string)
                except Exception as expt:
                    message_box = QtGui.QMessageBox(None)
                    message_box.warning(None, '', 'Could not evaluate expression: \"%s\"; error: \n\n%s' % (
                        new_value_string, expt.message))
                    return False
                else:
                    del self.h5file[current_name]
                    self.h5file[current_name] = new_value
                    self.h5file[current_name].attrs['source_expression'] = new_value_string

            self.dataChanged.emit(index, index)
            return True
        return False

    def removeRowByName(self, name):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)

        device = self.__group()
        if name in device:
            del device[name]
        else:
            raise KeyError('Cannot find key \'%s\' in device group' % name)

        self.endRemoveRows()

    def removeRows(self, position, rows, parent = None, *args, **kwargs):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
        self.endRemoveRows()

    def addRow(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        name = self.empty_row_string
        if not name in self.__group():
            self.__group()[name] = ''
        self.endInsertRows()

if __name__ == '__main__':
    app = QtGui.QApplication([])

    if os.path.exists('test.h5'):
        os.remove('test.h5')
    if os.path.exists('foobar.h5'):
        os.remove('foobar.h5')

    h5file = h5py.File('foobar.h5')
    devices = h5file.create_group('devices')
    RGA = devices.create_group('RGA')
    RGA['test1'] = 1
    RGA['test2'] = 2
    RGA['test3'] = [14, 16, 18, 28, 32, 40, 44]
    RGA['<Click to add row>'] = ''

    testFile = h5py.File('test.h5')
    h5file.copy('devices', testFile)

    model = GroupTableModel(h5file, group_name='devices/RGA', parent=None)

    #commands to create the views
    view = QtGui.QTableView()
    view.setModel(model)

    view.show()
    app.exec_()
    h5file.close()
