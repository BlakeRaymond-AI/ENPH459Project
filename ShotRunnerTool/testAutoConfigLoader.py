from FluentDictionary import FluentDictionary

__author__ = 'Blake'

import unittest
import config
import AutoConfigLoader


class testAutoConfigLoader(unittest.TestCase):
    def tearDown(self):
        config.settings = FluentDictionary({})

    def test_loadsFromDefaultFileOnImportModule(self):
        self.assertIsNotNone(AutoConfigLoader.SETTINGS_FILE_NAME) # prevent PyCharm from optimizing away the import

        self.assertEqual('bar', config.settings.FooDevice.stringConstant)
        self.assertEqual(1, config.settings.FooDevice.intConstant)
