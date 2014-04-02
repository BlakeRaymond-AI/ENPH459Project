__author__ = 'Blake'

from PyQt4 import QtCore


class GeneratorEmitter(QtCore.QThread):

    def __init__(self, generator, signal):
        QtCore.QThread.__init__(self)
        self.generator = generator
        self.signal = signal

    def run(self):
        for item in self.generator:
            self.signal.emit(item)
