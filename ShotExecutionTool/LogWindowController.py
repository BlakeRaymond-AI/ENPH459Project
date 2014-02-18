from signals.StringSignal import StringSignal

__author__ = 'Blake'

from GeneratorEmitter import GeneratorEmitter


class LogWindowController(object):
    def __init__(self, runner, logWindow):
        self.runner = runner
        self.logWindow = logWindow
        self.signal = StringSignal()
        self.signal.get().connect(self.logWindow.appendMessage)

    def runAsync(self):
        if not self.runner.isRunning():
            self.runner.executeAsync()

        self.outputEmitter = GeneratorEmitter(self.runner.outputStream(), self.signal.get())
        self.errorEmitter = GeneratorEmitter(self.runner.errorStream(), self.signal.get())
        self.outputEmitter.start()
        self.errorEmitter.start()

    def run(self):
        if not self.runner.isRunning():
            self.runner.executeAsync()

        self.outputEmitter = GeneratorEmitter(self.runner.outputStream(), self.signal.get())
        self.errorEmitter = GeneratorEmitter(self.runner.errorStream(), self.signal.get())
        self.outputEmitter.run()
        self.errorEmitter.run()

    def join(self):
        output, error = self.runner.join()
        if output:
            self.signal.get().emit(output)
        if error:
            self.signal.get().emit(error)
        self.outputEmitter.wait()
        self.errorEmitter.wait()


from ScriptRunner import ScriptRunner
from LogWindow import LogWindow
from PyQt4 import QtGui

if __name__ == '__main__':
    app = QtGui.QApplication([])
    runner = ScriptRunner('sample.py')
    window = LogWindow(None)
    controller = LogWindowController(runner, window)
    window.show()
    controller.runAsync()
    app.exec_()
    controller.join()
