__author__ = 'Blake'

import sys
import os

from PyQt4 import QtGui, QtCore

from shotpreparationtool_ui import Ui_MainWindow
from ShotPrepToolModel import ShotPrepToolModel


class ShotPreparationToolUi(object):
    def __init__(self, app):
        self.main_window = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.main_window)
        self.app = app
        self.init_ui()
        self.connect_buttons()
        self.app.lastWindowClosed.connect(self.actionClose)
        self.unsaved_changes = False

    def init_ui(self):
        self.app.setStyle("Plastique")

    def connect_buttons(self):
        form = self.ui_form

        form.actionNew.triggered.connect(self.actionNew)
        form.actionOpen.triggered.connect(self.actionOpen)
        form.actionSave.triggered.connect(self.actionSave)
        form.actionSave_As.triggered.connect(self.actionSave_As)
        form.actionClose.triggered.connect(self.actionClose)
        form.actionExit.triggered.connect(self.actionExit)
        form.actionAddGroup.triggered.connect(self.actionAddGroup)
        form.actionRemoveGroup.triggered.connect(self.actionRemoveGroup)
        form.actionRemoveRow.triggered.connect(self.actionRemoveRow)

    def setTitle(self):
        if self.file_name is not None:
            path_leaf = os.path.basename(self.file_name)
            if self.unsaved_changes:
                path_leaf += '*'
            self.main_window.setWindowTitle('%s - QDG Lab Shot Preparation Tool' % path_leaf)
        else:
            self.main_window.setWindowTitle('QDG Lab Shot Preparation Tool')

    def modelChanged(self):
        self.unsaved_changes = True
        self.setTitle()

    def modelSaved(self):
        self.unsaved_changes = False
        self.setTitle()

    def actionNew(self):
        file_dialog = QtGui.QFileDialog(self.main_window)
        dialog_return = file_dialog.getSaveFileNameAndFilter(parent=self.main_window, caption='New HDF5 file',
                                                             directory=str(os.getcwd()), filter='*.h5')
        if dialog_return[0]:
            self.actionClose()
            self.file_name = str(dialog_return[0])
            self.model = ShotPrepToolModel(self.file_name)
            self.init_tabs(self.model.returnModelsInFile())
            self.modelSaved()

    def actionOpen(self):
        file_dialog = QtGui.QFileDialog(self.main_window)
        dialog_return = file_dialog.getOpenFileNameAndFilter(parent=self.main_window, caption='Open existing HDF5 file',
                                                             directory=str(os.getcwd()), filter='*.h5')
        file_name = str(dialog_return[0])

        if file_name:
            self.actionClose()
            self.file_name = file_name
            self.model = ShotPrepToolModel(self.file_name)
            self.init_tabs(self.model.returnModelsInFile())
            self.modelSaved()

    def actionSave(self):
        if self.file_name:
            self.model.saveChanges()
            self.modelSaved()

    def actionSave_As(self):
        file_dialog = QtGui.QFileDialog(self.main_window)
        dialog_return = file_dialog.getSaveFileNameAndFilter(parent=self.main_window, caption='Save As HDF5 file',
                                                             directory=str(os.getcwd()), filter='*.h5')
        file_name = str(dialog_return[0])
        if file_name:
            self.model.saveAs(file_name)
            self.actionClose()
            self.file_name = file_name
            self.modelSaved()

            self.model = ShotPrepToolModel(self.file_name)
            self.init_tabs(self.model.returnModelsInFile())

    def actionClose(self):
        if self.unsaved_changes:
            message_box = QtGui.QMessageBox()
            response = message_box.question(self.main_window, 'Unsaved changes',
                                            'You have unsaved changes.  Are you sure you wish to continue?',
                                            QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel,
                                            QtGui.QMessageBox.Cancel)
            if response == QtGui.QMessageBox.Cancel:
                return

        if hasattr(self, 'model') and self.model:
            self.clear_tabs()
            self.model.cleanUp()
            self.model = None
            self.file_name = None
            self.modelSaved()

    def actionExit(self):
        self.actionClose()
        self.app.quit()

    def actionAddGroup(self):
        if hasattr(self, 'model') and self.model:
            dialog = QtGui.QInputDialog(self.main_window)
            response = dialog.getText(self.main_window, 'Add group', 'Enter name of device:')
            group_name = response[0]
            self.model.addDevice(str(group_name))
            self.init_tabs(self.model.returnModelsInFile())
            self.modelChanged()

        else:
            dialog = QtGui.QMessageBox(self.main_window)
            dialog.warning(self.main_window, 'Please load first', 'Please open an H5 file first.')

    def actionRemoveGroup(self):
        if not (hasattr(self, 'model') and self.model):
            dialog = QtGui.QMessageBox(self.main_window)
            dialog.warning(self.main_window, 'Please load first', 'Please open an H5 file first.')

        current_tab = self.ui_form.tabWidget.currentWidget()
        device_name = str(current_tab.windowTitle())
        self.model.removeDevice(device_name)
        self.init_tabs(self.model.returnModelsInFile())
        self.modelChanged()

    def actionRemoveRow(self):
        current_tab = self.ui_form.tabWidget.currentWidget()
        table = current_tab.findChild(QtGui.QTableView)
        selected = table.selectedIndexes()
        key_indices = [i.sibling(i.row(), 0) for i in selected]
        model = table.model()
        for index in key_indices:
            name = model.data(index, role=QtCore.Qt.DisplayRole)
            model.removeRowByName(name)
        else:
            self.modelChanged()

    def show(self):
        self.main_window.show()

    def clear_tabs(self):
        self.ui_form.tabWidget.clear()

    def init_tabs(self, models):
        self.connectModelSignals(models)
        self.clear_tabs()
        tab_widget = self.ui_form.tabWidget
        for title, model in models.items():
            page = QtGui.QWidget()
            layout = QtGui.QHBoxLayout(page)

            table_view = QtGui.QTableView(page)
            table_view.horizontalHeader().setResizeMode(1) #fit to width
            table_view.horizontalHeader().setVisible(False)
            table_view.verticalHeader().setVisible(False)
            table_view.setFont(QtGui.QFont("Courier New"))

            layout.addWidget(table_view)
            table_view.setModel(model)
            tab_widget.addTab(page, title)
            page.setWindowTitle(title)

    def connectModelSignals(self, models):
        for title, model in models.items():
            model.dataChanged.connect(self.modelChanged)
            model.rowsInserted.connect(self.modelChanged)
            model.rowsRemoved.connect(self.modelChanged)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = ShotPreparationToolUi(app)
    ui.show()
    sys.exit(app.exec_())


