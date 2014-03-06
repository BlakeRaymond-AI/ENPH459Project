__author__ = 'Blake'

import socket

import config
import AutoConfigLoader

_ = AutoConfigLoader.SETTINGS_FILE_NAME  # prevent IDE from optimizing away the import

HOST, PORT = config.settings.TCPServer.HOST, config.settings.TCPServer.PORT
DATA = config.settings.TCPServer.DATA

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(DATA + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
    print received

finally:
    sock.close()
