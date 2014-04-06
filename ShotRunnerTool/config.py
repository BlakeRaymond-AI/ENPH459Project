from ShotRunnerTool.FluentDictionary import FluentDictionary


settings = None
settingsDict = {}


def load(newValues):
    global settingsDict
    global settings

    settingsDict = newValues
    settings = FluentDictionary(newValues)
