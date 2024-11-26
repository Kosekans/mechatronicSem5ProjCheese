import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Get the current file's directory and add parent to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir.parent))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from config.settings import QML_SETTINGS

# viewManager.py
class ViewManager(QObject):
    """Manages QML views and navigation"""
    
    # Signals
    buttonClicked = pyqtSignal(str)
    warningMessage = pyqtSignal(str)
    pageChanged = pyqtSignal(str)

    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.app = app
        self.engine = QQmlApplicationEngine()
        self.page_stack: List[str] = ['main']
        self.setupPages()
        self.setupUI()

    def setupPages(self) -> None:
        """Setup available QML pages"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.qml_dir = os.path.join(current_dir, 'qml')
        # Register the QML directory for imports
        self.engine.addImportPath(self.qml_dir)
        # Map page names to their QML file names
        self.page_files = {
            'main': 'mainMenu.qml',
            'settings': 'settings.qml',
            'highscore': 'highscore.qml',
            'credits': 'credits.qml'
        }
        self.pages = set(self.page_files.keys())

    def setupUI(self) -> None:
        # Expose manager to QML
        self.engine.rootContext().setContextProperty("viewManager", self)
        
        # Set window properties
        self.engine.rootContext().setContextProperty("windowWidth", QML_SETTINGS['WINDOW_WIDTH'])
        self.engine.rootContext().setContextProperty("windowHeight", QML_SETTINGS['WINDOW_HEIGHT'])
        self.engine.rootContext().setContextProperty("windowTitle", QML_SETTINGS['TITLE'])
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qml_path = os.path.join(current_dir, 'qml', 'mainWindow.qml')
        
        # Verify all required QML files exist
        required_files = [qml_path]
        for qml_file in self.page_files.values():
            required_files.append(os.path.join(self.qml_dir, qml_file))
            
        for file in required_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required QML file not found: {file}")
            
        self.engine.load(qml_path)
        
        # Check for QML loading errors
        if not self.engine.rootObjects():
            raise RuntimeError("Failed to load QML")

    def navigateToPage(self, page_name: str) -> None:
        """Navigate to a new page"""
        if page_name in self.pages:
            self.page_stack.append(page_name)
            self.pageChanged.emit(page_name)

    def goBack(self) -> None:
        """Navigate to previous page"""
        if len(self.page_stack) > 1:
            self.page_stack.pop()
            previous = self.page_stack[-1]
            self.pageChanged.emit(previous)
    
    def connectSignals(self, controller) -> None:
        """Connect signals to controller slots"""
        self.buttonClicked.connect(controller.handleButtonClicked)

    @pyqtSlot(str)
    def onButtonClick(self, button_id: str) -> None:
        """Handle button clicks from QML"""
        self.buttonClicked.emit(button_id)

    @pyqtSlot(str)
    def showWarning(self, message: str) -> None:
        """Show warning dialog in QML"""
        self.warningMessage.emit(message)