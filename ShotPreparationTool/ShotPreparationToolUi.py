__author__ = 'Blake'

import sys
from PyQt4 import QtGui

from mainwindow import Ui_MainWindow


class ShotPreparationToolUi(object):
    def __init__(self, app):
        self.main_window = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.main_window)
        self.app = app
        self.init_ui()
        self.connect_buttons()

    def init_ui(self):
        self.main_window.resize(800, 600)
        self.main_window.setWindowTitle("QDG Lab Shot Preparation Tool")
        centre_point = QtGui.QDesktopWidget().availableGeometry().center()
        self.main_window.frameGeometry().moveCenter(centre_point)
        self.main_window.move(self.main_window.frameGeometry().topLeft())

    def connect_buttons(self):
        self.ui_form.addTabButton.pressed.connect(self.add_tab_button_pressed)
        self.ui_form.addRowButton.pressed.connect(self.add_row_button_pressed)
        self.ui_form.removeTabButton.pressed.connect(self.remove_tab_button_pressed)
        self.ui_form.removeRowButton.pressed.connect(self.remove_row_button_pressed)
        self.ui_form.saveButton.pressed.connect(self.save_button_pressed)
        self.ui_form.discardButton.pressed.connect(self.discard_button_pressed)
        self.ui_form.browseSettingsDirectoryButton.pressed.connect(self.browse_settings_button_pressed)
        self.ui_form.importButton.pressed.connect(self.import_button_pressed)

    def show(self):
        self.main_window.show()

    def save_button_pressed(self):
        print 'save button'

    def discard_button_pressed(self):
        print 'discard button'

    def import_button_pressed(self):
        print 'import button'

    def browse_settings_button_pressed(self):
        print 'browse settings'

    def add_row_button_pressed(self):
        print 'add row'

    def remove_row_button_pressed(self):
        print 'remove row'

    def add_tab_button_pressed(self):
        print 'add tab'

    def remove_tab_button_pressed(self):
        print 'remove tab'


if __name__ == '__main__':
    app = QtGui.QApplication([])
    ui = ShotPreparationToolUi(None)
    ui.show()
    sys.exit(app.exec_())


