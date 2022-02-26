#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import os
from utils import presets
from services import data
import datetime

# create_weather_menu by Istvan Petres
def create_weather_menu(app, ICONS_PATH, gw_config, weather):
    city_id = gw_config['city_id']
    icons_menu_name = gw_config['icons_menu_name']
    stock_icons_path = ICONS_PATH+'/'+icons_menu_name+'/stock/'
    preset_number = gw_config['preset_number']
    current_place = 'Unknown';

    if not os.path.isdir(stock_icons_path):
        stock_icons_path = ICONS_PATH+'/default/stock/'

    # create menu and fill 
    menu = Gtk.Menu()

    # main menu
    menu_items = Gtk.ImageMenuItem('⇆ '+_('Switch to app menu'))
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'weather_menu')
    menu_items.show()

    menu_items = Gtk.ImageMenuItem('⇅ '+_('Show/Hide widget'))
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'show_hide_widget')
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('Location')+': '+weather['city_name'][0])
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'goto_site', 0)
    menu_items.show()

    try:
        weather['icon_now']
    except NameError:
        return menu

    menu_items = Gtk.SeparatorMenuItem()
    menu.append(menu_items)
    menu_items.show()

    menu_items = Gtk.ImageMenuItem('')
    image = Gtk.Image()
    image.set_from_file(stock_icons_path+weather['icon_now'][0].split(';')[1])
    menu_items.set_image(image)
    menu_items.set_always_show_image(always_show=True);
    label = menu_items.get_children()[0]
    label.set_markup('<b>'+_('Now')+' '+weather['t_now'][0].split(';')[0]+'</b> ('+weather['t_day'][0].split(';')[0]+' / '+weather['t_night'][0].split(';')[0]+')')
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'goto_site_hourly')
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('Humidity')+': '+weather['hum_now'][0]+'%')
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'goto_site_hourly')
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('Wind')+': '+weather['wind_speed_now'][0].split(';')[gw_config['wind_units']])
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'goto_site_hourly')
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(weather['text_now'][0])
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'goto_site_hourly')
    menu_items.show()

    if weather['sunrise'] != '?':
        menu_items = Gtk.ImageMenuItem(_('Sunrise')+': '+weather['sunrise'])
        menu.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'goto_site_hourly')
        menu_items.show()

        menu_items = Gtk.ImageMenuItem(_('Sunset')+': '+weather['sunset'])
        menu.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'goto_site_hourly')
        menu_items.show()

    now = datetime.datetime.now()

    for i in range(1, gw_config['n']+1):
        now += datetime.timedelta(days=1)

        try:
            weather['icon'][i]
        except:
            break

        menu_items = Gtk.SeparatorMenuItem()
        menu.append(menu_items)
        menu_items.show()
        menu_items = Gtk.ImageMenuItem('')
        image = Gtk.Image()
        image.set_from_file(stock_icons_path+weather['icon'][i].split(';')[1])
        menu_items.set_image(image)
        menu_items.set_always_show_image(always_show=True);
        label = menu_items.get_children()[0]
        if i == 1:
            label.set_markup('<b>'+_('Tomorrow')+' '+weather['t_day'][i].split(';')[0]+' / '+weather['t_night'][i].split(';')[0]+'</b>')
        else:
            label.set_markup('<b>'+now.strftime("%A")+' '+weather['t_day'][i].split(';')[0]+' / '+weather['t_night'][i].split(';')[0]+'</b>')
        menu.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'goto_site_day', i+1)
        menu_items.show()

        if weather['chance_of_rain'] != '?' and weather['chance_of_rain'][i] != '':
            menu_items = Gtk.ImageMenuItem(_('Precipitation')+': '+weather['chance_of_rain'][i])
            menu.append(menu_items)
            menu_items.connect("activate", app.menu_response, 'goto_site_day', i+1)
            menu_items.show()

        menu_items = Gtk.ImageMenuItem(weather['text'][i])
        menu.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'goto_site_day', i+1)
        menu_items.show()


    return menu


