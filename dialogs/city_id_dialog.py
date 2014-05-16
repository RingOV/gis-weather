#!/usr/bin/env python3

from gi.repository import Gtk
import os

def create(window, city_id, city_id_add, APP_PATH):
    dialog = Gtk.Dialog(_('Location'), window)
    dialog.resize(300, 100)
    dialog.add_buttons(_('Add'), Gtk.ResponseType.OK,
        _('Close'), Gtk.ResponseType.CANCEL,
        _('Remove selected'), Gtk.ResponseType.ACCEPT)
    dialog.set_icon_from_file(os.path.join(APP_PATH, "icon.png"))

    hbox = Gtk.HBox(False, 8)
    hbox.set_border_width(8)
    dialog.vbox.pack_start(hbox, False, False, 0)
    table = Gtk.Table(2, 3)
    table.set_row_spacings(4)
    table.set_col_spacings(4)
    hbox.pack_start(table, True, True, 0)

    entrybox = Gtk.Entry()
    entrybox.set_text(str(city_id))
    text = _("""Choose your city on <a href='http://www.gismeteo.com'> http://www.gismeteo.com </a>
and copy number at the end of reference
For example <u><span foreground='blue'>http://www.gismeteo.com/city/daily/<b>1234</b>/</span></u>
City code<b>1234</b>""")
    
    label = Gtk.Label()
    label.set_markup(text)

    bar_err = Gtk.InfoBar()
    bar_err.set_message_type(Gtk.MessageType.ERROR)
    bar_err.get_content_area().pack_start(
        Gtk.Label(_('Invalid location code')), True, True, 0)
    table.attach(bar_err, 0, 1, 2, 3)

    bar_ok = Gtk.InfoBar()
    bar_ok.set_message_type(Gtk.MessageType.INFO)
    bar_label = Gtk.Label(label=_('Added'))
    bar_ok.get_content_area().pack_start(
        bar_label, True, True, 0)
    table.attach(bar_ok, 0, 1, 2, 3)

    label_err = Gtk.Label(label='\n')
    table.attach(label, 0, 1, 0, 1)
    table.attach(entrybox, 0, 1, 1, 2)
    table.attach(label_err, 0, 1, 2, 3)

    sw = Gtk.ScrolledWindow()
    sw.set_shadow_type(Gtk.ShadowType.ETCHED_IN)
    sw.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

    store = create_model(city_id_add)
    treeView = Gtk.TreeView(store)
    sw.add(treeView)
    create_columns(treeView)
    table.attach(sw, 1, 2, 0, 3)
    return dialog, entrybox, treeView, bar_err, bar_ok, bar_label

def create_model(city_id_add):
    store = Gtk.ListStore(str, str)

    for item in city_id_add:
        store.append([item.split(';')[0], item.split(';')[1]])
    return store


def create_columns(treeView):

    rendererText = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(_('Code'), rendererText, text=0)
    treeView.append_column(column)
    
    rendererText = Gtk.CellRendererText()
    column = Gtk.TreeViewColumn(_('Place'), rendererText, text=1)
    treeView.append_column(column)