import pathlib
import math
import cv2

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtMultimediaWidgets
from PySide2 import QtMultimedia

from reference_player import Logger
from reference_player.core.reference import Reference
from reference_player.widgets.playback_controls_widget import QDPlaybackControls


class MediaFile:
    SUPPORTED_FPS = (60, 59.94, 50, 48, 47.952, 40, 30, 29.97,
                     25, 24, 23.976, 20, 16, 15, 12, 10, 8, 6, 5, 4, 3, 2)

    def __repr__(self) -> str:
        return f"Video - {self.path.name}: {self.frame_count} frames; {self.fps}fps; {self.duration_ms} ms"

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
        self.duratiion_sec = self.frame_count / self.fps
        self.duration_ms = self.duratiion_sec * 1000
        Logger.info(self)

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
    def __init__(self, reference: Reference, parent: QtWidgets.QWidget = None):
        """Widget with media player and playback controls.

        Args:
            video_file (str): path to video file.
            parent (QtWidgets.QWidget, optional): parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.media_file: MediaFile = None
        self.reference: Reference = reference

        # Initialize UI
        self.create_actions()
        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.update_media_file()

    def create_actions(self):
        """Create and configure QActions."""
        self.frame_step_forward_action = QtWidgets.QAction(self, "Frame step forward")
        self.frame_step_back_action = QtWidgets.QAction(self, "Frame step back")
        self.frame_step_back_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_A))
        self.frame_step_forward_action.setShortcut(QtGui.QKeySequence(QtCore.Qt.Key_D))
        # Add actions
        self.addAction(self.frame_step_back_action)
        self.addAction(self.frame_step_forward_action)

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
        self.media_controls = QDPlaybackControls(self.media_player)
        self.video_panel.addWidget(self.frame_counter)
        self.video_panel.addWidget(self.video_widget)

    def create_layouts(self):
        """Create and populate layouts."""
        self.main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(self.video_panel)
        self.main_layout.addWidget(self.media_controls)

    def create_connections(self):
        # Actions
        self.frame_step_back_action.triggered.connect(self.frame_step_back)
        self.frame_step_forward_action.triggered.connect(self.frame_step_forward)

        # Reference
        self.reference.signals.media_file_changed.connect(self.update_media_file)

        # """Create signal to slot connections."""
        self.media_player.positionChanged.connect(self.on_position_change)
        self.media_player.stateChanged.connect(self.on_media_state_change)
        self.media_controls.time_slider.sliderMoved.connect(self.set_position)
        self.frame_counter.editingFinished.connect(self.on_frame_counter_edit)

        # # Media controls
        self.media_controls.go_to_start_btn.clicked.connect(self.go_to_start)
        self.media_controls.step_back_btn.clicked.connect(self.frame_step_back)
        self.media_controls.play_btn.clicked.connect(self.play)
        self.media_controls.step_forward_btn.clicked.connect(self.frame_step_forward)
        self.media_controls.go_to_end_btn.clicked.connect(self.go_to_end)

    def update_media_file(self):
        if not self.reference.is_media_file_valid():
            self.media_file = None
            return

        self.media_file = MediaFile(self.reference.media_file)
        self.load_media_file()

    @QtCore.Slot()
    def load_media_file(self):
        """Load video file"""
        self.media_player.setMedia(QtMultimedia.QMediaContent(
            QtCore.QUrl.fromLocalFile(self.media_file.path.as_posix())))
        self.media_player.setNotifyInterval(1 / self.media_file.fps * 1000)
        self.media_controls.time_slider.set_time_range((0, self.media_file.frame_count))
        self.frame_counter.setMinimum(0)
        self.frame_counter.setMaximum(self.media_file.frame_count)
        self.media_player.play()

    @QtCore.Slot()
    def on_media_state_change(self):
        """Callback for media state change signal:

        - Changes icon between "pause" and "play"
        """
        self.media_controls.set_play_button_icon(self.media_player.state())

    @QtCore.Slot(int)
    def on_position_change(self, position: int):
        """Callback for media player playback position change:

        - Sets time slider position
        - Sets frame counter value

        Args:
            position (int): current playback position
        """
        if not self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            return

        current_frame = self.position_to_frame(position)
        self.media_controls.time_slider.setValue(current_frame)
        if not self.frame_counter.hasFocus():
            self.frame_counter.setValue(current_frame)

        if current_frame >= self.media_controls.time_slider.maximum():
            self.media_player.pause()

    @QtCore.Slot(float)
    def position_to_frame(self, position: float) -> int:
        """Convert position in ms to frame number.

        Args:
            position (float): position in ms

        Returns:
            int: current frame
        """
        if not self.media_file:
            return 0
        progress = position / self.media_file.duration_ms
        frame = progress * self.media_file.frame_count
        return math.ceil(frame)

    @QtCore.Slot(int)
    def frame_to_position(self, frame: int) -> float:
        """Convert current frame to position in ms

        Args:
            frame (int): current frame

        Returns:
            float: playback position in ms
        """
        if not self.media_file:
            return 0

        progress = frame / self.media_file.frame_count
        position = progress * self.media_file.duration_ms
        return position

    @QtCore.Slot()
    def on_frame_counter_edit(self):
        """Callback for editing frame count lineedit:

        - Sets time slider value
        - Sets playback position
        """
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            return

        self.media_controls.time_slider.setValue(self.frame_counter.value())
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

    def frame_step_forward(self):
        self.go_frame(self.media_controls.time_slider.value() + 1)

    def frame_step_back(self):
        self.go_frame(self.media_controls.time_slider.value() - 1)

    def go_frame(self, frame: int):
        """Go to frame.

        Args:
            frame (int): frame number
        """
        self.set_position(frame)
        self.media_controls.time_slider.setValue(frame)

    def go_to_start(self):
        """Go to the start of the playback."""
        self.go_frame(self.media_controls.time_slider.minimum())

    def go_to_end(self):
        """Go to the end of the playback."""
        self.go_frame(self.media_controls.time_slider.maximum())

    def play(self):
        """Play media file."""
        if self.media_player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            if self.media_controls.time_slider.value() >= self.media_controls.time_slider.maximum():
                self.go_to_start()
            self.media_player.play()
