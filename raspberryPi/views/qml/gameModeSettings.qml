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

    CustomButton {
        id: infoButton
        text: "Info"
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 20
        width: 100
        height: 60
        font.pixelSize: 20
        onClicked: viewManager.onPageChangeClick("gameModeInfo")
    }

    RowLayout {
        anchors.centerIn: parent
        anchors.margins: 20
        width: parent.width * 0.9
        height: parent.height * 0.8
        spacing: 40

        // Left Category - Game Modes
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 15

            Label {
                text: "Game Mode"
                font.bold: true
                font.pixelSize: 24
                color: mainWindow.theme.textColor
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
                font.pixelSize: 20
                indicator: Rectangle {
                    width: 20
                    height: 20
                    radius: 10
                    border.color: mainWindow.theme.accentColor
                    border.width: 1
                    color: "transparent"

                    Rectangle {
                        anchors.centerIn: parent
                        width: 12
                        height: 12
                        radius: 6
                        color: mainWindow.theme.accentColor
                        visible: parent.parent.checked
                    }
                }
                contentItem: Text {
                    text: parent.text
                    color: mainWindow.theme.textColor
                    font.pixelSize: 20
                    leftPadding: parent.indicator.width + 8
                }
            }
            RadioButton {
                text: "Goal"
                ButtonGroup.group: gameModeGroup
                property string modeValue: viewManager.getGameMode("goal")
                onClicked: if (checked) viewManager.onGameModeChanged(modeValue)
                font.pixelSize: 20
                indicator: Rectangle {
                    width: 20
                    height: 20
                    radius: 10
                    border.color: mainWindow.theme.accentColor
                    border.width: 1
                    color: "transparent"

                    Rectangle {
                        anchors.centerIn: parent
                        width: 12
                        height: 12
                        radius: 6
                        color: mainWindow.theme.accentColor
                        visible: parent.parent.checked
                    }
                }
                contentItem: Text {
                    text: parent.text
                    color: mainWindow.theme.textColor
                    font.pixelSize: 20
                    leftPadding: parent.indicator.width + 8
                }
            }
            RadioButton {
                text: "Infinity"
                ButtonGroup.group: gameModeGroup
                property string modeValue: viewManager.getGameMode("infinity")
                onClicked: if (checked) viewManager.onGameModeChanged(modeValue)
                font.pixelSize: 20
                indicator: Rectangle {
                    width: 20
                    height: 20
                    radius: 10
                    border.color: mainWindow.theme.accentColor
                    border.width: 1
                    color: "transparent"

                    Rectangle {
                        anchors.centerIn: parent
                        width: 12
                        height: 12
                        radius: 6
                        color: mainWindow.theme.accentColor
                        visible: parent.parent.checked
                    }
                }
                contentItem: Text {
                    text: parent.text
                    color: mainWindow.theme.textColor
                    font.pixelSize: 20
                    leftPadding: parent.indicator.width + 8
                }
            }
            RadioButton {
                text: "Inverse Follow"
                ButtonGroup.group: gameModeGroup
                property string modeValue: viewManager.getGameMode("inverseFollow")
                onClicked: if (checked) viewManager.onGameModeChanged(modeValue)
                font.pixelSize: 20
                indicator: Rectangle {
                    width: 20
                    height: 20
                    radius: 10
                    border.color: mainWindow.theme.accentColor
                    border.width: 1
                    color: "transparent"

                    Rectangle {
                        anchors.centerIn: parent
                        width: 12
                        height: 12
                        radius: 6
                        color: mainWindow.theme.accentColor
                        visible: parent.parent.checked
                    }
                }
                contentItem: Text {
                    text: parent.text
                    color: mainWindow.theme.textColor
                    font.pixelSize: 20
                    leftPadding: parent.indicator.width + 8
                }
            }
            RadioButton {
                text: "Demo Mode"
                ButtonGroup.group: gameModeGroup
                property string modeValue: viewManager.getGameMode("demo")
                onClicked: if (checked) viewManager.onGameModeChanged(modeValue)
                font.pixelSize: 20
                indicator: Rectangle {
                    width: 20
                    height: 20
                    radius: 10
                    border.color: mainWindow.theme.accentColor
                    border.width: 1
                    color: "transparent"

                    Rectangle {
                        anchors.centerIn: parent
                        width: 12
                        height: 12
                        radius: 6
                        color: mainWindow.theme.accentColor
                        visible: parent.parent.checked
                    }
                }
                contentItem: Text {
                    text: parent.text
                    color: mainWindow.theme.textColor
                    font.pixelSize: 20
                    leftPadding: parent.indicator.width + 8
                }
            }
        }

        // Right Category - Settings
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 15

            Label {
                text: "Settings"
                font.bold: true
                font.pixelSize: 24
                color: mainWindow.theme.textColor
            }

            RowLayout {
                CheckBox {
                    id: inverseSticks
                    text: "Inverse Sticks"
                    enabled: !randomInverseSticks.checked
                    onClicked: viewManager.onCheckboxChanged("inverseSticks", checked)
                    font.pixelSize: 18
                    indicator: Rectangle {
                        width: 20
                        height: 20
                        border.color: mainWindow.theme.accentColor
                        border.width: 1
                        color: "transparent"

                        Rectangle {
                            anchors.centerIn: parent
                            width: 12
                            height: 12
                            color: mainWindow.theme.accentColor
                            visible: parent.parent.checked
                        }
                    }
                    contentItem: Text {
                        text: parent.text
                        color: mainWindow.theme.textColor
                        font.pixelSize: 18
                        leftPadding: parent.indicator.width + 8
                    }
                }
                CheckBox {
                    id: randomInverseSticks
                    text: "Random"
                    onClicked: viewManager.onCheckboxChanged("randomInverseSticks", checked)
                    font.pixelSize: 18
                    indicator: Rectangle {
                        width: 20
                        height: 20
                        border.color: mainWindow.theme.accentColor
                        border.width: 1
                        color: "transparent"

                        Rectangle {
                            anchors.centerIn: parent
                            width: 12
                            height: 12
                            color: mainWindow.theme.accentColor
                            visible: parent.parent.checked
                        }
                    }
                    contentItem: Text {
                        text: parent.text
                        color: mainWindow.theme.textColor
                        font.pixelSize: 18
                        leftPadding: parent.indicator.width + 8
                    }
                }
            }

            Label {
                text: "Rocket Velocity"
                font.pixelSize: 20
                color: mainWindow.theme.textColor
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
                    handle: Rectangle {
                        x: parent.leftPadding + parent.visualPosition * (parent.availableWidth - width)
                        y: parent.topPadding + parent.availableHeight / 2 - height / 2
                        width: 20
                        height: 20
                        radius: 10
                        color: mainWindow.theme.buttonColor
                        border.color: mainWindow.theme.accentColor
                        border.width: 1
                    }
                    background: Rectangle {
                        x: parent.leftPadding
                        y: parent.topPadding + parent.availableHeight / 2 - height / 2
                        width: parent.availableWidth
                        height: 4
                        radius: 2
                        color: mainWindow.theme.buttonColor
                        Rectangle {
                            width: parent.parent.visualPosition * parent.width
                            height: parent.height
                            color: mainWindow.theme.accentColor
                            radius: 2
                        }
                    }
                }
                CheckBox {
                    id: randomRocketVelocity
                    text: "Random"
                    onClicked: viewManager.onCheckboxChanged("randomRocketVelocity", checked)
                    font.pixelSize: 18
                    indicator: Rectangle {
                        width: 20
                        height: 20
                        border.color: mainWindow.theme.accentColor
                        border.width: 1
                        color: "transparent"

                        Rectangle {
                            anchors.centerIn: parent
                            width: 12
                            height: 12
                            color: mainWindow.theme.accentColor
                            visible: parent.parent.checked
                        }
                    }
                    contentItem: Text {
                        text: parent.text
                        color: mainWindow.theme.textColor
                        font.pixelSize: 18
                        leftPadding: parent.indicator.width + 8
                    }
                }
            }

            Label {
                text: "Latency"
                font.pixelSize: 20
                color: mainWindow.theme.textColor
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
                    handle: Rectangle {
                        x: parent.leftPadding + parent.visualPosition * (parent.availableWidth - width)
                        y: parent.topPadding + parent.availableHeight / 2 - height / 2
                        width: 20
                        height: 20
                        radius: 10
                        color: mainWindow.theme.buttonColor
                        border.color: mainWindow.theme.accentColor
                        border.width: 1
                    }
                    background: Rectangle {
                        x: parent.leftPadding
                        y: parent.topPadding + parent.availableHeight / 2 - height / 2
                        width: parent.availableWidth
                        height: 4
                        radius: 2
                        color: mainWindow.theme.buttonColor
                        Rectangle {
                            width: parent.parent.visualPosition * parent.width
                            height: parent.height
                            color: mainWindow.theme.accentColor
                            radius: 2
                        }
                    }
                }
                CheckBox {
                    id: randomLatency
                    text: "Random"
                    onClicked: viewManager.onCheckboxChanged("randomLatency", checked)
                    font.pixelSize: 18
                    indicator: Rectangle {
                        width: 20
                        height: 20
                        border.color: mainWindow.theme.accentColor
                        border.width: 1
                        color: "transparent"

                        Rectangle {
                            anchors.centerIn: parent
                            width: 12
                            height: 12
                            color: mainWindow.theme.accentColor
                            visible: parent.parent.checked
                        }
                    }
                    contentItem: Text {
                        text: parent.text
                        color: mainWindow.theme.textColor
                        font.pixelSize: 18
                        leftPadding: parent.indicator.width + 8
                    }
                }
            }
        }
    }

    CustomButton {
        text: "Back"
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.margins: 20
        width: 200
        height: 60
        font.pixelSize: 24
        onClicked: viewManager.onPageChangeClick("back")
    }
}