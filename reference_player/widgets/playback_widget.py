import pathlib
import cv2
from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtMultimediaWidgets
from PySide2 import QtMultimedia

from reference_player import Logger
from reference_player.widgets.media_controls_widget import QDMediaControls


class VideoFile:
    SUPPORTED_FPS = [60, 59.94, 50, 48, 47.952, 40, 30, 29.97,
                     25, 24, 23.976, 20, 16, 15, 12, 10, 8, 6, 5, 4, 3, 2]

    def __repr__(self) -> str:
        return f"Video - {self.path.name}: {self.frame_count} frames; {self.fps}fps, {self.duration_ms}({self.duration_sec})ms"

    def __init__(self, file_path: str):
        """Video file data.

        Args:
            file_path (str): path to video file.
        """
        self.path = pathlib.Path(file_path)
        self.capture = cv2.VideoCapture(self.path.as_posix())
        self.frame_count = self.get_frame_count()
        self.fps: int = min(self.SUPPORTED_FPS, key=lambda x: abs(
            x - self.capture.get(cv2.CAP_PROP_FPS)))
        self.duration_sec = self.frame_count / self.fps
        self.duration_ms = self.duration_sec * 1000
        Logger.debug(self)

    def get_frame_count(self) -> int:
        """Get frame count of the video from file metadata.

        If metadata doesn't have info - count manually (slow)

        Returns:
            int: number of frames
        """
        # Try fast count
        frames = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if not frames:
            Logger.warning("Failed to get frame count from meta data, counting frames...")
            frames = 0
            success = True
            while success:
                success, image = self.capture.read()
                frames += 1

        return frames


class QDPlaybackWidget(QtWidgets.QWidget):
    def __init__(self, video_file: str, parent: QtWidgets.QWidget = None):
        """Widget with media player and playback controls.

        Args:
            video_file (str): path to video file.
            parent (QtWidgets.QWidget, optional): parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.video_file = VideoFile(video_file)

        # Initialize UI
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        # Load video file
        self.load_file()

    def create_actions(self):
        """Create and configure QActions."""
        pass

    def create_widgets(self):
        """Create and configure widgets."""
        # Video panel
        self.video_panel = QtWidgets.QStackedWidget()
        self.video_panel.layout().setStackingMode(QtWidgets.QStackedLayout.StackAll)
        self.video_widget = QtMultimediaWidgets.QVideoWidget(self)
        self.frame_counter: QtWidgets.QSpinBox = QtWidgets.QSpinBox()
        self.frame_counter.setFrame(False)
        self.frame_counter.setMaximumSize(40, 20)
        self.frame_counter.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.frame_counter.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.media_player = QtMultimedia.QMediaPlayer(self, QtMultimedia.QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)

        # Playback controls
        self.controls = QDMediaControls()
        self.time_slider = QtWidgets.QSlider(orientation=QtCore.Qt.Horizontal)
        self.play_btn = QtWidgets.QPushButton()
        self.play_btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.video_panel.addWidget(self.frame_counter)
        self.video_panel.addWidget(self.video_widget)

    def create_layouts(self):
        """Create and populate layouts."""
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.video_panel)
        self.main_layout.addWidget(self.time_slider)
        self.main_layout.addWidget(self.play_btn)

    def create_connections(self):
        """Create signal to slot connections."""
        self.media_player.positionChanged.connect(self.on_position_change)
        self.media_player.stateChanged.connect(self.on_media_state_change)
        self.time_slider.sliderMoved.connect(self.set_position)
        self.frame_counter.editingFinished.connect(self.on_frame_counter_edit)
        self.play_btn.clicked.connect(self.play)

    @QtCore.Slot()
    def load_file(self):
        """Load video file"""
        self.media_player.setMedia(QtMultimedia.QMediaContent(
            QtCore.QUrl.fromLocalFile(self.video_file.path.as_posix())))
        self.media_player.setNotifyInterval(1 / self.video_file.fps * 1000)
        self.time_slider.setMinimum(0)
        self.time_slider.setMaximum(self.video_file.frame_count)
        self.frame_counter.setMinimum(0)
        self.frame_counter.setMaximum(self.video_file.frame_count)
        self.media_player.play()

    @QtCore.Slot()
    def on_media_state_change(self):
        """Callback for media state change signal:

        - Changes icon between "pause" and "play"
        """
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.play_btn.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.play_btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

    @QtCore.Slot(int)
    def on_position_change(self, position: int):
        """Callback for media player playback position change:

        - Sets time slider position
        - Sets frame counter value

        Args:
            position (int): current playback position
        """
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            current_frame = self.position_to_frame(position)
            # Logger.debug(current_frame)
            if current_frame > self.time_slider.maximum():
                self.time_slider.setValue(self.time_slider.maximum())
                self.media_player.pause()
            else:
                self.time_slider.setValue(current_frame)
                self.frame_counter.setValue(current_frame)

    @QtCore.Slot(float)
    def position_to_frame(self, position: float) -> int:
        """Convert position in ms to frame number.

        Args:
            position (float): position in ms

        Returns:
            int: current frame
        """

        frame = 0
        if position:
            progress = position / self.video_file.duration_ms
            frame = progress * self.video_file.frame_count
        return int(frame)

    @QtCore.Slot(int)
    def frame_to_position(self, frame: int) -> float:
        """Convert current frame to position in ms

        Args:
            frame (int): current frame

        Returns:
            float: playback position in ms
        """
        progress = frame / self.video_file.frame_count
        position = progress * self.video_file.duration_ms
        return position

    @QtCore.Slot()
    def on_frame_counter_edit(self):
        """Callback for editing frame count lineedit:

        - Sets time slider value
        - Sets playback position
        """
        self.time_slider.setValue(self.frame_counter.value())
        self.set_position(self.frame_counter.value())

    @QtCore.Slot()
    def set_position(self, frame: int):
        """Set playback position from frame.

        Args:
            frame (int): frame number
        """
        prev_state = self.media_player.state()
        new_position = self.frame_to_position(frame)
        self.media_player.setPosition(new_position)
        self.frame_counter.setValue(frame)
        self.media_player.play()
        if prev_state == self.media_player.PausedState:
            self.media_player.pause()

    def go_frame(self, frame: int):
        """Go to frame.

        Args:
            frame (int): frame number
        """
        self.set_position(frame)
        self.time_slider.setValue(frame)

    def go_to_start(self):
        """Go to the start of the playback."""
        self.go_frame(self.time_slider.minimum())

    def go_to_end(self):
        """Go to the end of the playback."""
        self.go_frame(self.time_slider.maximum())

    def play(self):
        """Play media file."""
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            if self.time_slider.value() >= self.time_slider.maximum():
                self.go_to_start()
            self.media_player.play()