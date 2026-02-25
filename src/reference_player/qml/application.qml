import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    title: "Reference Player"
    visible: true
    width: 1280
    height: 720
    minimumWidth: 960
    minimumHeight: 540

    ReferencePlayer {
        anchors.fill: parent
    }
}
