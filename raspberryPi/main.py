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
        # Set base display configuration
        os.environ['DISPLAY'] = ':0'
        os.environ['QT_QPA_PLATFORM'] = 'eglfs'
        
        # Set EGLFS specific configuration
        os.environ['QT_QPA_EGLFS_DEVICE'] = '/dev/dri/card0'  # Add device path
        os.environ['QT_QPA_EGLFS_INTEGRATION'] = 'eglfs_kms'
        os.environ['QT_QPA_EGLFS_KMS_ATOMIC'] = '1'
        os.environ['QT_QPA_EGLFS_KMS_CONFIG'] = '/etc/kms.conf'
        os.environ['QT_QPA_EGLFS_ALWAYS_SET_MODE'] = '1'
        os.environ['QT_QPA_EGLFS_PHYSICAL_WIDTH'] = '800'
        os.environ['QT_QPA_EGLFS_PHYSICAL_HEIGHT'] = '480'
        
        # Set debugging
        os.environ['QT_LOGGING_RULES'] = '*.debug=true;qt.qpa.*=true'
        os.environ['QT_DEBUG_PLUGINS'] = '1'

        # QML paths
        os.environ['QML_IMPORT_PATH'] = '/usr/lib/aarch64-linux-gnu/qt5/qml'
        os.environ['QML2_IMPORT_PATH'] = '/usr/lib/aarch64-linux-gnu/qt5/qml'
        print("Raspberry Pi display configured")
    else:
        os.environ['QT_QPA_PLATFORM'] = 'windows'

def check_display():
    """Check if display is available"""
    try:
        setup_platform_display()
        if HelperFunctions.is_raspberry_pi():
            device_path = os.environ.get('QT_QPA_EGLFS_DEVICE')
            if not device_path:
                print("QT_QPA_EGLFS_DEVICE not set")
                return False
            if not os.path.exists(device_path):
                print(f"DRM device not found: {device_path}")
                return False
            print(f"Using display device: {device_path}")
        return True
    except Exception as e:
        print(f"Display initialization failed: {str(e)}")
        logging.error(f"Display initialization failed: {str(e)}", exc_info=True)
        return False

def get_log_path():
    """Get platform-specific log path"""
    if HelperFunctions.is_raspberry_pi():
        print("getting Raspberry Pi log path")
        return '/var/log/cheese.log'
    else:
        return str(Path.home() / 'cheese.log')

def main():
    try:
        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename=get_log_path()
        )
        print("Logging configured")

        if not check_display():
            logging.error("Display not available")
            return 1
        print("Display available")

        # Enable Qt debugging
        os.environ['QT_DEBUG_PLUGINS'] = '1'
        print("Qt debugging enabled")
        
        # Create application
        app = QApplication(sys.argv)
        print("Application created")
        
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
        arduinoController = ArduinoController()
        viewManager = ViewManager(app, internetConnection, updateSuccessful)
        inputController = InputController()
        gameController = GameController(gameState, viewManager, arduinoController, inputController)
        print("Initialized components")

        # Configure window
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

        # Connect signals
        viewManager.connectSignals(gameController)
        print("Connected signals to viewManager")
        #may be stupid
        inputController.connectSignals(gameController)
        print("Connected signals to inputController")

        return app.exec_()

    except Exception as e:
        logging.error(f"Application failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())