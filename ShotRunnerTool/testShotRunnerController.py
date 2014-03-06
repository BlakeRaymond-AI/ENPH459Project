import os
import os.path
from unittest import TestCase
import SocketServer
import threading

import h5py

from ShotRunnerController import ShotRunnerController


__author__ = 'Blake'

HOST, PORT = "localhost", 9999
DATA = "Hello from test script"

TEST_SCRIPT = \
    '''
    import socket

    import config
    import AutoConfigLoader

    HOST, PORT = config.settings.TCPServer.HOST, config.settings.TCPServer.PORT
    DATA = config.settings.TCPServer.DATA

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(DATA + "\\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
    finally:
        sock.close()
    '''


class TestShotRunnerController(TestCase):
    def setUp(self):
        self.scriptFileName = '.testShotRunnerControllerScript.py'
        self.settingsFileName = '.testShotRunnerControllerSettings.h5'
        self.removeTempFiles()

        self.createTestScript()
        self.createTestScriptParameters()

        self.messages = []

        self.server = SocketServer.TCPServer((HOST, PORT), self.generateHandlerClass())
        self.serverThread = threading.Thread(target=self.runServer)
        self.serverThread.start()

    def removeTempFiles(self):
        if os.path.exists(self.scriptFileName):
            os.remove(self.scriptFileName)
        if os.path.exists(self.settingsFileName):
            os.remove(self.settingsFileName)

    def tearDown(self):
        self.removeTempFiles()
        self.server.shutdown()

    def runServer(self):
        self.server.serve_forever()

    def createTestScript(self):
        with open(self.scriptFileName, 'w') as f:
            f.write(TEST_SCRIPT)

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
        scripts = [self.scriptFileName]
        settingsFiles = [self.settingsFileName]
        controller = ShotRunnerController(scripts, settingsFiles)
        controller.run()
        self.assertEqual(1, len(self.messages))
        self.assertEqual(DATA, self.messages[0])
