// settings.qml
import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Item {
    id: settingsPage
    anchors.fill: parent

    GridLayout {
        anchors.centerIn: parent
        width: parent.width * 0.8
        columns: 4
        rowSpacing: 10
        columnSpacing: 10

        Button {
            text: "Back"
            Layout.fillWidth: true
            onClicked: viewManager.onPageChangeClick("back")
        }

        Button {
            text: "null the motors"
            Layout.fillWidth: true
            onClicked: viewManager.onButtonClick("null")
        }

        Button {
            text: "Update Ports"
            Layout.fillWidth: true
            onClicked: viewManager.onButtonClick("updatePorts")
        }

        Button {
            text: "Initialize Serial Comunication with Arduinos"
            Layout.fillWidth: true
            onClicked: viewManager.onButtonClick("initializeHardware")
        }
    }
}