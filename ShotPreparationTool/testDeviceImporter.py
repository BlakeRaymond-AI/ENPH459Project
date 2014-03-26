import h5py

from DeviceImporter import DeviceImporter


__author__ = 'Blake'

import unittest


class TestDeviceImporter(unittest.TestCase):
    def test_canAddDevicesToH5FileFromDict(self):
        newDevices = {
            'FooDevice': {
                'BarConstant': 'BazValue'
            }
        }
        targetFile = h5py.File('test_canAddDevicesToH5FileFromDict.h5', driver='core',
                               backing_store=False)  # memory-only
        deviceImporter = DeviceImporter(targetFile)
        deviceImporter.importFromDict(newDevices)

        self.assertTrue('FooDevice' in targetFile)
        self.assertTrue('BarConstant' in targetFile['FooDevice'])
        self.assertEqual('BazValue', targetFile['FooDevice/BarConstant'][()])

    def test_canAddDevicesToH5FileFromOtherH5File(self):
        sourceFile = h5py.File('source.h5', driver='core', backing_store=False)  # memory-only
        targetFile = h5py.File('target.h5', driver='core', backing_store=False)  # memory-only

        fooDevice = sourceFile.create_group('FooDevice')
        fooDevice['BarConstant'] = 'BazValue'

        deviceImporter = DeviceImporter(targetFile)
        deviceImporter.importFromH5File(sourceFile)

        self.assertTrue('FooDevice' in targetFile)
        self.assertTrue('BarConstant' in targetFile['FooDevice'])
        self.assertEqual('BazValue', targetFile['FooDevice/BarConstant'][()])

    def test_canSpecifyDevicesToInclude(self):
        newDevices = {
            'FooDevice': {
                'BarConstant': 'BazValue'
            },
            'BarDevice': {
                'QuuxConstant': 'CorgeValue'
            }
        }
        targetFile = h5py.File('test_canSpecifyDevicesToInclude.h5', driver='core', backing_store=False)  # memory-only
        deviceImporter = DeviceImporter(targetFile)
        deviceImporter.importFromDict(newDevices, ['BarDevice'])

        self.assertFalse('FooDevice' in targetFile)
        self.assertTrue('BarDevice' in targetFile)

    def test_willOverwriteExistingDevices(self):
        existing = {
            'Device': {
                'Parameter': 'ExistingValue'
            }
        }
        override = {
            'Device': {
                'Parameter': 'NewValue'
            }
        }

        targetFile = h5py.File('test_willOverwriteExistingDevices.h5', driver='core',
                               backing_store=False)  # memory-only
        deviceImporter = DeviceImporter(targetFile)

        deviceImporter.importFromDict(existing)
        self.assertEqual('ExistingValue', targetFile['Device/Parameter'][()])

        deviceImporter.importFromDict(override)
        self.assertEqual('NewValue', targetFile['Device/Parameter'][()])
