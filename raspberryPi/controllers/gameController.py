import sys
import os
from PyQt5.QtCore import QObject, pyqtSignal

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from controllers import *
from models import *
from views.viewManager import ViewManager
from utils.helperFunctions import HelperFunctions
from config.settings import ERROR_MESSAGES, GAME_SETTINGS

class GameController(QObject):
    gameStateChanged = pyqtSignal(dict)
    
    def __init__(self, gameState: GameState, viewManager: ViewManager, arduinoController: ArduinoController, inputController: GpioPinsController):
        super().__init__()  # Initialize QObject
        self.gameState = gameState
        self.viewManager = viewManager
        self.arduinoController = arduinoController
        self.inputController = inputController
        self.inputController.buttonClicked.connect(self.handleButtonClicked)
        
        # Initialize hardware state
        self.gameState.portsFound = False
        self.gameState.hardwareInitialized = False
        
        # Try to initialize hardware
        if self.arduinoController.updatePorts():
            self.gameState.portsFound = True
            if self.arduinoController.initializeHardware():
                self.gameState.hardwareInitialized = True

    
    def setupGame(self):
        if self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['follow']:
            pass#todo
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['goal']:
            #chaesZielsystemCom.writeSerial(goalCoordsToString(currentGame.goalCoords,currentGame.goalCoordsVelo))
            pass#todo
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['infinity']:
            pass#todo
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['inverseFollow']:
            pass#todo

    def handleButtonClicked(self, buttonId: str):
        # Dictionary to map button IDs to their corresponding methods
        button_actions = {
            'startGame': self.clickStartGame,
            'saveSettings': self.clickSaveSettings,
            'updatePorts': self.clickUpdatePorts,
            'initializeHardware': self.clickInitializeHardware,
            'lightSensor': self.triggerLightSensor
        }
        
        # Call the corresponding method if button ID exists
        action = button_actions.get(buttonId)
        if action:
            try:
                action()
            except Exception as e:
                # Show error to user through ViewManager
                self.viewManager.showWarning(str(e))

    def getGameStateInfo(self):
        """Return current game state as a dictionary for UI updates"""
        return {
            'gameMode': self.gameState.gameMode,
            'inverseSticks': self.gameState.inverseSticks,
            'randomInverseSticks': self.gameState.randomInverseSticks,
            'rocketVelocity': self.gameState.rocketVelocity,
            'randomRocketVelocity': self.gameState.randomRocketVelocity,
            'latency': self.gameState.latency,
            'randomLatency': self.gameState.randomLatency
        }

    #buttons from GUI
    def clickStartGame(self):
        # Validate game state before proceeding
        if self.gameState.gameMode is None:
            raise ValueError(ERROR_MESSAGES['NO_GAME_MODE_SELECTED'])
        elif not self.gameState.hardwareInitialized:
            raise ValueError(ERROR_MESSAGES['HARDWARE_NOT_INITIALIZED'])
        # Proceed with game start logic

    def clickSaveSettings(self):
        # Save settings to (maybe???????????) config file or certain model object
        pass
    
    def clickUpdatePorts(self):
        # Update ports for serial communication
        if self.arduinoController.updatePorts() is False:
            raise ValueError(ERROR_MESSAGES['PORT_UPDATE_FAILED'])
        else:
            self.gameState.portsFound = True
            raise ValueError(ERROR_MESSAGES['SUCCESS'])
        
    def clickInitializeHardware(self):
        if self.gameState.portsFound is False:
            raise ValueError(ERROR_MESSAGES['NO_PORTS_FOUND'])
        elif self.arduinoController.initializeHardware() is False:
            raise ValueError(ERROR_MESSAGES['HARDWARE_INITIALIZATION_FAILED'])
        else:
            self.gameState.hardwareInitialized = True
            raise ValueError(ERROR_MESSAGES['SUCCESS'])

    def triggerLightSensor(self):
        pass

    def handleCheckboxChanged(self, checkbox_id: str, is_checked: bool):
        """Handle checkbox state changes from the settings view."""
        # Update game state based on checkbox changes
        if checkbox_id == "inverseSticks":
            self.gameState.inverseSticks = is_checked
        elif checkbox_id == "randomInverseSticks":
            self.gameState.randomInverseSticks = is_checked
        elif checkbox_id == "randomRocketVelocity":
            self.gameState.randomRocketVelocity = is_checked
        elif checkbox_id == "randomLatency":
            self.gameState.randomLatency = is_checked
        self.gameStateChanged.emit(self.getGameStateInfo())

    def handleSliderChanged(self, slider_id: str, value: float):
        """Handle slider value changes from the settings view."""
        if slider_id == "rocketVelocity":
            self.gameState.rocketVelocity = value
        elif slider_id == "latency":
            self.gameState.latency = value
        self.gameStateChanged.emit(self.getGameStateInfo())
        

    def handleGameModeChanged(self, mode: str):
        """Handle game mode changes from the settings view."""
        self.gameState.gameMode = mode
        self.gameStateChanged.emit(self.getGameStateInfo())