__author__ = 'Blake'

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
        if role == QtCore.Qt.EditRole:
            name = self.__group().keys()[index.row()]
            current_name = self.group_name + '/' + name

            if index.column() == 0:
                # rename
                new_name = self.group_name + '/' + str(value.toString())
                current_group = self.h5file[current_name]
                if not str(value.toString()) or new_name == current_name:
                    return False
                self.h5file[new_name] = current_group
                del self.h5file[current_name]
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


if __name__ == '__main__':
    app = QtGui.QApplication([])

    if os.path.exists('foobar.h5'):
        h5file = h5py.File('foobar.h5')
    else:
        h5file = h5py.File('foobar.h5')
        groups = h5file.create_group('groups')
        group1 = groups.create_group('group1')
        group1['rb_pump_amplitude'] = 1
        group1['rb_pump_detuning'] = 2
        group1['Channels.Parameters.Mass.FirstMass'] = [14, 16, 18, 28, 32, 40, 44]

    model = GroupTableModel(h5file, group_name='groups/group1', parent=None)

    view = QtGui.QTableView()
    view.setModel(model)

    view.show()
    app.exec_()
    h5file.close()