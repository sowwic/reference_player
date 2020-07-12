import os
import socket
import cv2
import json
import logging
from PySide2 import QtWidgets, QtGui, QtCore, QtMultimediaWidgets, QtMultimedia
from scripts import settingsFn
from scripts import resources  # noqa: F401

VERSION = "1.3.2"

# Logger
logger = logging.getLogger(__name__)


class _videoMetaStruct:
    def __init__(self):
        self.readFlag = None
        self.frameCount = None
        self.duration = None
        self.frameRate = None


class Window(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.version = VERSION
        self.settings = settingsFn.Settings()

        # Setup logging file
        fileLogHandler = logging.FileHandler(filename=os.path.join(self.settings.directory, "dsReferencePlayerExceptions.log"), mode="w")
        fileLogHandler.setLevel(logging.DEBUG)
        # Formatter
        baseFormatter = logging.Formatter(f'ver.{VERSION} - %(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fileLogHandler.setFormatter(baseFormatter)
        # Add handlers
        logger.addHandler(fileLogHandler)

        # ADD BARS
        self.addStatusBar()
        self.addMenuBar()

        # BUILD UI
        # Set window options
        self.setWindowTitle('dsReferencePlayer')
        self.setMinimumSize(400, 300)
        self.setWindowIcon(QtGui.QIcon(":/images/dsIcon.ico"))

        # Create
        self.createWidgets()
        self.createLayouts()
        self.createConnections()
        self.toggleOnTop(self.settings.current.get("alwaysOnTop", True), update=False)

        # Video data struct
        self.videoMeta = _videoMetaStruct()

        # INIT MAYA CLIENT
        self.mayaClient = None
        self.connected = False
        if self.settings.current.get("connectOnStart", False):
            self.connectToMaya()
        self.updateConnectionStatus()

    def connectToMaya(self):
        try:
            del self.mayaClient
            self.mayaClient = MayaClient(port=self.settings.current["port"])
            self.connected = self.mayaClient.connect()
        except Exception as e:
            logger.error(
                f"Failed to connect to port {self.settings.current['port']}")
            self.connected = self.mayaClient.connect()

        if not self.connected:
            msg = QtWidgets.QMessageBox(parent=self)
            msg.setWindowTitle("Failed to connect")
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setWindowIcon(QtGui.QIcon(":/images/dsIcon.ico"))
            msg.setText(
                "Failed to connect to Maya, check if port is correct at 'File > Set port' and try connecting again")
            msg.setTextFormat(QtCore.Qt.RichText)
            msg.exec_()

        self.updateConnectionStatus()

    def addMenuBar(self):
        # INIT MENUS
        self.mainMenubar = self.menuBar()
        self.fileMenu = self.mainMenubar.addMenu("&File")
        self.viewMenu = self.mainMenubar.addMenu("View")
        self.playBackMenu = self.mainMenubar.addMenu("Playback")
        self.helpMenu = self.mainMenubar.addMenu("Help")

        # FILE OPTIONS
        # Open file
        self.openAction = QtWidgets.QAction(
            QtGui.QIcon("open.png"), "&Open", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.setStatusTip("Open reference file")

        # Set maya port
        self.portAction = QtWidgets.QAction("Set connection port", self)

        # Save/Load preset
        self.savePresetAction = QtWidgets.QAction("Save preset", self)
        self.loadPresetAction = QtWidgets.QAction("Load preset", self)
        self.savePresetAction.setEnabled(False)
        self.loadPresetAction.setEnabled(False)

        # Connect to maya
        self.connectToMayaAction = QtWidgets.QAction("Connect to Maya", self)
        self.connectOnStartAction = QtWidgets.QAction(
            "Auto connect on launch", self)
        self.connectOnStartAction.setCheckable(True)
        self.connectOnStartAction.setChecked(
            self.settings.current.get("connectOnStart", False))

        # VIEW OPTIONS
        # Always on top
        self.alwaysOnTopAction = QtWidgets.QAction("Always on top", self)
        self.alwaysOnTopAction.setCheckable(True)
        self.alwaysOnTopAction.setChecked(
            self.settings.current.get("alwaysOnTop", True))

        # Counter toggle
        self.counterAction = QtWidgets.QAction("Frame Counter", self)
        self.counterAction.setCheckable(True)
        self.counterAction.setChecked(True)

        # Statusbar toggle
        self.statusBarAction = QtWidgets.QAction("Status Bar", self)
        self.statusBarAction.setCheckable(True)
        self.statusBarAction.setChecked(False)

        # Time line panel toggle
        self.timeLinePanelAction = QtWidgets.QAction("Time Line Panel", self)
        self.timeLinePanelAction.setCheckable(True)
        self.timeLinePanelAction.setChecked(True)

        # Viewer toggle
        self.previewPanelAction = QtWidgets.QAction("Video Preview", self)
        self.previewPanelAction.setCheckable(True)
        self.previewPanelAction.setChecked(True)

        # Control panel toggle
        self.controlPanelAction = QtWidgets.QAction("Control Panel", self)
        self.controlPanelAction.setCheckable(True)
        self.controlPanelAction.setChecked(True)

        # PLAYBACK OPTIONS
        self.negatePlayBackStartAction = QtWidgets.QAction(
            "Negate playback start")
        self.setPlayBackStartAction = QtWidgets.QAction("Set start frame")
        self.setPlayBackEndAction = QtWidgets.QAction("Set end frame")
        self.setPlayBackStartAction.setShortcut("S")
        self.setPlayBackEndAction.setShortcut("Alt+S")
        # Match playback options
        self.matchPlaybackOptionsAction = QtWidgets.QAction(
            "Match player playback options")

        # Help options
        self.commandPortHelpAction = QtWidgets.QAction("Maya connection")
        self.aboutAction = QtWidgets.QAction("About")

        # ADD TO ACTIONS TO MENUS
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.savePresetAction)
        self.fileMenu.addAction(self.loadPresetAction)
        mayaConnSeparator = self.fileMenu.addSeparator()
        mayaConnSeparator.setText("Maya")
        self.fileMenu.addAction(self.connectToMayaAction)
        self.fileMenu.addAction(self.portAction)
        self.fileMenu.addAction(self.connectOnStartAction)

        panelViewSeparator = self.viewMenu.addSeparator()
        panelViewSeparator.setText("Panels")
        self.viewMenu.addAction(self.timeLinePanelAction)
        self.viewMenu.addAction(self.controlPanelAction)
        self.viewMenu.addAction(self.previewPanelAction)
        self.viewMenu.addAction(self.counterAction)
        self.viewMenu.addAction(self.statusBarAction)
        windowViewSeparator = self.viewMenu.addSeparator()
        self.viewMenu.addAction(self.alwaysOnTopAction)
        windowViewSeparator.setText("Window")

        playerPlayBackSeparator = self.playBackMenu.addSeparator()
        playerPlayBackSeparator.setText("Player")
        self.playBackMenu.addAction(self.negatePlayBackStartAction)
        self.playBackMenu.addAction(self.setPlayBackStartAction)
        self.playBackMenu.addAction(self.setPlayBackEndAction)
        mayaPlayBackSeparator = self.playBackMenu.addSeparator()
        mayaPlayBackSeparator.setText("Maya")
        self.playBackMenu.addAction(self.matchPlaybackOptionsAction)

        self.helpMenu.addAction(self.commandPortHelpAction)
        self.helpMenu.addAction(self.aboutAction)

    def addStatusBar(self):
        self.statusBar = QtWidgets.QStatusBar()
        self.statusBar.setMaximumHeight(30)
        self.statusBar.setEnabled(False)

    def createWidgets(self):
        self.mainWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.mainWidget)

        # UTILS
        boldFont = QtGui.QFont()
        boldFont.setBold(True)
        # VIDEO
        self.mediaPlayer = QtMultimedia.QMediaPlayer(
            None, QtMultimedia.QMediaPlayer.VideoSurface)
        self.videoWidget = QtMultimediaWidgets.QVideoWidget()
        self.frameCounter = QtWidgets.QLineEdit()
        self.frameCounter.setMaximumSize(40, 20)
        self.frameCounter.setFrame(False)
        self.frameCounter.setFont(boldFont)
        self.frameCounter.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.frameCounter.setValidator(QtGui.QIntValidator(-9999, 9999))
        self.frameCounter.setEnabled(False)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.videoWidget.show()

        # TIMELINE
        self.playBackOffset = QtWidgets.QLineEdit()
        self.playBackStart = QtWidgets.QLineEdit()
        self.timeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.playBackEnd = QtWidgets.QLineEdit()
        self.videoEnd = QtWidgets.QLineEdit()
        self.playBackOffset.setValidator(QtGui.QIntValidator(-9999, 9999))
        self.playBackStart.setValidator(QtGui.QIntValidator(-9999, 9999))
        self.playBackEnd.setValidator(QtGui.QIntValidator(-9999, 9999))
        self.videoEnd.setValidator(QtGui.QIntValidator(-9999, 9999))

        self.playBackOffset.setMaximumWidth(35)
        self.playBackStart.setMaximumWidth(35)
        self.playBackEnd.setMaximumWidth(35)
        self.videoEnd.setMaximumWidth(35)
        self.timeSlider.setRange(0, 0)
        self.timeSlider.setTickPosition(QtWidgets.QSlider.TicksBothSides)

        # Default values
        self.playBackOffset.setEnabled(False)
        self.videoEnd.setEnabled(False)
        self.playBackOffset.setText(str(0))
        self.videoEnd.setText(str(0))
        self.playBackStart.setText(str(0))
        self.playBackEnd.setText(str(0))
        # CONTROLS
        self.syncCheckBox = QtWidgets.QCheckBox()
        self.frameRateLabel = QtWidgets.QLabel()
        self.syncLabel = QtWidgets.QLabel("Sync")
        self.backToStartButton = QtWidgets.QPushButton()
        self.frameBackButton = QtWidgets.QPushButton()
        self.playButton = QtWidgets.QPushButton()
        self.frameForwardButton = QtWidgets.QPushButton()
        self.toEndButton = QtWidgets.QPushButton()
        self.muteButton = QtWidgets.QPushButton()
        self.volumeSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.backToStartButton.setIcon(self.style().standardIcon(
            QtWidgets.QStyle.SP_MediaSkipBackward))
        self.frameBackButton.setIcon(self.style().standardIcon(
            QtWidgets.QStyle.SP_MediaSeekBackward))
        self.playButton.setIcon(self.style().standardIcon(
            QtWidgets.QStyle.SP_MediaPlay))
        self.frameForwardButton.setIcon(
            self.style().standardIcon(QtWidgets.QStyle.SP_MediaSeekForward))
        self.toEndButton.setIcon(self.style().standardIcon(
            QtWidgets.QStyle.SP_MediaSkipForward))
        self.muteButton.setIcon(self.style().standardIcon(
            QtWidgets.QStyle.SP_MediaVolume))
        self.muteButton.setFlat(True)
        self.volumeSlider.setMaximumWidth(60)
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setValue(100)

        for btn in [self.playButton, self.backToStartButton, self.frameBackButton, self.frameForwardButton, self.toEndButton]:
            btn.setEnabled(False)
            btn.setFlat(True)

    def createLayouts(self):
        self.previewPanel = QtWidgets.QWidget()
        stackedLayout = QtWidgets.QStackedLayout()
        stackedLayout.addWidget(self.videoWidget)
        stackedLayout.addWidget(self.frameCounter)
        stackedLayout.setStackingMode(QtWidgets.QStackedLayout.StackAll)
        self.previewPanel.setLayout(stackedLayout)

        self.timeLinePanel = QtWidgets.QWidget()
        timeLineLayout = QtWidgets.QHBoxLayout()
        timeLineLayout.setContentsMargins(0, 0, 0, 0)
        timeLineLayout.addWidget(self.playBackOffset)
        timeLineLayout.addWidget(self.playBackStart)
        timeLineLayout.addWidget(self.timeSlider)
        timeLineLayout.addWidget(self.playBackEnd)
        timeLineLayout.addWidget(self.videoEnd)
        self.timeLinePanel.setLayout(timeLineLayout)

        self.controlPanel = QtWidgets.QWidget()
        controlsLayout = QtWidgets.QHBoxLayout()
        controlsLayout.addWidget(self.syncCheckBox)
        controlsLayout.addWidget(self.syncLabel)
        controlsLayout.addWidget(self.frameRateLabel)
        controlsLayout.addSpacing(40)
        controlsLayout.addStretch()
        controlsLayout.addWidget(self.backToStartButton)
        controlsLayout.addWidget(self.frameBackButton)
        controlsLayout.addWidget(self.playButton)
        controlsLayout.addWidget(self.frameForwardButton)
        controlsLayout.addWidget(self.toEndButton)
        controlsLayout.addSpacing(40)
        controlsLayout.addStretch()
        controlsLayout.addWidget(self.muteButton)
        controlsLayout.addWidget(self.volumeSlider)
        self.controlPanel.setLayout(controlsLayout)
        self.controlPanel.setMaximumHeight(38)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.previewPanel)
        mainLayout.addWidget(self.timeLinePanel)
        mainLayout.addWidget(self.controlPanel)
        mainLayout.addWidget(self.statusBar)

        self.mainWidget.setLayout(mainLayout)

    def createConnections(self):
        # MENU BAR
        # File
        self.openAction.triggered.connect(self.openFile)
        self.savePresetAction.triggered.connect(self.savePreset)
        self.loadPresetAction.triggered.connect(self.loadPreset)
        self.portAction.triggered.connect(self.changeMayaPort)
        self.connectToMayaAction.triggered.connect(self.connectToMaya)
        self.connectOnStartAction.toggled.connect(self.toggleAutoConnect)
        # Playback
        self.negatePlayBackStartAction.triggered.connect(
            self.negatePlayBackStart)
        self.setPlayBackStartAction.triggered.connect(
            self.setCurrentFrameAsStart)
        self.setPlayBackEndAction.triggered.connect(self.setCurrentFrameAsEnd)
        self.matchPlaybackOptionsAction.triggered.connect(
            self.setMayaPlaybackOptions)
        # View
        self.counterAction.toggled.connect(self.frameCounter.setVisible)
        self.timeLinePanelAction.toggled.connect(self.timeLinePanel.setVisible)
        self.controlPanelAction.toggled.connect(self.controlPanel.setVisible)
        self.previewPanelAction.toggled.connect(self.previewPanel.setVisible)
        self.alwaysOnTopAction.toggled.connect(self.toggleOnTop)
        # Help
        self.aboutAction.triggered.connect(self.showAbout)
        self.commandPortHelpAction.triggered.connect(self.showCommandPortHelp)
        self.statusBarAction.toggled.connect(self.statusBar.setVisible)
        # FRAME COUNTER
        self.frameCounter.returnPressed.connect(self.goToFrame)

        # MAYA COMMANDS
        self.timeSlider.valueChanged.connect(self.setMayaTimeSlider)

        # PLAYBACK
        self.playButton.clicked.connect(self.play)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.timeSlider.sliderMoved.connect(self.setPosition)
        self.frameForwardButton.clicked.connect(self.stepFrameForward)
        self.frameBackButton.clicked.connect(self.stepFrameBackward)
        self.backToStartButton.clicked.connect(self.toStart)
        self.toEndButton.clicked.connect(self.toEnd)

        # RANGE
        self.playBackStart.returnPressed.connect(self.setRange)
        self.playBackEnd.returnPressed.connect(self.setRange)

        # VOLUME
        self.volumeSlider.sliderMoved.connect(self.setVolume)
        self.muteButton.clicked.connect(self.toggleMute)

        # Status bar
        self.statusBar.messageChanged.connect(self.hideEmptyStatusBar)

    def setMayaTimeSlider(self, *args):
        if self.syncCheckBox.isChecked() and self.connected:
            if self.mayaClient.connect():
                self.mayaClient.setCurrentTime(
                    int(self.playBackOffset.text()) + self.timeSlider.value())
            else:
                self.timeSlider.valueChanged.disconnect()

    def openFile(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open Reference", QtCore.QDir.homePath())
        if fileName:
            # STORE META DATA
            self.videoMeta.path = fileName
            self.videoMeta.frameCount = self.getFrames(fileName)

            # SET MEDIA FILE
            self.mediaPlayer.setMedia(QtMultimedia.QMediaContent(
                QtCore.QUrl.fromLocalFile(fileName)))
            self.mediaPlayer.play()
            self.mediaPlayer.pause()
            for btn in [self.playButton, self.backToStartButton, self.frameBackButton, self.frameForwardButton, self.toEndButton]:
                btn.setEnabled(True)

    def play(self, *args):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            if self.timeSlider.value() >= self.timeSlider.maximum():
                self.toStart()
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPause))
            self.frameCounter.setEnabled(False)
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
            self.frameCounter.setEnabled(True)

    def positionChanged(self, position):
        if self.mediaPlayer.state() == QtMultimedia.QMediaPlayer.PlayingState:
            frame = self.positionToFrame(position)
            if frame:
                if frame >= self.timeSlider.maximum():
                    self.timeSlider.setValue(self.timeSlider.maximum())
                    self.mediaPlayer.pause()
                else:
                    self.timeSlider.setValue(frame)

                self.frameCounter.setText(str(self.timeSlider.value()))

    def setPosition(self, position):
        self.frameCounter.setText(str(position))
        currentPosition = self.frameToPosition(position)
        self.mediaPlayer.setPosition(currentPosition)
        self.mediaPlayer.play()
        self.mediaPlayer.pause()

    def durationChanged(self, duration):
        if duration:
            frameRates = [60, 59.94, 50, 48, 47.952, 40, 30, 29.97,
                          25, 24, 23.976, 20, 16, 15, 12, 10, 8, 6, 5, 4, 3, 2]
            self.videoMeta.duration = duration / 1000
            self.timeSlider.setRange(0, self.videoMeta.frameCount)

            # Get frame rate
            rate = self.videoMeta.frameCount / self.videoMeta.duration
            self.videoMeta.frameRate = min(
                frameRates, key=lambda x: abs(x - rate))
            # Set media player update time
            self.mediaPlayer.setNotifyInterval(
                1 / self.videoMeta.frameRate * 1000)
            self.frameRateLabel.setText(str(self.videoMeta.frameRate) + " fps")
            self.playBackOffset.setText(str(0))
            self.playBackOffset.setEnabled(True)
            self.videoEnd.setText(str(self.videoMeta.frameCount))
            self.playBackStart.setText(str(0))
            self.playBackEnd.setText(str(self.videoMeta.frameCount))
            self.frameCounter.setText(str(0))
            self.frameCounter.setEnabled(True)
            self.savePresetAction.setEnabled(True)
            self.loadPresetAction.setEnabled(True)

    def getFrames(self, filePath):
        try:
            capture = cv2.VideoCapture(filePath)
            success, image = capture.read()
        except Exception as e:
            logger.exception(
                "Failed to read file {0}".format(filePath), exc_info=1)
            raise e

        # Try fast count
        frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        if not frames:
            logger.warning(
                "Failed to get frame count from meta data, counting frames...")
            frames = 0
            success = True
            while success:
                success, image = capture.read()
                frames += 1

        return frames

    def positionToFrame(self, position):
        if position:
            progress = (position / 1000) / self.videoMeta.duration
            frame = progress * self.videoMeta.frameCount
            return frame

    def frameToPosition(self, frame):
        progress = frame / self.videoMeta.frameCount
        position = progress * self.videoMeta.duration * 1000
        return int(position)

    def stepFrameForward(self):
        nextFrame = self.timeSlider.value() + 1
        self.toFrame(nextFrame)

    def stepFrameBackward(self):
        prevFrame = self.timeSlider.value() - 1
        self.toFrame(prevFrame)

    def toFrame(self, frame):
        self.setPosition(frame)
        self.timeSlider.setValue(frame)

    def setRange(self):
        playbackStart = int(self.playBackStart.text())
        playbackEnd = int(self.playBackEnd.text())
        if playbackStart > playbackEnd:
            playbackStart = playbackEnd
            self.playBackStart.setText(str(playbackEnd))
        if playbackEnd < playbackStart:
            playbackEnd = playbackStart
            self.playBackEnd.setText(str(playbackStart))
        self.timeSlider.setRange(playbackStart, playbackEnd)
        self.setPosition(self.timeSlider.value())

    def toStart(self):
        self.toFrame(self.timeSlider.minimum())

    def toEnd(self):
        self.toFrame(self.timeSlider.maximum())

    def setVolume(self, value):
        self.mediaPlayer.setVolume(value)

    def toggleMute(self):
        if self.mediaPlayer.isMuted():
            self.mediaPlayer.setMuted(0)
            self.muteButton.setIcon(self.style().standardIcon(
                QtWidgets.QStyle.SP_MediaVolume))
        else:
            self.mediaPlayer.setMuted(1)
            self.muteButton.setIcon(self.style().standardIcon(
                QtWidgets.QStyle.SP_MediaVolumeMuted))

    def toggleOnTop(self, state, update=True):
        if state:
            self.setWindowFlags(self.windowFlags() |
                                QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~
                                QtCore.Qt.WindowStaysOnTopHint)

        if update:
            self.settings.current["alwaysOnTop"] = state
            self.settings.save()
            self.show()

    def toggleAutoConnect(self, state):
        self.settings.current["connectOnStart"] = state
        self.settings.save()

    def goToFrame(self):
        self.toFrame(int(self.frameCounter.text()))

    def setCurrentFrameAsStart(self):
        currentFrame = self.timeSlider.value()
        self.playBackStart.setText(str(currentFrame))
        self.setRange()

    def setCurrentFrameAsEnd(self):
        currentFrame = self.timeSlider.value()
        self.playBackEnd.setText(str(currentFrame))
        self.setRange()

    def negatePlayBackStart(self):
        negatedStart = int(self.playBackStart.text()) * -1
        self.playBackOffset.setText(str(negatedStart))

    def setMayaPlaybackOptions(self):
        unitLookUp = {15: "game",
                      24: "film",
                      25: "pal",
                      30: "ntsc",
                      48: "show",
                      50: "palf",
                      60: "ntscf"}

        if self.mayaClient.connect() and self.videoMeta:
            # Set framerate
            if self.videoMeta.frameRate in unitLookUp.keys():
                unitName = unitLookUp[self.videoMeta.frameRate]
                cmd = "maya.cmds.currentUnit(time='{0}')".format(unitName)
                self.mayaClient.send(cmd)

            # Set animation end
            cmd = "maya.cmds.playbackOptions(aet={0}, e=1)".format(
                self.videoMeta.frameCount)
            self.mayaClient.send(cmd)
            # Set playback start
            cmd = "maya.cmds.playbackOptions(min={0}, e=1)".format(
                float(self.playBackStart.text()) + float(self.playBackOffset.text()))
            self.mayaClient.send(cmd)
            # Set playback end
            cmd = "maya.cmds.playbackOptions(max={0}, e=1)".format(
                float(self.playBackEnd.text()) - float(self.playBackStart.text()))
            self.mayaClient.send(cmd)
        else:
            self.timeSlider.valueChanged.disconnect()

    def changeMayaPort(self):
        currentPort = str(self.settings.current["port"])
        text, result = QtWidgets.QInputDialog.getText(
            self, "Maya port", "Set port: ", QtWidgets.QLineEdit.Normal, currentPort)
        if result:
            try:
                self.settings.current["port"] = int(text)
                self.settings.save()
                self.statusBar.showMessage(
                    f"Port set to {self.settings.current['port']}", 4000)

            except Exception as e:
                logger.error(f"Failed to connect to set port {text}")

    def updateConnectionStatus(self):
        # UTILS
        if self.connected:
            self.syncCheckBox.setEnabled(True)
            self.statusBar.showMessage("*Connected to Maya", 5000)
        else:
            self.syncCheckBox.setEnabled(False)
            self.syncCheckBox.setChecked(False)
            self.statusBar.showMessage("*Not Connected", 5000)

    def hideEmptyStatusBar(self, msg):
        if not msg and not self.statusBarAction.isChecked():
            self.statusBar.setVisible(False)
        else:
            self.statusBar.setVisible(True)

    def showAbout(self):
        aboutDialog = QtWidgets.QMessageBox(self)
        aboutDialog.setWindowTitle("About")
        aboutDialog.setText(
            "Author: Dmitrii Shevchenko\nVersion: {0}".format(self.version))
        aboutDialog.exec_()

    def showCommandPortHelp(self):
        helpDialog = QtWidgets.QMessageBox(self)
        helpDialog.setWindowTitle("How to connect to Maya")
        helpDialog.setText(
            "Using Maya's script editor run the following command:")
        helpDialog.setInformativeText(
            "maya.cmds.commandPort(name='127.0.0.1:7221', stp='python', echoOutput=True)")
        helpDialog.setDetailedText(
            "You can change last four digits after : if you want different port opened.")
        helpDialog.exec_()

    def savePreset(self):
        preset = {}
        preset["playbackStart"] = self.playBackStart.text()
        preset["playbackEnd"] = self.playBackEnd.text()
        preset["offset"] = self.playBackOffset.text()

        fileName, extension = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Preset", QtCore.QDir.homePath(), "JSON (*.json)")
        with open(fileName, "w") as jsonFile:
            json.dump(preset, jsonFile, indent=4)
        self.statusBar.showMessage(
            "Saved preset as {0}".format(fileName), 5000)

    def loadPreset(self):
        fileName, extension = QtWidgets.QFileDialog.getOpenFileName(
            self, "Load Preset", QtCore.QDir.homePath(), "JSON (*.json)")
        if fileName:
            with open(fileName, "r") as jsonFile:
                preset = json.load(jsonFile)
            self.playBackStart.setText(preset["playbackStart"])
            self.playBackEnd.setText(preset["playbackEnd"])
            self.playBackOffset.setText(preset["offset"])
            self.setRange()


