#!/usr/bin/env python3

import gettext
import sys
import os
import json
import locale
if sys.platform.startswith("win"):
    WIN = True
else:
    WIN = False

def set():
    CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')
    if sys.platform.startswith("win"):
        CONFIG_PATH = CONFIG_PATH.decode(sys.getfilesystemencoding())
    try:
        gw_config_loaded=json.load(open(os.path.join(CONFIG_PATH, 'gw_config.json')))
        lang = gw_config_loaded['app_lang']
    except:
        lang = 'auto'
    LANG_PATH = os.path.join(os.path.abspath(os.path.split(os.path.dirname(__file__))[0]), 'i18n')
    if lang == 'auto':
        if WIN:
            lang = gettext.translation('gis-weather', localedir=LANG_PATH, languages=[locale.getdefaultlocale()[0]], fallback=True)
            lang.install()
        else:
            l = gettext.translation('gis-weather', localedir=LANG_PATH, fallback=True)
            l.install()
    else:
        l = gettext.translation('gis-weather', localedir=LANG_PATH, languages=[lang], fallback=True)
        l.install()