import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Item {
    id: highscorePage
    anchors.fill: parent

    GridLayout {
        anchors.fill: parent
        anchors.margins: 20
        columns: 1
        rowSpacing: 20

        Text {
            Layout.alignment: Qt.AlignHCenter
            text: "Highscores"
            font.pixelSize: 48
            color: "white"
        }

        Text {
            Layout.alignment: Qt.AlignHCenter
            text: "Infinity Mode Count: " + infinityCount
            font.pixelSize: 32
            color: "white"
        }

        Text {
            Layout.alignment: Qt.AlignHCenter
            text: "Time Played (minutes): " + timePlayed
            font.pixelSize: 32
            color: "white"
        }

        Item {
            Layout.fillHeight: true
            Layout.fillWidth: true
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
