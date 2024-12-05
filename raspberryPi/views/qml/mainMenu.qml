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
        Button {
            text: "Set Game Mode"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onPageChangeClick("setGameMode")
        }
        Button {
            text: "Settings"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onPageChangeClick("settings")
        }
        Button {
            text: "Credits"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onPageChangeClick("credits")
        }
        Button {
            text: "Highscore"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onPageChangeClick("highscore")
        }
    }
}