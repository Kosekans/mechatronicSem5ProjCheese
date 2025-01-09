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
        height: parent.height * 0.8
        columns: 2
        rows: 2
        rowSpacing: 20
        columnSpacing: 20

        CustomButton {
            text: "Null the\nmotors"
            Layout.fillWidth: true
            Layout.fillHeight: true
            font.pixelSize: 24
            onClicked: viewManager.onButtonClick("null")
        }

        CustomButton {
            text: "Transportmode\ntight the strings"
            Layout.fillWidth: true
            Layout.fillHeight: true
            font.pixelSize: 24
            onClicked: viewManager.onButtonClick("transport")
        }

        CustomButton {
            text: "Update\nPorts"
            Layout.fillWidth: true
            Layout.fillHeight: true
            font.pixelSize: 24
            onClicked: viewManager.onButtonClick("updatePorts")
        }

        CustomButton {
            text: "Initialize Serial\nComunication\nwith Arduinos"
            Layout.fillWidth: true
            Layout.fillHeight: true
            font.pixelSize: 24
            onClicked: viewManager.onButtonClick("initializeHardware")
        }

        CustomButton {
            text: "Back"
            Layout.alignment: Qt.AlignBottom | Qt.AlignHCenter
            Layout.preferredWidth: 200
            Layout.preferredHeight: 60
            font.pixelSize: 24
            onClicked: viewManager.onPageChangeClick("back")
        }
    }
}