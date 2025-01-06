# inputController.py
import time
import os
import sys
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import platform
import RPi.GPIO as GPIO

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from config.settings import RASPBERRY_PI_SETTINGS

class GpioPinsController(QObject):
    START_BUTTON_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['START_BUTTON_PIN']  # GPIO22 physical pin 15
    
    def __init__(self):
        super().__init__()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.START_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.setupGPIO()
    
    def setupGPIO(self):
        GPIO.add_event_detect(self.START_BUTTON_PIN, GPIO.FALLING, callback=self.startgame, bouncetime=200)
    
    def cleanup(self):
        GPIO.cleanup()

    def startgame(self):
        """when the physical start button is pressed, print 'Start'"""
        print("Start button pressed")

if __name__ == "__main__":
    controller = GpioPinsController()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller.cleanup()
