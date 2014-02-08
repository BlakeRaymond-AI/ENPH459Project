__author__ = 'Blake'

from threading import Thread, Lock, Event

import subprocess
import sys
from PyQt4 import QtGui

REFRESH_TIME_IN_SECONDS = 25. / 1000


class ConsoleController(object):
    def __init__(self, textWidget, streams):
        self.textWidget = textWidget
        self.streams = streams

        self.lock = Lock()
        self.quitting = Event()
        self.threads = [Thread(target=self._copyStreamToWidget, args=[stream]) for stream in self.streams]
        for thread in self.threads:
            thread.start()

    def join(self):
        self.quitting.set()
        for thread in self.threads:
            thread.join()

    def _copyStreamToWidget(self, stream):
        for line in stream:
            self.lock.acquire()
            self.textWidget.insertPlainText(line)
            self.lock.release()
            if self.quitting.isSet():
                break


if __name__ == '__main__':
    p = subprocess.Popen([sys.executable, 'sample.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    app = QtGui.QApplication([])
    wnd = QtGui.QPlainTextEdit(None)
    cont = ConsoleController(wnd, [p.stdout])
    wnd.show()
    app.exec_()
    p.wait()
    cont.join()
    app.exit()
