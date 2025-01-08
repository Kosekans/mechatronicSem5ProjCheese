import platform
import json
import random
import os

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
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Create the full path to coordinates.json
        json_path = os.path.join(current_dir, "coordinates.json")
        
        # Load the JSON file with the full path
        with open(json_path, "r") as file:
            coordinates = json.load(file)
        
        # Get the length of the coordinates list
        length = len(coordinates)
        
        # Choose a random index within the range of the list length
        random_index = random.randint(0, length - 1)
        
        # Retrieve the random set of x/y coordinates
        random_coordinates = coordinates[random_index] #Form: Python Dictionary

        coordsList = [random_coordinates['X'], random_coordinates['Y']]
        
        return coordsList
    
    @staticmethod
    def coordsMatchCheck(coords1: list[int], coords2: list[int], tolerance: int) -> bool:
        return abs(coords1[0] - coords2[0]) <= tolerance and abs(coords1[1] - coords2[1]) <= tolerance