__author__ = 'Blake'

import unittest
import time
from StringIO import StringIO

from PyQt4 import QtGui

from ConsoleController import ConsoleController


class ConsoleControllerTests(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])

    def tearDown(self):
        self.app.exit()

    def test_AsyncUpdatesWidgetWithStreamData(self):
        textWidget = QtGui.QPlainTextEdit(None)

        stream = StringIO('foo')
        controller = ConsoleController(textWidget, [stream])
        time.sleep(0.05)
        controller.join()

        widgetData = str(textWidget.toPlainText())
        self.assertEqual('foo', widgetData)


if __name__ == '__main__':
    unittest.main()
