#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gtk
from urllib2 import urlopen
import re
import pango
import os
import subprocess, shlex

def get_changes():
    try:
        source = urlopen('http://sourceforge.net/p/gis-weather/changelog/').read()
    except:
        print '[!] Невозможно получить изменения'
        changes = ['','']
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


def show(v, new_ver, CONFIG_PATH, APP_PATH):
    dialog = gtk.Dialog('Gis Weather: Новая версия')
    dialog.set_border_width(10)
    dialog.resize(500, 200)
    dialog.add_buttons('Скачать и установить', gtk.RESPONSE_OK, gtk.STOCK_CLOSE, gtk.RESPONSE_CANCEL)

    label_cur = gtk.Label('Установлена версия:')
    label_cur.set_alignment(xalign=1.0, yalign=1.0)
    label_cur_ver = gtk.Label(v)
    label_cur_ver.set_alignment(xalign=0.0, yalign=1.0)
    label_new = gtk.Label('Доступна версия:')
    label_new.set_alignment(xalign=1.0, yalign=0.0)
    label_new_ver = gtk.Label()
    label_new_ver.set_markup('<b><span gravity="east">%s</span></b>'%new_ver+' <a href="http://sourceforge.net/projects/gis-weather/files/gis-weather/%s/">Скачать</a>'%new_ver)
    label_new_ver.set_alignment(xalign=0.0, yalign=0.0)

    label_links = gtk.Label()
    label_links.set_markup('<a href="https://github.com/RingOV/gis-weather">Исходный код</a> | \
<a href="http://sourceforge.net/p/gis-weather/changelog/2014/01/changelog/">История версий</a>')
    # тестовый буфер, в него запишется форматированные текст
    changes = get_changes() # получаем текст обновления
    changes_text = gtk.TextBuffer()
    # тег для форматирования
    changes_text.create_tag("heading", weight=pango.WEIGHT_BOLD, size=15000)
    # позиция для вставки текста
    iter = changes_text.get_iter_at_offset(0)
    changes_text.insert_with_tags_by_name(iter, changes[0], "heading")
    changes_text.insert(iter, changes[1])
    # буфер готов, создаем текстовое поле
    changes_view = gtk.TextView(changes_text)
    changes_view.set_wrap_mode(gtk.WRAP_WORD)
    changes_view.set_editable(False)
    changes_view.set_left_margin(10)
    #changes_view.set_right_margin(10)
    # эмблема виждета
    pic = gtk.Image()
    pic.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size(os.path.join(APP_PATH, 'icon.png'), 64, 64))
    # выравнивание по левому краю
    pic.set_alignment(xalign=0.0, yalign=0.0)
    # контейнер таблица(столбцы, строки)
    table = gtk.Table(2, 5)
    table.set_row_spacings(4)
    table.set_col_spacings(4)

    label_space = gtk.Label('')
    upgrade_step1 = gtk.Label('1. Скачать обновление')
    upgrade_step1.set_alignment(xalign=0.0, yalign=0.0)
    upgrade_step2 = gtk.Label('2. Установить')
    upgrade_step2.set_alignment(xalign=0.0, yalign=0.0)
    upgrade_step3 = gtk.Label('3. Очистить временные файлы')
    upgrade_step3.set_alignment(xalign=0.0, yalign=0.0)
    upgrade_status = gtk.Label('Скачиваю ываыфваыфваыф')
    table_upgrade = gtk.Table(2, 5)
    table_upgrade.attach(label_space, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10, ypadding=-5)
    table_upgrade.attach(upgrade_step1, 1, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10)
    table_upgrade.attach(upgrade_step2, 1, 2, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10)
    table_upgrade.attach(upgrade_step3, 1, 2, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL, xpadding=10)
    table_upgrade.attach(upgrade_status, 1, 2, 4, 5)

    notebook = gtk.Notebook()
    notebook.set_show_tabs(False)
    notebook.append_page(changes_view)
    notebook.append_page(table_upgrade)


    dialog.vbox.add(table)
    table.attach(pic, 0, 1, 0, 2)
    table.attach(label_cur, 0, 1, 0, 1)
    table.attach(label_cur_ver, 1, 2, 0, 1)
    table.attach(label_new, 0, 1, 1, 2)
    table.attach(label_new_ver, 1, 2, 1, 2)
    table.attach(notebook, 0, 2, 2, 3)
    table.attach(label_links, 0, 2, 4, 5)
    dialog.show_all()
    dialog.resize(400, 200)
    get_changes()
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        notebook.next_page()
        # url = 'http://sourceforge.net/projects/gis-weather/files/gis-weather/%s/gis-weather_%s_all.deb/download'%(new_ver, new_ver)
        # file_ = os.path.join(CONFIG_PATH, 'gis-weather_%s_all.deb'%new_ver)
        # command_line = 'x-terminal-emulator -e %s/updater.sh %s %s'%(os.path.dirname(__file__), url, file_)
        # # переводим в список аргументов, чтобы Popen нормально это "съел"
        # args = shlex.split(command_line)
        # subprocess.call(args)
        # print 'УЖЕ'
        # if os.path.exists('/usr/bin/gis-weather'):
        #     os.execl('/usr/bin/gis-weather', '')
        #     gtk.main_quit()
    #dialog.hide()
