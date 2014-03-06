__author__ = 'Blake'

import unittest

import config
from ConfigLoader import ConfigLoader


class testConfigLoader(unittest.TestCase):
    class StubFileLoader(object):
        def __init__(self, settingsToReturn):
            self.settingsToReturn = settingsToReturn

        def loadDevices(self, path):
            return self.settingsToReturn

    class StubObject(object):
        def __init__(self):
            pass

    def test_loadsDeviceConstantsIntoConfig(self):
        FooDevice = self.StubObject()
        FooDevice.stringConstant = 'bar'
        FooDevice.intConstant = 1
        devices = {
            'FooDevice': FooDevice
        }
        stubLoader = self.StubFileLoader(devices)
        configLoader = ConfigLoader()
        configLoader.loadFromFile(stubLoader, None) #TODO this file interface is gross
        self.assertEqual('bar', config.settings.FooDevice.stringConstant)
        self.assertEqual(1, config.settings.FooDevice.intConstant)
