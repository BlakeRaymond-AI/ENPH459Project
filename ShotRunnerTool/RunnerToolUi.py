__author__ = 'Jeff'

import sys, os
from PyQt4 import QtGui

from runnertool_ui import Ui_MainWindow
from RunnerToolTableModel import RunnerToolTableModel

class ShotRunnerToolUi(object):
    def __init__(self, app):
        self.mainWindow = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.mainWindow)
        self.app = app
        self.init_ui()
        self.runnerTableModel = RunnerToolTableModel(self.mainWindow)
        self.init_model()
        self.connectButtons()
        self.fileName = None

    def init_model(self):
        self.ui_form.tableView.setModel(self.runnerTableModel)
        self.ui_form.tableView.horizontalHeader().setResizeMode(1)
        self.ui_form.tableView.horizontalHeader().setVisible(False)
        self.ui_form.tableView.verticalHeader().setVisible(False)
        self.ui_form.tableView.setFont(QtGui.QFont("Courier New"))
        self.connectModelSignals()

    def init_ui(self):
        self.mainWindow.resize(800, 600)
        self.mainWindow.setWindowTitle("QDG Lab Shot Runner Tool")
        centre_point = QtGui.QDesktopWidget().availableGeometry().center()
        self.mainWindow.frameGeometry().moveCenter(centre_point)
        self.mainWindow.move(self.mainWindow.frameGeometry().topLeft())

    def connectButtons(self):
        self.ui_form.runButton.pressed.connect(self.runScripts)
        self.ui_form.actionNew.triggered.connect(self.actionNew)
        self.ui_form.actionOpen.triggered.connect(self.actionOpen)
        self.ui_form.actionSave.triggered.connect(self.actionSave)
        self.ui_form.actionSaveAs.triggered.connect(self.actionSaveAs)
        self.ui_form.actionExit.triggered.connect(self.actionExit)
        self.ui_form.actionClose.triggered.connect(self.actionClose)
        self.ui_form.actionAddRow.triggered.connect(self.actionAddRow)
        self.ui_form.actionRemoveRow.triggered.connect(self.actionRemoveRow)

    def connectModelSignals(self):
        pass

    def show(self):
        self.mainWindow.show()

    def runScripts(self):
        print "running the scripts"

    def actionNew(self):
        #saves the filename for the wanted new file for the runner tool's table model.
        #the filename will be what is written to when the save command is called
        fileDialog = QtGui.QFileDialog(self.mainWindow)
        dialogReturn = fileDialog.getSaveFileNameAndFilter(parent=self.mainWindow, caption='New Json File',
                                                           directory=str(os.getcwd()), filter='*.json')
        if dialogReturn[0]:
            self.actionClose()
            self.fileName = str(dialogReturn[0])

    def actionSave(self):
        #saves the data in the tablemodel to the json file that was selected with new or open.

        #what should we do if no file has been selected? check if the filename hasn't been set to none, if it has then
        #call the actionNew method???
        self.runnerTableModel.saveDataToFileByPath(self.fileName)


    def actionSaveAs(self):
        #opens a new file and then saves the data to the new file immediatly. Stores that file so the next save command
        #will also save to that file
        fileDialog = QtGui.QFileDialog(self.mainWindow)
        dialogReturn = fileDialog.getSaveFileNameAndFilter(parent=self.mainWindow, caption='New Json File',
                                                           directory=str(os.getcwd()), filter='*.json')
        if dialogReturn[0]:
            self.actionClose()
            self.fileName = str(dialogReturn[0])

        self.runnerTableModel.saveDataToFileByPath(self.fileName)

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