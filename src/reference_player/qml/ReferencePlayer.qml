import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtMultimedia
import "./controls"

Item {
    id: root

    MediaPlayer {
        id: mediaPlayer
        source: "/Users/dima/Library/Mobile Documents/com~apple~CloudDocs/Music Production/Edit Clips/saccharine.mov"

        videoOutput: videoOutput
        audioOutput: audioOutput
    }

    VideoOutput {
        id: videoOutput

        anchors.fill: parent
        visible: mediaPlayer.mediaStatus > 0
    }

    AudioOutput {
        id: audioOutput
        muted: playbackController.muted
        volume: playbackController.volume
    }

    PlaybackControl {
        id: playbackController

        mediaPlayer: mediaPlayer
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
    }
}
