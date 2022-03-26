import sys
from reference_player.player_application import QReferencePlayerApplication


if __name__ == "__main__":
    app = QReferencePlayerApplication(sys.argv)
    ret_code = app.exec_()
    app.config.save()
