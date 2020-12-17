 #!/bin/bash  
APP_NAME="reference_player"
MAIN_FILE_PATH=reference_player/main.py
SITE_PACKAGES_PATH=.env/Lib/site-packages
RES_FOLDER="./res;./res"
DEFAULT_CONFIG="default_config.json;."
ICON_PATH="./res/images/player_icon.ico"

py -3 -m PyInstaller --onedir --noconsole \
--icon $ICON_PATH \
--paths $SITE_PACKAGES_PATH \
--add-data=$RES_FOLDER \
--add-data=$DEFAULT_CONFIG \
-n $APP_NAME \
$MAIN_FILE_PATH

$SHELL 
