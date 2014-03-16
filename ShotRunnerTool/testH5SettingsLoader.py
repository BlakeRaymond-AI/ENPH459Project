__author__ = 'Blake'

import unittest
import os
import os.path

import h5py

from H5SettingsLoader import H5SettingsLoader


class testH5SettingsLoader(unittest.TestCase):
    def setUp(self):
        self.tempFileName = 'temp.h5'
        tempFile = h5py.File(self.tempFileName)
        devices = tempFile.create_group('devices')

        device1 = devices.create_group('testDevice1')
        device1['stringConstant'] = 'baz'
        device1['intConstant'] = 2
        device1['floatConstant'] = 3.14
        device1['arrayConstant'] = [1, 2]

        device2 = devices.create_group('testDevice2')
        device2['stringConstant'] = 'quux'

        tempFile.close()

    def tearDown(self):
        if os.path.exists(self.tempFileName):
            os.remove(self.tempFileName)

    def test_loadsOneDeviceObjectPerGroupUnderDevices(self):
        loader = H5SettingsLoader()
        settings = loader.loadSettings(self.tempFileName)
        self.assertTrue('testDevice1' in settings)
        self.assertTrue('testDevice2' in settings)

    def test_loadsSettingsFromDeviceKeysAndValues(self):
        loader = H5SettingsLoader()
        settings = loader.loadSettings(self.tempFileName)
        self.assertEqual('baz', settings['testDevice1']['stringConstant'])
        self.assertEqual(2, settings['testDevice1']['intConstant'])
        self.assertEqual(3.14, settings['testDevice1']['floatConstant'])
        self.assertEqual([1, 2], settings['testDevice1']['arrayConstant'])
