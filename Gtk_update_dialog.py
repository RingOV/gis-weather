#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gtk
from urllib2 import urlopen
import re
import pango
import os
import subprocess

def get_changes():
    try:
        source = urlopen('http://sourceforge.net/p/gis-weather/changelog/').read()
    except:
        print '[!] Невозможно получить изменения'
        return ''
    changes = re.findall('markdown_content.>(.*?)\.\.\. <a', source, re.DOTALL)
    changes = re.sub('<ul>', '', changes[0])
    changes = re.sub('</li>', '', changes)
    changes = re.sub('<li>', '  - ', changes)
    changes = re.sub('</h1>', '', changes)
    changes = re.sub('<h1.*>', '', changes)
    lines = changes.split('\n')
    changes = ['', '']
    changes[0] = lines[0]+'\n'
    changes[1] = '\n'.join(lines[2:])
    return changes


def show(v, new_ver, path):
    dialog = gtk.Dialog('Доступна новая версия')
    dialog.set_border_width(10)
    dialog.resize(400, 200)
    dialog.add_buttons('Скачать и установить', gtk.RESPONSE_OK, gtk.STOCK_CLOSE, gtk.RESPONSE_CANCEL)
    gtk.Label()
    label_cur = gtk.Label('Текущая версия:')
    label_cur.set_alignment(xalign=1.0, yalign=1.0)
    label_cur_ver = gtk.Label(v)
    label_cur_ver.set_alignment(xalign=0.0, yalign=1.0)
    label_new = gtk.Label('Новая версия:')
    label_new.set_alignment(xalign=1.0, yalign=0.0)
    label_new_ver = gtk.Label()
    label_new_ver.set_markup('<b><span gravity="east">%s</span></b>'%new_ver+' <a href="http://sourceforge.net/projects/gis-weather/files/latest/download">Скачать</a>')
    label_new_ver.set_alignment(xalign=0.0, yalign=0.0)

    label_links = gtk.Label()
    label_links.set_markup('<a href="https://github.com/RingOV/gis-weather">Исходный код</a> | \
<a href="http://sourceforge.net/p/gis-weather/changelog/2014/01/changelog/">История версий</a>')

    changes = get_changes()
    changes_text = gtk.TextBuffer()
    changes_text.create_tag("heading", weight=pango.WEIGHT_BOLD, size=15000)
    iter = changes_text.get_iter_at_offset(0)
    changes_text.insert_with_tags_by_name(iter, changes[0], "heading")
    changes_text.insert(iter, changes[1])
    
    changes_view = gtk.TextView(changes_text)
    changes_view.set_wrap_mode(gtk.WRAP_WORD)
    changes_view.set_editable(False)

    table = gtk.Table(2, 5)
    table.set_row_spacings(4)
    table.set_col_spacings(4)

    dialog.vbox.add(table)
    table.attach(label_cur, 0, 1, 0, 1)
    table.attach(label_cur_ver, 1, 2, 0, 1)
    table.attach(label_new, 0, 1, 1, 2)
    table.attach(label_new_ver, 1, 2, 1, 2)
    table.attach(changes_view, 0, 2, 2, 3)
    table.attach(label_links, 0, 2, 4, 5)

    dialog.show_all()
    get_changes()
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        path = os.path.join(path, 'gis-weather_%s_all.deb'%new_ver)
        os.popen('x-terminal-emulator -e "wget -c http://sourceforge.net/projects/gis-weather/files/gis-weather_%s_all.deb/download -O %s"'%(new_ver, path))
        os.popen('x-terminal-emulator -e "sudo dpkg -i %s"'%path)
        os.popen('x-terminal-emulator -e "rm %s"'%path)
        os.execl('/usr/bin/gis-weather', '')
        gtk.main_quit()
    dialog.hide()
