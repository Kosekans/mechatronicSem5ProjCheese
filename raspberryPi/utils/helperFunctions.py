import os
import platform
import sys
# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
from config.settings import RASPBERRY_PI_SETTINGS

class HelperFunctions:

    @staticmethod
    def is_raspberry_pi():
        # Check if running on Raspberry Pi
        if platform.system() != "Linux":
            return False
        try:
            with open('/proc/device-tree/model') as model_file:
                model = model_file.read().lower()
                return 'raspberry pi' in model
        except FileNotFoundError:
            return False

    @staticmethod
    def createGoalCoords():
        goalCoords: list[int] = [2341, 2134]
        return goalCoords