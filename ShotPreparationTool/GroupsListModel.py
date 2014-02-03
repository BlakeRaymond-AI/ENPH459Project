__author__ = 'Blake'

import os
import os.path

from PyQt4 import QtGui, QtCore
import h5py


class GroupsListModel(QtCore.QAbstractListModel):
    def __init__(self, h5file, parent, groups_name='groups'):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.h5file = h5file
        self.groups_name = 'groups'
        if not self.groups_name in self.h5file:
            self.h5file.create_group(self.groups_name)

    def rowCount(self, QModelIndex_parent=None, *args, **kwargs):
        return len(self.h5file[self.groups_name].keys())

    def data(self, index, role=None):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.h5file[self.groups_name].keys()[index.row()]

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def setData(self, index, value, role=None):
        if role == QtCore.Qt.EditRole:
            current_group_name = self.h5file[self.groups_name].keys()[index.row()]
            current_group = self.h5file[self.groups_name + '/' + current_group_name]
            new_group_name = self.groups_name + '/' + str(value.toString())

            if current_group_name == new_group_name or not str(value.toString()):
                return False

            self.h5file[new_group_name] = current_group
            del self.h5file[self.groups_name + '/' + current_group_name]
            self.dataChanged.emit(index, index)
            return True

        return False

    def insertRows(self, position, rows, QModelIndex_parent=None, *args, **kwargs):
        self.beginInsertRows(QtCore.QModelIndex(), 0, rows + len(self.h5file[self.groups_name].keys()) - 1)

        for i in range(rows):
            name = 'group_' + str(len(self.h5file[self.groups_name].keys()))
            new_grp = self.h5file[self.groups_name].create_group(name)

        self.endInsertRows()

        return True


if __name__ == '__main__':
    app = QtGui.QApplication([])

    table_view = QtGui.QTableView()

    if os.path.exists('foobar.h5'):
        os.remove('foobar.h5')

    h5file = h5py.File('foobar.h5')
    grp = h5file.create_group('groups')
    groups_model = GroupsListModel(h5file, parent=None)
    groups_model.insertRows(0, 1)
    groups_model.insertRows(1, 1)

    table_view.setModel(groups_model)
    table_view.show()

    app.exec_()

    h5file.close()
