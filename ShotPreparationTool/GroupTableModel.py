__author__ = 'Blake & Jeff'

import os
import os.path

from PyQt4 import QtGui, QtCore
import h5py
import numpy as np


class GroupTableModel(QtCore.QAbstractTableModel):

    def __init__(self, h5file, group_name, parent):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.h5file = h5file
        self.group_name = group_name

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

                if '<Click to add row>' in current_name:
                    self.add_row()

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

    def insertRows(self, position, rows, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertRows(QtCore.QModelIndex(), 0, rows + len(self.__group().keys()) - 1)

        for i in range(rows):
            name = 'item_' + str(len(self.__group().keys()))
            self.__group()[name] = ''

        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent = None, *args, **kwargs):
        self.beginRemoveRows(QtCore.QModelIndex(), 0, 0)
        #TODO: insert removing rows here
        self.endRemoveRows()


    def add_row(self):
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        name = '<Click to add row>'
        self.__group()[name] = ''
        self.endInsertRows()
        return True


if __name__ == '__main__':
    app = QtGui.QApplication([])

    if os.path.exists('foobar.h5'):
        os.remove('test.h5')
        os.remove('foobar.h5')

    h5file = h5py.File('foobar.h5')
    devices = h5file.create_group('devices')
    RGA = devices.create_group('RGA')
    MOT = devices.create_group('MOT')
    RGA['test1'] = 1
    RGA['test2'] = 2
    RGA['test3'] = [14, 16, 18, 28, 32, 40, 44]
    RGA['<Click to add row>'] = ''
    MOT['stuff'] = "test string"

    testFile = h5py.File('test.h5')
#    testFile.create_group('devices')
#    del testFile['devices']
    h5file.copy('devices', testFile)

    model = GroupTableModel(h5file, group_name='devices/RGA', parent=None)

    #commands to create the views
    view = QtGui.QTableView()
    view.setModel(model)

    view.show()
    app.exec_()
    h5file.close()
