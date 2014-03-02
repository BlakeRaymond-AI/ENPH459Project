__author__ = 'Blake'

# This logic is here to facilitate a very simple API for writing experiment scripts.
# The runner tool will create a settings file by this name with the shot parameters.
# By importing this file, the shot parameters are automatically loaded into the config module.

import os.path

from ConfigLoader import ConfigLoader
from H5SettingsLoader import H5SettingsLoader


SETTINGS_FILE_NAME = '.shot_parameters.h5'
SETTINGS_LOADER = H5SettingsLoader()
CONFIG_LOADER = ConfigLoader()


class ConfigError(RuntimeError):
    def __init__(self, msg):
        RuntimeError.__init__(self, msg)


if os.path.exists(SETTINGS_FILE_NAME):
    try:
        CONFIG_LOADER.loadFromFile(SETTINGS_LOADER, SETTINGS_FILE_NAME)
    except:
        raise ConfigError('Could not load device parameters from default settings file: \'%s\'' % SETTINGS_FILE_NAME)
else:
    raise ConfigError('Could not find default settings file \'%s\'' % SETTINGS_FILE_NAME)
