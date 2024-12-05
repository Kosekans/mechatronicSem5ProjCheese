# inputController.py
import os
import sys
from pathlib import Path

# Add parent directory to system path
current_dir = Path(__file__).parent
parent_dir = str(current_dir.parent)
sys.path.append(parent_dir)

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import platform

from config.settings import RASPBERRY_PI_SETTINGS
from utils.gpioMock import GPIOMock

# Check if running on Raspberry Pi to determine which GPIO implementation to use
isRasperrypi: bool = platform.system() == "Linux" and os.uname().nodename == RASPBERRY_PI_SETTINGS['OS_USERNAME']

# Import real GPIO on Pi, mock on other systems
if isRasperrypi:
    import RPi.GPIO as GPIO
else:
    GPIO = GPIOMock()

class InputController(QObject):
    """
    Handles hardware input from GPIO pins (buttons, switches etc.).
    Inherits from QObject to enable Qt's signal/slot mechanism.
    """
    # Signal emitted when button is pressed, carries button identifier
    buttonClicked = pyqtSignal(str)
    
    # Pin number definitions - using BCM numbering
    START_BUTTON_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['START_BUTTON_PIN']
    LIGHT_SENSOR_PIN = RASPBERRY_PI_SETTINGS['GPIO_PINS']['LIGHT_BARRIER_PIN']
    
    def __init__(self):
        """Initialize controller and setup GPIO configurations"""
        super().__init__()  # Initialize QObject parent
        self._last_tick = {self.START_BUTTON_PIN: 0, self.LIGHT_SENSOR_PIN: 0}
        self._input_state = {self.START_BUTTON_PIN: False, self.LIGHT_SENSOR_PIN: False}
        self.setupGPIO()  # Fix: Call correct method name
        
    def setupGPIO(self):
        """
        Initialize GPIO settings and pin modes.
        Only performs actual hardware setup on Raspberry Pi.
        """
        if not isRasperrypi:
            return
            
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            
            for pin in [self.START_BUTTON_PIN, self.LIGHT_SENSOR_PIN]:
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
            self.buttonClicked.emit("startGame")
        if channel == self.LIGHT_SENSOR_PIN:
            self.buttonClicked.emit("lightSensor")
    
    def cleanup(self):
        GPIO.cleanup()

    def connectSignals(self, controller) -> None:
        self.buttonClicked.connect(controller.handleButtonClicked)

    @pyqtSlot(str)
    def onButtonClick(self, button_id: str) -> None:
        self.buttonClicked.emit(button_id)