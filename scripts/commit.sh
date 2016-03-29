#!/bin/bash

S_PATH=$(pwd)
cd $S_PATH
cd ..
GW_PATH=$(pwd)

# pull l10n from https://www.transifex.com/gis-weather-team/gis-weather/
tx -r "$GW_PATH/po/" pull -a
python3 "$S_PATH/update_mo.py"
git add -A && git commit && git push