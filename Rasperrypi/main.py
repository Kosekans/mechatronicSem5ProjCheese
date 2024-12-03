from models.gameState import GameState
from views.viewManager import ViewManager
from controllers import *
from controllers.gameController import GameController
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys
import subprocess
import socket

def check_internet_connection():
    try:
        # Connect to a well-known host (Google DNS) to check for internet connection
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def update_repository():
    try:
        subprocess.check_call(["git", "pull"])
        return True
    except subprocess.CalledProcessError as e:
        return False

def main():
    # Update the repository to the latest version
    internetConnection: bool = check_internet_connection()
    updateSuccessful: bool = False
    if internetConnection:
        updateSuccessful = update_repository()

    # Create core application
    app = QApplication(sys.argv)
    
    # Initialize components with explicit dependencies
    gameState = GameState()
    arduinoController = ArduinoController()
    viewManager = ViewManager(app, internetConnection, updateSuccessful)
    inputController = InputController()
    gameController = GameController(gameState, viewManager, arduinoController, inputController)
    # Force fullscreen and disable window controls
    for widget in app.topLevelWidgets():
        widget.setWindowFlags(
            Qt.Window |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )
        widget.showFullScreen()
        
        # Prevent Alt+F4
        widget.closeEvent = lambda event: event.ignore()

    # Connect signals/slots after all components exist
    viewManager.connectSignals(gameController)
    inputController.connectSignals(gameController)
    
    # Start application
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()