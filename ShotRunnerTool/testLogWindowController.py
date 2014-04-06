import unittest
import os
import os.path
from PyQt4 import QtGui
from ShotRunnerTool.LogWindowController import LogWindowController
from ShotRunnerTool.LogWindow import LogWindow
from ShotRunnerTool.ScriptRunner import ScriptRunner


class TestLogWindowController(unittest.TestCase):
    def setUp(self):
        self.app = QtGui.QApplication([])
        self.tempFile = 'foo.tmp'
        with open(self.tempFile, 'w') as _:
            pass

    def tearDown(self):
        if os.path.exists(self.tempFile):
            os.remove(self.tempFile)

    def test_copiesSubprocessOutputToLogWindow(self):
        with open(self.tempFile, 'w') as f:
            f.write("print 'Foobar'")
        runner = ScriptRunner(self.tempFile)
        logWindow = LogWindow(None)
        controller = LogWindowController(runner, logWindow)
        controller.run()
        controller.join()
        self.assertEqual('Foobar', str(logWindow.toPlainText()).strip())

    def test_copiesSubprocessErrorsToLogWindow(self):
        with open(self.tempFile, 'w') as f:
            f.write("raise Exception('Foobar')")
        runner = ScriptRunner(self.tempFile)
        logWindow = LogWindow(None)
        controller = LogWindowController(runner, logWindow)
        controller.run()
        controller.join()
        self.assertTrue('Foobar' in str(logWindow.toPlainText()).strip())
