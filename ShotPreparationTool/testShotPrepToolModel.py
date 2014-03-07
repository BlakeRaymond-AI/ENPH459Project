import os
import unittest

import h5py

from GroupTableModel import GroupTableModel
from ShotPrepToolModel import ShotPrepToolModel


class TestShotPrepToolModel(unittest.TestCase):
    #test case #1: make sure that it will import and create files (h5 files)
    #test case #2: make sure that it will copy from the original file to the test file
    #test case #3: check that discard changes works as expected
    #test case #4: check that save works as expected
    #test case #5: check that cleanup works as expected
    #test case #6: check that adding a row will work
    #test case #7: check that adding in a new device will work
    #test case #8: check that removing a group will work
    #test case #9: check that removing a row will work
    def setUp(self):
        h5pathname = 'test_file.h5'
        self.h5file = h5py.File(h5pathname)
        devices = self.h5file.create_group('devices')
        RGA = devices.create_group('RGA')
        MOT = devices.create_group('MOT')
        RGA['test data point'] = '1'
        MOT['test data point 2'] = '2'
        self.h5file.close()
        self.testModel = ShotPrepToolModel(h5pathname)

    def tearDown(self):
        self.testModel.cleanUp()
        if os.path.exists('test_file.h5'):
            os.remove('test_file.h5')

    def test_InitWillLoadModel(self):
        devices = self.testModel.returnModelsInFile()
        self.assertIsInstance(devices['RGA'], GroupTableModel)
        self.assertIsInstance(devices['MOT'], GroupTableModel)

    def test_ModelActuallyHasTheData(self):
        devices = self.testModel.returnModelsInFile()
        self.assertEqual(devices['RGA'].group['test data point'][()], '1')
        self.assertEqual(devices['MOT'].group['test data point 2'][()], '2')

    def test_DiscardChangesWillRevertChanges(self):
        devices = self.testModel.returnModelsInFile()

        devices['RGA'].group['test data point'][()] = '2'
        self.assertEqual(devices['RGA'].group['test data point'][()], '2')

        devices['MOT'].group['test data point 2'][()] = '1'
        self.assertEqual(devices['MOT'].group['test data point 2'][()], '1')

        self.testModel.discardCharges()
        devices = self.testModel.returnModelsInFile()

        self.assertEqual('1', devices['RGA'].group['test data point'][()])
        self.assertEqual('2', devices['MOT'].group['test data point 2'][()])

    def test_SaveChangesWillSaveChanges(self):
        devices = self.testModel.returnModelsInFile()

        devices['RGA'].group['test data point'][()] = '2'
        self.assertEqual(devices['RGA'].group['test data point'][()], '2')
        devices['MOT'].group['test data point 2'][()] = '1'
        self.assertEqual(devices['MOT'].group['test data point 2'][()], '1')

        self.testModel.saveChanges()

        saveFile = h5py.File('test_file.h5')
        self.assertEqual('2', saveFile['devices/RGA/test data point'][()])
        self.assertEqual('1', saveFile['devices/MOT/test data point 2'][()])
        saveFile.close()


if __name__ == '__main__':
    unittest.main()