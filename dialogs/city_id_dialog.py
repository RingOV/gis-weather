#!/usr/bin/env python3

from gi.repository import Gtk
import os
from utils import localization
from services import gismeteo

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')

def create(window, city_id, city_id_add, APP_PATH, weather_lang):

    ui = Gtk.Builder()
    ui.add_from_file(os.path.join(APP_PATH, "dialogs","city_id_dialog.ui"))
    dialog = ui.get_object('dialog1')

    dialog.set_icon_from_file(os.path.join(APP_PATH, "icon.png"))
    list_o = ui.get_objects()
    dict_o = {}
    dict_o = localization.translate_ui(list_o, dict_o)
    dialog.set_title(_('Location'))

    service = gismeteo.service
    example = gismeteo.example
    code = gismeteo.code
    text = _("Choose your city on")+" <a href='%s'>%s</a>\n" %(service, service)+\
        _("and copy city code from the reference")+"\n"+\
        _("For example")+ " <u><span foreground='blue'>%s/</span></u>\n" %example+\
        _("City code")+" %s" %code
    
    label = ui.get_object('label1')
    label.set_markup(text)

    entrybox = ui.get_object('entrybox')
    bar_ok = ui.get_object('bar_ok')
    bar_err = ui.get_object('bar_err')
    bar_label = ui.get_object('bar_label')

    treeView = ui.get_object('treeView')
    create_columns(treeView)

    store = ui.get_object('liststore1')
    for item in city_id_add:
        store.append([item.split(';')[0], item.split(';')[1]])

    dict_weather_lang = gismeteo.dict_weather_lang
    weather_lang_list = gismeteo.weather_lang_list
    liststore2 = ui.get_object('liststore2')
    combobox_weather_lang = ui.get_object('combobox_weather_lang')
    for i in range(len(weather_lang_list)):
        try:
            liststore2.append([dict_weather_lang[weather_lang_list[i]]])
        except:
            liststore2.append([weather_lang_list[i]])
        if weather_lang_list[i] == weather_lang:
            combobox_weather_lang.set_active(i)

    return dialog, entrybox, treeView, bar_err, bar_ok, bar_label, combobox_weather_lang, weather_lang_list

def create_columns(treeView):

    rendererText = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(_('Code'), rendererText, text=0)
    treeView.append_column(column)
    
    rendererText = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(_('Place'), rendererText, text=1)
    treeView.append_column(column)