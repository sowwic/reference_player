#!/bin/bash  
APP_NAME="reference_player"
MAIN_FILE_PATH=reference_player/main.py
RES_FOLDER="./res;./res"
ICON_PATH="./res/images/player_icon.ico"

# Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    SITE_PACKAGES_PATH=.env/Lib/site-packages
# Mac OSX
elif [[ "$OSTYPE" == "darwin"* ]]; then
    SITE_PACKAGES_PATH=.env/lib64/python3.9/site-packages
# Windows
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]] ||  [[ "$OSTYPE" == "cygwin" ]]; then
    SITE_PACKAGES_PATH=.venv/Lib/site-packages
else
    echo "Unsupported OS: $OSTYPE"
    exit 1
fi
echo "Building for $OSTYPE"

# Cleanup
echo "Cleaning up build files..."
rm -rf build dist reference_player.spec

echo "Running pyinstaller..."
py -3 -m PyInstaller --onedir --noconsole \
--icon $ICON_PATH \
--paths $SITE_PACKAGES_PATH \
--add-data=$RES_FOLDER \
-n $APP_NAME \
$MAIN_FILE_PATH

$SHELL 
