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
from config.settings import QML_SETTINGS

class ViewManager(QObject):
    """
    Main view manager class responsible for handling QML views, navigation, and UI interactions.
    Manages the lifecycle of pages and provides communication between QML and Python.
    """
    
    # Define PyQt signals for inter-component communication
    buttonClicked = pyqtSignal(str)  # Emitted when a button is clicked in QML
    warningMessage = pyqtSignal(str)  # Emitted to display warning messages in QML
    pageChanged = pyqtSignal(str)     # Emitted when navigation between pages occurs

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
            'credits': 'credits.qml'
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

    def goBack(self) -> None:
        """
        Navigate to the previous page in the navigation stack.
        Does nothing if already at the root page.
        """
        if len(self.page_stack) > 1:
            self.page_stack.pop()
            previous = self.page_stack[-1]
            self.pageChanged.emit(previous)
    
    def connectSignals(self, controller) -> None:
        """
        Connect this manager's signals to controller slots.
        Args:
            controller: The controller instance to connect signals to
        """
        self.buttonClicked.connect(controller.handleButtonClicked)

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