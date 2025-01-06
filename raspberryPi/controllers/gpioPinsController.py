# inputController.py
import time
import os
import sys
from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import platform

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from config.settings import RASPBERRY_PI_SETTINGS
from utils.gpioMock import GPIOMock
from utils.helperFunctions import HelperFunctions

# Check if running on Raspberry Pi to determine which GPIO implementation to use
isRaspberryPi = HelperFunctions.is_raspberry_pi()  # type: bool

# Import real GPIO on Pi, mock on other systems
if isRaspberryPi:
    import RPi.GPIO as GPIO
else:
    GPIO = GPIOMock()

class GpioPinsController(QObject):
    """
    Handles hardware input from GPIO pins (buttons, switches etc.).
    Inherits from QObject to enable Qt's signal/slot mechanism.
    """
    # Signal emitted when button is pressed, carries button identifier
    gpioInputEvent = pyqtSignal(str)
    
    # Pin number definitions - using BCM numbering
    BALL_EJECT_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['BALL_EJECT_PIN']  # GPIO27 physical pin 13
    BALL_FALLING_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['BALL_FALLING_PIN']  # GPIO18 physical pin 12
    START_BUTTON_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['START_BUTTON_PIN']  # GPIO17 physical pin 11
    START_BUTTON_LED_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['START_BUTTON_LED_PIN']  # GPIO22 physical pin 15
    
    def __init__(self):
        """Initialize controller and setup GPIO configurations"""
        super().__init__()
        self.setupGPIO()

        
    def setupGPIO(self):
        """
        Initialize GPIO settings and pin modes.
        Only performs actual hardware setup on Raspberry Pi.
        """
        if not isRaspberryPi:
            return
            
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.START_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.BALL_EJECT_PIN, GPIO.OUT)
            GPIO.setup(self.BALL_FALLING_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.START_BUTTON_LED_PIN, GPIO.OUT)

            # Add event detection for START_BUTTON_PIN
            GPIO.add_event_detect(self.START_BUTTON_PIN, GPIO.FALLING, callback=self.startgame, bouncetime=200)
            GPIO.add_event_detect(self.BALL_FALLING_PIN, GPIO.FALLING, callback=self.lostball, bouncetime=200)
            GPIO.add_event_detect(self.BALL_FALLING_PIN, GPIO.RISING, callback=self.balldetected, bouncetime=200)

        except Exception as e:
            print(f"GPIO Setup failed: {e}")
    
    def cleanup(self):
        GPIO.cleanup()

    def connectSignals(self, controller) -> None:
        #print(f"Controller type: {type(controller)}")
        self.gpioInputEvent.connect(controller.handleGpioInput)

    @pyqtSlot()
    def startgame(self, channel):
        """Manual trigger for start game event"""
        self.gpioInputEvent.emit("Start")

    def ejectball(self):
        p = GPIO.PWM(self.BALL_EJECT_PIN, 50) # GPIO 17 als PWM mit 50Hz
        p.start(2.5) # Initialisierung
        try:
            # Rotate to 180 degrees
            p.ChangeDutyCycle(12.5)
            time.sleep(5)  # Wait for 5 seconds
            # Return to the starting position (0 degrees)
            p.ChangeDutyCycle(2.5)
        finally:
            p.stop()
            self.cleanup()

    @pyqtSlot()
    def lostball(self):
        self.gpioInputEvent.emit("Ball lost")

    @pyqtSlot()
    def balldetected(self):
        self.gpioInputEvent.emit("Ball detected")

    def blinkStartButtonLed(self):
        while True:
            try:
                GPIO.output(self.START_BUTTON_LED_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(self.START_BUTTON_LED_PIN, GPIO.LOW)
            finally:
                self.cleanup()