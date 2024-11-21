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
        self.port = self.settings['PORT']
        self.baud_rate = self.settings['BAUD_RATE']
        self.timeout = self.settings['TIMEOUT']
        self.bytesize = self.settings['BYTESIZE']
        self.connection = None

    def connect(self):
        self.connection = SerialCommunication.create_connection(
            self.port,
            self.baud_rate,
            self.timeout,
            self.bytesize
        )
        return self.connection is not None
    
    def writeSerial(self, x: str):
        self.connection.write(bytes(x, 'utf-8'))

    def readSerialLine(self):
        data: str = self.connection.readLine()#.decode('utf-8').strip()
        return data