__author__ = 'Blake'

import unittest
from config import *
from ConfigLoader import ConfigLoader


class ConfigLoaderTests(unittest.TestCase):
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
        self.assertEqual('bar', settings.FooDevice.stringConstant)
        self.assertEqual(1, settings.FooDevice.intConstant)
