from PySide2 import (QtWidgets,
                     QtCore,
                     QtMultimedia)

from reference_player import Logger
from reference_player.widgets.time_slider import QDTimeSlider


class QDPlaybackControls(QtWidgets.QWidget):

    def __init__(self, media_player: QtMultimedia.QMediaPlayer, parent=None):
        super().__init__(parent)

        self.__media_player = media_player
        self._mute_icons_map = {True: self.style().standardIcon(QtWidgets.QStyle.SP_MediaVolumeMuted),
                                False: self.style().standardIcon(QtWidgets.QStyle.SP_MediaVolume)}

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    @property
    def media_player(self):
        return self.__media_player

    def create_widgets(self):
        self.time_slider = QDTimeSlider()
        self.go_to_start_btn = QtWidgets.QPushButton()
        self.step_back_btn = QtWidgets.QPushButton()
        self.play_btn = QtWidgets.QPushButton()
        self.step_forward_btn = QtWidgets.QPushButton()
        self.go_to_end_btn = QtWidgets.QPushButton()
        self.mute_button = QtWidgets.QPushButton()
        self.volume_slider = QtWidgets.QSlider(orientation=QtCore.Qt.Horizontal)

        # Set icons
        self.play_btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.go_to_start_btn.setIcon(self.style().standardIcon(
            QtWidgets.QStyle.SP_MediaSkipBackward))
        self.step_back_btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekBackward))
        self.step_forward_btn.setIcon(self.style().standardIcon(
            QtWidgets.QStyle.SP_MediaSeekForward))
        self.go_to_end_btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaSkipForward))
        self.mute_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaVolume))
        self.mute_button.setFlat(True)
        self.volume_slider.setMaximumWidth(60)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(100)

    def create_layouts(self):
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.go_to_start_btn)
        buttons_layout.addWidget(self.step_back_btn)
        buttons_layout.addWidget(self.play_btn)
        buttons_layout.addWidget(self.step_forward_btn)
        buttons_layout.addWidget(self.go_to_end_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.mute_button)
        buttons_layout.addWidget(self.volume_slider)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.time_slider)
        self.main_layout.addLayout(buttons_layout)

    def create_connections(self):
        self.volume_slider.sliderMoved.connect(self.media_player.setVolume)
        self.volume_slider.sliderMoved.connect(lambda value: self.set_muted(
            True) if not value else self.set_muted(False))
        self.mute_button.clicked.connect(lambda: self.set_muted(not self.media_player.isMuted()))

    @QtCore.Slot(int)
    def set_play_button_icon(self, media_player_state: int):
        if media_player_state == QtMultimedia.QMediaPlayer.PlayingState:
            self.play_btn.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
        else:
            self.play_btn.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))

    @QtCore.Slot()
    def set_muted(self, state: bool):
        self.media_player.setMuted(state)
        self.mute_button.setIcon(self._mute_icons_map[state])
