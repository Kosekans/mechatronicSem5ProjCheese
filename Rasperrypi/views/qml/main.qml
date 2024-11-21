import QtQuick 2.12
import QtQuick.Window 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Window {
    visible: true
    width: windowWidth
    height: windowHeight
    title: windowTitle

    GridLayout {
        anchors.fill: parent
        columns: 3
        rows: 2
        
        Button {
            text: "Start Game"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onButtonClick(1)
        }
        
        Button {
            text: "Gamemode 1"
            Layout.fillWidth: true
            Layout.fillHeight: true
            onClicked: viewManager.onButtonClick(2)
        }
    }
}