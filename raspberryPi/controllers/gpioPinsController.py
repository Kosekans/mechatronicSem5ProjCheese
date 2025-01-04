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
    buttonClicked = pyqtSignal(str)
    
    # Pin number definitions - using BCM numbering
    START_BUTTON_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['START_BUTTON_PIN']
    BALL_FALLING_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['BALL_FALLING_PIN']
    BALL_EJECT_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['BALL_EJECT_PIN']
    pins = [START_BUTTON_PIN, BALL_FALLING_PIN, BALL_EJECT_PIN]
    
    def __init__(self):
        """Initialize controller and setup GPIO configurations"""
        super().__init__()  # Initialize QObject parent
        self._last_tick = {self.START_BUTTON_PIN: 0, self.BALL_FALLING_PIN: 0, self.BALL_EJECT_PIN: 0}
        self._input_state = {self.START_BUTTON_PIN: False, self.BALL_FALLING_PIN: False, self.BALL_EJECT_PIN: False}
        self.setupGPIO()  # Fix: Call correct method name
        
    def setupGPIO(self):
        """
        Initialize GPIO settings and pin modes.
        Only performs actual hardware setup on Raspberry Pi.
        """
        if not isRaspberryPi:
            return
            
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            for pin in self.pins:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                # Handle both edges for more reliable detection
                GPIO.add_event_detect(
                    pin,
                    GPIO.BOTH,  # Detect both RISING and FALLING edges
                    callback=self._edge_callback,
                    bouncetime=20  # Reduced for better responsiveness
                )
        except Exception as e:
            print(f"GPIO Setup failed: {e}")
    
    def _edge_callback(self, channel):
        """Low-level interrupt callback with debouncing and edge detection"""
        import time
        current_tick = time.time() * 1000  # Get current time in ms
        
        # Software debouncing with time checking
        if (current_tick - self._last_tick[channel]) <= 20:  # 20ms debounce
            return
            
        self._last_tick[channel] = current_tick
        
        # Read actual pin state
        state = not GPIO.input(channel)  # Inverted because of pull-up
        if state == self._input_state[channel]:  # Ignore if state hasn't changed
            return
            
        self._input_state[channel] = state
        
        # Only trigger on button press (False->True transition)
        if state:
            self.inputCallback(channel)
    
    def inputCallback(self, channel):
        """
        Callback triggered by button press.
        Emits buttonClicked signal with "startGame" identifier.
        """
        if channel == self.START_BUTTON_PIN:
            self.buttonClicked.emit(self.START_BUTTON_PIN)
        if channel == self.BALL_FALLING_PIN:
            self.buttonClicked.emit(self.BALL_FALLING_PIN)
        if channel == self.BALL_EJECT_PIN:
            self.buttonClicked.emit(self.BALL_EJECT_PIN)
    
    def cleanup(self):
        GPIO.cleanup()

    def connectSignals(self, controller) -> None:
        self.buttonClicked.connect(controller.handleButtonClicked)

    def 
    @pyqtSlot(str)
    def onButtonClick(self, button_id: str) -> None:
        self.buttonClicked.emit(button_id)

    def ejectball(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BALL_EJECT_PIN, GPIO.OUT)

        p = GPIO.PWM(BALL_EJECT_PIN, 50) # GPIO 17 als PWM mit 50Hz
        p.start(2.5) # Initialisierung
        try:
            # Rotate to 180 degrees
            p.ChangeDutyCycle(12.5)
            print("Ejecting ball")
            time.sleep(5)  # Wait for 5 seconds
            # Return to the starting position (0 degrees)
            p.ChangeDutyCycle(2.5)
        finally:
            print("Servo in starting position")
            p.stop()
            GPIO.cleanup()

    def lostball(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BALL_FALLING_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up pin as input with pull-up resistor

        try:
            input_state = GPIO.input(BALL_FALLING_PIN)
            if input_state == GPIO.LOW:
                print("Ball falling detected")
        finally:
            GPIO.cleanup()

    def startgame(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(START_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set up pin as input with pull-up resistor

        try:
            input_state = GPIO.input(START_BUTTON_PIN)
            if input_state == GPIO.LOW:
                print("Button pressed")
        finally:
            GPIO.cleanup()    

    def blinkStartButtonLed(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(START_BUTTON_LED_PIN, GPIO.OUT)

        while True:
            try:
                GPIO.output(START_BUTTON_LED_PIN, GPIO.HIGH)
                time.sleep(1)
                GPIO.output(START_BUTTON_LED_PIN, GPIO.LOW)
            finally:
                GPIO.cleanup()