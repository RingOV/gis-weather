#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  settings.py
#  Copyright 2013-2014 Alexander Koltsov
#
#  powered by Sloth 0.2
#  Copyright (c) 2011 Mikhail Valkov


# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can find the full text of the license under
# http://www.gnu.org/licenses/gpl.txt

#import pygtk
#pygtk.require('2.0')
import gtk
import os
import json
import pango
import autorun
import sys
if sys.platform.startswith("win"):
    WIN = True
else:
    WIN = False

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')
if WIN:
    CONFIG_PATH = CONFIG_PATH.decode(sys.getfilesystemencoding())

work_path = os.path.dirname(sys.argv[0])
if WIN:
    work_path = work_path.decode(sys.getfilesystemencoding())

gw_config_default_set = {}
gw_config_set = {}
drawing_area_set = None
state_lock = True
App_gw = None
icons_list_set = [] 
backgrounds_list_set = []

def Save_Config():
    json.dump(gw_config_set, open(os.path.join(CONFIG_PATH, 'gw_config.json'), "w"), sort_keys=True, indent=4, separators=(', ', ': '))

class settings():
    def __init__(self):
        #Загружаем файл интерфса
        #Должен валяться в папке со скриптом
        self.gladefile = os.path.abspath(os.path.join(globals()['work_path'],"settings.glade"))
        #Дерево элементов интерфеса
        self.widgets_tree = gtk.Builder()
        self.widgets_tree.add_from_file(self.gladefile)

        #загружаем элементы формы
        self.window1 = self.widgets_tree.get_object('window1')
        self.window1.set_icon_from_file("icon.png")

        # Общие
        self.spinbutton_upd_time = self.widgets_tree.get_object('spinbutton_upd_time')
        self.spinbutton_upd_time.connect("value-changed", self.save_settings)
        self.checkbutton_t_feel = self.widgets_tree.get_object('checkbutton_t_feel')
        self.checkbutton_t_feel.connect("toggled", self.save_settings)
        self.checkbutton_fix_BadDrawable = self.widgets_tree.get_object('checkbutton_fix_BadDrawable')
        self.checkbutton_fix_BadDrawable.connect("toggled", self.save_settings)
        self.combobox_check_for_updates = self.widgets_tree.get_object('combobox_check_for_updates')
        self.combobox_check_for_updates.connect("changed", self.save_settings)
        self.button_city_id = self.widgets_tree.get_object('button_city_id')
        self.button_city_id.connect("clicked", App_gw.menu_response, 'edit_city_id')
        self.button_open_config_folder = self.widgets_tree.get_object('button_open_config_folder')
        self.button_open_config_folder.connect("clicked", App_gw.menu_response, 'edit')
        self.checkbutton_autorun = self.widgets_tree.get_object('checkbutton_autorun')
        self.checkbutton_autorun.connect("toggled", self.set_autorun)

        self.clear_upd_time = self.widgets_tree.get_object('clear_upd_time')
        self.clear_upd_time.connect("clicked", self.clear_settings)
        self.clear_t_feel = self.widgets_tree.get_object('clear_t_feel')
        self.clear_t_feel.connect("clicked", self.clear_settings)
        self.clear_fix_BadDrawable = self.widgets_tree.get_object('clear_fix_BadDrawable')
        self.clear_fix_BadDrawable.connect("clicked", self.clear_settings)
        self.clear_check_for_updates = self.widgets_tree.get_object('clear_check_for_updates')
        self.clear_check_for_updates.connect("clicked", self.clear_settings)


        # Окно
        self.spinbutton_x_pos = self.widgets_tree.get_object('spinbutton_x_pos')
        self.spinbutton_x_pos.connect("value-changed", self.save_settings)
        self.spinbutton_y_pos = self.widgets_tree.get_object('spinbutton_y_pos')
        self.spinbutton_y_pos.connect("value-changed", self.save_settings)
        self.spinbutton_margin = self.widgets_tree.get_object('spinbutton_margin')
        self.spinbutton_margin.connect("value-changed", self.save_settings)
        self.spinbutton_opacity = self.widgets_tree.get_object('spinbutton_opacity')
        self.spinbutton_opacity.connect("value-changed", self.save_settings)
        self.checkbutton_fix_position = self.widgets_tree.get_object('checkbutton_fix_position')
        self.checkbutton_fix_position.connect("toggled", self.save_settings)
        self.checkbutton_sticky = self.widgets_tree.get_object('checkbutton_sticky')
        self.checkbutton_sticky.connect("toggled", self.save_settings)

        self.clear_x_pos = self.widgets_tree.get_object('clear_x_pos')
        self.clear_x_pos.connect("clicked", self.clear_settings)
        self.clear_margin = self.widgets_tree.get_object('clear_margin')
        self.clear_margin.connect("clicked", self.clear_settings)
        self.clear_y_pos = self.widgets_tree.get_object('clear_y_pos')
        self.clear_y_pos.connect("clicked", self.clear_settings)
        self.clear_opacity = self.widgets_tree.get_object('clear_opacity')
        self.clear_opacity.connect("clicked", self.clear_settings)
        self.clear_fix_position = self.widgets_tree.get_object('clear_fix_position')
        self.clear_fix_position.connect("clicked", self.clear_settings)
        self.clear_sticky = self.widgets_tree.get_object('clear_sticky')
        self.clear_sticky.connect("clicked", self.clear_settings)

        # Вид
        self.checkbutton_show_block_today = self.widgets_tree.get_object('checkbutton_show_block_today')
        self.checkbutton_show_block_today.connect("toggled", self.save_settings)
        self.spinbutton_block_today_left = self.widgets_tree.get_object('spinbutton_block_today_left')
        self.spinbutton_block_today_left.connect("value-changed", self.save_settings)
        self.checkbutton_show_block_tomorrow = self.widgets_tree.get_object('checkbutton_show_block_tomorrow')
        self.checkbutton_show_block_tomorrow.connect("toggled", self.save_settings)
        self.spinbutton_block_tomorrow_left = self.widgets_tree.get_object('spinbutton_block_tomorrow_left')
        self.spinbutton_block_tomorrow_left.connect("value-changed", self.save_settings)
        self.checkbutton_show_block_wind_direct = self.widgets_tree.get_object('checkbutton_show_block_wind_direct')
        self.checkbutton_show_block_wind_direct.connect("toggled", self.save_settings)
        self.spinbutton_block_wind_direct_left = self.widgets_tree.get_object('spinbutton_block_wind_direct_left')
        self.spinbutton_block_wind_direct_left.connect("value-changed", self.save_settings)
        self.checkbutton_wind_direct_small = self.widgets_tree.get_object('checkbutton_wind_direct_small')
        self.checkbutton_wind_direct_small.connect("toggled", self.save_settings)
        self.spinbutton_angel = self.widgets_tree.get_object('spinbutton_angel')
        self.spinbutton_angel.connect("value-changed", self.save_settings)
        self.checkbutton_show_block_add_info = self.widgets_tree.get_object('checkbutton_show_block_add_info')
        self.checkbutton_show_block_add_info.connect("toggled", self.save_settings)
        self.spinbutton_block_add_info_left = self.widgets_tree.get_object('spinbutton_block_add_info_left')
        self.spinbutton_block_add_info_left.connect("value-changed", self.save_settings)
        self.spinbutton_n = self.widgets_tree.get_object('spinbutton_n')
        self.spinbutton_n.connect("value-changed", self.save_settings)
        self.checkbutton_show_time_receive = self.widgets_tree.get_object('checkbutton_show_time_receive')
        self.checkbutton_show_time_receive.connect("toggled", self.save_settings)
        self.combobox_show_splash_screen = self.widgets_tree.get_object('combobox_show_splash_screen')
        self.combobox_show_splash_screen.connect("changed", self.save_settings)
        self.spinbutton_max_try_show = self.widgets_tree.get_object('spinbutton_max_try_show')
        self.spinbutton_max_try_show.connect("value-changed", self.save_settings)


        self.clear_show_block_today = self.widgets_tree.get_object('clear_show_block_today')
        self.clear_show_block_today.connect("clicked", self.clear_settings)
        self.clear_block_today_left = self.widgets_tree.get_object('clear_block_today_left')
        self.clear_block_today_left.connect("clicked", self.clear_settings)
        self.clear_show_block_tomorrow = self.widgets_tree.get_object('clear_show_block_tomorrow')
        self.clear_show_block_tomorrow.connect("clicked", self.clear_settings)
        self.clear_block_tomorrow_left = self.widgets_tree.get_object('clear_block_tomorrow_left')
        self.clear_block_tomorrow_left.connect("clicked", self.clear_settings)
        self.clear_show_block_wind_direct = self.widgets_tree.get_object('clear_show_block_wind_direct')
        self.clear_show_block_wind_direct.connect("clicked", self.clear_settings)
        self.clear_block_wind_direct_left = self.widgets_tree.get_object('clear_block_wind_direct_left')
        self.clear_block_wind_direct_left.connect("clicked", self.clear_settings)
        self.clear_wind_direct_small = self.widgets_tree.get_object('clear_wind_direct_small')
        self.clear_wind_direct_small.connect("clicked", self.clear_settings)
        self.clear_angel = self.widgets_tree.get_object('clear_angel')
        self.clear_angel.connect("clicked", self.clear_settings)
        self.clear_show_block_add_info = self.widgets_tree.get_object('clear_show_block_add_info')
        self.clear_show_block_add_info.connect("clicked", self.clear_settings)
        self.clear_block_add_info_left = self.widgets_tree.get_object('clear_block_add_info_left')
        self.clear_block_add_info_left.connect("clicked", self.clear_settings)
        self.clear_n = self.widgets_tree.get_object('clear_n')
        self.clear_n.connect("clicked", self.clear_settings)
        self.clear_show_time_receive = self.widgets_tree.get_object('clear_show_time_receive')
        self.clear_show_time_receive.connect("clicked", self.clear_settings)
        self.clear_show_splash_screen = self.widgets_tree.get_object('clear_show_splash_screen')
        self.clear_show_splash_screen.connect("clicked", self.clear_settings)
        self.clear_max_try_show = self.widgets_tree.get_object('clear_max_try_show')
        self.clear_max_try_show.connect("clicked", self.clear_settings)

        #Оформление
        self.fontbutton_font = self.widgets_tree.get_object('fontbutton_font')
        self.fontbutton_font.connect("font-set", self.set_font)
        self.colorbutton_color_text = self.widgets_tree.get_object('colorbutton_color_text')
        self.colorbutton_color_text.connect("color-set", self.set_color)
        self.colorbutton_color_text_week = self.widgets_tree.get_object('colorbutton_color_text_week')
        self.colorbutton_color_text_week.connect("color-set", self.set_color)
        self.colorbutton_color_shadow = self.widgets_tree.get_object('colorbutton_color_shadow')
        self.colorbutton_color_shadow.connect("color-set", self.set_color)
        self.colorbutton_color_high_wind = self.widgets_tree.get_object('colorbutton_color_high_wind')
        self.colorbutton_color_high_wind.connect("color-set", self.set_color)
        self.colorbutton_color_bg = self.widgets_tree.get_object('colorbutton_color_bg')
        self.colorbutton_color_bg.connect("color-set", self.set_color)
        self.checkbutton_draw_shadow = self.widgets_tree.get_object('checkbutton_draw_shadow')
        self.checkbutton_draw_shadow.connect("toggled", self.save_settings)
        self.spinbutton_high_wind = self.widgets_tree.get_object('spinbutton_high_wind')
        self.spinbutton_high_wind.connect("value-changed", self.save_settings)
        self.checkbutton_show_bg_png = self.widgets_tree.get_object('checkbutton_show_bg_png')
        self.checkbutton_show_bg_png.connect("toggled", self.save_settings)
        self.spinbutton_r = self.widgets_tree.get_object('spinbutton_r')
        self.spinbutton_r.connect("value-changed", self.save_settings)

        self.combobox_icons_name = self.widgets_tree.get_object('combobox_icons_name')
        self.combobox_icons_name.connect("changed", self.set_icon_bg)
        self.liststore3 = self.widgets_tree.get_object('liststore3')
        self.combobox_bg_custom = self.widgets_tree.get_object('combobox_bg_custom')
        self.combobox_bg_custom.connect("changed", self.set_icon_bg)
        self.liststore4 = self.widgets_tree.get_object('liststore4')


        self.clear_font = self.widgets_tree.get_object('clear_font')
        self.clear_font.connect("clicked", self.clear_settings)
        self.clear_color_text = self.widgets_tree.get_object('clear_color_text')
        self.clear_color_text.connect("clicked", self.clear_settings)
        self.clear_color_text_week = self.widgets_tree.get_object('clear_color_text_week')
        self.clear_color_text_week.connect("clicked", self.clear_settings)
        self.clear_color_shadow = self.widgets_tree.get_object('clear_color_shadow')
        self.clear_color_shadow.connect("clicked", self.clear_settings)
        self.clear_color_high_wind = self.widgets_tree.get_object('clear_color_high_wind')
        self.clear_color_high_wind.connect("clicked", self.clear_settings)
        self.clear_color_bg = self.widgets_tree.get_object('clear_color_bg')
        self.clear_color_bg.connect("clicked", self.clear_settings)
        self.clear_draw_shadow = self.widgets_tree.get_object('clear_draw_shadow')
        self.clear_draw_shadow.connect("clicked", self.clear_settings)
        self.clear_high_wind = self.widgets_tree.get_object('clear_high_wind')
        self.clear_high_wind.connect("clicked", self.clear_settings)
        self.clear_show_bg_png = self.widgets_tree.get_object('clear_show_bg_png')
        self.clear_show_bg_png.connect("clicked", self.clear_settings)
        self.clear_r = self.widgets_tree.get_object('clear_r')
        self.clear_r.connect("clicked", self.clear_settings)
        self.clear_icons_name = self.widgets_tree.get_object('clear_icons_name')
        self.clear_icons_name.connect("clicked", self.clear_settings)
        self.clear_bg_custom = self.widgets_tree.get_object('clear_bg_custom')
        self.clear_bg_custom.connect("clicked", self.clear_settings)

        
        self.button_close = self.widgets_tree.get_object('button_close')
        self.button_close.connect("clicked", self.close_window)

        self.window1.connect("delete_event", self.close_window)
        self.window1.show()

    def load_config_into_form(self):
        global state_lock
        state_lock = True

        self.load(self.spinbutton_upd_time)
        self.load(self.checkbutton_t_feel)
        self.load(self.checkbutton_fix_BadDrawable)
        self.load(self.spinbutton_x_pos)
        self.load(self.spinbutton_y_pos)
        self.load(self.spinbutton_margin)
        self.load(self.spinbutton_opacity)
        self.load(self.checkbutton_fix_position)
        self.load(self.checkbutton_sticky)
        self.load(self.spinbutton_block_today_left)
        self.load(self.checkbutton_show_block_today)
        self.load(self.spinbutton_block_tomorrow_left)
        self.load(self.checkbutton_show_block_tomorrow)
        self.load(self.spinbutton_block_wind_direct_left)
        self.load(self.checkbutton_show_block_wind_direct)
        self.load(self.spinbutton_angel)
        self.load(self.checkbutton_wind_direct_small)
        self.load(self.spinbutton_block_add_info_left)
        self.load(self.checkbutton_show_block_add_info)
        self.load(self.spinbutton_n)
        self.load(self.checkbutton_show_time_receive)
        self.load(self.combobox_check_for_updates)
        self.load(self.combobox_show_splash_screen)
        self.load(self.spinbutton_max_try_show)
        self.fontbutton_font.set_font_name(gw_config_set['font'])
        self.load(self.colorbutton_color_text)
        self.load(self.colorbutton_color_text_week)
        self.load(self.colorbutton_color_shadow)
        self.load(self.colorbutton_color_high_wind)
        self.load(self.colorbutton_color_bg)
        self.load(self.checkbutton_draw_shadow)
        self.load(self.spinbutton_high_wind)
        self.load(self.checkbutton_show_bg_png)
        self.load(self.spinbutton_r)

        self.liststore3.clear()
        for i in range(len(icons_list_set)):
            self.liststore3.append([icons_list_set[i]])
            if icons_list_set[i] == gw_config_set['icons_name']: 
                self.combobox_icons_name.set_active(i)
        self.liststore4.clear()
        for i in range(len(backgrounds_list_set)):
            self.liststore4.append([backgrounds_list_set[i]])
            if backgrounds_list_set[i] == gw_config_set['bg_custom']: 
                self.combobox_bg_custom.set_active(i)
        if autorun.exists("Gis Weather"):
            self.checkbutton_autorun.set_active(True)

        state_lock = False

    def load(self, widget):
        w_type = widget.get_name()
        w_name = gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        if w_type == 'GtkSpinButton':
            widget.set_value(gw_config_set[name])
        else:
            if w_type == 'GtkColorButton':
                c = gw_config_set[name]
                color = gtk.gdk.Color(int(c[0]*65535), int(c[1]*65535), int(c[2]*65535))
                widget.set_color(color)
                widget.set_alpha(int(c[3]*65535))
            else:
                widget.set_active(gw_config_set[name])


    def close_window(self, widget, data = None):
        self.window1.hide()
        gtk.main_quit()

    def save_settings(self, widget):
        if state_lock:
            return
        global gw_config_set
        value = None
        w_type = widget.get_name()
        w_name = gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        if w_type == 'GtkSpinButton':
            if name in ('opacity'):
                value = widget.get_value()
            else:
                value = int(widget.get_value())
        else:
            value = widget.get_active()
        if value != None:
            gw_config_set[name] = value
        Save_Config()
        drawing_area_set.redraw(False, False, load_config = True)

    def clear_settings(self, widget):
        global gw_config_set
        w_name = gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        gw_config_set[name] = gw_config_default_set[name]
        Save_Config()
        drawing_area_set.redraw(False, False, load_config = True)
        self.load_config_into_form()

    def set_font(self, widget):
        if state_lock:
            return
        global gw_config_set
        font_desc = pango.FontDescription(self.fontbutton_font.get_font_name())
        font = font_desc.get_family()
        gw_config_set['font'] = font
        Save_Config()
        drawing_area_set.redraw(False, False, load_config = True)

    def set_icon_bg(self, widget):
        if state_lock:
            return
        global gw_config_set
        w_name = gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        i = widget.get_active()
        if name == 'icons_name':
            gw_config_set[name] = icons_list_set[i]
        else:
            gw_config_set[name] = backgrounds_list_set[i]
        Save_Config()
        drawing_area_set.redraw(False, False, load_config = True)

    def set_color(self, widget):
        if state_lock:
            return
        global gw_config_set
        w_name = gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        alpha = (widget.get_alpha()*100)/65535.0
        alpha = alpha/100.0
        color = widget.get_color()
        gw_config_set[name] = (color.red_float, color.green_float, color.blue_float, alpha)
        Save_Config()
        drawing_area_set.redraw(False, False, load_config = True)

    def set_autorun(self, widget):
        if state_lock:
            return
        if widget.get_active() == True:
            if WIN:
                autorun.add("Gis Weather", work_path+'\\gis-weather.exe')
            else:
                autorun.add("Gis Weather", "/usr/bin/gis-weather")
        else:
            autorun.remove("Gis Weather")

def main(gw_config_default, gw_config, drawing_area, app_gw, icons_list, backgrounds_list):
    global gw_config_default_set, gw_config_set, drawing_area_set, App_gw, icons_list_set, backgrounds_list_set
    for i in gw_config_default.keys():
        gw_config_default_set[i] = gw_config_default[i]
    for i in gw_config.keys():
        gw_config_set[i] = gw_config[i]

    icons_list_set = []
    backgrounds_list_set = []
    icons_list_set.append('default')
    icons_list_set.extend(icons_list)
    backgrounds_list_set.extend(backgrounds_list)
    
    drawing_area_set = drawing_area
    App_gw = app_gw
    App = settings()
    App.load_config_into_form()
    gtk.main()
