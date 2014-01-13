__author__ = 'Blake'

import sys
import json
import os

from PyQt4.QtGui import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QWidget, QSizePolicy, QVBoxLayout, QDesktopWidget

from mainwindow import Ui_MainWindow


def make_auto_expand(widget):
    sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    sizePolicy.setHorizontalStretch(0)
    sizePolicy.setVerticalStretch(0)
    sizePolicy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
    widget.setSizePolicy(sizePolicy)


def configure_table(table):
    table.horizontalHeader().setResizeMode(1)
    table.horizontalHeader().setVisible(False)
    table.verticalHeader().setVisible(False)


settings_dir = os.getcwd() + '\\settings\\'
files = os.listdir(settings_dir)
settings_files = filter(lambda fname: fname.endswith('.json'), files)

app = QApplication(sys.argv)
wnd = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(wnd)

tables = []

for fname in settings_files:
    with open('settings\\' + fname, 'r') as f:
        settings = json.loads(f.read())

        new_page = QWidget()
        make_auto_expand(new_page)
        vertical_layout = QVBoxLayout(new_page)
        ui.tabWidget.addTab(new_page, fname.replace('.json', ''))

        table = QTableWidget(new_page)
        configure_table(table)
        tables.append((fname, table))
        vertical_layout.addWidget(table)

        table.setColumnCount(2)
        table.setRowCount(len(settings.keys()))
        for i, key in enumerate(settings.keys()):
            table.setItem(i, 0, QTableWidgetItem(str(key)))
            table.setItem(i, 1, QTableWidgetItem(json.dumps(settings[key])))

wnd.resize(800, 600)
wnd.show()
centre_point = QDesktopWidget().availableGeometry().center()
wnd.frameGeometry().moveCenter(centre_point)
wnd.move(wnd.frameGeometry().topLeft())
rvalue = app.exec_()

for fname, table in tables:
    settings = dict()
    for row_index in range(table.rowCount()):
        settings[str(table.item(row_index, 0).text())] = json.loads(str(table.item(row_index, 1).text()))
    json_string = json.dumps(settings, indent=4, sort_keys=True, separators=(',', ': '))
    with open('settings\\' + fname, 'w') as f:
        f.write(json_string)

sys.exit(rvalue)
