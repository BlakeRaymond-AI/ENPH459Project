import json

__author__ = 'Blake & Jeff'

import os
import os.path
import re
import sys
import cPickle

from PyQt4 import QtGui

from mainwindow import Ui_MainWindow

#todo: stuff and things
#features to add - create a new hdf5 file in the folder
#close with and without saving
#work with a temp file
#save file (copies the temp file over the old file)
#we should remove


class ShotPreparationToolApp(object):

    #go to a directory
    #load all the files into tables
    #display all the data to the user through the model-view pattern.

    #save and discard - will need a temp file. The model automatically saves all changes.

    def __init__(self):
        self.app = QtGui.QApplication([])
        self.main_window = QtGui.QMainWindow()
        self.ui_form = Ui_MainWindow()
        self.ui_form.setupUi(self.main_window)

        self.ui_form.saveButton.pressed.connect(self.save_with_prompt)
        self.ui_form.discardButton.pressed.connect(self.reload_with_prompt)
        self.ui_form.importButton.pressed.connect(self.load_tabs_with_prompt)
        self.ui_form.browseSettingsDirectoryButton.pressed.connect(self.__browse_settings_dir_dialog)
        self.ui_form.addRowButton.pressed.connect(self.__add_row)
        self.ui_form.removeRowButton.pressed.connect(self.__remove_row)

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

        #todo: get the load_tabs function to work with the model and view pattern
        #change the tabWidget to the GroupTableModel.
        #to start, don't need the listmodel.

        self.pages = []
        self.tables = []
        self.ui_form.tabWidget.clear()

        for filename in self.settings_files:
            page = QtGui.QWidget()
            self.ui_form.tabWidget.addTab(page, re.sub('\.json', '', filename))
            layout = QtGui.QVBoxLayout(page)
            table = QtGui.QTableWidget(page)

            table.horizontalHeader().setResizeMode(1) #fit to width
            table.horizontalHeader().setVisible(False)
            table.verticalHeader().setVisible(False)
            table.setFont(QtGui.QFont("Courier New"))

            layout.addWidget(table)
            self.pages.append(page)
            self.tables.append((table, filename))

        self.reload()

    def load_tabs_with_prompt(self):
        if hasattr(self, 'pages') and self.pages is not None:
            if not self.__prompt_reimport() == QtGui.QMessageBox.Discard:
                return

        self.load_tabs()

    def reload(self):
        for table, filename in self.tables:
            settings_dict = self.__load_settings_dict(filename)
            table.setRowCount(len(settings_dict))
            table.setColumnCount(2)
            self.__reload_table_data(table, settings_dict)

    def reload_with_prompt(self):
        if self.__prompt_discard_changes() == QtGui.QMessageBox.Discard:
            self.reload()

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
                raise TypeError('Settings file top-level object must be a dictionary')
            return settings_dict

    def save(self):
        for table, filename in self.tables:
            settings = self.__get_settings_from_table(table)
            self.__save_to_settings_file(settings, filename)

    def save_with_prompt(self):
        if self.__prompt_save_changes() == QtGui.QMessageBox.SaveAll:
            self.save()

    def __get_settings_from_table(self, table):
        settings = dict()
        for row_index in range(table.rowCount()):
            table_key = self.__qstring_to_str(table.item(row_index, 0))
            table_value = self.__qstring_to_str(table.item(row_index, 1))
            if table_key:
                settings[table_key] = table_value
        return settings

    def __qstring_to_str(self, table_key):
        return str(table_key.text())

    def __get_settings_value(self, table_value):
        table_str_value = self.__qstring_to_str(table_value)
        try:
            return eval(table_str_value)
        except NameError:
            return str(table_str_value)

    def __save_to_settings_file(self, settings, settings_file):
        if not isinstance(settings, dict):
            raise TypeError('Settings file top-level object must be a dictionary')
        absolute_filename = os.path.normpath(os.path.join(self.settings_dir, settings_file))
        with open(absolute_filename, 'w') as file_handle:
            file_handle.write(json.dumps(settings))

    def __set_settings_dir(self, settings_dir):
        self.settings_dir = os.path.abspath(settings_dir)
        self.settings_files = filter(lambda filename: filename.endswith('.json'), os.listdir(self.settings_dir))

    def __browse_settings_dir_dialog(self):
        dialog = QtGui.QFileDialog(self.main_window)
        selected_dir = dialog.getExistingDirectory(self.main_window)
        self.__update_settings_dir_edit(str(selected_dir))

    def __update_settings_dir_edit(self, directory):
        self.ui_form.settingsDirectoryEdit.setText(directory)

    def __prompt_save_changes(self):
        message_box = QtGui.QMessageBox(self.main_window)
        return message_box.question(self.main_window, 'Save changes', 'Are you sure you want to save all changes?',
                                    QtGui.QMessageBox.Cancel | QtGui.QMessageBox.SaveAll, QtGui.QMessageBox.SaveAll)

    def __prompt_discard_changes(self):
        message_box = QtGui.QMessageBox(self.main_window)
        return message_box.question(self.main_window, 'Discard changes',
                                    'Are you sure you want to discard all changes?',
                                    QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

    def __prompt_reimport(self):
        message_box = QtGui.QMessageBox(self.main_window)
        return message_box.question(self.main_window, 'Discard changes',
                                    'Are you sure you want to reimport?  Doing so will discard all changes.',
                                    QtGui.QMessageBox.Discard | QtGui.QMessageBox.Cancel, QtGui.QMessageBox.Cancel)

    def __add_row(self):
        current_page_index = self.ui_form.tabWidget.currentIndex()
        if current_page_index == -1:
            message_box = QtGui.QMessageBox(self.main_window)
            message_box.information(self.main_window, '', 'Please import first.')
            return
        table = self.tables[current_page_index][0]
        table.setRowCount(table.rowCount() + 1)

    def __remove_row(self):
        current_page_index = self.ui_form.tabWidget.currentIndex()
        if current_page_index == -1:
            message_box = QtGui.QMessageBox(self.main_window)
            message_box.information(self.main_window, '', 'Please import first.')
            return
        table = self.tables[current_page_index][0]
        current_row = table.currentRow()
        table.removeRow(current_row)


if __name__ == '__main__':
    app = ShotPreparationToolApp()
    retval = app.exec_()
    sys.exit(retval)
