import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Item {
    id: audioController

    property alias busy: slider.pressed
    property alias muted: muteButton.checked
    property real volume: slider.value
    property alias showSlider: slider.visible
    property int iconDimension: 24

    implicitHeight: 46
    implicitWidth: mainLayout.width

    RowLayout {
        id: mainLayout
        spacing: 10
        anchors.verticalCenter: parent.verticalCenter

        ToolButton {
            id: muteButton
            implicitHeight: 40
            implicitWidth: 40
            icon.source: audioController.muted ? "qrc:/icons/mute" : "qrc:/icons/volume"
            icon.width: audioController.iconDimension
            icon.height: audioController.iconDimension
            icon.color: palette.buttonText
            flat: true
            checkable: true
        }

        Slider {
            id: slider
            visible: !audioController.showSlider
            implicitWidth: 70
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignVCenter

            enabled: !audioController.muted
            value: 1
        }
    }
}
