#!/usr/bin/env python3

import os
import json
from utils import instance

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')
CONFIG_PATH_FILE = os.path.join(CONFIG_PATH, instance.get_config_file())

def get(name):
    if os.path.exists(CONFIG_PATH_FILE):
        gw_config_loaded=json.load(open(CONFIG_PATH_FILE))
        return gw_config_loaded[name]