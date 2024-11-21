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
    def __init__(self, ):
        # Initialize both Arduinos using settings
        self.arduinoAntrieb = ArduinoInterface('chaesAntrieb')
        self.arduinoZielsystem = ArduinoInterface('chaesZielsystem')
        self.connected = False

    def initialize_hardware(self):
        # Connect to both Arduinos
        arduinoAntriebConnected = self.arduinoAntrieb.connect()
        arduinoZielsystemConnected = self.arduinoZielsystem.connect()
        self.connected = arduinoAntriebConnected and arduinoZielsystemConnected
        return self.connected
    
    def sendMode(self, x: str):
        self.arduinoAntriebConnected.write
        
    