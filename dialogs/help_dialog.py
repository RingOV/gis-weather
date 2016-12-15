#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from utils import localization
import os

linkbutton_send = None

def set_message_subject(widget, subject):
    if widget.get_active():
        if subject == 'Localization':
            linkbutton_send.set_uri("https://github.com/RingOV/gis-weather/wiki/Want-to-translate%3F")
            linkbutton_send.set_label(_("Go to link"))
        else:
            linkbutton_send.set_uri("mailto:ringov.gisweather@gmail.com?subject="+subject)
            linkbutton_send.set_label(_("Send email"))

def create(APP_PATH):
    global linkbutton_send
    ui = Gtk.Builder()
    ui.add_from_file(os.path.join(APP_PATH, "dialogs","help_dialog.ui"))
    dialog = ui.get_object('dialog1')
    dialog.set_icon_from_file(os.path.join(APP_PATH, "icon.png"))

    list_o = ui.get_objects()
    dict_o = {}
    dict_o = localization.translate_ui(list_o, dict_o)
    dialog.set_title('Gis Weather: '+_('Help'))

    radiobutton1 = ui.get_object('radiobutton1')
    radiobutton2 = ui.get_object('radiobutton2')
    radiobutton3 = ui.get_object('radiobutton3')
    radiobutton4 = ui.get_object('radiobutton4')
    linkbutton_send = ui.get_object('linkbutton_send')

    radiobutton1.connect("toggled", set_message_subject, "Bug")
    radiobutton2.connect("toggled", set_message_subject, "Localization")
    radiobutton3.connect("toggled", set_message_subject, "Question")
    radiobutton4.connect("toggled", set_message_subject, "Suggestion")

    response = dialog.run()
    dialog.hide()