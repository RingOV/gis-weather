#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gtk
from urllib2 import urlopen
import re
import pango
import os
import subprocess, shlex
import urllib
import sys

updating_step1 = None

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


def dlProgress(count, blockSize, totalSize):
    global updating_step1
    percent = int(count*blockSize*100/totalSize)
    total = str(round(totalSize/1024/1024.0*10)/10.0)
    updating_step1.set_text("1. Скачиваю (%s Мб)... %d%%" %(total, percent))
    # перерисовка окна
    while gtk.events_pending():
        gtk.main_iteration_do(True)


def restart(widget):
        if os.path.exists('/usr/bin/gis-weather'):
            os.execl('/usr/bin/gis-weather', '')
            gtk.main_quit()


def show(v, new_ver, CONFIG_PATH, APP_PATH):
    dialog = gtk.Dialog('Gis Weather: Обновление')
    dialog.set_border_width(10)
    dialog.resize(500, 200)
    dialog.add_buttons('Обновить', gtk.RESPONSE_OK, gtk.STOCK_CLOSE, gtk.RESPONSE_CANCEL)

    label_cur = gtk.Label('Установленная версия:')
    label_cur.set_alignment(xalign=1.0, yalign=1.0)
    label_cur_ver = gtk.Label(v)
    label_cur_ver.set_alignment(xalign=0.0, yalign=1.0)
    label_new = gtk.Label('Доступна версия:')
    label_new.set_alignment(xalign=1.0, yalign=0.0)
    label_new_ver = gtk.Label()
    label_new_ver.set_markup('<b><span gravity="east">%s</span></b>'%new_ver+' <a href="http://sourceforge.net/projects/gis-weather/files/gis-weather/%s/">На сайт</a>'%new_ver)
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
    global updating_step1
    updating_step1 = gtk.Label('1. Скачиваю... 0%')
    updating_step1.set_alignment(xalign=0.0, yalign=0.0)
    updating_step2 = gtk.Label('2. Установка')
    updating_step2.set_alignment(xalign=0.0, yalign=0.0)
    updating_step3 = gtk.Label('3. Очистка временных файлов')
    updating_step3.set_alignment(xalign=0.0, yalign=0.0)
    updating_space = gtk.Label('')
    updating_status = gtk.Label('')
    bar = gtk.InfoBar()
    bar.set_message_type(gtk.MESSAGE_ERROR)
    bar.get_content_area().pack_start(updating_status)

    button_restart = gtk.Button('Перезапустить')
    button_restart.connect("clicked", restart)

    pix_loading = gtk.gdk.PixbufAnimation(os.path.join(APP_PATH, 'themes', 'loading.gif'))

    pic_step1 = gtk.Image()
    pic_step2 = gtk.Image()
    pic_step3 = gtk.Image()

    table_updating = gtk.Table(2, 7)
    table_updating.attach(label_space, 1, 2, 0, 1, xoptions=gtk.FILL, yoptions=gtk.FILL,ypadding=-7)
    table_updating.attach(updating_step1, 1, 2, 1, 2, xoptions=gtk.FILL, yoptions=gtk.FILL)
    table_updating.attach(updating_step2, 1, 2, 2, 3, xoptions=gtk.FILL, yoptions=gtk.FILL)
    table_updating.attach(updating_step3, 1, 2, 3, 4, xoptions=gtk.FILL, yoptions=gtk.FILL)
    table_updating.attach(updating_space, 1, 2, 4, 5, ypadding=10)
    table_updating.attach(pic_step1, 0, 1, 1, 2, xoptions=gtk.SHRINK, yoptions=gtk.FILL, xpadding=10)
    table_updating.attach(pic_step2, 0, 1, 2, 3, xoptions=gtk.SHRINK, yoptions=gtk.FILL, xpadding=10)
    table_updating.attach(pic_step3, 0, 1, 3, 4, xoptions=gtk.SHRINK, yoptions=gtk.FILL, xpadding=10)
    table_updating.attach(bar, 0, 2, 5, 6, yoptions=gtk.FILL)
    table_updating.attach(button_restart, 0, 2, 6, 7, xoptions=gtk.SHRINK, yoptions=gtk.FILL, ypadding=10)

    notebook = gtk.Notebook()
    notebook.set_show_tabs(False)
    notebook.append_page(changes_view)
    notebook.append_page(table_updating)


    dialog.vbox.add(table)
    table.attach(pic, 0, 1, 0, 2)
    table.attach(label_cur, 0, 1, 0, 1)
    table.attach(label_cur_ver, 1, 2, 0, 1)
    table.attach(label_new, 0, 1, 1, 2)
    table.attach(label_new_ver, 1, 2, 1, 2)
    table.attach(notebook, 0, 2, 2, 3)
    table.attach(label_links, 0, 2, 4, 5)
    dialog.show_all()
    button_restart.hide()
    bar.hide()
    dialog.resize(400, 200)
    get_changes()
    response = dialog.run()

    while response == gtk.RESPONSE_OK:
        notebook.next_page()
        #updating_step1 = gtk.Label('1. Скачиваю... 0%')
        pic_step1.set_from_animation(pix_loading)
        pic_step2.clear()
        pic_step3.clear()
        button_restart.hide()
        bar.hide()
        updating_status.set_text('Произошла ошибка при обновлении')
        bar.set_message_type(gtk.MESSAGE_ERROR)
        # перерисовка окна
        while gtk.events_pending():
            gtk.main_iteration_do(True)
        url = 'http://sourceforge.net/projects/gis-weather/files/gis-weather/%s/gis-weather_%s_all.deb/download'%(new_ver, new_ver)
        _file = os.path.join(CONFIG_PATH, 'gis-weather_%s_all.deb'%new_ver)
        try:
            urllib.urlretrieve(url, _file, reporthook=dlProgress)
            pic_step1.set_from_stock(gtk.STOCK_OK, 4)
        except:
            print '[!] Ошибка скачивания обновления'
            pic_step1.set_from_stock(gtk.STOCK_DIALOG_ERROR, 4)
            bar.show()
        else:
            pic_step2.set_from_animation(pix_loading)
            # перерисовка окна
            while gtk.events_pending():
                gtk.main_iteration_do(True)
            p = subprocess.Popen(["gksu", "dpkg -i %s" %_file], stdout=subprocess.PIPE)
            out, err = p.communicate()
            if (out == '' or out == 'None') and err != 'None':
                print '[!] Ошибка установки обновления'
                pic_step2.set_from_stock(gtk.STOCK_DIALOG_ERROR, 4)
                bar.show()
            else:
                print '> Установка:'
                print out
                pic_step2.set_from_stock(gtk.STOCK_OK, 4)
                pic_step3.set_from_animation(pix_loading)
                try:
                    os.remove(_file)
                    pic_step3.set_from_stock(gtk.STOCK_OK, 4)
                except:
                    print '[!] Ошибка удаления'
                    pic_step3.set_from_stock(gtk.STOCK_DIALOG_ERROR, 4)
                    bar.show()
                else:
                    updating_status.set_text('Обновление успешно завершено')
                    bar.set_message_type(gtk.MESSAGE_INFO)
                    bar.show()
                    button_restart.show()
        response = dialog.run()

    dialog.hide()
