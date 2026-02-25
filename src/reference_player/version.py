# Determine base directory
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    # PyInstaller bundle
    BASE_DIR = Path(sys._MEIPASS)
else:
    # Running from source
    # adjust to project root
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Read version from VERSION file
VERSION_FILE = BASE_DIR / "VERSION"
try:
    with VERSION_FILE.open() as f:
        __version__ = f.read().strip()
except FileNotFoundError:
    __version__ = "0.0.0"
