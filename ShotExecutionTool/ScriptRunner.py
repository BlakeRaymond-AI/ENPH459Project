__author__ = 'Blake'

import subprocess
from subprocess import PIPE
import sys


class ScriptRunner(object):
    def __init__(self, scriptPath):
        self.scriptPath = scriptPath
        self.running = False

    def _start(self):
        self.process = subprocess.Popen([sys.executable, self.scriptPath], stdout=PIPE, stderr=PIPE)
        self.running = True

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
        out, err = self.process.communicate()
        self.running = False
        return out, err

    def getOutputStream(self):
        if not self.running:
            raise RuntimeError('Subprocess not started')
        return self.process.stdout

    def getErrorStream(self):
        if not self.running:
            raise RuntimeError('Subprocess not started')
        return self.process.stderr