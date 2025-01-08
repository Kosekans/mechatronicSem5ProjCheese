import sys
import os
from PyQt5.QtCore import QObject, pyqtSignal
import time

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from controllers import *
from models import *
from views.viewManager import ViewManager
from utils.helperFunctions import HelperFunctions
from config.settings import ERROR_MESSAGES, GAME_SETTINGS, SUCCESS_MESSAGES

class GameController(QObject):
    gameStateChanged = pyqtSignal(dict)
    
    def __init__(self, gameState: GameState, viewManager: ViewManager, arduinoController: ArduinoController, gpioPinsController: GpioPinsController):
        super().__init__()  # Initialize QObject
        self.gameState = gameState
        self.viewManager = viewManager
        self.arduinoController = arduinoController
        self.gpioPinsController = gpioPinsController
        self.startTime = None
        
        # Initialize hardware state
        self.gameState.portsFound = False
        self.gameState.hardwareInitialized = False
        
        # Try to initialize hardware
        if self.arduinoController.updatePorts():
            self.gameState.portsFound = True
            if self.arduinoController.initializeHardware():
                self.gameState.hardwareInitialized = True
    
    def setupGame(self):
        self.gameState.active = True
        self.prepareRocket()
        if self.gameState.gameMode == GAME_SETTINGS['GAME_MODE']['follow']:
            initGoalCoords = [0, 150]
            self.gameState.goalCoords = initGoalCoords
            self.runGame()
            while self.compareCoords():
                self.arduinoController.sendZiel(self.gameState.goalCoordsToString)
                self.gameState.goalCoords = HelperFunctions.createFollowCoords(self.gameState.goalCoords, 50)
            self.gameOver()
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['goal']:
            self.gameState.goalCoords = HelperFunctions.createGoalCoords()
            self.arduinoController.sendZiel(self.gameState.goalCoordsToString)
            self.runGame()
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['infinity']:
            pass
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['inverseFollow']:
            pass
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['demo']:
            self.gameState.active = True
            self.arduinoController.sendAntrieb("DEMO")
            self.arduinoController.sendZiel("DEMO")
        
    def runGame(self):
        self.arduinoController.sendAntrieb("PLAY")
        self.viewManager.navigateToPage('runningGame')
        self.startTime = time.time()
    
    def gameOver(self):
        self.gameState.timePlayed = time.time() - self.startTime
        timeMessage = SUCCESS_MESSAGES['GAME_ENDED_WITH_TIME'] + str(self.gameState.timePlayed)
        self.checkHighScore()
        if self.gameState.gameMode == GAME_SETTINGS['GAME_MODE']['follow']:
            self.viewManager.showSuccess(timeMessage)
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['goal']:
            if self.compareCoords():
                self.viewManager.showSuccess(SUCCESS_MESSAGES['GAME_WON'])
            else:
                self.viewManager.showWarning(ERROR_MESSAGES['GAME_LOST'])
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['infinity']:
            pass
        elif self.gameState.gameMode == GAME_SETTINGS['GAME_MODES']['inverseFollow']:
            pass
        self.clickAbortGame()
        self.viewManager.navigateToPage('main')
    
    def compareCoords(self):
        self.arduinoController.sendAntrieb("COORDS")
        currentCoords = self.arduinoController.getAntrieb()
        return HelperFunctions.coordsMatchCheck(currentCoords, self.gameState.goalCoords, 50)

    def checkHighScore(self):
        pass
    
    def clickAbortGame(self):
        self.gameState.reset
        self.prepareRocket()

    def prepareRocket(self):
        self.gameState.arduinoBusy = True
        self.arduinoController.sendAntrieb(self.gameState.getInfoForAntrieb)
        self.arduinoController.sendAntrieb("EJECTPOS")
        while self.gameState.ballInRocket == False:
            pass
        self.arduinoController.sendAntrieb("STARTPOS")
        while self.arduinoController.getAntrieb != "DONE":
            self.gameState.arduinoBusy = True
        self.gameState.arduinoBusy = False
        
    def handleGpioInput(self, event: str):
        print(f"GameController received GPIO event: {event}") # Add debug print
        pin_actions = {
            'Start': self.clickStartGame,
            'Ball lost': self.ballInRocket(False),
            'Ball detected': self.ballInRocket(True)
        }
        
        action = pin_actions.get(event)
        if action:
            try:
                action()
            except Exception as e:
                self.viewManager.showWarning(str(e))
    
    def ballInRocket(self, value: bool):
        self.gameState.ballInRocket = value
        if not value and self.gameState.active:
            self.gameOver()
    
    def clickStartGame(self):
        # Validate game state before proceeding
        if self.gameState.gameMode is None:
            raise ValueError(ERROR_MESSAGES['NO_GAME_MODE_SELECTED'])
        elif not self.gameState.hardwareInitialized:
            raise ValueError(ERROR_MESSAGES['HARDWARE_NOT_INITIALIZED'])
        elif self.gameState.active:
            raise ValueError(ERROR_MESSAGES['RUNNING_GAME'])
        elif self.gameState.arduinoBusy:
            raise ValueError(ERROR_MESSAGES['ARDUINO_BUSY'])
        else:
            self.setupGame()

    def handleButtonClicked(self, buttonId: str):
        # Dictionary to map button IDs to their corresponding methods
        button_actions = {
            'startGame': self.clickStartGame,
            'updatePorts': self.clickUpdatePorts,
            'initializeHardware': self.clickInitializeHardware,
            'null': self.clickNullAntrieb,
            'abort': self.clickAbortGame
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
    def clickUpdatePorts(self):
        # Update ports for serial communication
        if self.arduinoController.updatePorts() is False:
            raise ValueError(ERROR_MESSAGES['PORT_UPDATE_FAILED'])
        else:
            self.gameState.portsFound = True
            self.viewManager.showSuccess(SUCCESS_MESSAGES['PORTS_UPDATED'])
        
    def clickInitializeHardware(self):
        if self.gameState.portsFound is False:
            raise ValueError(ERROR_MESSAGES['NO_PORTS_FOUND'])
        elif self.arduinoController.initializeHardware() is False:
            raise ValueError(ERROR_MESSAGES['HARDWARE_INITIALIZATION_FAILED'])
        else:
            self.gameState.hardwareInitialized = True
            self.viewManager.showSuccess(SUCCESS_MESSAGES['HARDWARE_INITIALIZED'])
    
    def clickNullAntrieb(self):
        self.arduinoController.sendAntrieb("null")
        while self.arduinoController.getAntrieb != "DONE":
            self.gameState.arduinoBusy = True
        self.gameState.arduinoBusy = False
        self.viewManager.showSuccess(SUCCESS_MESSAGES['NULL_ANTRIEB'])

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