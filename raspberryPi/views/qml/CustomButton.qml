import QtQuick 2.12
import QtQuick.Controls 2.12

Button {
    id: control
    
    background: Rectangle {
        color: control.pressed ? mainWindow.theme.buttonHoverColor : mainWindow.theme.buttonColor
        radius: 6
        border.color: mainWindow.theme.accentColor
        border.width: 1

        Rectangle {
            anchors.fill: parent
            radius: 6
            color: mainWindow.theme.accentColor
            opacity: control.hovered ? 0.1 : 0
        }

        layer.enabled: true
        layer.effect: ShaderEffect {
            property real spread: 0.5
            fragmentShader: "
                varying highp vec2 qt_TexCoord0;
                uniform sampler2D source;
                uniform lowp float qt_Opacity;
                uniform lowp float spread;
                void main() {
                    lowp vec4 color = texture2D(source, qt_TexCoord0);
                    gl_FragColor = vec4(color.rgb, color.a * qt_Opacity) * 1.1;
                }"
        }
    }

    contentItem: Text {
        text: control.text
        font: control.font
        color: mainWindow.theme.textColor
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
    }
}
