import json
from models.gameState import GameState
from views.viewManager import ViewManager
from controllers import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys
import os
from controllers.gameController import GameController


def main():
    # Update the repository to the latest version
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'config', 'setup_status.json')
    with open(config_path) as f:
        status = json.load(f)
    internetConnection: bool = status['internetConnection']
    updateSuccessful: bool = status['updateSuccessful']

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