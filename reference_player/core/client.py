import socket
from reference_player import Logger


class MayaClient(object):
    """Client for communication with Maya via socket
    """
    BUFFER_SIZE = 4096

    def __init__(self, port: int = 7221):
        self.port = port
        self.maya_socket = None

    def connect(self, port: int = -1) -> bool:
        if port >= 0:
            self.port = port

        try:
            self.maya_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.maya_socket.connect(("localhost", self.port))
        except Exception:
            Logger.exception("Failed to create socket")
            return False
        return True

    def disconnect(self) -> bool:
        try:
            self.maya_socket.close()
        except Exception:
            Logger.exception("Failed to disconnect socket")
            return False
        return True

    def send(self, cmd) -> str:
        try:
            self.maya_socket.sendall(cmd.encode())
        except Exception:
            Logger.exception("Failed to send command: {0}".format(cmd))
            return None
        return self.recv()

    def recv(self) -> str:
        try:
            data = self.maya_socket.recv(MayaClient.BUFFER_SIZE)
        except Exception:
            Logger.exception("Failed to recieve data")
            return None
        return data.decode().replace("\x00", "")

    # ----------------------------------------------------------------------------
    # COMMANDS
    # ----------------------------------------------------------------------------
    # Add command methods here
    def echo(self, text: str):
        cmd = "eval(\"'{0}'\")".format(text)
        return self.send(cmd)

    def setCurrentTime(self, frame: int):
        cmd = "cmds.currentTime({})".format(frame)
        return self.send(cmd)
