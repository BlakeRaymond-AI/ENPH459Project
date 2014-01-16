# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Jan 16 11:53:20 2014
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
        self.label = QtGui.QLabel(self.centralWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.settingsDirectoryEdit = QtGui.QLineEdit(self.centralWidget)
        self.settingsDirectoryEdit.setObjectName(_fromUtf8("settingsDirectoryEdit"))
        self.horizontalLayout_2.addWidget(self.settingsDirectoryEdit)
        self.browseSettingsDirectoryButton = QtGui.QToolButton(self.centralWidget)
        self.browseSettingsDirectoryButton.setObjectName(_fromUtf8("browseSettingsDirectoryButton"))
        self.horizontalLayout_2.addWidget(self.browseSettingsDirectoryButton)
        self.importButton = QtGui.QPushButton(self.centralWidget)
        self.importButton.setObjectName(_fromUtf8("importButton"))
        self.horizontalLayout_2.addWidget(self.importButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.verticalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, -1, -1, 10)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.addRowButton = QtGui.QPushButton(self.centralWidget)
        self.addRowButton.setObjectName(_fromUtf8("addRowButton"))
        self.horizontalLayout_3.addWidget(self.addRowButton)
        self.removeRowButton = QtGui.QPushButton(self.centralWidget)
        self.removeRowButton.setObjectName(_fromUtf8("removeRowButton"))
        self.horizontalLayout_3.addWidget(self.removeRowButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setContentsMargins(-1, -1, 0, 0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.saveButton = QtGui.QPushButton(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout.addWidget(self.saveButton)
        self.discardButton = QtGui.QPushButton(self.centralWidget)
        self.discardButton.setObjectName(_fromUtf8("discardButton"))
        self.horizontalLayout.addWidget(self.discardButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 710, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Settings directory:", None))
        self.browseSettingsDirectoryButton.setText(_translate("MainWindow", "...", None))
        self.importButton.setText(_translate("MainWindow", "Import", None))
        self.addRowButton.setText(_translate("MainWindow", "Add row", None))
        self.removeRowButton.setText(_translate("MainWindow", "Remove row", None))
        self.saveButton.setText(_translate("MainWindow", "Save", None))
        self.discardButton.setText(_translate("MainWindow", "Discard", None))

