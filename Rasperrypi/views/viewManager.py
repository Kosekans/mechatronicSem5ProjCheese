import sys
import os

# Get the current file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the parent directory to the system path
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from PySide6.QtQuick import QQuickView
from PySide6.QtCore import QUrl
from config.settings import QML_SETTINGS

class ViewManager(QQuickView):
    def __init__(self):
        super().__init__()
        # Use settings from config file
        self.setSource(QUrl.fromLocalFile(QML_SETTINGS['QML_MAIN_FILE']))
        self.setResizeMode(QQuickView.SizeRootObjectToView)
        self.setTitle(QML_SETTINGS['TITLE'])
        self.setWidth(QML_SETTINGS['WINDOW_WIDTH'])
        self.setHeight(QML_SETTINGS['WINDOW_HEIGHT'])