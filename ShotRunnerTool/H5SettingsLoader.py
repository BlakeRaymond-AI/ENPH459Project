__author__ = 'Blake'

import os
import os.path

import h5py

from H5DataSetLoader import H5DataSetLoader


class H5SettingsLoader(object):
    # static member
    devicesGroupName = 'devices'

    def loadSettings(self, path):
        if not os.path.exists(path):
            raise RuntimeError('Could not find settings file %s' % path)
        h5file = h5py.File(path)
        devices = h5file[self.devicesGroupName]
        deviceSettingsDict = {}
        for deviceName, device in devices.items():
            deviceSettings = {}
            for key, value in device.items():
                loadedValue = H5DataSetLoader.load(value)
                deviceSettings[key] = loadedValue
            deviceSettingsDict[deviceName] = deviceSettings
        h5file.close()
        return deviceSettingsDict
