#!/usr/bin/env python3

import gettext
import sys
import os
import json
import locale
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils import instance

if sys.platform.startswith("win"):
    WIN = True
else:
    WIN = False

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')
CONFIG_PATH_FILE = os.path.join(CONFIG_PATH, instance.get_config_file())

def set():
    try:
        gw_config_loaded=json.load(open(CONFIG_PATH_FILE))
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

def translate_ui(list_o, dict_o):
    # get original text
    if dict_o == {}:
        for i in range(len(list_o)):
            try:
                if list_o[i].get_name() == 'GtkLabel':
                    dict_o[Gtk.Buildable.get_name(list_o[i])] = list_o[i].get_text()
                if list_o[i].get_name() in  ('GtkButton', 'GtkLinkButton', 'GtkRadioButton'):
                    dict_o[Gtk.Buildable.get_name(list_o[i])] = list_o[i].get_label()
            except:
                pass
    # translate
    for i in range(len(list_o)):
        try:
            if list_o[i].get_name() == 'GtkLabel':
                if list_o[i].get_text() != '':
                    list_o[i].set_text(_(dict_o[Gtk.Buildable.get_name(list_o[i])]))
            if list_o[i].get_name() in  ('GtkButton', 'GtkLinkButton', 'GtkRadioButton'):
                if list_o[i].get_label() != None:
                    list_o[i].set_label(_(dict_o[Gtk.Buildable.get_name(list_o[i])]))
        except:
            pass
    return dict_o