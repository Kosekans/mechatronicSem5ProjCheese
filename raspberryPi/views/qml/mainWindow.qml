// mainWindow.qml
import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Dialogs 1.3

Window {
    id: mainWindow
    visible: true
    width: windowWidth
    height: windowHeight
    title: windowTitle
    visibility: Window.FullScreen

    // Global theme properties
    property QtObject theme: QtObject {
        property color backgroundColor: "#1a1b2e"  // Dark blue night sky
        property color buttonColor: "#2e344f"      // Moon surface color
        property color buttonHoverColor: "#3d4266" // Lighter moon surface
        property color textColor: "#e1e1ff"        // Soft white moonlight
        property color accentColor: "#8585ad"      // Lunar glow
    }

    Rectangle {
        anchors.fill: parent
        color: theme.backgroundColor
    }

    Loader {
        id: pageLoader
        anchors.fill: parent
        source: "mainMenu.qml"  // default page
    }

    Connections {
        target: viewManager
        function onPageChanged(pageName) {
            if (pageName === "main") {
                pageLoader.source = "mainMenu.qml"
            } else if (pageName === "settings") {
                pageLoader.source = "settings.qml"
            } else if (pageName === "highscore") {
                pageLoader.source = "highscore.qml"
            } else if (pageName === "credits") {
                pageLoader.source = "credits.qml"
            } else if (pageName === "setGameMode") {
                pageLoader.source = "gameModeSettings.qml"
            } else if (pageName === "gameModeInfo") {
                pageLoader.source = "gameModeInfo.qml"
            } else if (pageName === "popUpHighscore") {
                pageLoader.source = "popUpHighscore.qml"
            } else if (pageName === "runningGame") {
                pageLoader.source = "runningGame.qml"
            }
        }
    }

    MessageDialog {
        id: warningDialog
        title: "Warning"
        icon: StandardIcon.Warning
        standardButtons: StandardButton.Ok
        modality: Qt.ApplicationModal
        visible: false 
        
        // Close only when Ok is clicked
        onAccepted: {
            close()
        }
    }

    MessageDialog {
        id: successDialog
        title: "Success"
        icon: StandardIcon.Information
        standardButtons: StandardButton.Ok
        modality: Qt.ApplicationModal
        visible: false 
        
        onAccepted: {
            close()
        }
    }

    Connections {
        target: viewManager
        function onWarningMessage(message) {
            warningDialog.text = message
            warningDialog.open()
        }
    }

    Connections {
        target: viewManager
        function onSuccessMessage(message) {
            successDialog.text = message
            successDialog.open()
        }
    }
}