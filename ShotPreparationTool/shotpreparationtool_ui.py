# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shotpreparationtool.ui'
#
# Created: Sat Apr 12 18:41:29 2014
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
        MainWindow.resize(710, 473)
        MainWindow.setStyleSheet(_fromUtf8(""))
        self.centralWidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.verticalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 710, 23))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuGroup = QtGui.QMenu(self.menuBar)
        self.menuGroup.setObjectName(_fromUtf8("menuGroup"))
        self.menuRow = QtGui.QMenu(self.menuBar)
        self.menuRow.setObjectName(_fromUtf8("menuRow"))
        MainWindow.setMenuBar(self.menuBar)
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionSave_As = QtGui.QAction(MainWindow)
        self.actionSave_As.setObjectName(_fromUtf8("actionSave_As"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionAddDevice = QtGui.QAction(MainWindow)
        self.actionAddDevice.setObjectName(_fromUtf8("actionAddDevice"))
        self.actionRemoveDevice = QtGui.QAction(MainWindow)
        self.actionRemoveDevice.setObjectName(_fromUtf8("actionRemoveDevice"))
        self.actionRemoveRow = QtGui.QAction(MainWindow)
        self.actionRemoveRow.setObjectName(_fromUtf8("actionRemoveRow"))
        self.actionImport = QtGui.QAction(MainWindow)
        self.actionImport.setObjectName(_fromUtf8("actionImport"))
        self.actionRename = QtGui.QAction(MainWindow)
        self.actionRename.setObjectName(_fromUtf8("actionRename"))
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_As)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionClose)
        self.menuFile.addAction(self.actionExit)
        self.menuGroup.addAction(self.actionAddDevice)
        self.menuGroup.addAction(self.actionRemoveDevice)
        self.menuGroup.addAction(self.actionRename)
        self.menuGroup.addAction(self.actionImport)
        self.menuRow.addAction(self.actionRemoveRow)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuGroup.menuAction())
        self.menuBar.addAction(self.menuRow.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "QDG Lab Shot Preparation Tool", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuGroup.setTitle(_translate("MainWindow", "Device", None))
        self.menuRow.setTitle(_translate("MainWindow", "Row", None))
        self.actionNew.setText(_translate("MainWindow", "New...", None))
        self.actionOpen.setText(_translate("MainWindow", "Open...", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionSave_As.setText(_translate("MainWindow", "Save As...", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
        self.actionAddDevice.setText(_translate("MainWindow", "Add", None))
        self.actionRemoveDevice.setText(_translate("MainWindow", "Remove Current", None))
        self.actionRemoveRow.setText(_translate("MainWindow", "Remove Selected", None))
        self.actionImport.setText(_translate("MainWindow", "Import...", None))
        self.actionRename.setText(_translate("MainWindow", "Rename", None))

