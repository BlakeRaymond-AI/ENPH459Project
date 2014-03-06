import shutil

from ScriptRunner import ScriptRunner
import AutoConfigLoader


__author__ = 'Blake'


class ShotRunnerController(object):
    def __init__(self, scripts, settingsFiles):
        self.scripts = scripts
        self.settingsFiles = settingsFiles

    def run(self):
        for script, settingsFile in zip(self.scripts, self.settingsFiles):
            runner = ScriptRunner(script)
            shutil.copyfile(settingsFile, AutoConfigLoader.SETTINGS_FILE_NAME)
            runner.execute()

