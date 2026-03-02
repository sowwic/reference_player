import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    title: "Reference Player"
    visible: true
    width: minimumWidth
    height: minimumHeight
    minimumWidth: 700
    minimumHeight: 540

    ReferencePlayer {
        anchors.fill: parent
    }
}