class MayaClient(object):
    """[summary]

    Args:
        object ([type]): [description]
    """
    BUFFER_SIZE = 4096

    def __init__(self, port=7221):
        self.port = port
        self.mayaSocket = None

    def connect(self, port=-1):
        if port >= 0:
            self.port = port

        try:
            self.mayaSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.mayaSocket.connect(("localhost", self.port))
        except Exception as e:
            logger.exception("Failed to create socket", exc_info=1)
            return False

        return True

    def disconnect(self):
        try:
            self.mayaSocket.close()
        except Exception as e:
            logger.exception("Failed to disconnect socket", exc_info=1)
            return False

        return True

    def send(self, cmd):
        try:
            self.mayaSocket.sendall(cmd.encode())
        except Exception as e:
            logger.exception(
                "Failed to send command: {0}".format(cmd), exc_info=1)
            return None
        return self.recv()

    def recv(self):
        try:
            data = self.mayaSocket.recv(MayaClient.BUFFER_SIZE)
        except Exception as e:
            logger.exception("Failed to recieve data", exc_info=1)
            return None

        return data.decode().replace("\x00", "")

    # ----------------------------------------------------------------------------
    # COMMANDS
    # ----------------------------------------------------------------------------

    # Add command methods here
    def echo(self, text):
        cmd = "eval(\"'{0}'\")".format(text)

        return self.send(cmd)

    def setCurrentTime(self, frame):
        cmd = "cmds.currentTime({})".format(frame)

        return self.send(cmd)


