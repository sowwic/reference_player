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

    ColumnLayout {
        anchors.fill: parent

        VideoOutput {
            id: videoOutput

            Layout.fillHeight: true
            Layout.fillWidth: true
        }

        AudioOutput {
            id: audioOutput
            muted: playbackController.muted
            volume: playbackController.volume
        }

        PlaybackControl {
            id: playbackController
            Layout.preferredHeight: 50
            Layout.preferredWidth: implicitWidth
            Layout.alignment: Qt.AlignCenter
            mediaPlayer: mediaPlayer
        }
    }
}
