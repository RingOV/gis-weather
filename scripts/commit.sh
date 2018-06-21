#!/bin/bash

S_PATH=$(pwd)
cd $S_PATH
cd ..
GW_PATH=$(pwd)

# pull l10n from https://www.transifex.com/gis-weather-team/gis-weather/
cd "$GW_PATH/po/"
tx pull -a
cd $S_PATH
python3 "$S_PATH/update_mo.py"
cd $GW_PATH
git add -A && git commit && git push