// mainMenu.qml
import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick.Dialogs 1.3

Item {
    id: mainPage
    anchors.fill: parent

    GridLayout {
        anchors.fill: parent
        columns: 3
        rows: 2
        
        Button {
            text: "Start Game"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onButtonClick("startGame")
        }
        ComboBox {
            id: gameModeComboBox
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: ["Select Gamemode", "Ring zeigt Ziel", "Verfolgungsmodus"]
            onCurrentTextChanged: viewManager.onButtonClick(currentText)
        }
        Button {
            text: "Settings"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onButtonClick("settings")
        }
        Button {
            text: "Credits"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onButtonClick("credits")
        }
        Button {
            text: "Highscore"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onButtonClick("highscore")
        }
    }

    MessageDialog {
        id: warningDialog
        title: "Warning"
        icon: StandardIcon.Warning
        standardButtons: StandardButton.Ok
    }

    Connections {
        target: viewManager
        function onWarningMessage(message) {
            warningDialog.text = message
            warningDialog.open()
        }
    }
}