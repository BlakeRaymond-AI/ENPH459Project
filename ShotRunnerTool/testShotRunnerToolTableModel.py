__author__ = 'Jeff'

from unittest import TestCase

from ShotRunnerToolTableModel import *


class TestShotRunnerToolTableModel(TestCase):
    def test_rowCount(self):
        tableModel = ShotRunnerToolTableModel()
        self.assertEqual(tableModel.rowCount(), 1)  #check that there is one row by default
        tableModel.addRow()
        tableModel.fileData[1]['scriptFileName'] = 'test'
        self.assertEqual(tableModel.rowCount(), 2)  #make sure that there are now 2 rows

    def test_columnCount(self):
        tableModel = ShotRunnerToolTableModel()
        self.assertEqual(tableModel.columnCount(), 2)

    def test_addRow(self):
        tableModel = ShotRunnerToolTableModel()
        self.assertEqual(tableModel.rowCount(), 1)  #check that there is one row by default
        tableModel.addRow()
        self.assertEqual(tableModel.rowCount(), 2)  #check that the number of rows has been incremented

    def test_saveDataToFileByPath(self):
        tableModel = ShotRunnerToolTableModel()
        filePath = 'test_TableModelSaveData.json'
        tableModel.saveDataToFileByPath(filePath)
        self.assertTrue(os.path.exists(filePath))
        os.remove(filePath)

    def test_close(self):
        tableModel = ShotRunnerToolTableModel()
        tableModel.addRow()
        tableModel.addRow()
        tableModel.close()
        self.assertEqual(tableModel.rowCount(), 1)

    def test_getScriptsAndSettingsFilePaths(self):
        tableModel = ShotRunnerToolTableModel()
        tableModel.addRow()
        tableModel.fileData[1]['scriptFileName'] = 'foo'
        tableModel.fileData[1]['scriptFilePath'] = 'shoop'
        tableModel.fileData[1]['settingsFilePath'] = 'baz'
        settings, scripts = tableModel.getScriptsAndSettingsFilePaths()
        self.assertEqual(settings[0], 'shoop')
        self.assertEqual(scripts[0], 'baz')