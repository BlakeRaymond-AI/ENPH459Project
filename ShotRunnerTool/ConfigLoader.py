from FluentDictionary import FluentDictionary

__author__ = 'Blake'

import config


class ConfigLoader(object):
    def __init__(self):
        pass

    def load(self, settingsDict):
        config.settingsDict = settingsDict
        config.settings = FluentDictionary(settingsDict)
