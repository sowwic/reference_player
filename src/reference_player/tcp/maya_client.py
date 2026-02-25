import logging
import socket

LOGGER = logging.getLogger(__name__)


class MayaClient:
    """Maya TCP client."""

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
        except Exception:
            LOGGER.exception("Failed to create socket", exc_info=1)
            return False

        return True

    def disconnect(self):
        try:
            self.mayaSocket.close()
        except Exception:
            LOGGER.exception("Failed to disconnect socket", exc_info=1)
            return False

        return True

    def send(self, cmd):
        try:
            self.mayaSocket.sendall(cmd.encode())
        except Exception:
            LOGGER.exception(f"Failed to send command: {cmd}", exc_info=1)
            return None
        return self.recv()

    def recv(self):
        try:
            data = self.mayaSocket.recv(MayaClient.BUFFER_SIZE)
        except Exception:
            LOGGER.exception("Failed to receive data", exc_info=1)
            return None

        return data.decode().replace("\x00", "")

    # ----------------------------------------------------------------------------
    # COMMANDS
    # ----------------------------------------------------------------------------

    # Add command methods here
    def echo(self, text):
        cmd = f"eval(\"'{text}'\")"

        return self.send(cmd)

    def setCurrentTime(self, frame):
        cmd = f"cmds.currentTime({frame})"

        return self.send(cmd)
