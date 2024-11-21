import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from controllers.arduinoController import ArduinoController
from models import *
from views.viewManager import ViewManager
from utils.helperFunctions import HelperFunctions

from typing import List

class GameController:
    def __init__(self, gameState: GameState, viewManager: ViewManager, arduinoController: ArduinoController):
        self.gameState = gameState
        self.viewManager = viewManager
        self.arduinoController = arduinoController

    def launch(self):
        self.viewManager.show()

    # Click game start button from GUI
    def clickGameStart(self):
        if self.gameState.goalCoords != None:
            #chaesZielsystemCom.writeSerial(goalCoordsToString(currentGame.goalCoords,currentGame.goalCoordsVelo))
            pass

    def clickGameMode1(self):
        self.gameState.goalCoords = HelperFunctions.createGoalCoords()
        self.gameState.goalCoordsVelo = 100