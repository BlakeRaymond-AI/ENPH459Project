__author__ = 'Blake'

import os
import os.path
import re
import json
import sys

from PyQt4 import QtGui

from mainwindow import Ui_MainWindow


class ShotPreparationToolApp(object):
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.main_window)

        self.ui_form.saveButton.pressed.connect(self.save)
        self.ui_form.discardButton.pressed.connect(self.reload)
        self.ui_form.importButton.pressed.connect(self.load_tabs)
        self.ui_form.browseSettingsDirectoryButton.pressed.connect(self.__browse_settings_dir_dialog)

        self.main_window.resize(800, 600)
        self.main_window.setWindowTitle("QDG Lab Shot Preparation Tool")
        self.main_window.show()
        centre_point = QtGui.QDesktopWidget().availableGeometry().center()
        self.main_window.frameGeometry().moveCenter(centre_point)
        self.main_window.move(self.main_window.frameGeometry().topLeft())

    def exec_(self):
        self.main_window.show()
        return self.app.exec_()

    def load_tabs(self):
        self.__set_settings_dir(str(self.ui_form.settingsDirectoryEdit.text()))

        self.pages = []
        self.tables = []
        self.ui_form.tabWidget.clear()

        for filename in self.settings_files:
            page = QtGui.QWidget()
            self.ui_form.tabWidget.addTab(page, re.sub('\.json', '', filename))
            layout = QtGui.QVBoxLayout(page)
            table = QtGui.QTableWidget(page)

            table.setFont(QtGui.QFont("Courier New"))

            layout.addWidget(table)
            self.pages.append(page)
            self.tables.append((table, filename))

        self.reload()

    def reload(self):
        for table, filename in self.tables:
            settings_dict = self.__load_settings_dict(filename)
            table.setRowCount(len(settings_dict))
            table.setColumnCount(2)
            self.__reload_table_data(table, settings_dict)

    def __reload_table_data(self, table, settings):
        for row_index, key in enumerate(settings.keys()):
            table.setItem(row_index, 0, QtGui.QTableWidgetItem(str(key)))
            table.setItem(row_index, 1, QtGui.QTableWidgetItem(self.__get_display_value(settings[key])))

    def __get_display_value(self, dict_value):
        return json.dumps(dict_value)

    def __load_settings_dict(self, filename):
        absolute_filename = os.path.normpath(os.path.join(self.settings_dir, filename))
        with open(absolute_filename, 'r') as file_handle:
            settings_dict = json.loads(file_handle.read())
            if not isinstance(settings_dict, dict):
                raise TypeError('Settings file top-level JSON object must be a dictionary')
            return settings_dict

    def save(self):
        for table, filename in self.tables:
            settings = self.__get_settings_from_table(table)
            self.__save_to_settings_file(settings, filename)

    def __get_settings_from_table(self, table):
        settings = dict()
        for row_index in range(table.rowCount()):
            settings[self.__qstring_to_str(table.item(row_index, 0))] = self.__get_settings_value(
                table.item(row_index, 1))
        return settings

    def __qstring_to_str(self, table_key):
        return str(table_key.text())

    def __get_settings_value(self, table_value):
        return json.loads(self.__qstring_to_str(table_value))

    def __save_to_settings_file(self, settings, settings_file):
        if not isinstance(settings, dict):
            raise TypeError('Settings file top-level JSON object must be a dictionary')
        absolute_filename = os.path.normpath(os.path.join(self.settings_dir, settings_file))
        with open(absolute_filename, 'w') as file_handle:
            file_handle.write(json.dumps(settings, separators=(',', ': '), indent=4, sort_keys=True))

    def __set_settings_dir(self, settings_dir):
        self.settings_dir = os.path.abspath(settings_dir)
        self.settings_files = filter(lambda filename: filename.endswith('.json'), os.listdir(self.settings_dir))

    def __browse_settings_dir_dialog(self):
        dialog = QtGui.QFileDialog(self.main_window)
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        dialog.exec_()
        self.__update_settings_dir_edit(str(dialog.directory().absolutePath()))

    def __update_settings_dir_edit(self, directory):
        self.ui_form.settingsDirectoryEdit.setText(directory)


if __name__ == '__main__':
    app = ShotPreparationToolApp()
    retval = app.exec_()
    sys.exit(retval)
