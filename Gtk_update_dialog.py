#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gtk
from urllib2 import urlopen
import re
import pango

label_changes = gtk.Label()

def get_changes():
    global label_changes
    try:
        source = urlopen('http://sourceforge.net/p/gis-weather/changelog/').read()
    except:
        print '[!] Невозможно получить изменения'
        return False
    changes = re.findall('markdown_content.>(.*?)\.\.\. <a', source, re.DOTALL)
    changes = re.sub('<ul>', '', changes[0])
    changes = re.sub('</li>', '', changes)
    changes = re.sub('<li>', '  - ', changes)
    changes = re.sub('</h1>', '</big', changes)
    changes = re.sub('<h1.*>', '<big>', changes)
    changes = re.sub('</big', '</big>', changes)
    label_changes.set_markup(changes)
    label_changes.set_line_wrap(True)


def show(v, new_ver):
    dialog = gtk.Dialog('Доступна новая версия')
    dialog.set_border_width(10)
    dialog.add_buttons(gtk.STOCK_CLOSE, gtk.RESPONSE_CANCEL)
    gtk.Label()
    label_cur = gtk.Label('Текущая версия:')
    label_cur.set_alignment(xalign=1.0, yalign=0.0)
    label_cur_ver = gtk.Label(v)
    label_cur_ver.set_alignment(xalign=0.0, yalign=0.0)
    label_new = gtk.Label('Новая версия:')
    label_new.set_alignment(xalign=1.0, yalign=0.0)
    label_new_ver = gtk.Label()
    label_new_ver.set_markup('<b><span gravity="east">%s</span></b>'%new_ver)
    label_new_ver.set_alignment(xalign=0.0, yalign=0.0)

    label_links = gtk.Label()
    label_links.set_markup('<a href="http://sourceforge.net/projects/gis-weather/files/latest/download">Скачать</a>')
    label_links.set_alignment(xalign=0.0, yalign=0.0)

    table = gtk.Table(10, 5)
    table.set_row_spacings(4)
    table.set_col_spacings(4)

    dialog.vbox.add(table)
    table.attach(label_cur, 0, 1, 0, 1)
    table.attach(label_cur_ver, 1, 2, 0, 1, xoptions=gtk.SHRINK)
    table.attach(label_new, 0, 1, 1, 2)
    table.attach(label_new_ver, 1, 2, 1, 2, xoptions=gtk.SHRINK)
    table.attach(label_changes, 0, 2, 2, 3)
    table.attach(label_links, 0, 2, 4, 5)

    dialog.show_all()
    get_changes()
    response = dialog.run()
    dialog.hide()