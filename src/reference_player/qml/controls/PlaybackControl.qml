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

    implicitHeight: 200
    implicitWidth: 300

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

    RowLayout {
        id: controlsLayout

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

        AudioControl {
            id: audioControl

            showSlider: true
        }
    }
}
