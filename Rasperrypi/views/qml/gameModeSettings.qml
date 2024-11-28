import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12

Item {
    id: highscorePage
    anchors.fill: parent

    signal gameModeChanged(string mode)
    signal settingsChanged(bool inverseSticks, bool randomInverseSticks,
                         real rocketVelocity, bool randomRocketVelocity,
                         real latency, bool randomLatency)

    Connections {
        target: viewManager
        function onGameStateUpdated(state) {
            // Update radio buttons
            for(let i = 0; i < gameModeGroup.buttons.length; i++) {
                let button = gameModeGroup.buttons[i]
                if(button.modeValue === state.gameMode) {
                    button.checked = true
                    break
                }
            }
            
            // Update checkboxes
            inverseSticks.checked = state.inverseSticks
            randomInverseSticks.checked = state.randomInverseSticks
            randomRocketVelocity.checked = state.randomRocketVelocity
            randomLatency.checked = state.randomLatency
            
            // Update sliders
            rocketVelocity.value = state.rocketVelocity
            latency.value = state.latency
        }
    }

    Button {
        id: infoButton
        text: "Info"
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 10
        onClicked: viewManager.onPageChangeClick("gameModeInfo")
    }

    RowLayout {
        anchors.centerIn: parent
        width: parent.width * 0.8
        spacing: 20

        // Left Category - Game Modes
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 10

            Label {
                text: "Game Mode"
                font.bold: true
            }

            ButtonGroup {
                id: gameModeGroup
                // Remove onCheckedButtonChanged handler from here
            }

            RadioButton {
                text: "Follow"
                ButtonGroup.group: gameModeGroup
                property string modeValue: viewManager.getGameMode("follow")
                onClicked: if (checked) viewManager.onGameModeChanged(modeValue)
            }
            RadioButton {
                text: "Goal"
                ButtonGroup.group: gameModeGroup
                property string modeValue: viewManager.getGameMode("goal")
                onClicked: if (checked) viewManager.onGameModeChanged(modeValue)
            }
            RadioButton {
                text: "Infinity"
                ButtonGroup.group: gameModeGroup
                property string modeValue: viewManager.getGameMode("infinity")
                onClicked: if (checked) viewManager.onGameModeChanged(modeValue)
            }
            RadioButton {
                text: "Inverse Follow"
                ButtonGroup.group: gameModeGroup
                property string modeValue: viewManager.getGameMode("inverseFollow")
                onClicked: if (checked) viewManager.onGameModeChanged(modeValue)
            }
        }

        // Right Category - Settings
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 10

            Label {
                text: "Settings"
                font.bold: true
            }

            RowLayout {
                CheckBox {
                    id: inverseSticks
                    text: "Inverse Sticks"
                    enabled: !randomInverseSticks.checked
                    onClicked: viewManager.onCheckboxChanged("inverseSticks", checked)
                }
                CheckBox {
                    id: randomInverseSticks
                    text: "Random"
                    onClicked: viewManager.onCheckboxChanged("randomInverseSticks", checked)
                }
            }

            Label {
                text: "Rocket Velocity"
            }
            RowLayout {
                Slider {
                    id: rocketVelocity
                    Layout.fillWidth: true
                    from: 0
                    to: 1
                    value: 0.5
                    enabled: !randomRocketVelocity.checked
                    onMoved: viewManager.onSliderValueChanged("rocketVelocity", value)
                }
                CheckBox {
                    id: randomRocketVelocity
                    text: "Random"
                    onClicked: viewManager.onCheckboxChanged("randomRocketVelocity", checked)
                }
            }

            Label {
                text: "Latency"
            }
            RowLayout {
                Slider {
                    id: latency
                    Layout.fillWidth: true
                    from: 0
                    to: 1
                    value: 0.5
                    enabled: !randomLatency.checked
                    onMoved: viewManager.onSliderValueChanged("latency", value)
                }
                CheckBox {
                    id: randomLatency
                    text: "Random"
                    onClicked: viewManager.onCheckboxChanged("randomLatency", checked)
                }
            }
        }
    }

    Button {
        text: "Back"
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 10
        onClicked: viewManager.onPageChangeClick("back")
    }
}