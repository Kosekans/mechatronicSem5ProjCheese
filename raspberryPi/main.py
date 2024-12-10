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

def setup_platform_display():
    """Configure display settings based on platform"""
    if HelperFunctions.is_raspberry_pi():
        # Raspberry Pi settings
        os.environ['DISPLAY'] = ':0'
        os.environ['QT_QPA_PLATFORM'] = 'eglfs'
        os.environ['QT_QPA_EGLFS_KMS_ATOMIC'] = '1'
        os.environ['QT_QPA_EGLFS_ALWAYS_SET_MODE'] = '1'
        os.environ['XDG_RUNTIME_DIR'] = '/run/user/1000'
    else:
        # Windows settings
        os.environ['QT_QPA_PLATFORM'] = 'windows'
        
def get_log_path():
    """Get platform-specific log path"""
    if HelperFunctions.is_raspberry_pi():
        return '/var/log/cheese.log'
    else:
        return str(Path.home() / 'cheese.log')

def check_display():
    """Check if display is available"""
    try:
        setup_platform_display()
        if HelperFunctions.is_raspberry_pi():
            # Check if we can connect to X server
            from subprocess import check_call, DEVNULL
            try:
                check_call(['xset', 'q'], stdout=DEVNULL, stderr=DEVNULL)
            except:
                logging.warning("X server not running, using EGLFS")
        return True
    except Exception as e:
        logging.error(f"Display initialization failed: {e}")
        return False

def main():
    try:
        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=get_log_path()
        )

        if not check_display():
            logging.error("Display not available")
            return 1

        # Enable Qt debugging
        os.environ['QT_DEBUG_PLUGINS'] = '1'
        
        # Create application
        app = QApplication(sys.argv)
        
        # Default values for development
        internetConnection = True 
        updateSuccessful = True

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
            else:
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