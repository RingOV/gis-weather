#!/usr/bin/env python3

from gi.repository import Gtk
import os
from utils import localization, instance
from services import data
from dialogs.settings_dialog import services_list
import json

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')
CONFIG_PATH_FILE = os.path.join(CONFIG_PATH, instance.get_config_file())

url = None
example = None
code = None
dict_weather_lang = None
weather_lang_list = None
gw_config = None

def Save_Config():
    json.dump(gw_config, open(CONFIG_PATH_FILE, "w"), sort_keys=True, indent=4, separators=(', ', ': '))

def Load_Config():
    global gw_config
    try:
        gw_config = json.load(open(CONFIG_PATH_FILE))
    except:
        print ('[!] '+_('Error loading config file'))

def set_service(widget, label, liststore2, combobox_weather_lang, weather_lang, store):
    global gw_config
    Load_Config()
    i = widget.get_active()
    load_data(i, label, liststore2, combobox_weather_lang, weather_lang, store)
    gw_config['service'] = i
    gw_config['weather_lang'] = weather_lang_list[combobox_weather_lang.get_active()]
    try:
        gw_config['city_id'] = gw_config[data.get_city_list(i)][0].split(';')[0]
    except:
        pass
    gw_config['max_days'] = data.get_max_days(i)
    if gw_config['n'] > gw_config['max_days']:
        gw_config['n'] = gw_config['max_days']
    Save_Config()

def set_weather_lang(widget):
    global gw_config
    i = widget.get_active()
    gw_config['weather_lang'] = weather_lang_list[i]
    Save_Config()

def load_data(service, label, liststore2, combobox_weather_lang, weather_lang, store):
    global url, example, code, dict_weather_lang, weather_lang_list, gw_config
    url, example, code, dict_weather_lang, weather_lang_list = data.get(service)
    text = _("Choose your city on")+" <a href='%s'>%s</a>\n" %(url, url)+\
        _("and copy the city code below")+"\n"+\
        _("For example")+ ":\n<u><span foreground='blue'>%s/</span></u>\n" %example+\
        _("City code")+" %s" %code
    label.set_markup(text)
    liststore2.clear()
    for i in range(len(weather_lang_list)):
        try:
            liststore2.append([dict_weather_lang[weather_lang_list[i]]])
        except:
            if weather_lang_list[i] != '':
                liststore2.append([weather_lang_list[i]])
        if weather_lang_list[i] == weather_lang:
            combobox_weather_lang.set_active(i)
        if combobox_weather_lang.get_active() == -1:
            combobox_weather_lang.set_active(0)
    Load_Config()
    try:
        city_list = gw_config[data.get_city_list(service)]
    except:
        city_list = []
    store.clear()
    for item in city_list:
        store.append([item.split(';')[0], item.split(';')[1]])

def create(window, APP_PATH, weather_lang, service):
    Load_Config()
    ui = Gtk.Builder()
    ui.add_from_file(os.path.join(APP_PATH, "dialogs","city_id_dialog.ui"))
    dialog = ui.get_object('dialog1')

    dialog.set_icon_from_file(os.path.join(APP_PATH, "icon.png"))
    list_o = ui.get_objects()
    dict_o = {}
    dict_o = localization.translate_ui(list_o, dict_o)
    dialog.set_title(_('Location'))
    dialog.set_default_size(100, 400)

    liststore2 = ui.get_object('liststore2')
    combobox_weather_lang = ui.get_object('combobox_weather_lang')
    combobox_weather_lang.connect("changed", set_weather_lang)
    combobox_service = ui.get_object('combobox_service')
    liststore3 = ui.get_object('liststore3')
    label = ui.get_object('label1')
    for i in range(len(services_list)):
        liststore3.append([services_list[i]])
    combobox_service.set_active(service)
    store = ui.get_object('liststore1')

    load_data(service, label, liststore2, combobox_weather_lang, weather_lang, store)

    combobox_service.connect("changed", set_service, label, liststore2, combobox_weather_lang, weather_lang, store)
    
    entrybox = ui.get_object('entrybox')
    bar_ok = ui.get_object('bar_ok')
    bar_err = ui.get_object('bar_err')
    bar_label = ui.get_object('bar_label')

    treeView = ui.get_object('treeView')
    create_columns(treeView)

    return dialog, entrybox, treeView, bar_err, bar_ok, bar_label, combobox_weather_lang, weather_lang_list, combobox_service

def create_columns(treeView):
    rendererText = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(_('Code'), rendererText, text=0)
    treeView.append_column(column)
    
    rendererText = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(_('Place'), rendererText, text=1)
    treeView.append_column(column)