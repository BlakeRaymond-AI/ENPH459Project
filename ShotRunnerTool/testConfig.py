__author__ = 'Blake'

import unittest

import config


class testConfig(unittest.TestCase):
    def test_loadsDeviceConstantsIntoConfig(self):
        devices = {
            'FooDevice': {
                'stringConstant': 'bar',
                'intConstant': 1
            }
        }
        config.load(devices)

        self.assertEqual('bar', config.settingsDict['FooDevice']['stringConstant'])
        self.assertEqual(1, config.settingsDict['FooDevice']['intConstant'])

    def test_loadsSettingsAsFluentDictionary(self):
        devices = {
            'FooDevice': {
                'stringConstant': 'bar',
                'intConstant': 1
            }
        }
        config.load(devices)

        self.assertEqual('bar', config.settings.FooDevice.stringConstant)
        self.assertEqual(1, config.settings.FooDevice.intConstant)
