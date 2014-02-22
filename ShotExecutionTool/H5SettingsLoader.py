__author__ = 'Blake'

import os
import os.path

import h5py

from H5DataSetLoader import H5DataSetLoader


class H5SettingsLoader(object):
    devicesGroupName = 'devices'

    class Settings(object):
        def __init__(self):
            pass

    def __init__(self):
        pass

    def loadSettings(self, path):
        deviceSettings = self.loadDevices(path)
        settings = self.Settings()
        for deviceName, device in deviceSettings.items():
            setattr(settings, deviceName, device)
        return settings

    def loadDevices(self, path):
        if not os.path.exists(path):
            raise RuntimeError('Could not find settings file %s' % path)
        h5file = h5py.File(path)
        devices = h5file[self.devicesGroupName]
        deviceSettingsDict = {}
        for deviceName, device in devices.items():
            deviceSettings = self.Settings()
            for key, value in device.items():
                loadedValue = H5DataSetLoader.load(value)
                setattr(deviceSettings, key, loadedValue)
            deviceSettingsDict[deviceName] = deviceSettings
        h5file.close()
        return deviceSettingsDict
