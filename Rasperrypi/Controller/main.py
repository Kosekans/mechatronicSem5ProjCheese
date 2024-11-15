import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

# Now import the Model package
from Model import *

from typing import List

#chaesAntriebCom = Com('COM1', 9600, .1)
#chaesZielsystemCom = Com('COM2', 9600, .1)

# Main code
def main():
    return

def createGoalCoords():
    goalCoords = [2341, 2134]
    return goalCoords

# Click game start button from GUI
def clickGameStart():
    if currentGame.goalCoords != None:
        #chaesZielsystemCom.writeSerial(goalCoordsToString(currentGame.goalCoords,currentGame.goalCoordsVelo))
        pass

def clickGameMode1():
    goalCoords = createGoalCoords()
    goalCoordsVelo = 100
    global currentGame
    currentGame = gameState("1", goalCoords, goalCoordsVelo)

if __name__ == "__main__":
    main()