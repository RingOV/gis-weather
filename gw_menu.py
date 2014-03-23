#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gtk
import os


def create_menu(app, ICONS_PATH, BGS_PATH, ICONS_USER_PATH, BGS_USER_PATH, icons_name, show_bg_png, 
    color_bg, bg_custom, color_scheme, color_scheme_number, city_id_add, city_id, fix_position, sticky):
    menu = None
    # из папки скрипта (dirs - иконки, files - фоны)
    root, dirs, files = os.walk(ICONS_PATH).next()
    files = os.listdir(BGS_PATH)
    dirs.sort()
    files.sort()
    dirs.remove('default')
    # из папки пользователя (dirs_user - иконки, files_user - фоны)
    root, dirs_user, files_user = os.walk(ICONS_USER_PATH).next()
    files_user = os.listdir(BGS_USER_PATH)
    dirs_user.sort()
    files_user.sort()
    dirs_user.remove('default')
    # списки с иконками и фонами
    icons_list = []
    icons_list.extend(dirs)
    icons_list.extend(dirs_user)
    backgrounds_list = []
    backgrounds_list.extend(files)
    backgrounds_list.extend(files_user)
    # Создаем меню и заполняем найденными иконками и фонами
    menu = gtk.Menu()
    sub_menu_icons = gtk.Menu()
    sub_menu_bgs = gtk.Menu()
    sub_menu_color_text = gtk.Menu()
    sub_menu_place = gtk.Menu()
    sub_menu_settings = gtk.Menu()
    sub_menu_window = gtk.Menu()

    # Иконки
    group = None
    menu_items = gtk.RadioMenuItem(group, '0. Default')
    if icons_name == 'default':
        menu_items.set_active(True)
    group = menu_items
    sub_menu_icons.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'redraw_icons', 'default')
    menu_items.show()
    for i in range(len(icons_list)):
        buf = icons_list[i].split('_') # из _ делаем __ (отображается как _)
        buf = '__'.join(buf)
        menu_items = gtk.RadioMenuItem(group, str(i+1)+'. '+buf)
        if icons_name == icons_list[i]:
            menu_items.set_active(True)
        group = menu_items
        sub_menu_icons.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'redraw_icons', icons_list[i])
        menu_items.show()

    # Фоны
    group = None
    menu_items = gtk.RadioMenuItem(group, '0. '+_('No'))
    if show_bg_png == False and color_bg[3]==0:
        menu_items.set_active(True)
    group = menu_items
    sub_menu_bgs.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'redraw_bg', 'Нет')
    menu_items.show()
    for i in range(len(backgrounds_list)):
        buf = backgrounds_list[i].split('_')
        buf = '__'.join(buf)
        menu_items = gtk.RadioMenuItem(group, str(i+1)+'. '+buf)
        if bg_custom == backgrounds_list[i]:
            menu_items.set_active(True)
        group = menu_items
        sub_menu_bgs.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'redraw_bg', backgrounds_list[i])
        menu_items.show()

    # Цвет текста
    group = None
    for i in range(len(color_scheme)):
        menu_items = gtk.RadioMenuItem(group, _('Color scheme')+' #' + str(i))
        if i == color_scheme_number:
            menu_items.set_active(True)
        group = menu_items
        sub_menu_color_text.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'redraw_text', i)
        menu_items.show()

    # sub_menu_place
    group = None
    if len(city_id_add) > 0:
        for i in range(len(city_id_add)):
            menu_items = gtk.RadioMenuItem(group, city_id_add[i].split(';')[1])
            if city_id_add[i].split(';')[0] == str(city_id):
                menu_items.set_active(True)
            group = menu_items
            sub_menu_place.append(menu_items)
            menu_items.connect("activate", app.menu_response, 'reload', city_id_add[i])
            menu_items.show()
        menu_items = gtk.SeparatorMenuItem()
        sub_menu_place.append(menu_items)
        menu_items.show()

    menu_items = gtk.MenuItem(_('Setup...'))
    sub_menu_place.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'edit_city_id')
    menu_items.show()

    sub_menu_window
    menu_items = gtk.CheckMenuItem(_('Lock position'))
    menu_items.set_active(fix_position)
    menu_items.connect("activate", app.menu_response, 'fix')
    sub_menu_window.append(menu_items)
    menu_items.show()

    menu_items = gtk.CheckMenuItem(_('On all desktops'))
    menu_items.set_active(sticky)
    menu_items.connect("activate", app.menu_response, 'sticky')
    sub_menu_window.append(menu_items)
    menu_items.show()

    # main menu
    menu_items = gtk.ImageMenuItem(_('Refresh'))
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_REFRESH, gtk.ICON_SIZE_MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'reload', 0)
    menu_items.show()

    menu_items = gtk.SeparatorMenuItem()
    menu.append(menu_items)
    menu_items.show()

    menu_items = gtk.MenuItem(_('Location'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_place)
    menu_items.show()

    menu_items = gtk.MenuItem(_('Icons'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_icons)
    menu_items.show()
    
    menu_items = gtk.MenuItem(_('Background'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_bgs)
    menu_items.show()
    
    menu_items = gtk.MenuItem(_('Text'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_color_text)
    menu_items.show()

    menu_items = gtk.MenuItem(_('Window'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_window)
    menu_items.show()

    menu_items = gtk.ImageMenuItem(_('Properties'))
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_PROPERTIES, gtk.ICON_SIZE_MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'setup')
    menu_items.show()

    menu_items = gtk.ImageMenuItem(_('About'))
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_ABOUT, gtk.ICON_SIZE_MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'about')
    menu_items.show()

    menu_items = gtk.SeparatorMenuItem()
    menu.append(menu_items)
    menu_items.show()

    menu_items = gtk.ImageMenuItem(_('Close'))
    image = gtk.Image()
    image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", gtk.main_quit)
    menu_items.show()
    return menu, icons_list, backgrounds_list