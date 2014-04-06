import unittest
from ShotRunnerTool import config


class TestConfig(unittest.TestCase):
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

        FooDevice = getattr(config.settings, 'FooDevice')
        stringConstant = getattr(FooDevice, 'stringConstant')
        intConstant = getattr(FooDevice, 'intConstant')

        self.assertEqual('bar', stringConstant)
        self.assertEqual(1, intConstant)
