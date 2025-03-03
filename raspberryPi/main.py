import json
from models.gameState import GameState
from views.viewManager import ViewManager
from utils.helperFunctions import HelperFunctions
from controllers import *
from controllers.gameController import GameController
from PyQt5.QtWidgets import QApplication
import sys
import os

def main():
    try:
        # Create core application
        app = QApplication(sys.argv)
        print("craeted QApplication")
                
        # Default values for development
        isRasbperryPi = HelperFunctions.is_raspberry_pi()
        print("is rasbperry pi: " + str(isRasbperryPi))

        if isRasbperryPi:
            # Load real status on Pi
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                config_path = os.path.join(current_dir, 'config', 'setup_status.json')
                if os.path.exists(config_path):
                    with open(config_path) as f:
                        status = json.load(f)
                        internetConnection = status['internetConnection']
                        updateSuccessful = status['updateSuccessful']
            except Exception as e:
                print(f"Could not load setup status: {e}")
        else:
            internetConnection = updateSuccessful = True; #default values for dev

        # Initialize components
        gameState = GameState()
        print("initialized component GameState")
        arduinoController = ArduinoController()
        print("initialized component ArduinoController")
        viewManager = ViewManager(app, internetConnection, updateSuccessful)
        print("initialized component ViewManager")
        gpioPinsController = GpioPinsController()
        print("initialized component InputController")
        gameController = GameController(gameState, viewManager, arduinoController, gpioPinsController)
        print("initialized component GameController")

        # Connect signals/slots after all components exist
        viewManager.connectSignals(gameController)
        print("View signals connected")
        gpioPinsController.connectSignals(gameController) 
        print("GPIO signals connected")
        
        # Start application
        return app.exec_()

    except Exception as e:
        print(f"Application failed: {e}")
        return 1

if __name__ == "__main__":
    main()