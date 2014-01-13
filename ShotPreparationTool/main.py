__author__ = 'Blake'

import sys
from PyQt4.uic import loadUi
from PyQt4.QtGui import QApplication, QMainWindow, QTableWidgetItem
from mainwindow import Ui_MainWindow
import json

app = QApplication(sys.argv)
wnd = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(wnd)

with open('settings.json', 'r') as f:
    settings = json.loads(f.read())
    ui.tableWidget.setColumnCount(2)
    ui.tableWidget.setRowCount(len(settings.keys()))
    for i, key in enumerate(settings.keys()):
        ui.tableWidget.setItem(i, 0, QTableWidgetItem(str(key)))
        ui.tableWidget.setItem(i, 1, QTableWidgetItem(str(settings[key])))

wnd.show()

sys.exit(app.exec_())
