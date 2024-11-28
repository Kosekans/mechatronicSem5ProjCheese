import os
import sys
from pathlib import Path
from typing import List

# Add parent directory to system path to enable imports from parent modules
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent))

from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from config.settings import QML_SETTINGS, GAME_SETTINGS  # Update import at top

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
    # Add new signal for state updates
    gameStateUpdated = pyqtSignal('QVariant')
    initialStateLoaded = pyqtSignal()  # Add new signal

    def __init__(self, app: QApplication) -> None:
        """
        Initialize the ViewManager with a QApplication instance.
        Sets up the QML engine and initializes the page navigation stack.
        
        Args:
            app (QApplication): The main application instance
        """
        super().__init__()
        self.app = app
        self.engine = QQmlApplicationEngine()
        self.page_stack: List[str] = ['main']  # Initialize navigation stack with main page
        self.setupPages()
        self.setupUI()

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
            'popUpHighscore': 'popUpHighscore.qml',
            'runningGame': 'runningGame.qml'
        }
        self.pages = set(self.page_files.keys())

    def setupUI(self) -> None:
        """
        Initialize the UI components and load the main QML window.
        Validates required QML files and sets up window properties.
        Raises:
            FileNotFoundError: If required QML files are missing
            RuntimeError: If QML loading fails
        """
        # Expose this instance to QML for direct access
        self.engine.rootContext().setContextProperty("viewManager", self)
        # Get actual screen dimensions
        screen = QDesktopWidget().screenGeometry()
        
        # Configure window properties in QML context
        self.engine.rootContext().setContextProperty("windowWidth", screen.width())
        self.engine.rootContext().setContextProperty("windowHeight", screen.height())
        self.engine.rootContext().setContextProperty("windowTitle", QML_SETTINGS['TITLE'])
        self.engine.rootContext().setContextProperty("warningMessage", self.warningMessage)  
        
        # Locate and validate all required QML files
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qml_path = os.path.join(current_dir, 'qml', 'mainWindow.qml')
        
        required_files = [qml_path] + [
            os.path.join(self.qml_dir, qml_file)
            for qml_file in self.page_files.values()
        ]
        
        # Verify existence of all required QML files
        for file in required_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required QML file not found: {file}")
            
        # Load main QML file and verify successful loading
        self.engine.load(qml_path)
        if not self.engine.rootObjects():
            raise RuntimeError("Failed to load QML")

    def navigateToPage(self, page_name: str) -> None:
        """
        Navigate to a specified page by name.
        Args:
            page_name (str): Name of the page to navigate to
        """
        if page_name in self.pages:
            self.page_stack.append(page_name)
            self.pageChanged.emit(page_name)
            # Directly load game state when navigating to gameModeSettings
            if page_name == 'setGameMode':
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