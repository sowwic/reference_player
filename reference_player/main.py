import os
import sys
from reference_player import Logger
from reference_player.player_application import QReferencePlayerApplication


if __name__ == "__main__":
    os.environ["QT_MAC_WANTS_LAYER"] = "1"
    app = QReferencePlayerApplication(sys.argv)
    ret_code = app.exec_()
    if ret_code:
        Logger.error(f"Application exit with code {ret_code}")
    app.config.save()
