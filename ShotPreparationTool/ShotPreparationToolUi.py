import h5py

from ListSelectionDialog import ListSelectionDialog


__author__ = 'Blake'

import sys
import os

from PyQt4 import QtGui, QtCore

from shotpreparationtool_ui import Ui_MainWindow
from ShotPrepToolModel import ShotPrepToolModel


H5_FILE_EXTENSION = '*.h5'


class ShotPreparationToolUi(object):

    def __init__(self, app):
        self.fileName = None
        self.model = None

        self.mainWindow = QtGui.QMainWindow()
        self.uiForm = Ui_MainWindow()
        self.uiForm.setupUi(self.mainWindow)
        self.app = app
        self.initUI()
        self.connectButtons()
        self.hookCloseEvent()
        self.unsavedChanges = False

    def initUI(self):
        self.app.setStyle("Plastique")

    def connectButtons(self):
        form = self.uiForm

        form.actionNew.triggered.connect(self.actionNew)
        form.actionOpen.triggered.connect(self.actionOpen)
        form.actionSave.triggered.connect(self.actionSave)
        form.actionSave_As.triggered.connect(self.actionSave_As)
        form.actionClose.triggered.connect(self.actionClose)
        form.actionExit.triggered.connect(self.actionExit)
        form.actionAddDevice.triggered.connect(self.actionAddDevice)
        form.actionRemoveDevice.triggered.connect(self.actionRemoveDevice)
        form.actionRemoveRow.triggered.connect(self.actionRemoveRow)
        form.actionImport.triggered.connect(self.actionImport)

    def setTitle(self):
        if self.fileName is not None:
            pathLeaf = os.path.basename(self.fileName)
            if self.unsavedChanges:
                pathLeaf += '*'
            self.mainWindow.setWindowTitle(
                '%s - QDG Lab Shot Preparation Tool' %
                pathLeaf)
        else:
            self.mainWindow.setWindowTitle('QDG Lab Shot Preparation Tool')

    def checkShouldDiscardAnyUnsavedChanges(self):
        if self.unsavedChanges:
            messageBox = QtGui.QMessageBox()
            response = messageBox.question(
                self.mainWindow,
                'Unsaved changes',
                'You have unsaved changes.  Are you sure you wish to continue?',
                QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel,
                QtGui.QMessageBox.Cancel)
            if response == QtGui.QMessageBox.Cancel:
                return False
        return True

    def checkHasOpenFile(self):
        if self.model is None:
            self.warnUser('Please load first', 'Please open an H5 file first.')
            return False
        return True

    def hookCloseEvent(self):
        def handleCloseEvent(event):
            if self.checkShouldDiscardAnyUnsavedChanges():
                self.close()
                event.accept()
            else:
                event.ignore()

        self.mainWindow.closeEvent = handleCloseEvent
        self.app.closeEvent = handleCloseEvent

    def modelChanged(self):
        self.unsavedChanges = True
        self.setTitle()

    def modelSaved(self):
        self.unsavedChanges = False
        self.setTitle()

    def actionNew(self):
        if self.checkShouldDiscardAnyUnsavedChanges():
            fileDialog = QtGui.QFileDialog(self.mainWindow)
            dialogReturn = fileDialog.getSaveFileNameAndFilter(
                parent=self.mainWindow,
                caption='New HDF5 file',
                directory=str(
                    os.getcwd()),
                filter=H5_FILE_EXTENSION)
            if dialogReturn[0]:
                self.close()
                self.fileName = str(dialogReturn[0])
                self.model = ShotPrepToolModel(self.fileName)
                try:
                    self.model.importFromDefaults()
                except Exception as e:
                    self.warnUser('Error importing defaults', e.message)
                self.initTabs(self.model.returnModelsInFile())
                self.modelSaved()

    def actionOpen(self):
        fileDialog = QtGui.QFileDialog(self.mainWindow)
        dialogReturn = fileDialog.getOpenFileNameAndFilter(
            parent=self.mainWindow,
            caption='Open existing HDF5 file',
            directory=str(
                os.getcwd()),
            filter=H5_FILE_EXTENSION)
        fileName = str(dialogReturn[0])

        if fileName:
            self.actionClose()
            self.fileName = fileName
            try:
                self.model = ShotPrepToolModel(self.fileName)
            except RuntimeError as e:
                self.warnUser('File locked', e.message)
                return
            self.initTabs(self.model.returnModelsInFile())
            self.modelSaved()

    def actionSave(self):
        if self.fileName is not None:
            self.model.saveChanges()
            self.modelSaved()

    def actionSave_As(self):
        fileDialog = QtGui.QFileDialog(self.mainWindow)
        dialogReturn = fileDialog.getSaveFileNameAndFilter(
            parent=self.mainWindow,
            caption='Save As HDF5 file',
            directory=str(
                os.getcwd()),
            filter=H5_FILE_EXTENSION)
        fileName = str(dialogReturn[0])
        if fileName:
            self.model.saveAs(fileName)
            self.close()
            self.fileName = fileName
            self.modelSaved()

            self.model = ShotPrepToolModel(self.fileName)
            self.initTabs(self.model.returnModelsInFile())

    def actionClose(self):
        if self.model is not None and self.checkShouldDiscardAnyUnsavedChanges():
            self.close()

    def close(self):
        if self.model is not None:
            self.clearTabs()
            self.model.cleanUp()
            self.model = None
            self.fileName = None
            self.modelSaved()

    def actionExit(self):
        if self.model is not None and self.checkShouldDiscardAnyUnsavedChanges():
            self.close()
            self.app.quit()

    def actionAddDevice(self):
        if self.checkHasOpenFile():
            dialog = QtGui.QInputDialog(self.mainWindow)
            response = dialog.getText(
                self.mainWindow,
                'Add group',
                'Enter name of device:')
            groupName = response[0]
            if groupName:
                try:
                    self.model.addDevice(str(groupName))
                except KeyError as e:
                    self.warnUser('Device name in use', e.message)
                    return
                except SyntaxError as e:
                    self.warnUser('Invalid device name', e.message)
                self.initTabs(self.model.returnModelsInFile())
                self.modelChanged()

    def actionRemoveDevice(self):
        if self.checkHasOpenFile():
            currentTab = self.uiForm.tabWidget.currentWidget()
            deviceName = str(currentTab.windowTitle())
            self.model.removeDevice(deviceName)
            self.initTabs(self.model.returnModelsInFile())
            self.modelChanged()

    def actionRemoveRow(self):
        if self.checkHasOpenFile():
            currentTab = self.uiForm.tabWidget.currentWidget()
            table = currentTab.findChild(QtGui.QTableView)
            selected = table.selectedIndexes()
            keyIndices = [i.sibling(i.row(), 0) for i in selected]
            model = table.model()
            for index in keyIndices:
                name = model.data(index, role=QtCore.Qt.DisplayRole)
                model.removeRowByName(name)
            else:
                self.modelChanged()

    def verifyOverwriteExistingDevices(self, checkedItems):
        messageBox = QtGui.QMessageBox()
        response = messageBox.question(
            self.mainWindow,
            'Overwriting existing device',
            'One or more devices to be imported were already found.  These devices will be overwritten.',
            QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel,
            QtGui.QMessageBox.Cancel)
        if response == QtGui.QMessageBox.Cancel:
            return False
        return True

    def actionImport(self):
        if not self.checkHasOpenFile():
            return
        fileDialog = QtGui.QFileDialog(self.mainWindow)
        dialogReturn = fileDialog.getOpenFileNameAndFilter(
            parent=self.mainWindow,
            caption='Import from HDF5 file',
            directory=str(
                os.getcwd()),
            filter='*.h5')
        fileName = str(dialogReturn[0])
        if not fileName:
            return
        file = h5py.File(fileName)
        devices = ShotPrepToolModel.getListOfDevices(file)
        dialog = ListSelectionDialog(self.mainWindow)
        dialog.addItems(devices)
        response = dialog.exec_()
        if response == QtGui.QDialog.Accepted:
            checkedItems = dialog.getCheckedItems()
            if set(checkedItems).intersection(self.model.returnModelsInFile().keys()):
                if (self.verifyOverwriteExistingDevices(checkedItems)):
                    self.model.importDevices(dialog.getCheckedItems(), file)
                    self.clearTabs()
                    self.initTabs(self.model.returnModelsInFile())
                    self.modelChanged()
            else:
                self.model.importDevices(dialog.getCheckedItems(), file)
                self.clearTabs()
                self.initTabs(self.model.returnModelsInFile())
                self.modelChanged()

        file.close()

    def show(self):
        self.mainWindow.show()

    def clearTabs(self):
        self.uiForm.tabWidget.clear()

    def initTabs(self, models):
        self.connectModelSignals(models)
        self.clearTabs()
        tabWidget = self.uiForm.tabWidget
        for title, model in models.items():
            page = QtGui.QWidget()
            layout = QtGui.QHBoxLayout(page)

            tableView = QtGui.QTableView(page)
            tableView.horizontalHeader().setResizeMode(1)  # fit to width
            tableView.horizontalHeader().setVisible(False)
            tableView.verticalHeader().setVisible(False)
            tableView.setFont(QtGui.QFont("Courier New"))

            layout.addWidget(tableView)
            tableView.setModel(model)
            tabWidget.addTab(page, title)
            page.setWindowTitle(title)

    def connectModelSignals(self, models):
        for title, model in models.items():
            model.dataChanged.connect(self.modelChanged)
            model.rowsInserted.connect(self.modelChanged)
            model.rowsRemoved.connect(self.modelChanged)

    def warnUser(self, title, message):
        warningDialog = QtGui.QMessageBox(self.mainWindow)
        warningDialog.warning(self.mainWindow, title, message)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = ShotPreparationToolUi(app)
    ui.show()
    sys.exit(app.exec_())
