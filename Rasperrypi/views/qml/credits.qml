import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Item {
    id: creditsPage
    anchors.fill: parent

    GridLayout {
        anchors.centerIn: parent
        width: parent.width * 0.8
        columns: 1
        rowSpacing: 10

        Button {
            text: "Back"
            Layout.fillWidth: true
            onClicked: viewManager.onButtonClick("back")
        }
    }
}
