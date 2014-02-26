__author__ = 'Blake'

import unittest

from PyQt4 import QtGui, QtCore

from signals.StringSignal import StringSignal
from LogWindow import LogWindow


class testLogWindow(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])

    def test_canConnectSignalToAppendMessageSlot(self):
        signal = StringSignal()
        window = LogWindow(None)
        signal.get().connect(window.appendMessage)
        signal.get().emit('Foobar')
        self.assertEqual('Foobar', window.toPlainText())

    def test_canEmitMessageFromSeparateThread(self):
        signal = StringSignal()
        window = LogWindow(None)
        signal.get().connect(window.appendMessage)

        class EmitterThread(QtCore.QThread):
            def __init__(self, signal, args):
                QtCore.QThread.__init__(self)
                self.signal = signal
                self.args = args

            def run(self):
                self.signal.emit(*self.args)

        thread = EmitterThread(signal.get(), ['Foobar'])
        thread.run()
        thread.wait()

        self.assertEqual('Foobar', window.toPlainText())


if __name__ == '__main__':
    unittest.main()
