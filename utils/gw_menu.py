#!/usr/bin/env python3

from gi.repository import Gtk
import os

def create_menu(app, ICONS_PATH, BGS_PATH, ICONS_USER_PATH, BGS_USER_PATH, icons_name, show_bg_png, 
    color_bg, bg_custom, color_scheme, color_scheme_number, city_list, city_id, fix_position, sticky):
    menu = None
    # из папки скрипта (dirs - иконки, files - фоны)
    for root, dirs, files in os.walk(ICONS_PATH):
        break
    files = os.listdir(BGS_PATH)
    dirs.sort()
    files.sort()
    dirs.remove('default')
    # из папки пользователя (dirs_user - иконки, files_user - фоны)
    for root, dirs_user, files_user in os.walk(ICONS_USER_PATH):
        break
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
    menu = Gtk.Menu()
    sub_menu_place = Gtk.Menu()
    sub_menu_icons = Gtk.Menu()
    sub_menu_bgs = Gtk.Menu()
    sub_menu_color_text = Gtk.Menu()
    sub_menu_window = Gtk.Menu()

    # sub_menu_place
    if len(city_list) > 0:
        for i in range(len(city_list)):
            menu_items = Gtk.RadioMenuItem(label=city_list[i].split(';')[1])
            if city_list[i].split(';')[0] == str(city_id):
                menu_items.set_active(True)
            sub_menu_place.append(menu_items)
            menu_items.connect("activate", app.menu_response, 'reload', city_list[i])
            menu_items.show()
        menu_items = Gtk.SeparatorMenuItem()
        sub_menu_place.append(menu_items)
        menu_items.show()
    menu_items = Gtk.MenuItem(_('Setup...'))
    sub_menu_place.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'edit_city_id')
    menu_items.show()

    # sub_menu_icons
    menu_items = Gtk.RadioMenuItem(label='0. Default')
    if icons_name == 'default':
        menu_items.set_active(True)
    sub_menu_icons.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'redraw_icons', 'default')
    menu_items.show()
    for i in range(len(icons_list)):
        menu_items = Gtk.RadioMenuItem(label=str(i+1)+'. '+icons_list[i])
        if icons_name == icons_list[i]:
            menu_items.set_active(True)
        sub_menu_icons.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'redraw_icons', icons_list[i])
        menu_items.show()

    # sub_menu_bgs
    menu_items = Gtk.RadioMenuItem(label='0. '+_('No'))
    if show_bg_png == False and color_bg[3]==0:
        menu_items.set_active(True)
    sub_menu_bgs.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'redraw_bg', 'Нет')
    menu_items.show()
    for i in range(len(backgrounds_list)):
        menu_items = Gtk.RadioMenuItem(label=str(i+1)+'. '+backgrounds_list[i])
        if bg_custom == backgrounds_list[i]:
            menu_items.set_active(True)
        sub_menu_bgs.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'redraw_bg', backgrounds_list[i])
        menu_items.show()

    # sub_menu_color_text
    for i in range(len(color_scheme)):
        menu_items = Gtk.RadioMenuItem(label=_('Color scheme')+' #' + str(i))
        if i == color_scheme_number:
            menu_items.set_active(True)
        sub_menu_color_text.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'redraw_text', i)
        menu_items.show()

    # sub_menu_window
    menu_items = Gtk.CheckMenuItem(_('Lock position'))
    menu_items.set_active(fix_position)
    menu_items.connect("activate", app.menu_response, 'fix')
    sub_menu_window.append(menu_items)
    menu_items.show()

    menu_items = Gtk.CheckMenuItem(_('On all desktops'))
    menu_items.set_active(sticky)
    menu_items.connect("activate", app.menu_response, 'sticky')
    sub_menu_window.append(menu_items)
    menu_items.show()

    # main menu
    menu_items = Gtk.ImageMenuItem(_('Refresh'))
    image = Gtk.Image()
    image.set_from_stock(Gtk.STOCK_REFRESH, Gtk.IconSize.MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'reload', 0)
    menu_items.show()

    menu_items = Gtk.SeparatorMenuItem()
    menu.append(menu_items)
    menu_items.show()

    menu_items = Gtk.MenuItem(_('Location'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_place)
    menu_items.show()

    menu_items = Gtk.MenuItem(_('Icons'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_icons)
    menu_items.show()
    
    menu_items = Gtk.MenuItem(_('Background'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_bgs)
    menu_items.show()
    
    menu_items = Gtk.MenuItem(_('Text'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_color_text)
    menu_items.show()

    menu_items = Gtk.MenuItem(_('Window'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_window)
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('Preferences'))
    image = Gtk.Image()
    image.set_from_stock(Gtk.STOCK_PREFERENCES, Gtk.IconSize.MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'setup')
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('Help'))
    image = Gtk.Image()
    image.set_from_stock(Gtk.STOCK_HELP, Gtk.IconSize.MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'help')
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('About'))
    image = Gtk.Image()
    image.set_from_stock(Gtk.STOCK_ABOUT, Gtk.IconSize.MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'about')
    menu_items.show()

    menu_items = Gtk.SeparatorMenuItem()
    menu.append(menu_items)
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('Close'))
    image = Gtk.Image()
    image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", Gtk.main_quit)
    menu_items.show()
    return menu, icons_list, backgrounds_list