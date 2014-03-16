__author__ = 'Blake'

from PyQt4 import QtGui, QtCore


class ListSelectionDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)

        layout = QtGui.QVBoxLayout(self)
        self.setLayout(layout)
        self.devicesList = QtGui.QListWidget(self)
        layout.addWidget(self.devicesList)

        horizontalLayout = QtGui.QHBoxLayout()
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        horizontalLayout.addItem(spacerItem)

        buttonDialog = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
        buttonDialog.accepted.connect(self.accept)
        buttonDialog.rejected.connect(self.reject)
        horizontalLayout.addWidget(buttonDialog)

        layout.addLayout(horizontalLayout)


    def addItems(self, devices):
        for device in devices:
            item = QtGui.QListWidgetItem(device, self.devicesList)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)


    def getCheckedItems(self):
        def isChecked(item):
            return item.checkState() == QtCore.Qt.Checked

        items = map(lambda index: self.devicesList.item(index), range(self.devicesList.count()))
        checkedItems = filter(isChecked, items)
        return map(lambda item: str(item.text()), checkedItems)
