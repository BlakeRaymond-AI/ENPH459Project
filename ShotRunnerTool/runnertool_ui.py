# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'runnertool_ui.ui'
#
# Created: Wed Mar 05 16:06:21 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(900, 604)
        self.centralWidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.runButton = QtGui.QPushButton(self.centralWidget)
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.horizontalLayout_2.addWidget(self.runButton)
        self.moveShotUpButton = QtGui.QPushButton(self.centralWidget)
        self.moveShotUpButton.setText(_fromUtf8(""))
        self.moveShotUpButton.setObjectName(_fromUtf8("moveShotUpButton"))
        self.horizontalLayout_2.addWidget(self.moveShotUpButton)
        self.moveShotDownButton = QtGui.QPushButton(self.centralWidget)
        self.moveShotDownButton.setText(_fromUtf8(""))
        self.moveShotDownButton.setObjectName(_fromUtf8("moveShotDownButton"))
        self.horizontalLayout_2.addWidget(self.moveShotDownButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableView = QtGui.QTableView(self.centralWidget)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout.addWidget(self.tableView)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 900, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuRow = QtGui.QMenu(self.menuBar)
        self.menuRow.setObjectName(_fromUtf8("menuRow"))
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSaveAs = QtGui.QAction(MainWindow)
        self.actionSaveAs.setObjectName(_fromUtf8("actionSaveAs"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAddRow = QtGui.QAction(MainWindow)
        self.actionAddRow.setObjectName(_fromUtf8("actionAddRow"))
        self.actionRemoveRow = QtGui.QAction(MainWindow)
        self.actionRemoveRow.setObjectName(_fromUtf8("actionRemoveRow"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionExit)
        self.menuRow.addAction(self.actionRemoveRow)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuRow.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.runButton.setText(_translate("MainWindow", "Run Scripts", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuRow.setTitle(_translate("MainWindow", "Row", None))
        self.actionNew.setText(_translate("MainWindow", "New...", None))
        self.actionOpen.setText(_translate("MainWindow", "Open...", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSaveAs.setText(_translate("MainWindow", "Save As...", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionAddRow.setText(_translate("MainWindow", "Add Row", None))
        self.actionRemoveRow.setText(_translate("MainWindow", "Remove Row", None))

