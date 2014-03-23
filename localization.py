#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gettext
import sys
import os
import json

def set():
    CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')
    if sys.platform.startswith("win"):
        CONFIG_PATH = CONFIG_PATH.decode(sys.getfilesystemencoding())
    try:
        gw_config_loaded=json.load(file(os.path.join(CONFIG_PATH, 'gw_config.json')))
        lang = gw_config_loaded['app_lang']
    except:
        lang = 'auto'
    LANG_PATH = os.path.join(os.path.dirname(sys.argv[0]), 'i18n')
    if lang == 'auto':
        l = gettext.translation('gis-weather', localedir=LANG_PATH, fallback=True)
        l.install(unicode=True)
    else:
        l = gettext.translation('gis-weather', localedir=LANG_PATH, languages=[lang], fallback=True)
        l.install(unicode=True)