import shutil

from PyQt4 import QtCore

from GeneratorEmitter import GeneratorEmitter
from ShotRunnerTool.ScriptRunner import ScriptRunner
from ShotRunnerTool import AutoConfigLoader
from StringSignal import StringSignal


class ShotRunnerController(QtCore.QThread):
    def __init__(self, scripts, settingsFiles, logWindow):
        QtCore.QThread.__init__(self)
        self.scripts = scripts
        self.settingsFiles = settingsFiles
        self.logWindow = logWindow

    def run(self):
        for script, settingsFile in zip(self.scripts, self.settingsFiles):
            scriptRunner = ScriptRunner(script)
            shutil.copyfile(settingsFile, AutoConfigLoader.SETTINGS_FILE_NAME)

            signal = StringSignal()
            signal.get().connect(self.logWindow.appendMessage)

            outputEmitter = GeneratorEmitter(scriptRunner.outputStream(), signal)
            outputEmitter.start()

            errorEmitter = GeneratorEmitter(scriptRunner.errorStream(), signal)
            errorEmitter.start()

            out, err = scriptRunner.execute()
            if out:
                self.logWindow.appendMessage(out)
            if err:
                self.logWindow.appendMessage(err)
