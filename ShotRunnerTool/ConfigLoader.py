__author__ = 'Blake'

import config


class ConfigLoader(object):
    def __init__(self):
        pass

    def addDevice(self, device, deviceName):
        if hasattr(config.settings, deviceName):
            raise RuntimeError('Config already has device named \'%s\'' % deviceName)
        setattr(config.settings, deviceName, device)

    def loadFromFile(self, fileLoader, path):
        devices = fileLoader.loadDevices(path)
        for deviceName, device in devices.items():
            self.addDevice(device, deviceName)
