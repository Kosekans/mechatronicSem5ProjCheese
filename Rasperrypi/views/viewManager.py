import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from config.settings import QML_SETTINGS

class ViewManager(QObject):
    buttonClicked = pyqtSignal(int)
    warningMessage = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        # Create the Qt Application
        self.app = QGuiApplication(sys.argv)
        
        # Create QML engine
        self.engine = QQmlApplicationEngine()
        
        # Expose this Python object to QML
        self.engine.rootContext().setContextProperty("viewManager", self)
        
        # Set QML context properties from settings
        self.engine.rootContext().setContextProperty("windowWidth", QML_SETTINGS['WINDOW_WIDTH'])
        self.engine.rootContext().setContextProperty("windowHeight", QML_SETTINGS['WINDOW_HEIGHT'])
        self.engine.rootContext().setContextProperty("windowTitle", QML_SETTINGS['TITLE'])
        
        # Get the absolute path to the main.qml file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qml_path = os.path.join(current_dir, 'qml', os.path.basename(QML_SETTINGS['QML_MAIN_FILE']))
        
        # Load the main QML file using absolute path
        self.engine.load(qml_path)

        # Get the root object
        if not self.engine.rootObjects():
            sys.exit(-1)
        
        # Expose warning signal to QML
        self.engine.rootContext().setContextProperty("viewManager", self)

    def run(self):
        # Start the event loop
        sys.exit(self.app.exec_())

    @pyqtSlot(int)
    def onButtonClick(self, buttonId):
        # Emit signal when button is clicked in QML
        self.buttonClicked.emit(buttonId)
    
    @pyqtSlot(str)
    def showWarning(self, message):
        # Emit a signal to show warning in QML
        self.warningMessage.emit(message)