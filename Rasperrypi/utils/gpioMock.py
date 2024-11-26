class GPIOMock:
    """
    Mock implementation of RPi.GPIO for development on non-Raspberry Pi systems.
    Provides the same interface as RPi.GPIO but with no actual hardware interaction.
    """
    # Constants matching RPi.GPIO pin numbering modes and states
    BCM = "BCM"      # Broadcom chip-specific pin numbers
    IN = "IN"        # Pin mode for inputs
    PUD_UP = "PUD_UP"  # Internal pull-up resistor configuration
    FALLING = "FALLING"  # Trigger on falling edge (button press)
    
    # Static methods are used because RPi.GPIO uses class-level methods
    # that don't require instance state
    @staticmethod
    def setmode(mode): 
        """Mock setting the pin numbering mode (BCM or BOARD)"""
        pass
    
    @staticmethod
    def setwarnings(flag):
        """Mock enabling/disabling GPIO warnings"""
        pass
    
    @staticmethod
    def setup(channel, mode, pull_up_down=None):
        """Mock configuring a GPIO pin's mode and pull resistor"""
        pass
    
    @staticmethod
    def add_event_detect(channel, edge, callback=None, bouncetime=None):
        """Mock setting up event detection on a GPIO pin"""
        pass
    
    @staticmethod
    def cleanup():
        """Mock cleaning up GPIO configurations"""
        pass