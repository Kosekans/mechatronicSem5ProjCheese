// mainWindow.qml
import QtQuick 2.12
import QtQuick.Window 2.12

Window {
    id: mainWindow
    visible: true
    width: windowWidth
    height: windowHeight
    title: windowTitle

    Loader {
        id: pageLoader
        anchors.fill: parent
        source: "mainMenu.qml"  // default page
    }

    Connections {
        target: viewManager
        function onPageChanged(pageName) {
            if (pageName === "main") {
                pageLoader.source = "mainMenu.qml"
            } else if (pageName === "settings") {
                pageLoader.source = "settings.qml"
            } else if (pageName === "highscore") {
                pageLoader.source = "highscore.qml"
            } else if (pageName === "credits") {
                pageLoader.source = "credits.qml"
            }
        }
    }
}