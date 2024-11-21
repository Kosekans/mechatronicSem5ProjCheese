from PySide6.QtGui import QGuiApplication
import sys
from models.gameState import GameState
from views.viewManager import ViewManager
from controllers.gameController import GameController
from controllers.arduinoController import ArduinoController

def main():
    app = QGuiApplication(sys.argv)
    
    # Initialize components
    gameState = GameState()
    arduinoController = ArduinoController()
    while not arduinoController.initialize_hardware():
        pass
    viewManager = ViewManager()
    gameController = GameController(gameState, viewManager, arduinoController)
    
    # Start the game
    gameController.launch()
    
    # Start Qt event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()