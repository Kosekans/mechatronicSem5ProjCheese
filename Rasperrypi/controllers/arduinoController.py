from config.settings import ARDUINO_SETTINGS
from models.arduinoInterface import ArduinoInterface

class ArduinoController:
    def __init__(self):
        # Initialize both Arduinos using settings
        self.arduinoAntrieb = ArduinoInterface('chaesAntrieb')
        self.arduinoZielsystem = ArduinoInterface('chaesZielsystem')
        self.connected = False

    def initialize_hardware(self):
        # Connect to both Arduinos
        arduinoAntriebConnected: bool = self.arduinoAntrieb.connect()
        arduinoZielsystemConnected: bool = self.arduinoZielsystem.connect()
        self.connected = arduinoAntriebConnected and arduinoZielsystemConnected
        return self.connected
    
    def sendMode(self, x: str):
        self.arduinoAntrieb.writeSerial("{}\n".format(x))

    def sendCoords(self, x: str):
        self.arduinoZielsystem.writeSerial("{}\n".format(x))

    def getPos(self):
        return self.arduinoAntrieb.readSerialLine()