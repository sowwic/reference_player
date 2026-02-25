import sys
import reference_player.resources.resources_rc  # noqa: F401
from reference_player.application import ReferencePlayerApplication


def main():
    app = ReferencePlayerApplication(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
