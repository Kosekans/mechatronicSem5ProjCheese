from models.gameState import GameState
from views.viewManager import ViewManager
from controllers import *
from controllers.gameController import GameController
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import sys

def main():
    # Create core application
    app = QApplication(sys.argv)
    
    # Initialize components with explicit dependencies
    gameState = GameState()
    arduinoController = ArduinoController()
    viewManager = ViewManager(app)
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