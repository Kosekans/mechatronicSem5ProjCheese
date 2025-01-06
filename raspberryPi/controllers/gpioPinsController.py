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
        print("Initializing GpioPinsController...")
        self.setupGPIO()
        print("GPIO setup completed")
        
    def setupGPIO(self):
        """
        Initialize GPIO settings and pin modes.
        Only performs actual hardware setup on Raspberry Pi.
        """
        if not isRaspberryPi:
            return
            
        try:
            print("Setting up GPIO pins...")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.START_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            print(f"START_BUTTON_PIN {self.START_BUTTON_PIN} configured")
            GPIO.setup(self.BALL_EJECT_PIN, GPIO.OUT)
            print(f"BALL_EJECT_PIN {self.BALL_EJECT_PIN} configured")
            GPIO.setup(self.BALL_FALLING_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            print(f"BALL_FALLING_PIN {self.BALL_FALLING_PIN} configured")
            GPIO.setup(self.START_BUTTON_LED_PIN, GPIO.OUT)
            print(f"START_BUTTON_LED_PIN {self.START_BUTTON_LED_PIN} configured")

            # Add event detection for START_BUTTON_PIN
            GPIO.add_event_detect(self.START_BUTTON_PIN, GPIO.FALLING, callback=self.startgame, bouncetime=200)
            print("Event detection added for START_BUTTON_PIN")
            GPIO.add_event_detect(self.BALL_FALLING_PIN, GPIO.FALLING, callback=self.lostball, bouncetime=200)
            print("Event falling detection added for BALL_FALLING_PIN")
            GPIO.add_event_detect(self.BALL_FALLING_PIN, GPIO.RISING, callback=self.balldetected, bouncetime=200)
            print("Event rising detection added for BALL_FALLING_PIN")


        except Exception as e:
            print(f"GPIO Setup failed: {e}")
    
    def cleanup(self):
        GPIO.cleanup()

    def connectSignals(self, controller) -> None:
        #print(f"Controller type: {type(controller)}")
        self.gpioInputEvent.connect(controller.handleGpioInput)
        print("Testing signal emission...")
        self.gpioInputEvent.emit("Test")  # Test signal emission
        print("GPIO signals connected")

    @pyqtSlot()
    def startgame(self, channel):
        """Manual trigger for start game event"""
        print(f"GPIO: Button press detected on pin {channel}")
        print("Emitting Start signal...")
        self.gpioInputEvent.emit("Start")
        print("Signal emitted")

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