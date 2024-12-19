import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from config.settings import ARDUINO_SETTINGS
from utils.serialCommunication import SerialCommunication

class ArduinoInterface:
    def __init__(self, arduino_id: str):
        # Use settings from config file
        self.settings = ARDUINO_SETTINGS[arduino_id]
        self.id = self.settings['ID']
        self.port: str = None
        self.baudRate = self.settings['BAUD_RATE']
        self.timeout = self.settings['TIMEOUT']
        self.bytesize = self.settings['BYTESIZE']
        self.characterEncoding = self.settings['CHARACTER_ENCODING']
        self.connection = None

    def connect(self):
        self.connection = SerialCommunication.create_connection(
            self.port,
            self.baudRate,
            self.timeout,
            self.bytesize
        )
        return self.connection is not None
    
    def writeSerial(self, x: str):
        self.connection.write(bytes(x, self.characterEncoding))

    def readSerialLine(self):
        data: str = self.connection.readline().decode(self.characterEncoding).strip()
        return data
    
    def updatePortSettings(self):
        print("looking for Arduino: ", self.id)
        connectedPorts = SerialCommunication.findConnectedPorts(
            self.baudRate,
            self.timeout,
            self.bytesize
        )
        print("connected ports:", ", ".join(connectedPorts))
        for port in connectedPorts:
            print("testing port", port)
            answer: str = SerialCommunication.testComunication(
                port,
                self.baudRate,
                self.timeout,
                self.bytesize,
                self.characterEncoding,
                'ID\n'
            )
            print("serial test connection answer: ", answer)
            if answer == self.id:
                self.port = port
                return True
        print(self.id, "Arduino not found")
        return False
