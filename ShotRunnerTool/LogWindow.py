__author__ = 'Blake'

from PyQt4 import QtGui, QtCore


class LogWindow(QtGui.QTextEdit):

    def __init__(self, parent):
        QtGui.QTextEdit.__init__(self, parent)

    @QtCore.pyqtSlot(QtCore.QString)
    def appendMessage(self, message):
        formattedMessage = str(message).strip()
        self.append(formattedMessage)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
