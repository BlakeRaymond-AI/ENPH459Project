__author__ = 'Jeff'

import sys, os
from PyQt4 import QtGui, QtCore

from runnertool_ui import Ui_MainWindow
from RunnerToolTableModel import RunnerToolTableModel

JSON_FILE_EXTENSION = '*.json'
UP_ARROW_ICON = "resources/upArrow.png"
DOWN_ARROW_ICON = "resources/downArrow.png"

class ShotRunnerToolUi(object):
    def __init__(self, app):
        self.mainWindow = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.mainWindow)
        self.app = app
        self.init_ui()
        self.runnerTableModel = RunnerToolTableModel(self.mainWindow)
        self.init_model()
        self.connectSignalsAndSlots()
        self.fileName = None
        self.dataSaved() #sets it so that there is no unsaved changes on initialization

    def init_model(self):
        self.ui_form.tableView.setModel(self.runnerTableModel)
        self.ui_form.tableView.horizontalHeader().setResizeMode(1)
        self.ui_form.tableView.horizontalHeader().setVisible(True)
        self.ui_form.tableView.verticalHeader().setVisible(False)
        self.ui_form.tableView.setFont(QtGui.QFont("Courier New"))

    def init_ui(self):
        self.mainWindow.resize(800, 600)
        self.mainWindow.setWindowTitle("QDG Lab Shot Runner Tool")
        centre_point = QtGui.QDesktopWidget().availableGeometry().center()
        self.mainWindow.frameGeometry().moveCenter(centre_point)
        self.mainWindow.move(self.mainWindow.frameGeometry().topLeft())
        try:
            self.__loadButtonImages()
        except:
            pass

    def __loadButtonImages(self):
        try:
            upIcon = QtGui.QIcon(UP_ARROW_ICON)
            downIcon = QtGui.QIcon(DOWN_ARROW_ICON)
            self.ui_form.moveShotUpButton.setIcon(upIcon)
            self.ui_form.moveShotDownButton.setIcon(downIcon)
        except:
            raise Exception, "Couldn't load images for the moveUp and moveDown buttons"

    def connectSignalsAndSlots(self):
        self.ui_form.runButton.pressed.connect(self.runScripts)
        self.ui_form.moveShotUpButton.pressed.connect(self.moveShotUpList)
        self.ui_form.moveShotDownButton.pressed.connect(self.moveShotDownList)
        self.ui_form.actionNew.triggered.connect(self.actionNew)
        self.ui_form.actionOpen.triggered.connect(self.actionOpen)
        self.ui_form.actionSave.triggered.connect(self.actionSave)
        self.ui_form.actionSaveAs.triggered.connect(self.actionSaveAs)
        self.ui_form.actionExit.triggered.connect(self.actionExit)
        self.ui_form.actionClose.triggered.connect(self.actionClose)
        self.ui_form.actionRemoveRow.triggered.connect(self.actionRemoveRow)
        self.runnerTableModel.dataChanged.connect(self.dataChanged)

    def show(self):
        self.mainWindow.show()

    def runScripts(self):
        print "running the scripts"

    def moveShotUpList(self):
        selected = self.ui_form.tableView.selectedIndexes()
        keyIndices = [i.sibling(i.row(), 0) for i in selected]
        for index in keyIndices:
            self.runnerTableModel.moveCurrentShotUp(index.row())

    def moveShotDownList(self):
        selected = self.ui_form.tableView.selectedIndexes()
        keyIndices = [i.sibling(i.row(), 0) for i in selected]
        for index in keyIndices:
            self.runnerTableModel.moveCurrentShotDown(index.row())

    def actionNew(self):
        #saves the filename for the wanted new file for the runner tool's table model.
        #the filename will be what is written to when the save command is called
        if self.shouldDiscardUnsavedChanges():
            fileDialog = QtGui.QFileDialog(self.mainWindow)
            dialogReturn = fileDialog.getSaveFileNameAndFilter(parent=self.mainWindow, caption='New Json File',
                                                               directory=str(os.getcwd()), filter=JSON_FILE_EXTENSION)
            if dialogReturn[0]:
                self.actionClose()
                self.fileName = str(dialogReturn[0])

    def actionSave(self):
        #saves the data in the tableModel to the json file that was selected with new or open.
        if self.fileName != None: #the filename will be none if no file has been selected yet
            self.runnerTableModel.saveDataToFileByPath(self.fileName)
            self.dataSaved()
        if self.fileName == None:
            self.actionSaveAs()
            self.dataSaved()

    def actionSaveAs(self):
        #opens a new file and then saves the data to the new file immediately. Stores that file so the next save command
        #will also save to that file
        fileDialog = QtGui.QFileDialog(self.mainWindow)
        dialogReturn = fileDialog.getSaveFileNameAndFilter(parent=self.mainWindow, caption='New Json File',
                                                           directory=str(os.getcwd()), filter='*.json')
        if str(dialogReturn[0]) != None and str(dialogReturn[0]) != '':
            self.fileName = str(dialogReturn[0])
            self.runnerTableModel.saveDataToFileByPath(self.fileName)
            self.dataSaved()

    def actionExit(self):
        if self.shouldDiscardUnsavedChanges():
            sys.exit()

    def actionOpen(self):
        #loads the data into the tableModel from a json file
        if self.shouldDiscardUnsavedChanges():
            fileDialog = QtGui.QFileDialog()
            dialogReturn = fileDialog.getOpenFileName(directory=str(os.getcwd()), filter='*.json*')
            if str(dialogReturn) != None and str(dialogReturn) != '':
                self.fileName = str(dialogReturn)
                try:
                    self.runnerTableModel.openDataByPath(self.fileName)
                except Exception as ex:
                    dialog = QtGui.QMessageBox(self.mainWindow)
                    dialog.warning(self.mainWindow, 'Error During Open', ex.message)
        self.setTitle()

    def actionClose(self):
        if self.shouldDiscardUnsavedChanges():
            self.fileName = None    #release the file that the save command would write to.
            self.runnerTableModel.close()
            self.dataSaved()

    def actionRemoveRow(self):
        selected = self.ui_form.tableView.selectedIndexes()
        keyIndices = [i.sibling(i.row(), 0) for i in selected]
        for index in keyIndices:
            self.runnerTableModel.removeRowByRowNumber(index.row())

    def shouldDiscardUnsavedChanges(self):
        if self.unsavedChanges:
            messageBox = QtGui.QMessageBox()
            response = messageBox.question(self.mainWindow, 'Unsaved changes',
                                           'You have unsaved changes. Are you sure you wish to continue?',
                                            QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel,
                                            QtGui.QMessageBox.Cancel)
            if response == QtGui.QMessageBox.Cancel:
                return False
        return True

    def dataChanged(self):
        self.unsavedChanges = True
        self.setTitle()

    def dataSaved(self):
        self.unsavedChanges = False
        self.setTitle()

    def setTitle(self):
        if self.fileName is not None:
            pathLeaf = os.path.basename(self.fileName)
            if self.unsavedChanges:
                pathLeaf += '*'
            self.mainWindow.setWindowTitle('%s - QDG Lab Shot Runner Tool' % pathLeaf)
        else:
            self.mainWindow.setWindowTitle('QDG Lab Shot Runner Tool')

if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = ShotRunnerToolUi(None)
    ui.show()
    sys.exit(app.exec_())

