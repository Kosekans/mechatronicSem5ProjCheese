from models.gameState import GameState
from views.viewManager import ViewManager
from controllers.gameController import GameController
from controllers.arduinoController import ArduinoController

def main():
    # Initialize components
    gameState = GameState()
    arduinoController = ArduinoController()
    while not arduinoController.initialize_hardware():
        pass
    viewManager = ViewManager()
    gameController = GameController(gameState, viewManager, arduinoController)

    # Run the application
    viewManager.run()

if __name__ == "__main__":
    main()