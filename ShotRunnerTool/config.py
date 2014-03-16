from FluentDictionary import FluentDictionary

__author__ = 'Blake'


def load(newValues):
    global settingsDict
    global settings

    settingsDict = newValues
    settings = FluentDictionary(newValues)
