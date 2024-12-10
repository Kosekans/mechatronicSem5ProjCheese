import json
from models.gameState import GameState
from views.viewManager import ViewManager
from utils.helperFunctions import HelperFunctions
from controllers import *
from controllers.gameController import GameController
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QGuiApplication
import sys
import os
import logging
import platform
from pathlib import Path

def get_log_path():
    """Get platform-specific log path"""
    if HelperFunctions.is_raspberry_pi():
        return '/var/log/cheese.log'
    else:
        # Windows development path
        return str(Path.home() / 'cheese.log')

def check_display():
    """Check if display is available"""
    try:
        if HelperFunctions.is_raspberry_pi():
            if not os.environ.get('DISPLAY') and not os.environ.get('QT_QPA_PLATFORM'):
                os.environ['QT_QPA_PLATFORM'] = 'eglfs'
        else:
            # Windows defaults
            os.environ['QT_QPA_PLATFORM'] = 'windows'
        return True
    except Exception as e:
        logging.error(f"Display initialization failed: {e}")
        return False

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=get_log_path()
    )

    if not check_display():
        logging.error("Display not available")
        return 1

    try:
        # Create core application with platform plugin
        os.environ['QT_DEBUG_PLUGINS'] = '1'
        app = QApplication(sys.argv)
        
        # Default values for development
        internetConnection: bool = True
        updateSuccessful: bool = True
        # Load setup status
        '''
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'config', 'setup_status.json')
        with open(config_path) as f:
            status = json.load(f)
        internetConnection = status['internetConnection']
        updateSuccessful = status['updateSuccessful']
        '''

        # Initialize components
        gameState = GameState()
        arduinoController = ArduinoController()
        viewManager = ViewManager(app, internetConnection, updateSuccessful)
        inputController = InputController()
        gameController = GameController(gameState, viewManager, arduinoController, inputController)

        # Configure window
        for widget in app.topLevelWidgets():
            if HelperFunctions.is_raspberry_pi():
                widget.setWindowFlags(
                    Qt.Window |
                    Qt.FramelessWindowHint |
                    Qt.WindowStaysOnTopHint
                )
                widget.showFullScreen()
                widget.closeEvent = lambda event: event.ignore()
            else:
                # Regular window for development
                widget.show()

        # Connect signals
        viewManager.connectSignals(gameController)
        inputController.connectSignals(gameController)

        return app.exec_()

    except Exception as e:
        logging.error(f"Application failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())