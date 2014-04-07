import os
import os.path
import h5py
from ShotRunnerTool import H5DataSetLoader


DEVICES_GROUP_NAME = 'devices'


def loadSettings(path):
    if not os.path.exists(path):
        raise RuntimeError('Could not find settings file %s' % path)
    h5file = h5py.File(path)
    devices = h5file[DEVICES_GROUP_NAME]
    deviceSettingsDict = {}
    for deviceName, device in devices.items():
        deviceSettings = {}
        for key, value in device.items():
            loadedValue = H5DataSetLoader.load(value)
            deviceSettings[key] = loadedValue
        deviceSettingsDict[deviceName] = deviceSettings
    h5file.close()
    return deviceSettingsDict
