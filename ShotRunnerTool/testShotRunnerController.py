import os
import os.path
import shutil
from unittest import TestCase
import SocketServer
import threading

import h5py
from PyQt4 import QtGui

import AutoConfigLoader

from LogWindow import LogWindow
from ShotRunnerController import ShotRunnerController


__author__ = 'Blake'

HOST, PORT = "localhost", 9999
DATA = "Hello from test script"
TEST_SCRIPT = "ShotRunnerControllerTestScript.py"


class TestShotRunnerController(TestCase):
    def setUp(self):
        self.settingsFileName = '.testShotRunnerControllerSettings.h5'
        self.removeTempFiles()
        self.createTestScriptParameters()
        self.backupDefaultSettings()

        self.messages = []

        self.server = SocketServer.TCPServer((HOST, PORT), self.generateHandlerClass())
        self.serverThread = threading.Thread(target=self.runServer)
        self.serverThread.start()

    def backupDefaultSettings(self):
        self.defaultSettingsFileBackup = '.shot_parameters.h5.backup'
        shutil.copyfile(AutoConfigLoader.SETTINGS_FILE_NAME, self.defaultSettingsFileBackup)

    def restoreDefaultSettings(self):
        shutil.copyfile(self.defaultSettingsFileBackup, AutoConfigLoader.SETTINGS_FILE_NAME)
        os.remove(self.defaultSettingsFileBackup)

    def removeTempFiles(self):
        if os.path.exists(self.settingsFileName):
            os.remove(self.settingsFileName)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.serverThread.join()
        self.removeTempFiles()
        self.restoreDefaultSettings()

    def runServer(self):
        self.server.serve_forever()

    def generateHandlerClass(self):
        messages = self.messages

        class TCPHandler(SocketServer.BaseRequestHandler):
            def handle(self):
                data = self.request.recv(1024).strip()
                messages.append(data)
                # just send back the same data
                self.request.sendall(data)

        return TCPHandler

    def createTestScriptParameters(self):
        h5File = h5py.File(self.settingsFileName)
        devices = h5File.create_group('devices')
        tcpServer = devices.create_group('TCPServer')
        tcpServer['HOST'] = HOST
        tcpServer['PORT'] = PORT
        tcpServer['DATA'] = DATA
        h5File.close()

    def test_canRunScriptWithInjectedParameters(self):
        scripts = ['ShotRunnerControllerTestScript.py']
        settingsFiles = [self.settingsFileName]
        controller = ShotRunnerController(scripts, settingsFiles)
        controller.run()
        self.assertEqual(1, len(self.messages))
        self.assertEqual(DATA, self.messages[0])

    def test_canConnectLogWindowToController(self):
        app = QtGui.QApplication([])
        logWindow = LogWindow(None)
        scripts = [TEST_SCRIPT]
        settingsFiles = [self.settingsFileName]
        controller = ShotRunnerController(scripts, settingsFiles, logWindow=logWindow)
        controller.run()
        self.assertEqual(DATA, str(logWindow.toPlainText()).strip())

    def test_canRunAsynchronously(self):
        app = QtGui.QApplication([])
        logWindow = LogWindow(None)
        scripts = [TEST_SCRIPT]
        settingsFiles = [self.settingsFileName]
        controller = ShotRunnerController(scripts, settingsFiles, logWindow=logWindow)
        controller.finished.connect(app.quit)
        controller.start()
        app.exec_()
        self.assertEqual(DATA, str(logWindow.toPlainText()).strip())

    def test_canRunMultipleScripts(self):
        numberOfScripts = 2
        scripts = [TEST_SCRIPT] * numberOfScripts
        settingsFiles = [self.settingsFileName] * numberOfScripts
        controller = ShotRunnerController(scripts, settingsFiles)
        controller.run()
        self.assertListEqual([DATA] * numberOfScripts, self.messages)

    def test_canRunMultipleScriptsAsynchronously(self):
        app = QtGui.QApplication([])
        logWindow = LogWindow(None)
        numberOfScripts = 2
        scripts = [TEST_SCRIPT] * numberOfScripts
        settingsFiles = [self.settingsFileName] * numberOfScripts
        controller = ShotRunnerController(scripts, settingsFiles, logWindow=logWindow)
        controller.finished.connect(app.quit)

        controller.start()
        app.exec_()

        messages = str(logWindow.toPlainText()).strip().splitlines()
        self.assertListEqual([DATA] * numberOfScripts, messages)
