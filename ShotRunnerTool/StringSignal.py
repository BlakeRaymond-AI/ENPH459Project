__author__ = 'Blake'

from PyQt4 import QtCore


class StringSignal(QtCore.QObject):
    signal = QtCore.pyqtSignal(QtCore.QString)

    def __init__(self):
        QtCore.QObject.__init__(self)

    def get(self):
        return self.signal

