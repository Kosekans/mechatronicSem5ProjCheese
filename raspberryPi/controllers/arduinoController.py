import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from config.settings import ARDUINO_SETTINGS
from models.arduinoInterface import ArduinoInterface

class ArduinoController:
    def __init__(self):
        # Initialize both Arduinos using settings
        self.arduinoAntrieb = ArduinoInterface('chaesAntrieb')
        self.arduinoZielsystem = ArduinoInterface('chaesZielsystem')
        self.connected = False

    def updatePorts(self) -> bool:
        try:
            antriebPortUpdated = self.arduinoAntrieb.updatePortSettings()
            zielsystemPortUpdated = self.arduinoZielsystem.updatePortSettings()
            self.connected = antriebPortUpdated and zielsystemPortUpdated
            return self.connected
        except Exception as e:
            print(f"Error updating ports: {e}")
            self.connected = False
            return False

    def initializeHardware(self) -> bool:
        try:
            if not self.connected:
                return False
            arduinoAntriebConnected = self.arduinoAntrieb.connect()
            arduinoZielsystemConnected = self.arduinoZielsystem.connect()
            self.connected = arduinoAntriebConnected and arduinoZielsystemConnected
            return self.connected
        except Exception as e:
            print(f"Error initializing hardware: {e}")
            self.connected = False
            return False
    
    def sendMode(self, x: str):
        self.arduinoAntrieb.writeSerial("{}\n".format(x))

    def sendCoords(self, x: str):
        self.arduinoZielsystem.writeSerial("{}\n".format(x))

    def getPos(self):
        return self.arduinoAntrieb.readSerialLine()