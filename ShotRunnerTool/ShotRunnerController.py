import shutil
from PyQt4 import QtCore
from ShotRunnerTool.LogWindowController import LogWindowController
from ShotRunnerTool.ScriptRunner import ScriptRunner
from ShotRunnerTool import AutoConfigLoader


class ShotRunnerController(QtCore.QThread):
    def __init__(self, scripts, settingsFiles, logWindow=None):
        QtCore.QThread.__init__(self)
        self.scripts = scripts
        self.settingsFiles = settingsFiles
        self.logWindow = logWindow

    def run(self):
        for script, settingsFile in zip(self.scripts, self.settingsFiles):
            runner = ScriptRunner(script)
            shutil.copyfile(settingsFile, AutoConfigLoader.SETTINGS_FILE_NAME)
            if self.logWindow:
                controller = LogWindowController(runner, self.logWindow)
                controller.run()
            else:
                runner.execute()
