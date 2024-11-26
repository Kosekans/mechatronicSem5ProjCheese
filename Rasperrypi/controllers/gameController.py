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
        # Connect the signal to the method
        self.viewManager.buttonClicked.connect(self.handleButtonClicked)
    
    def handleButtonClicked(self, buttonId: str):
        # Dictionary to map button IDs to their corresponding methods
        button_actions = {
            'startGame': self.clickStartGame,
            'Select Gamemode': self.clickSelectGameMode,
            'Ring zeigt Ziel': self.clickGMGoal,
            'Verfolgungsmodus': self.clickGMFollow,
            'settings': self.clickSettings,
            'credits': self.clickCredits,
            'highscore': self.clickHighscore,
            'SaveSettings': self.clickSaveSettings,
            'back': self.clickBack
        }
        
        # Call the corresponding method if button ID exists
        action = button_actions.get(buttonId)
        if action:
            try:
                action()
            except Exception as e:
                # Show error to user through ViewManager
                self.viewManager.showWarning(str(e))

    #buttons from GUI
    def clickStartGame(self):
        # Validate game state before proceeding
        if self.gameState.gameMode is None:
            raise ValueError("Please select Game Mode first")
        # Proceed with game start logic
        #chaesZielsystemCom.writeSerial(goalCoordsToString(currentGame.goalCoords,currentGame.goalCoordsVelo))
        pass

    def clickSettings(self):
        self.viewManager.navigateToPage('settings')

    def clickCredits(self):
        self.viewManager.navigateToPage('credits')
    
    def clickHighscore(self):
        self.viewManager.navigateToPage('highscore')

    def clickSelectGameMode(self):
        self.gameState.gameMode = None

    def clickGMGoal(self):
        # Set goal coordinates for Game Mode 1
        self.gameState.gameMode = 'goal'
        self.gameState.goalCoords = HelperFunctions.createGoalCoords()
        self.gameState.goalCoordsVelo = 100
    
    def clickGMFollow(self):
        self.gameState.gameMode = 'follow'

    def clickSaveSettings(self):
        # Save settings to (maybe???????????) config file or sertain model object
        pass

    def clickBack(self):
        self.viewManager.goBack()