import os
import platform
import sys
import json
import random

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)
from config.settings import RASPBERRY_PI_SETTINGS

class HelperFunctions:

    @staticmethod
    def is_raspberry_pi():
    #Check if running on Raspberry Pi
        return platform.system() == "Linux" and os.uname().nodename == RASPBERRY_PI_SETTINGS['OS_USERNAME']

    @staticmethod
    def createGoalCoords():
        # Load the JSON file
        with open("coordinates.json", "r") as file:
            coordinates = json.load(file)
        
        # Get the length of the coordinates list
        length = len(coordinates)
        
        # Choose a random index within the range of the list length
        random_index = random.randint(0, length - 1)
        
        # Retrieve the random set of x/y coordinates
        random_coordinates = coordinates[random_index] #Form: Python Dictionary
        
        #print(f"Random coordinates: X = {random_coordinates['X']}, Y = {random_coordinates['Y']}")
        
        return random_coordinates 