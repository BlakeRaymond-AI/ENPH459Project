import shutil

from PyQt4 import QtCore

from ShotRunnerTool.ScriptRunner import ScriptRunner
from ShotRunnerTool import AutoConfigLoader
from StringSignal import StringSignal


class StandardOutputReader(QtCore.QThread):
    def __init__(self, scriptRunner, signal):
        QtCore.QThread.__init__(self)
        self.scriptRunner = scriptRunner
        self.signal = signal

    def run(self):
        process = self.scriptRunner.process
        while process.poll() is None:
            line = process.stdout.readline()
            if line:
                self.signal.get().emit(line)


class StandardErrorReader(QtCore.QThread):
    def __init__(self, scriptRunner, signal):
        QtCore.QThread.__init__(self)
        self.scriptRunner = scriptRunner
        self.signal = signal

    def run(self):
        process = self.scriptRunner.process
        while process.poll() is None:
            line = process.stderr.readline()
            if line:
                self.signal.get().emit(line)


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

            outputReader = StandardOutputReader(scriptRunner, signal)
            errorReader = StandardErrorReader(scriptRunner, signal)

            scriptRunner.executeAsync()

            outputReader.start()
            errorReader.start()

            scriptRunner.wait()
            outputReader.wait()
            errorReader.wait()
