import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtMultimedia
import QtQuick.Dialogs

Item {
    id: root
    required property MediaPlayer mediaPlayer
    property alias muted: audioControl.muted
    property alias volume: audioControl.volume

    implicitHeight: 60

    // ---------------- Actions ----------------
    Action {
        id: homeAction
        icon.source: "qrc:/icons/home"
    }
    Action {
        id: playAction
        icon.source: "qrc:/icons/play"
        onTriggered: root.mediaPlayer.play()
    }
    Action {
        id: pauseAction
        icon.source: "qrc:/icons/pause"
        onTriggered: root.mediaPlayer.pause()
    }
    Action {
        id: skipNextAction
        icon.source: "qrc:/icons/skip_next"
    }
    Action {
        id: skipPreviousAction
        icon.source: "qrc:/icons/skip_previous"
    }
    Action {
        id: fastForwardAction
        icon.source: "qrc:/icons/fast_forward"
    }
    Action {
        id: fastRewindAction
        icon.source: "qrc:/icons/fast_rewind"
    }

    // ---------------- Layout ----------------
    Item {
        anchors.fill: parent

        // Playback buttons centered horizontally
        Row {
            id: playbackButtonsRow
            spacing: 5
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter

            PlaybackButton {
                action: skipPreviousAction
            }
            PlaybackButton {
                action: fastRewindAction
            }
            PlaybackButton {
                id: pauseButton
                action: pauseAction
                visible: root.mediaPlayer.playbackState === MediaPlayer.PlayingState
            }
            PlaybackButton {
                id: playButton
                action: playAction
                visible: root.mediaPlayer.playbackState !== MediaPlayer.PlayingState
            }
            PlaybackButton {
                action: fastForwardAction
            }
            PlaybackButton {
                action: skipNextAction
            }
        }

        // Audio control anchored to the right
        AudioControl {
            id: audioControl
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            anchors.rightMargin: 10
            showSlider: true
        }
    }
}
