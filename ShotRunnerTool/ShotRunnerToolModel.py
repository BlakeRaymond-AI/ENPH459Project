from ScriptRunner import ScriptRunner

__author__ = 'Blake'

from LogWindowController import LogWindowController
from PyQt4 import QtCore

class ShotRunnerToolModel(object):
    def __init__(self):
        pass

    def withLogWindow(self, logWindow):
        self.logWindow = logWindow
        return self

    def withScripts(self, scripts):
        self.scripts = scripts
        return self

    def withSettingsFiles(self, parameterFiles):
        self.parameterFiles = parameterFiles
        return self

    class RunScriptsQThread(QtCore.QThread):
        def __init__(self, controllers):
            QtCore.QThread.__init__(self)
            self.controllers = controllers

        def run(self):
            for controller in self.controllers:
                controller.run()

    def runScriptsAsync(self):
        self.runners = [ScriptRunner(script) for script in self.scripts]
        self.controllers = [LogWindowController(runner, self.logWindow) for runner in self.runners]
        self.thread = self.RunScriptsQThread(self.controllers)
        self.thread.start()
