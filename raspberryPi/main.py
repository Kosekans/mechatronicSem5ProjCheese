import json
from models.gameState import GameState
from views.viewManager import ViewManager
from utils.helperFunctions import HelperFunctions
from controllers import *
from controllers.gameController import GameController
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow
import sys
import os
from PyQt5.QtCore import QTimer
from pathlib import Path

def main():
    try:
        # Create core application
        app = QApplication(sys.argv)
        print("craeted QApplication")
                
        # Default values for development
        internetConnection = True
        updateSuccessful = True

        '''
        if HelperFunctions.is_raspberry_pi():
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
                logging.warning(f"Could not load setup status: {e}")
        '''

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

        # Create a timer to check GPIO status periodically
        gpio_timer = QTimer()
        gpio_timer.timeout.connect(lambda: print(f"GPIO pin state: {GPIO.input(gpioPinsController.START_BUTTON_PIN)}"))
        gpio_timer.start(1000)  # Check every second

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
        print("View signals connected")
        gpioPinsController.connectSignals(gameController) 
        print("GPIO signals connected")
        
        # Start application
        sys.exit(app.exec_())
        print("started application")

        #old
        '''
        root = viewManager.engine.rootObjects()[0]
        if root:
            root.setProperty("visibility", QWindow.FullScreen)
        '''

        # old
        '''
        for widget in app.topLevelWidgets():
            if HelperFunctions.is_raspberry_pi():
                widget.setWindowFlags(
                    Qt.Window |
                    Qt.FramelessWindowHint |
                    Qt.WindowStaysOnTopHint
                )
                print("Setting window to fullscreen")
                widget.showFullScreen()
                print("Window set to fullscreen")
            else:
                widget.show()
        '''
    except Exception as e:
        print.error(f"Application failed: {e}")
        return 1

if __name__ == "__main__":
    main()