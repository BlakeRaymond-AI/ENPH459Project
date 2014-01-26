__author__ = 'Blake'

import sys
from PyQt4 import QtGui
import inspect
import os

from shotpreparationtool_ui import Ui_MainWindow


class ShotPreparationToolUi(object):
    def __init__(self, app):
        self.main_window = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.main_window)
        self.app = app
        self.init_ui()
        self.connect_buttons()

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

    def actionNew(self):
        print inspect.stack()[0][3]

    def actionOpen(self):
        print inspect.stack()[0][3]
        file_dialog = QtGui.QFileDialog(self.main_window)
        dialog_return = file_dialog.getOpenFileNameAndFilter(parent=self.main_window, caption='Open existing HDF5 file', directory=str(os.getcwd()), filter='.h5')
        self.file_name = str(dialog_return[0])
        print 'would open %s' % str(self.file_name)

    def actionSave(self):
        print inspect.stack()[0][3]
        print 'would save to %s' % str(self.file_name)

    def actionSave_As(self):
        print inspect.stack()[0][3]
        file_dialog = QtGui.QFileDialog(self.main_window)
        dialog_return = file_dialog.getSaveFileNameAndFilter(parent=self.main_window, caption='Save As HDF5 file', directory=str(os.getcwd()), filter='.h5')
        self.file_name = str(dialog_return[0])
        print 'would save as %s' % str(self.file_name)

    def actionClose(self):
        print inspect.stack()[0][3]

    def actionExit(self):
        print inspect.stack()[0][3]
        self.app.quit()

    def actionAddGroup(self):
        print inspect.stack()[0][3]

    def actionRemoveGroup(self):
        print inspect.stack()[0][3]

    def actionRemoveRow(self):
        print inspect.stack()[0][3]

    def show(self):
        self.main_window.show()



if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = ShotPreparationToolUi(app)
    ui.show()
    sys.exit(app.exec_())


