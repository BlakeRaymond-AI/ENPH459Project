from ShotRunnerTool.GeneratorEmitter import GeneratorEmitter
from ShotRunnerTool.StringSignal import StringSignal


class LogWindowController(object):
    def __init__(self, runner, logWindow):
        self.runner = runner
        self.logWindow = logWindow
        self.signal = StringSignal()
        self.signal.get().connect(self.logWindow.appendMessage)
        self.outputEmitter = None
        self.errorEmitter = None

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
