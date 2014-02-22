__author__ = 'Blake'

import unittest
import os
import os.path

import h5py

from H5SettingsLoader import H5SettingsLoader


class H5SettingsLoaderTests(unittest.TestCase):
    def setUp(self):
        self.tempFileName = 'temp.h5'
        with open(self.tempFileName, 'w') as f:
            pass
        tempFile = h5py.File(self.tempFileName)
        devices = tempFile.create_group('devices')

        device1 = devices.create_group('fooDevice')
        device1['stringConstant'] = 'baz'
        device1['intConstant'] = 2
        device1['floatConstant'] = 3.14
        device1['arrayConstant'] = [1, 2]

        device2 = devices.create_group('barDevice')
        device2['stringConstant'] = 'quux'

        tempFile.close()

    def tearDown(self):
        if os.path.exists(self.tempFileName):
            os.remove(self.tempFileName)

    def test_loadsOneDeviceObjectPerGroupUnderDevices(self):
        loader = H5SettingsLoader()
        settings = loader.loadSettings(self.tempFileName)
        self.assertTrue(hasattr(settings, 'fooDevice'))
        self.assertTrue(hasattr(settings, 'barDevice'))

    def test_loadsSettingsFromDeviceKeysAndValues(self):
        loader = H5SettingsLoader()
        settings = loader.loadSettings(self.tempFileName)
        self.assertEqual('baz', settings.fooDevice.stringConstant)
        self.assertEqual(2, settings.fooDevice.intConstant)
        self.assertEqual(3.14, settings.fooDevice.floatConstant)
        self.assertEqual([1, 2], settings.fooDevice.arrayConstant)
