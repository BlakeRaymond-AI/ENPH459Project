__author__ = 'Jeff'

import sys, os
from PyQt4 import QtGui, QtCore

from runnertool_ui import Ui_MainWindow
from RunnerToolTableModel import RunnerToolTableModel

#TODOS:
#file menu:
#close
#quit

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

    def connectModelSignals(self, models=None):
        #for title, model in models.items():
            #model.dataChanged.connect(self.modelChanged) #modelchanged doesn't update the view, it only is a key if there's unsaved changes or not
            #model.rowsInserted.connect(self.modelChanged)
            #model.rowsRemoved.connect(self.modelChanged)
            #pass
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
        #saves the data in the tableModel to the json file that was selected with new or open.
        if self.fileName != None: #the filename will be none if no file has been selected yet
            self.runnerTableModel.saveDataToFileByPath(self.fileName)
        if self.fileName == None:
            self.actionSaveAs()

    def actionSaveAs(self):
        #opens a new file and then saves the data to the new file immediately. Stores that file so the next save command
        #will also save to that file
        self.actionNew()
        if self.fileName != None:
            self.runnerTableModel.saveDataToFileByPath(self.fileName)

    def actionExit(self):
        #if unsaved data:
        #check if the user wants to save the data.
        print "exiting the runner"

    def actionOpen(self):
        #loads the data into the tableModel from a json file
        fileDialog = QtGui.QFileDialog()
        dialogReturn = fileDialog.getOpenFileName(directory=str(os.getcwd()), filter='*.json*')
        self.fileName = str(dialogReturn)
        self.runnerTableModel.openDataByPath(self.fileName)
        #make sure that the runner table will actually update the view. Right now loading the data will not update the view

    def actionClose(self):
        self.fileName = None    #release the file that the save command would write to.

    def actionAddRow(self):
        self.runnerTableModel.addRow()

    def actionRemoveRow(self):
        selected = self.ui_form.tableView.selectedIndexes()
        keyIndices = [i.sibling(i.row(), 0) for i in selected]
        for index in keyIndices:
            row = self.runnerTableModel.data(index, role='removeRowRoll')
            self.runnerTableModel.removeRowByRowNumber(row)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = ShotRunnerToolUi(None)
    ui.show()
    sys.exit(app.exec_())