__author__ = 'Jeff'

import sys, os
from PyQt4 import QtGui

from runnertool_ui import Ui_MainWindow
from RunnerToolTableModel import RunnerToolTableModel

class ShotRunnerToolUi(object):
    def __init__(self, app):
        self.main_window = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.main_window)
        self.app = app
        self.init_ui()
        self.model = RunnerToolTableModel(self.main_window)
        self.init_model()
        self.connectButtons()

    def init_model(self):
        self.ui_form.tableView.setModel(self.model)
        self.ui_form.tableView.horizontalHeader().setResizeMode(1)
        self.ui_form.tableView.horizontalHeader().setVisible(False)
        self.ui_form.tableView.verticalHeader().setVisible(False)
        self.ui_form.tableView.setFont(QtGui.QFont("Courier New"))
        self.connectModelSignals()

    def init_ui(self):
        self.main_window.resize(800, 600)
        self.main_window.setWindowTitle("QDG Lab Shot Runner Tool")
        centre_point = QtGui.QDesktopWidget().availableGeometry().center()
        self.main_window.frameGeometry().moveCenter(centre_point)
        self.main_window.move(self.main_window.frameGeometry().topLeft())

    def connectButtons(self):
        self.ui_form.runButton.pressed.connect(self.runScripts)
        self.ui_form.actionNew.triggered.connect(self.actionNew)
        self.ui_form.actionOpen.triggered.connect(self.actionOpen)
        self.ui_form.actionSave.triggered.connect(self.actionSave)
        self.ui_form.actionSave_As.triggered.connect(self.actionSave_As)
        self.ui_form.actionExit.triggered.connect(self.actionExit)
        self.ui_form.actionClose.triggered.connect(self.actionClose)
        self.ui_form.actionAddRow.triggered.connect(self.actionAddRow)
        self.ui_form.actionRemoveRow.triggered.connect(self.actionRemoveRow)

    def connectModelSignals(self):
        pass

    def show(self):
        self.main_window.show()

    def runScripts(self):
        print "running the scripts"

    def actionNew(self):
        #create a new file with filename
        fileDialog = QtGui.QFileDialog(self.mainWindow)
        dialogReturn = fileDialog.getSaveFileNameAndFilter(parent=self.mainWindow, caption='New Json File',
                                                           directory=str(os.getcwd()), filter='*.h5')
        if dialogReturn[0]:
            self.actionClose()
            self.fileName = str(dialogReturn[0])
            self.model = ShotPrepToolModel(self.fileName)
            self.initTabs(self.model.returnModelsInFile())
            self.modelSaved()
        #check if that new file will overwrite a previous file
        #if the file doesn't exit or we don't care about overwriting the file then:
        #store the file name
        #if the file doesn't exist create a new file with that file name.
        #--Don't overwrite it until the save function is called. Don't need to overwrite the file here if it exists
        print "creating a new file"

    def actionSave(self):
        print "saving a file"

    def actionSave_As(self):
        print "saving a file as"

    def actionExit(self):
        print "quitting..."

    def actionOpen(self):
        print "opening a file"

    def actionClose(self):
        print "closing a file"

    def actionAddRow(self):
        print "adding a row"

    def actionRemoveRow(self):
        print "removing a row"

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = ShotRunnerToolUi(None)
    ui.show()
    sys.exit(app.exec_())