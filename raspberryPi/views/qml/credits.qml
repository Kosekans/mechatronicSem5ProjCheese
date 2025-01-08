import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Item {
    id: creditsPage
    anchors.fill: parent

    GridLayout {
        anchors.fill: parent
        anchors.margins: 20
        columns: 1
        rowSpacing: 20

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
