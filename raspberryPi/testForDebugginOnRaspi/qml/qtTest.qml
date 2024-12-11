import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Dialogs 1.3
import QtQuick.Controls 2.12

Window {
    visible: true
    width: 640
    height: 480
    title: "Debug Window"

    Column {
        anchors.centerIn: parent
        spacing: 20

        Text {
            text: "Debug Interface"
            font.pixelSize: 24
        }

        Button {
            text: "Test Button"
            onClicked: console.log("Button clicked!")
        }
    }
}