def create_menu(app, ICONS_PATH, BGS_PATH, ICONS_USER_PATH, BGS_USER_PATH, color_scheme, gw_config, for_indicator, test_on):
    icons_name = gw_config['icons_name']
    icons_menu_name = gw_config['icons_menu_name']
    show_bg_png = gw_config['show_bg_png']
    color_bg = gw_config['color_bg']
    bg_custom = gw_config['bg_custom']
    color_scheme_number = gw_config['color_scheme_number']
    city_id = gw_config['city_id']
    fix_position = gw_config['fix_position']
    sticky = gw_config['sticky']
    indicator_icons_name = gw_config['indicator_icons_name']
    preset_number = gw_config['preset_number']
    always_on_top = gw_config['always_on_top']

    menu = None
    # from script folder (dirs - icons, files - backdrounds)
    for root, dirs, files in os.walk(ICONS_PATH):
        break
    files = os.listdir(BGS_PATH)
    dirs.sort()
    files.sort()
    dirs.remove('default')
    # from user folder (dirs_user - icons, files_user - backdrounds)
    for root, dirs_user, files_user in os.walk(ICONS_USER_PATH):
        break
    files_user = os.listdir(BGS_USER_PATH)
    dirs_user.sort()
    files_user.sort()
    dirs_user.remove('default')
    # list with icons and backdrounds
    icons_list = []
    icons_list.extend(dirs)
    icons_list.extend(dirs_user)
    backgrounds_list = []
    backgrounds_list.extend(files)
    backgrounds_list.extend(files_user)
    # create menu and fill 
    menu = Gtk.Menu()
    sub_menu_place = Gtk.Menu()
    sub_menu_icons = Gtk.Menu()
    sub_menu_indicator_icons = Gtk.Menu()
    sub_menu_icons_for_menu = Gtk.Menu()
    sub_menu_bgs = Gtk.Menu()
    sub_menu_color_text = Gtk.Menu()
    sub_menu_window = Gtk.Menu()
    sub_menu_presets = Gtk.Menu()

    # sub_menu_place
    menu_items = Gtk.MenuItem(_('Setup...'))
    sub_menu_place.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'edit_city_id')
    menu_items.show()

    for i in range(len(data.services_list)):
        try:
            city_list = gw_config[data.get_city_list(data.services_list[i])]
        except:
            city_list = []
        if len(city_list) != 0:
            menu_items = Gtk.SeparatorMenuItem()
            sub_menu_place.append(menu_items)
            menu_items.show()

            menu_items = Gtk.MenuItem(label=data.services_list[i])
            sub_menu_place.append(menu_items)
            menu_items.show()
            menu_items.set_sensitive(False)

            for j in range(len(city_list)):
                menu_items = Gtk.RadioMenuItem(label=city_list[j].split(';')[1])
                if city_list[j].split(';')[0] == str(gw_config['city_id']) and gw_config['service'] == data.services_list[i]:
                    menu_items.set_active(True)
                sub_menu_place.append(menu_items)
                menu_items.connect("activate", app.menu_response, 'reload', [data.services_list[i], city_list[j], data.get(data.services_list[i])['weather_lang_list'][0]])
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

    # sub_menu_indicator_icons
    menu_items = Gtk.RadioMenuItem(label='0. Default')
    if indicator_icons_name == 'default':
        menu_items.set_active(True)
    sub_menu_indicator_icons.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'redraw_indicator_icons', 'default')
    menu_items.show()
    for i in range(len(icons_list)):
        menu_items = Gtk.RadioMenuItem(label=str(i+1)+'. '+icons_list[i])
        if indicator_icons_name == icons_list[i]:
            menu_items.set_active(True)
        sub_menu_indicator_icons.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'redraw_indicator_icons', icons_list[i])
        menu_items.show()

    # sub_menu_icons_for_menu
    menu_items = Gtk.RadioMenuItem(label='0. Default')
    if icons_menu_name == 'default':
        menu_items.set_active(True)
    sub_menu_icons_for_menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'redraw_menu_icons', 'default')
    menu_items.show()
    for i in range(len(icons_list)):
        menu_items = Gtk.RadioMenuItem(label=str(i+1)+'. '+icons_list[i])
        if icons_menu_name == icons_list[i]:
            menu_items.set_active(True)
        sub_menu_icons_for_menu.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'redraw_menu_icons', icons_list[i])
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
    color_scheme_names = (_('Black'),_('White'),_('Gray'))
    for i in range(len(color_scheme)):
        menu_items = Gtk.RadioMenuItem(label=color_scheme_names[i])
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

    menu_items = Gtk.CheckMenuItem(_('Always on top'))
    menu_items.set_active(always_on_top)
    menu_items.connect("activate", app.menu_response, 'always_on_top')
    sub_menu_window.append(menu_items)
    menu_items.show()

    menu_items = Gtk.SeparatorMenuItem()
    sub_menu_window.append(menu_items)
    menu_items.show()

    menu_items = Gtk.MenuItem(_('Save screenshot'))
    sub_menu_window.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'save_screenshot')
    menu_items.show()

    # sub_menu_presets
    for i in range(len(presets.list)):
        menu_items = Gtk.RadioMenuItem(label=presets.names[i])
        if i == preset_number:
            menu_items.set_active(True)
        sub_menu_presets.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'load_preset', i)
        menu_items.show()

    # main menu
    if for_indicator:
        menu_items = Gtk.ImageMenuItem('⇆ '+_('Switch to weather menu'))
        menu.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'weather_menu')
        menu_items.show()

        menu_items = Gtk.ImageMenuItem('⇅ '+_('Show/Hide widget'))
        menu.append(menu_items)
        menu_items.connect("activate", app.menu_response, 'show_hide_widget')
        menu_items.show()

        menu_items = Gtk.SeparatorMenuItem()
        menu.append(menu_items)
        menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('Refresh'))
    image = Gtk.Image()
    image.set_from_stock(Gtk.STOCK_REFRESH, Gtk.IconSize.MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'reload', 0)
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('Start new instance'))
    image = Gtk.Image()
    image.set_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'start_new_instance', 0)
    menu_items.show()

    menu_items = Gtk.ImageMenuItem(_('Go to site'))
    image = Gtk.Image()
    image.set_from_stock(Gtk.STOCK_JUMP_TO, Gtk.IconSize.MENU)
    menu_items.set_image(image)
    menu.append(menu_items)
    menu_items.connect("activate", app.menu_response, 'goto_site', 0)
    menu_items.show()

    menu_items = Gtk.SeparatorMenuItem()
    menu.append(menu_items)
    menu_items.show()

    menu_items = Gtk.MenuItem(_('Location'))
    menu.append(menu_items)
    menu_items.set_submenu(sub_menu_place)
    menu_items.show()

    if for_indicator:
        menu_items = Gtk.MenuItem(_('Indicator icons'))
        menu.append(menu_items)
        menu_items.set_submenu(sub_menu_indicator_icons)
        menu_items.show()

        menu_items = Gtk.MenuItem(_('Menu icons'))
        menu.append(menu_items)
        menu_items.set_submenu(sub_menu_icons_for_menu)
        menu_items.show()
    else:
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

        menu_items = Gtk.MenuItem(_('Presets'))
        menu.append(menu_items)
        menu_items.set_submenu(sub_menu_presets)
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
### testing menu
    if test_on:
        sub_menu_testing = Gtk.Menu()
        window_type_hint_list = (
            'Auto',
            'Gdk.WindowTypeHint.DOCK',
            'Gdk.WindowTypeHint.NORMAL',
            'Gdk.WindowTypeHint.DIALOG',
            'Gdk.WindowTypeHint.MENU',
            'Gdk.WindowTypeHint.TOOLBAR',
            'Gdk.WindowTypeHint.SPLASHSCREEN',
            'Gdk.WindowTypeHint.UTILITY',
            'Gdk.WindowTypeHint.DESKTOP',
            'Gdk.WindowTypeHint.DROPDOWN_MENU',
            'Gdk.WindowTypeHint.POPUP_MENU',
            'Gdk.WindowTypeHint.TOOLTIP',
            'Gdk.WindowTypeHint.NOTIFICATION',
            'Gdk.WindowTypeHint.COMBO',
            'Gdk.WindowTypeHint.DND'
            )
        for i in range(len(window_type_hint_list)):
            menu_items = Gtk.RadioMenuItem(label=window_type_hint_list[i])
            sub_menu_testing.append(menu_items)
            if i == gw_config['type_hint']:
                menu_items.set_active(True)
            menu_items.connect("activate", app.menu_response, 'set_window_type_hint', i)
            menu_items.show()

        menu_items = Gtk.MenuItem('[Testing] WindowTypeHint')
        menu.append(menu_items)
        menu_items.set_submenu(sub_menu_testing)
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
