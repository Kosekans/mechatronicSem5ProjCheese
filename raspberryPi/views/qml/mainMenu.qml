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
        anchors.margins: 20
        columns: 2
        rows: 2
        rowSpacing: 20
        columnSpacing: 20
        
        CustomButton {
            text: "Set Game\nMode"
            Layout.fillWidth: true
            Layout.fillHeight: true
            font.pixelSize: 24
            onClicked: viewManager.onPageChangeClick("setGameMode")
        }
        CustomButton {
            text: "Settings"
            Layout.fillWidth: true
            Layout.fillHeight: true
            font.pixelSize: 24
            onClicked: viewManager.onPageChangeClick("settings")
        }
        CustomButton {
            text: "Credits"
            Layout.fillWidth: true
            Layout.fillHeight: true
            font.pixelSize: 24
            onClicked: viewManager.onPageChangeClick("credits")
        }
        CustomButton {
            text: "Highscore"
            Layout.fillWidth: true
            Layout.fillHeight: true
            font.pixelSize: 24
            onClicked: viewManager.onPageChangeClick("highscore")
        }
    }
}