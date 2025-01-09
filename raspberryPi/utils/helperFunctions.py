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
    def getCoordinates():
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Create the full path to highscore_status.json
        json_path = os.path.join(current_dir, "../config/coordinates.json")
        
        # Load the JSON file with the full path
        with open(json_path, "r") as file:
            coordinates = json.load(file)
        
        return coordinates

    @staticmethod
    def createGoalCoords() -> list[int]:        
        coordinates = HelperFunctions.getCoordinates()  # Use class name to call static method
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
    
    @staticmethod
    def createFollowCoords(previous: list[int], step) -> list[int]:
        previousX = previous[0]
        previousY = previous[1]
        coordinates = HelperFunctions.getCoordinates()
        halfBoardWidth = 533/2
        boardHeight = 770
        current_step = step

        while True:
            attempts = 0
            while attempts < 10:  # Try 10 times with current step size
                if previousX < -halfBoardWidth + current_step:
                    newX = previousX + current_step
                elif previousX > halfBoardWidth - current_step:
                    newX = previousX - current_step
                elif previousY < current_step:
                    newY = previousY + current_step
                elif previousY > boardHeight - current_step:
                    newY = previousY - current_step
                else:
                    newX = previousX + random.choice([current_step, -current_step, 0])
                    newY = previousY + random.choice([current_step, -current_step, 0])
                
                newCoords = [newX, newY]
                
                collision = False
                for coord in coordinates:
                    if HelperFunctions.coordsMatchCheck(newCoords, [coord['X'], coord['Y']], 25):
                        collision = True
                        break
                
                if not collision:
                    return newCoords
                attempts += 1
            
            current_step += 1  # Increase step size if no valid coordinates found

    @staticmethod
    def makeGoalCoordsLegal(coords: list[int]) -> list[int]:
        x, y = coords[0], coords[1]
        distance_from_center = (x*x + y*y) ** 0.5
        
        if distance_from_center < 150:
            # Special case for (0,0) to avoid division by zero
            if distance_from_center == 0:
                return [0, 150]  # Return a point on the circle boundary
            
            # Scale the point to lie on the circle boundary
            scale_factor = 150 / distance_from_center
            coords[0] = int(x * scale_factor)
            coords[1] = int(y * scale_factor)
            
        return coords

    @staticmethod
    def checkHighScore(infinityCount: int, timePlayed: int):
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Create the full path to highscore_status.json
        json_path = os.path.join(current_dir, "../config/highscore_status.json")
        
        # Load the JSON file with the full path
        with open(json_path, "r") as file:
            highscore_status = json.load(file)

        # Check and update the high score if necessary
        if infinityCount > highscore_status.get("infinityCount", 0):
            highscore_status["infinityCount"] = infinityCount
        
        if timePlayed > highscore_status.get("timePlayed", 0):
            highscore_status["timePlayed"] = timePlayed
        
        # Save the updated high score back to the JSON file
        with open(json_path, "w") as file:
            json.dump(highscore_status, file, indent=4)