__author__ = 'Jeff'

import sys
from PyQt4 import QtGui

from runnertool_ui import Ui_MainWindow

class ShotRunnerToolUi(object):
    def __init__(self, app):
        self.main_window = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.main_window)
        self.app = app
        self.init_ui()
        self.connect_buttons()

    def init_ui(self):
        self.main_window.resize(800, 600)
        self.main_window.setWindowTitle("QDG Lab Shot Runner Tool")
        centre_point = QtGui.QDesktopWidget().availableGeometry().center()
        self.main_window.frameGeometry().moveCenter(centre_point)
        self.main_window.move(self.main_window.frameGeometry().topLeft())

    def connect_buttons(self):
        self.ui_form.runButton.pressed.connect(self.runScripts)
        self.ui_form.actionNew.triggered.connect(self.actionNew)
        self.ui_form.actionOpen.triggered.connect(self.actionOpen)
        self.ui_form.actionSave.triggered.connect(self.actionSave)
        self.ui_form.actionSave_As.triggered.connect(self.actionSave_As)
        self.ui_form.actionQuit.triggered.connect(self.actionQuit)

    def show(self):
        self.main_window.show()

    def runScripts(self):
        print "running the scripts"

    def actionNew(self):
        print "creating a new file"

    def actionSave(self):
        print "saving a file"

    def actionSave_As(self):
        print "saving a file as"

    def actionQuit(self):
        print "quitting..."

    def actionOpen(self):
        print "opening a file"

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = ShotRunnerToolUi(None)
    ui.show()
    sys.exit(app.exec_())