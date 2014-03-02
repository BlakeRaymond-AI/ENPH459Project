__author__ = 'Blake'

from PyQt4 import QtGui, QtCore


class LogWindow(QtGui.QPlainTextEdit):
    def __init__(self, parent):
        QtGui.QPlainTextEdit.__init__(self, parent)

    @QtCore.pyqtSlot(QtCore.QString)
    def appendMessage(self, message):
        formattedMessage = str(message).strip()
        self.appendPlainText(formattedMessage)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

