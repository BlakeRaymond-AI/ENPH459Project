import sys
import os
from PyQt4 import QtGui
from ShotRunnerTool.LogWindow import LogWindow
from ShotRunnerTool.ShotRunnerController import ShotRunnerController
from ShotRunnerTool.runnertool_ui import Ui_MainWindow
from ShotRunnerTool.ShotRunnerToolTableModel import ShotRunnerToolTableModel


JSON_FILE_EXTENSION = '*.json'
UP_ARROW_ICON = "resources/upArrow.png"
DOWN_ARROW_ICON = "resources/downArrow.png"
REMOVE_ROW_ICON = "resources/removeRows.png"

MONOSPACED_FONT = QtGui.QFont("Courier New", 9)
APP_STYLE = "Plastique"

COLOUR_OFF_BLACK = QtGui.QColor(39, 40, 34)
COLOUR_OFF_WHITE = QtGui.QColor(248, 248, 242)


class ShotRunnerToolUi(object):
    def __init__(self, application):
        self.mainWindow = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.mainWindow)
        self.app = application
        self.setAppStyle()
        self.init_ui()
        self.runnerTableModel = ShotRunnerToolTableModel(self.mainWindow)
        self.init_model()
        self.connectSignalsAndSlots()
        self.controller = None
        self.hookCloseEvent()
        self.fileName = None
        self.unsavedChanges = False
        self.logWindow = None

    def init_model(self):
        self.ui_form.tableView.setModel(self.runnerTableModel)
        self.ui_form.tableView.horizontalHeader().setResizeMode(1)
        self.ui_form.tableView.horizontalHeader().setVisible(True)
        self.ui_form.tableView.verticalHeader().setVisible(False)
        self.ui_form.tableView.setFont(MONOSPACED_FONT)

    def initLogWindow(self):
        self.logWindow = LogWindow(self.mainWindow)
        self.ui_form.horizontalLayout1.addWidget(self.logWindow)
        self.logWindow.setTextColor(COLOUR_OFF_WHITE)
        self.logWindow.setTextBackgroundColor(COLOUR_OFF_BLACK)
        self.logWindow.setStyleSheet("* { background-color: rgb(39, 40, 34); }")
        self.logWindow.setFont(MONOSPACED_FONT)
        self.logWindow.setReadOnly(True)

    def init_ui(self):
        self.mainWindow.resize(800, 600)
        self.mainWindow.setWindowTitle("QDG Lab Shot Runner Tool")
        centre_point = QtGui.QDesktopWidget().availableGeometry().center()
        self.mainWindow.frameGeometry().moveCenter(centre_point)
        self.mainWindow.move(self.mainWindow.frameGeometry().topLeft())

        self.initLogWindow()

        try:
            self.__loadButtonImages()
        except RuntimeError:
            pass

    def __loadButtonImages(self):
        try:
            upIcon = QtGui.QIcon(UP_ARROW_ICON)
            downIcon = QtGui.QIcon(DOWN_ARROW_ICON)
            removeIcon = QtGui.QIcon(REMOVE_ROW_ICON)
            self.ui_form.moveShotUpButton.setIcon(upIcon)
            self.ui_form.moveShotDownButton.setIcon(downIcon)
            self.ui_form.removeRowButton.setIcon(removeIcon)
        except:
            raise RuntimeError("Couldn't load images for the moveUp and moveDown buttons")

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
        self.ui_form.removeRowButton.pressed.connect(self.actionRemoveRow)
        self.runnerTableModel.dataChanged.connect(self.dataChanged)

    def show(self):
        self.mainWindow.show()

    def runScripts(self):
        if self.controller:
            raise RuntimeError('Already running scripts')
        scripts, settings = self.runnerTableModel.getScriptsAndSettingsFilePaths()
        self.controller = ShotRunnerController(scripts, settings, logWindow=self.logWindow)
        self.controller.finished.connect(self.finishedRunningScripts)
        self.ui_form.runButton.setEnabled(False)
        self.controller.start()

    def finishedRunningScripts(self):
        self.controller = None
        self.ui_form.runButton.setEnabled(True)

    def moveShotUpList(self):
        selected = self.ui_form.tableView.selectedIndexes()
        keyIndices = [i.sibling(i.row(), 0) for i in selected]
        keyIndices = list(set(keyIndices)) #removes all doubles in the list.
        for index in keyIndices:
            self.runnerTableModel.moveCurrentShotUp(index.row())

    def moveShotDownList(self):
        selected = self.ui_form.tableView.selectedIndexes()
        keyIndices = [i.sibling(i.row(), 0) for i in selected]
        keyIndices = reversed(list(set(keyIndices))) #removes all doubles in the list.
        for index in keyIndices:
            self.runnerTableModel.moveCurrentShotDown(index.row())

    def actionNew(self):
        #saves the filename for the wanted new file for the runner tool's table model.
        #the filename will be what is written to when the save command is called
        self.actionClose()
        self.fileName = None

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

    def hookCloseEvent(self):
        def handleCloseEvent(event):
            if self.shouldDiscardUnsavedChanges():
                event.accept()
            else:
                event.ignore()

        self.mainWindow.closeEvent = handleCloseEvent
        self.app.closeEvent = handleCloseEvent

    def actionOpen(self):
        # loads the data into the tableModel from a json file
        if self.shouldDiscardUnsavedChanges():
            fileDialog = QtGui.QFileDialog()
            dialogReturn = fileDialog.getOpenFileName(directory=str(os.getcwd()), filter='*.json*')
            if str(dialogReturn) not in (None, ''):
                self.fileName = str(dialogReturn)
                try:
                    self.runnerTableModel.openDataByPath(self.fileName)
                except Exception as ex:
                    dialog = QtGui.QMessageBox(self.mainWindow)
                    dialog.warning(self.mainWindow, 'Error During Open', str(ex))
        self.setTitle()

    def actionClose(self):
        if self.shouldDiscardUnsavedChanges():
            self.fileName = None    #release the file that the save command would write to.
            self.runnerTableModel.close()
            self.dataSaved()

    def actionRemoveRow(self):
        selected = self.ui_form.tableView.selectedIndexes()
        keyIndices = [i.sibling(i.row(), 0) for i in selected]
        setOfIndices = set(keyIndices)
        for index in setOfIndices:
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
            if self.unsavedChanges:
                self.mainWindow.setWindowTitle('* - QDG Lab Shot Runner Tool')
            else:
                self.mainWindow.setWindowTitle('QDG Lab Shot Runner Tool')

    def setAppStyle(self):
        self.app.setStyle(APP_STYLE)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = ShotRunnerToolUi(app)
    ui.show()
    sys.exit(app.exec_())

