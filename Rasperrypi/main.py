from models.gameState import GameState
from views.viewManager import ViewManager
from controllers import *
from controllers.gameController import GameController
from PyQt5.QtWidgets import QApplication
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

    # Connect signals/slots after all components exist
    viewManager.connectSignals(gameController)
    
    # Start application
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()