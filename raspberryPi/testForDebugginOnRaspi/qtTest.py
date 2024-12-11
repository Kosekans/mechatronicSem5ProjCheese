import os
import sys
from pathlib import Path
from typing import List

# Set required environment variables
os.environ["QT_QPA_PLATFORM"] = "eglfs"
os.environ["QT_QPA_EGLFS_ALWAYS_SET_MODE"] = "1"

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, Qt, QCoreApplication, pyqtSlot
print("imported qt schiisdräck")

class ViewManager(QObject):
    buttonClicked = pyqtSignal(str)
    warningMessage = pyqtSignal(str)
    pageChanged = pyqtSignal(str)
    checkboxChanged = pyqtSignal(str, bool)
    sliderChanged = pyqtSignal(str, float)
    gameModeChanged = pyqtSignal(str)
    gameStateUpdated = pyqtSignal('QVariant')
    initialStateLoaded = pyqtSignal()

    def __init__(self, app: QApplication, internetConnection: bool, updateSuccessful: bool) -> None:
        super().__init__()
        self.internetConnection = internetConnection
        self.updateSuccessful = updateSuccessful
        self.app = app
        self.engine = QQmlApplicationEngine()
        self.page_stack: List[str] = ['test']
        self.setupPages()
        self.setupUI()
        self.initErrorMessages()

    def initErrorMessages(self):
        if not self.internetConnection:
            self.showWarning("no internet connection")
        elif not self.updateSuccessful:
            self.showWarning("update failed")


    def setupPages(self) -> None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.qml_dir = os.path.join(current_dir, 'qml')
        self.engine.addImportPath(self.qml_dir)
        self.page_files = {
            'test': 'qtTest.qml'
        }
        self.pages = set(self.page_files.keys())

    def setupUI(self) -> None:
        self.engine.rootContext().setContextProperty("viewManager", self)
        screen = QDesktopWidget().screenGeometry()
        self.engine.rootContext().setContextProperty("windowWidth", screen.width())
        self.engine.rootContext().setContextProperty("windowHeight", screen.height())
        self.engine.rootContext().setContextProperty("windowTitle", "chüe")
        self.engine.rootContext().setContextProperty("warningMessage", self.warningMessage)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        qml_path = os.path.join(current_dir, 'qml', 'qtTest.qml')
        required_files = [qml_path] + [
            os.path.join(self.qml_dir, qml_file)
            for qml_file in self.page_files.values()
        ]
        for file in required_files:
            if not os.path.exists(file):
                raise FileNotFoundError(f"Required QML file not found: {file}")
        self.engine.load(qml_path)
        if not self.engine.rootObjects():
            raise RuntimeError("Failed to load QML")

    def navigateToPage(self, page_name: str) -> None:
        if page_name in self.pages:
            self.page_stack.append(page_name)
            self.pageChanged.emit(page_name)

    def goBack(self) -> None:
        if len(self.page_stack) > 1:
            self.page_stack.pop()
            previous = self.page_stack[-1]
            self.pageChanged.emit(previous)
            if previous == 'setGameMode':
                self.loadGameModeSettingInfo()
                self.initialStateLoaded.emit()
    
if __name__ == "__main__":
    try:
        # Configure EGLFS settings
        os.environ["QT_QPA_EGLFS_WIDTH"] = "800"
        os.environ["QT_QPA_EGLFS_HEIGHT"] = "480"
        os.environ["QT_QPA_EGLFS_PHYSICAL_WIDTH"] = "155"  # Display width in mm
        os.environ["QT_QPA_EGLFS_PHYSICAL_HEIGHT"] = "86"  # Display height in mm

        app = QApplication(sys.argv)
        app.setOverrideCursor(Qt.BlankCursor)  # Hide cursor for touch interface
        print("QApplication created")
        viewManager = ViewManager(app, True, True)
        print("viewManager created")
        for widget in app.topLevelWidgets():
            widget.setWindowFlags(
                Qt.Window |
                Qt.FramelessWindowHint |
                Qt.WindowStaysOnTopHint
            )
            print("Setting window to fullscreen")
            widget.showFullScreen()
            print("Window set to fullscreen")
        app.exec_()
    except Exception as e:
        print(f"Application failed: {e}")