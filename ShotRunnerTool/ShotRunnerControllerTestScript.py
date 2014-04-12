import socket
from ShotRunnerTool import config
from ShotRunnerTool import AutoConfigLoader


_ = AutoConfigLoader.SETTINGS_FILE_NAME  # prevent IDE from optimizing away the import

HOST, PORT = config.settingsDict['TCPServer']['HOST'], config.settingsDict['TCPServer']['PORT']
DATA = config.settingsDict['TCPServer']['DATA']


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