if __name__ == '__main__':
    app = QtWidgets.QApplication(os.sys.argv)
    app.setStyle(QtWidgets.QStyleFactory.create("fusion"))

    darkPalette = QtGui.QPalette()
    darkPalette.setColor(QtGui.QPalette.Window, QtGui.QColor(45, 45, 45))
    darkPalette.setColor(QtGui.QPalette.WindowText,
                         QtGui.QColor(208, 208, 208))
    darkPalette.setColor(QtGui.QPalette.Base, QtGui.QColor(25, 25, 25))
    darkPalette.setColor(QtGui.QPalette.AlternateBase,
                         QtGui.QColor(208, 208, 208))
    darkPalette.setColor(QtGui.QPalette.ToolTipBase,
                         QtGui.QColor(208, 208, 208))
    darkPalette.setColor(QtGui.QPalette.ToolTipBase,
                         QtGui.QColor(208, 208, 208))
    darkPalette.setColor(QtGui.QPalette.Text, QtGui.QColor(208, 208, 208))
    darkPalette.setColor(QtGui.QPalette.Button, QtGui.QColor(45, 45, 48))
    darkPalette.setColor(QtGui.QPalette.ButtonText,
                         QtGui.QColor(208, 208, 208))
    darkPalette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    darkPalette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    darkPalette.setColor(QtGui.QPalette.Highlight, QtCore.Qt.gray)
    app.setPalette(darkPalette)

    window = Window()
    window.resize(600, 400)
    window.show()

    app.exec_()
