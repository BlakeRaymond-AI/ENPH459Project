import subprocess
from subprocess import PIPE
import sys


class ScriptRunner(object):
    def __init__(self, scriptPath):
        self.scriptPath = scriptPath
        self.running = False
        self.process = None

    def _start(self):
        self.process = subprocess.Popen([sys.executable, self.scriptPath], stdout=PIPE, stderr=PIPE)
        self.running = True

    def isRunning(self):
        return self.running

    def execute(self):
        if self.running:
            raise RuntimeError('Subprocess already started')
        self._start()
        out, err = self.join()
        self.running = False
        return out, err

    def executeAsync(self):
        if self.running:
            raise RuntimeError('Subprocess already started')
        self._start()

    def join(self):
        if not self.running:
            raise RuntimeError('Subprocess not started')
        self.process.wait()
        self.running = False
        return None, None

    def wait(self):
        if not self.running:
            raise RuntimeError('Subprocess not started')
        self.process.wait()
        self.running = False
