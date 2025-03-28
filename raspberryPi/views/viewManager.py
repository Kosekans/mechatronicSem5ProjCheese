import os
import sys
from pathlib import Path
import json

# Add parent directory to system path to enable imports from parent modules
current_dir = Path(__file__).parent
parent_dir = str(current_dir.parent)
if (parent_dir not in sys.path):
    sys.path.append(parent_dir)

from typing import List
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor 
from config.settings import QML_SETTINGS, GAME_SETTINGS, ERROR_MESSAGES  # Update import at top


class ViewManager(QObject):
    """
    Main view manager class responsible for handling QML views, navigation, and UI interactions.
    Manages the lifecycle of pages and provides communication between QML and Python.
    """
    
    # Define PyQt signals for inter-component communication
    buttonClicked = pyqtSignal(str)  # Emitted when a button is clicked in QML
    warningMessage = pyqtSignal(str)  # Emitted to display warning messages in QML
    pageChanged = pyqtSignal(str)     # Emitted when navigation between pages occurs
    checkboxChanged = pyqtSignal(str, bool)  # Emitted when checkbox state changes
    sliderChanged = pyqtSignal(str, float)   # Emitted when slider value changes
    gameModeChanged = pyqtSignal(str)        # Emitted when game mode changes
    gameStateUpdated = pyqtSignal('QVariant')
    initialStateLoaded = pyqtSignal()
    successMessage = pyqtSignal(str)  # Emitted to display success messages in QML

    def __init__(self, app: QApplication, internetConnection: bool, updateSuccessful: bool) -> None:
        """
        Initialize the ViewManager with a QApplication instance.
        Sets up the QML engine and initializes the page navigation stack.
        
        Args:
            app (QApplication): The main application instance
        """
        super().__init__()
        self.internetConnection = internetConnection
        self.updateSuccessful = updateSuccessful
        self.app = app
        self.engine = QQmlApplicationEngine()
        self.page_stack: List[str] = ['main']  # Initialize navigation stack with main page
        self.setupPages()
        self.setupUI()
        self.initErrorMessages()

    def initErrorMessages(self):
        if not self.internetConnection:
            self.showWarning(ERROR_MESSAGES['NO_INTERNET_CONNECTION'])
        elif not self.updateSuccessful:
            self.showWarning(ERROR_MESSAGES['UPDATE_FAILED'])


    def setupPages(self) -> None:
        """
        Configure the available QML pages and their file mappings.
        Sets up the QML import path and defines the mapping between page names and QML files.
        """
        # Get the directory containing QML files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.qml_dir = os.path.join(current_dir, 'qml')
        
        # Configure QML engine to find custom imports
        self.engine.addImportPath(self.qml_dir)
        
        # Define mapping of logical page names to actual QML files
        self.page_files = {
            'main': 'mainMenu.qml',
            'settings': 'settings.qml',
            'highscore': 'highscore.qml',
            'credits': 'credits.qml',
            'setGameMode': 'gameModeSettings.qml',
            'gameModeInfo': 'gameModeInfo.qml',
            'runningGame': 'runningGame.qml'
        }
        self.pages = set(self.page_files.keys())

    def setupUI(self) -> None:
        """Initialize the UI components and load the main QML window."""
        # Hide cursor by setting a blank cursor
        blank_cursor = QCursor(Qt.BlankCursor)
        self.app.setOverrideCursor(blank_cursor)
        
        self.engine.rootContext().setContextProperty("viewManager", self)
        screen = QDesktopWidget().screenGeometry()
        
        self.engine.rootContext().setContextProperty("windowWidth", screen.width())
        self.engine.rootContext().setContextProperty("windowHeight", screen.height())
        self.engine.rootContext().setContextProperty("windowTitle", QML_SETTINGS['TITLE'])
        self.engine.rootContext().setContextProperty("warningMessage", self.warningMessage)
        self.engine.rootContext().setContextProperty("successMessage", self.successMessage)
        self.engine.rootContext().setContextProperty("infinityCount", self.getInfinityCount())
        self.engine.rootContext().setContextProperty("timePlayed", self.getTimePlayed())
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qml_path = os.path.join(current_dir, 'qml', 'mainWindow.qml')
        
        # Validate QML files
        required_files = [qml_path] + [
            os.path.join(self.qml_dir, qml_file)
            for qml_file in self.page_files.values()
        ]
        
        for file in required_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required QML file not found: {file}")
        
        self.engine.load(qml_path)
        if not self.engine.rootObjects():
            raise RuntimeError("Failed to load QML")
    
    def updateHighscoreValues(self) -> None:
        """Update the highscore values in QML context"""
        self.engine.rootContext().setContextProperty("infinityCount", self.getInfinityCount())
        self.engine.rootContext().setContextProperty("timePlayed", self.getTimePlayed())

    def navigateToPage(self, page_name: str) -> None:
        """
        Navigate to a specified page by name.
        Args:
            page_name (str): Name of the page to navigate to
        """
        if page_name in self.pages:
            self.page_stack.append(page_name)
            self.pageChanged.emit(page_name)
            # Update values when navigating to highscore page
            if page_name == 'highscore':
                self.updateHighscoreValues()
            # Directly load game state when navigating to gameModeSettings
            elif page_name == 'setGameMode':
                self.loadGameModeSettingInfo()

    def goBack(self) -> None:
        """Navigate to the previous page in the navigation stack."""
        if len(self.page_stack) > 1:
            self.page_stack.pop()
            previous = self.page_stack[-1]
            self.pageChanged.emit(previous)
            # Load game state when returning to gameModeSettings
            if previous == 'setGameMode':
                self.loadGameModeSettingInfo()
                self.initialStateLoaded.emit()
    
    def connectSignals(self, controller) -> None:
        """
        Connect this manager's signals to controller slots.
        This is the ONLY place where signals should be connected.
        Args:
            controller: The controller instance to connect signals to
        """
        # Safely disconnect existing connections
        try:
            self.buttonClicked.disconnect()
            self.checkboxChanged.disconnect()
            self.sliderChanged.disconnect()
            self.gameModeChanged.disconnect()
        except TypeError:
            # Ignore errors if signals weren't connected
            pass
        
        # Connect signals
        self.buttonClicked.connect(controller.handleButtonClicked)
        self.checkboxChanged.connect(controller.handleCheckboxChanged)
        self.sliderChanged.connect(controller.handleSliderChanged)
        self.gameModeChanged.connect(controller.handleGameModeChanged)
        controller.gameStateChanged.connect(self.handleGameStateChanged)
        self.controller = controller  # Store controller reference

    @pyqtSlot()
    def loadGameModeSettingInfo(self) -> None:
        """Request and broadcast current game state to QML"""
        if hasattr(self, 'controller'):
            state = self.controller.getGameStateInfo()
            self.gameStateUpdated.emit(state)

    @pyqtSlot(str)
    def onPageChangeClick(self, button_id: str) -> None:
        if button_id == 'back':
            self.goBack()
        else:
            self.navigateToPage(button_id)

    @pyqtSlot(str)
    def onButtonClick(self, button_id: str) -> None:
        """
        Handle button clicks from QML interface.
        Args:
            button_id (str): Identifier of the clicked button
        """
        self.buttonClicked.emit(button_id)

    @pyqtSlot(str)
    def showWarning(self, message: str) -> None:
        """
        Display a warning message in the QML interface.
        Args:
            message (str): Warning message to display
        """
        self.warningMessage.emit(message)

    @pyqtSlot(str, bool)
    def onCheckboxChanged(self, checkbox_id: str, is_checked: bool) -> None:
        """
        Handle checkbox state changes from QML interface.
        Args:
            checkbox_id (str): Identifier of the checkbox
            is_checked (bool): New state of the checkbox
        """
        self.checkboxChanged.emit(checkbox_id, is_checked)

    @pyqtSlot(str, float)
    def onSliderValueChanged(self, slider_id: str, slider_value: float) -> None:
        """
        Handle slider value changes from QML interface.
        Args:
            slider_id (str): Identifier of the slider
            slider_value (float): New value of the slider
        """
        self.sliderChanged.emit(slider_id, slider_value)

    @pyqtSlot(str)
    def onGameModeChanged(self, mode: str) -> None:
        """
        Handle game mode changes from QML interface.
        Args:
            mode (str): Selected game mode
        """
        self.gameModeChanged.emit(mode)

    @pyqtSlot(str, result=str)
    def getGameMode(self, mode_key: str) -> str:
        """
        Get game mode value from settings for QML.
        Args:
            mode_key (str): Key of the game mode
        Returns:
            str: The game mode value from settings
        """
        return GAME_SETTINGS['GAME_MODES'].get(mode_key, '')

    def handleGameStateChanged(self, state: dict) -> None:
        """Handle game state updates from controller"""
        self.gameStateUpdated.emit(state)

    @pyqtSlot(str)
    def showSuccess(self, message: str) -> None:
        """
        Display a success message in the QML interface.
        Args:
            message (str): Success message to display
        """
        self.successMessage.emit(message)

    @pyqtSlot(result=int)
    def getInfinityCount(self) -> int:
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(current_dir, 'config', 'highscore_status.json')
            with open(config_path, 'r') as f:
                data = json.load(f)
                return data.get('infinityCount', 0)
        except Exception as e:
            print(f"Error reading infinity count: {e}")
            return 0

    @pyqtSlot(result=int)
    def getTimePlayed(self) -> int:
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(current_dir, 'config', 'highscore_status.json')
            with open(config_path, 'r') as f:
                data = json.load(f)
                return data.get('timePlayed', 0)
        except Exception as e:
            print(f"Error reading time played: {e}")
            return 0