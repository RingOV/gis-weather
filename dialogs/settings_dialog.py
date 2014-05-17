#!/usr/bin/env python3

from gi.repository import Gtk, Pango, Gdk
from utils import autorun, localization
import os
import json
import sys
from services import gismeteo
if sys.platform.startswith("win"):
    WIN = True
else:
    WIN = False

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')
if WIN:
    CONFIG_PATH = CONFIG_PATH.decode(sys.getfilesystemencoding())

work_path = os.path.abspath(os.path.dirname(__file__))
if WIN:
    work_path = work_path.decode(sys.getfilesystemencoding())

gw_config_default_set = {}
gw_config_set = {}
drawing_area_set = None
state_lock = True
App_gw = None
icons_list_set = [] 
backgrounds_list_set = []

dict_weather_lang = gismeteo.dict_weather_lang

# available lang from gismeteo
weather_lang_list = gismeteo.weather_lang_list

dict_app_lang = {
    'auto': 'Auto',
    'en': 'English',
    'ru': 'Русский'
}
# find all available lang
available_lang = ['auto', 'en']
root, dirs, files = os.walk(os.path.join(os.path.split(work_path)[0], 'i18n'))
dirs = root[1]
dirs.sort()
for i in range(len(dirs)):
    available_lang.append(dirs[i])

def Save_Config():
    json.dump(gw_config_set, open(os.path.join(CONFIG_PATH, 'gw_config.json'), "w"), sort_keys=True, indent=4, separators=(', ', ': '))

class settings():
    def __init__(self):
        self.ui = Gtk.Builder()
        self.ui.add_from_file(os.path.join(work_path,"settings_dialog.ui"))

        self.window1 = self.ui.get_object('dialog1')
        self.window1.set_icon_from_file(os.path.join(os.path.split(work_path)[0], "icon.png"))

        self.list_o = self.ui.get_objects()
        self.dict_o = {}
        self.dict_o = localization.translate_ui(self.list_o, self.dict_o)
        self.window1.set_title(_('Preferences')+' Gis Weather')

        # General
        self.spinbutton_upd_time = self.ui.get_object('spinbutton_upd_time')
        self.spinbutton_upd_time.connect("value-changed", self.save_settings)
        self.switch_t_feel = self.ui.get_object('switch_t_feel')
        self.switch_t_feel.connect("notify::active", self.save_settings)
        self.switch_fix_BadDrawable = self.ui.get_object('switch_fix_BadDrawable')
        self.switch_fix_BadDrawable.connect("notify::active", self.save_settings)
        self.combobox_check_for_updates = self.ui.get_object('combobox_check_for_updates')
        self.combobox_check_for_updates.connect("changed", self.save_settings)
        self.button_city_id = self.ui.get_object('button_city_id')
        self.button_city_id.connect("clicked", App_gw.menu_response, 'edit_city_id')
        self.button_open_config_folder = self.ui.get_object('button_open_config_folder')
        self.button_open_config_folder.connect("clicked", App_gw.menu_response, 'edit')
        self.switch_autostart = self.ui.get_object('switch_autostart')
        self.switch_autostart.connect("notify::active", self.set_autorun)
        self.combobox_app_lang = self.ui.get_object('combobox_app_lang')
        self.combobox_app_lang.connect("changed", self.set_app_lang)
        self.combobox_weather_lang = self.ui.get_object('combobox_weather_lang')
        self.combobox_weather_lang.connect("changed", self.set_weather_lang)
        self.liststore1 = self.ui.get_object('liststore1')
        self.spinbutton_delay_start_time = self.ui.get_object('spinbutton_delay_start_time')
        self.spinbutton_delay_start_time.connect("value-changed", self.save_settings)
        self.label_delay_start_time = self.ui.get_object('label_delay_start_time')
        
        self.clear_upd_time = self.ui.get_object('clear_upd_time')
        self.clear_upd_time.connect("clicked", self.clear_settings)
        self.clear_t_feel = self.ui.get_object('clear_t_feel')
        self.clear_t_feel.connect("clicked", self.clear_settings)
        self.clear_fix_BadDrawable = self.ui.get_object('clear_fix_BadDrawable')
        self.clear_fix_BadDrawable.connect("clicked", self.clear_settings)
        self.clear_check_for_updates = self.ui.get_object('clear_check_for_updates')
        self.clear_check_for_updates.connect("clicked", self.clear_settings)
        self.clear_delay_start_time = self.ui.get_object('clear_delay_start_time')
        self.clear_delay_start_time.connect("clicked", self.clear_settings)


        # Window
        self.spinbutton_x_pos = self.ui.get_object('spinbutton_x_pos')
        self.spinbutton_x_pos.connect("value-changed", self.save_settings)
        self.spinbutton_y_pos = self.ui.get_object('spinbutton_y_pos')
        self.spinbutton_y_pos.connect("value-changed", self.save_settings)
        self.spinbutton_margin = self.ui.get_object('spinbutton_margin')
        self.spinbutton_margin.connect("value-changed", self.save_settings)
        self.spinbutton_opacity = self.ui.get_object('spinbutton_opacity')
        self.spinbutton_opacity.connect("value-changed", self.save_settings)
        self.switch_fix_position = self.ui.get_object('switch_fix_position')
        self.switch_fix_position.connect("notify::active", self.save_settings)
        self.switch_sticky = self.ui.get_object('switch_sticky')
        self.switch_sticky.connect("notify::active", self.save_settings)
        self.liststore5 = self.ui.get_object('liststore5')
        self.liststore6 = self.ui.get_object('liststore6')

        self.clear_x_pos = self.ui.get_object('clear_x_pos')
        self.clear_x_pos.connect("clicked", self.clear_settings)
        self.clear_margin = self.ui.get_object('clear_margin')
        self.clear_margin.connect("clicked", self.clear_settings)
        self.clear_y_pos = self.ui.get_object('clear_y_pos')
        self.clear_y_pos.connect("clicked", self.clear_settings)
        self.clear_opacity = self.ui.get_object('clear_opacity')
        self.clear_opacity.connect("clicked", self.clear_settings)
        self.clear_fix_position = self.ui.get_object('clear_fix_position')
        self.clear_fix_position.connect("clicked", self.clear_settings)
        self.clear_sticky = self.ui.get_object('clear_sticky')
        self.clear_sticky.connect("clicked", self.clear_settings)

        # View
        self.switch_show_block_today = self.ui.get_object('switch_show_block_today')
        self.switch_show_block_today.connect("notify::active", self.save_settings)
        self.spinbutton_block_today_left = self.ui.get_object('spinbutton_block_today_left')
        self.spinbutton_block_today_left.connect("value-changed", self.save_settings)
        self.switch_show_block_tomorrow = self.ui.get_object('switch_show_block_tomorrow')
        self.switch_show_block_tomorrow.connect("notify::active", self.save_settings)
        self.spinbutton_block_tomorrow_left = self.ui.get_object('spinbutton_block_tomorrow_left')
        self.spinbutton_block_tomorrow_left.connect("value-changed", self.save_settings)
        self.switch_show_block_wind_direct = self.ui.get_object('switch_show_block_wind_direct')
        self.switch_show_block_wind_direct.connect("notify::active", self.save_settings)
        self.spinbutton_block_wind_direct_left = self.ui.get_object('spinbutton_block_wind_direct_left')
        self.spinbutton_block_wind_direct_left.connect("value-changed", self.save_settings)
        self.switch_wind_direct_small = self.ui.get_object('switch_wind_direct_small')
        self.switch_wind_direct_small.connect("notify::active", self.save_settings)
        self.spinbutton_angel = self.ui.get_object('spinbutton_angel')
        self.spinbutton_angel.connect("value-changed", self.save_settings)
        self.switch_show_block_add_info = self.ui.get_object('switch_show_block_add_info')
        self.switch_show_block_add_info.connect("notify::active", self.save_settings)
        self.spinbutton_block_add_info_left = self.ui.get_object('spinbutton_block_add_info_left')
        self.spinbutton_block_add_info_left.connect("value-changed", self.save_settings)
        self.spinbutton_n = self.ui.get_object('spinbutton_n')
        self.spinbutton_n.connect("value-changed", self.save_settings)
        self.switch_show_time_receive = self.ui.get_object('switch_show_time_receive')
        self.switch_show_time_receive.connect("notify::active", self.save_settings)
        self.combobox_show_splash_screen = self.ui.get_object('combobox_show_splash_screen')
        self.combobox_show_splash_screen.connect("changed", self.save_settings)
        self.spinbutton_max_try_show = self.ui.get_object('spinbutton_max_try_show')
        self.spinbutton_max_try_show.connect("value-changed", self.save_settings)
        self.liststore2 = self.ui.get_object('liststore2')


        self.clear_show_block_today = self.ui.get_object('clear_show_block_today')
        self.clear_show_block_today.connect("clicked", self.clear_settings)
        self.clear_block_today_left = self.ui.get_object('clear_block_today_left')
        self.clear_block_today_left.connect("clicked", self.clear_settings)
        self.clear_show_block_tomorrow = self.ui.get_object('clear_show_block_tomorrow')
        self.clear_show_block_tomorrow.connect("clicked", self.clear_settings)
        self.clear_block_tomorrow_left = self.ui.get_object('clear_block_tomorrow_left')
        self.clear_block_tomorrow_left.connect("clicked", self.clear_settings)
        self.clear_show_block_wind_direct = self.ui.get_object('clear_show_block_wind_direct')
        self.clear_show_block_wind_direct.connect("clicked", self.clear_settings)
        self.clear_block_wind_direct_left = self.ui.get_object('clear_block_wind_direct_left')
        self.clear_block_wind_direct_left.connect("clicked", self.clear_settings)
        self.clear_wind_direct_small = self.ui.get_object('clear_wind_direct_small')
        self.clear_wind_direct_small.connect("clicked", self.clear_settings)
        self.clear_angel = self.ui.get_object('clear_angel')
        self.clear_angel.connect("clicked", self.clear_settings)
        self.clear_show_block_add_info = self.ui.get_object('clear_show_block_add_info')
        self.clear_show_block_add_info.connect("clicked", self.clear_settings)
        self.clear_block_add_info_left = self.ui.get_object('clear_block_add_info_left')
        self.clear_block_add_info_left.connect("clicked", self.clear_settings)
        self.clear_n = self.ui.get_object('clear_n')
        self.clear_n.connect("clicked", self.clear_settings)
        self.clear_show_time_receive = self.ui.get_object('clear_show_time_receive')
        self.clear_show_time_receive.connect("clicked", self.clear_settings)
        self.clear_show_splash_screen = self.ui.get_object('clear_show_splash_screen')
        self.clear_show_splash_screen.connect("clicked", self.clear_settings)
        self.clear_max_try_show = self.ui.get_object('clear_max_try_show')
        self.clear_max_try_show.connect("clicked", self.clear_settings)

        # Appearance
        self.fontbutton_font = self.ui.get_object('fontbutton_font')
        self.fontbutton_font.connect("font-set", self.set_font)
        self.colorbutton_color_text = self.ui.get_object('colorbutton_color_text')
        self.colorbutton_color_text.connect("color-set", self.set_color)
        self.colorbutton_color_text_week = self.ui.get_object('colorbutton_color_text_week')
        self.colorbutton_color_text_week.connect("color-set", self.set_color)
        self.colorbutton_color_shadow = self.ui.get_object('colorbutton_color_shadow')
        self.colorbutton_color_shadow.connect("color-set", self.set_color)
        self.colorbutton_color_high_wind = self.ui.get_object('colorbutton_color_high_wind')
        self.colorbutton_color_high_wind.connect("color-set", self.set_color)
        self.colorbutton_color_bg = self.ui.get_object('colorbutton_color_bg')
        self.colorbutton_color_bg.connect("color-set", self.set_color)
        self.switch_draw_shadow = self.ui.get_object('switch_draw_shadow')
        self.switch_draw_shadow.connect("notify::active", self.save_settings)
        self.spinbutton_high_wind = self.ui.get_object('spinbutton_high_wind')
        self.spinbutton_high_wind.connect("value-changed", self.save_settings)
        self.switch_show_bg_png = self.ui.get_object('switch_show_bg_png')
        self.switch_show_bg_png.connect("notify::active", self.save_settings)
        self.spinbutton_r = self.ui.get_object('spinbutton_r')
        self.spinbutton_r.connect("value-changed", self.save_settings)

        self.combobox_icons_name = self.ui.get_object('combobox_icons_name')
        self.combobox_icons_name.connect("changed", self.set_icon_bg)
        self.liststore3 = self.ui.get_object('liststore3')
        self.combobox_bg_custom = self.ui.get_object('combobox_bg_custom')
        self.combobox_bg_custom.connect("changed", self.set_icon_bg)
        self.liststore4 = self.ui.get_object('liststore4')


        self.clear_font = self.ui.get_object('clear_font')
        self.clear_font.connect("clicked", self.clear_settings)
        self.clear_color_text = self.ui.get_object('clear_color_text')
        self.clear_color_text.connect("clicked", self.clear_settings)
        self.clear_color_text_week = self.ui.get_object('clear_color_text_week')
        self.clear_color_text_week.connect("clicked", self.clear_settings)
        self.clear_color_shadow = self.ui.get_object('clear_color_shadow')
        self.clear_color_shadow.connect("clicked", self.clear_settings)
        self.clear_color_high_wind = self.ui.get_object('clear_color_high_wind')
        self.clear_color_high_wind.connect("clicked", self.clear_settings)
        self.clear_color_bg = self.ui.get_object('clear_color_bg')
        self.clear_color_bg.connect("clicked", self.clear_settings)
        self.clear_draw_shadow = self.ui.get_object('clear_draw_shadow')
        self.clear_draw_shadow.connect("clicked", self.clear_settings)
        self.clear_high_wind = self.ui.get_object('clear_high_wind')
        self.clear_high_wind.connect("clicked", self.clear_settings)
        self.clear_show_bg_png = self.ui.get_object('clear_show_bg_png')
        self.clear_show_bg_png.connect("clicked", self.clear_settings)
        self.clear_r = self.ui.get_object('clear_r')
        self.clear_r.connect("clicked", self.clear_settings)
        self.clear_icons_name = self.ui.get_object('clear_icons_name')
        self.clear_icons_name.connect("clicked", self.clear_settings)
        self.clear_bg_custom = self.ui.get_object('clear_bg_custom')
        self.clear_bg_custom.connect("clicked", self.clear_settings)
        
        if WIN:
            self.clear_delay_start_time.hide()
            self.spinbutton_delay_start_time.hide()
            self.label_delay_start_time.hide()

        self.button_close = self.ui.get_object('button_close')
        self.button_close.connect("clicked", self.close_window)

        self.window1.connect("delete_event", self.close_window)
        self.window1.show()

    def load_config_into_form(self):
        global state_lock
        state_lock = True

        self.liststore1.clear()
        self.liststore1.append([_('Never')])
        self.liststore1.append([_('Only at start')])
        self.liststore1.append([_('Always')])

        self.liststore2.clear()
        self.liststore2.append([_('No')])
        self.liststore2.append([_('Only background')])
        self.liststore2.append([_('Yes')])

        self.load(self.spinbutton_upd_time)
        self.load(self.switch_t_feel)
        self.load(self.switch_fix_BadDrawable)
        self.load(self.spinbutton_x_pos)
        self.load(self.spinbutton_y_pos)
        self.load(self.spinbutton_margin)
        self.load(self.spinbutton_opacity)
        self.load(self.switch_fix_position)
        self.load(self.switch_sticky)
        self.load(self.spinbutton_block_today_left)
        self.load(self.switch_show_block_today)
        self.load(self.spinbutton_block_tomorrow_left)
        self.load(self.switch_show_block_tomorrow)
        self.load(self.spinbutton_block_wind_direct_left)
        self.load(self.switch_show_block_wind_direct)
        self.load(self.spinbutton_angel)
        self.load(self.switch_wind_direct_small)
        self.load(self.spinbutton_block_add_info_left)
        self.load(self.switch_show_block_add_info)
        self.load(self.spinbutton_n)
        self.load(self.switch_show_time_receive)
        self.load(self.combobox_check_for_updates)
        self.load(self.combobox_show_splash_screen)
        self.load(self.spinbutton_max_try_show)
        self.fontbutton_font.set_font_name(gw_config_set['font'])
        self.load(self.colorbutton_color_text)
        self.load(self.colorbutton_color_text_week)
        self.load(self.colorbutton_color_shadow)
        self.load(self.colorbutton_color_high_wind)
        self.load(self.colorbutton_color_bg)
        self.load(self.switch_draw_shadow)
        self.load(self.spinbutton_high_wind)
        self.load(self.switch_show_bg_png)
        self.load(self.spinbutton_r)
        self.load(self.spinbutton_delay_start_time)

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

        if autorun.exists("gis-weather"):
            self.switch_autostart.set_active(True)

        self.liststore5.clear()
        for i in range(len(available_lang)):
            try:
                self.liststore5.append([dict_app_lang[available_lang[i]]])
            except:
                self.liststore5.append([available_lang[i]])
            if available_lang[i] == gw_config_set['app_lang']:
                self.combobox_app_lang.set_active(i)
        self.liststore6.clear()
        for i in range(len(weather_lang_list)):
            try:
                self.liststore6.append([dict_weather_lang[weather_lang_list[i]]])
            except:
                self.liststore6.append([weather_lang_list[i]])
            if weather_lang_list[i] == gw_config_set['weather_lang']:
                self.combobox_weather_lang.set_active(i)

        state_lock = False

    def load(self, widget):
        w_type = widget.get_name()
        w_name = Gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        if w_type == 'GtkSpinButton':
            widget.set_value(gw_config_set[name])
        else:
            if w_type == 'GtkColorButton':
                c = gw_config_set[name]
                color = Gdk.Color(int(c[0]*65535), int(c[1]*65535), int(c[2]*65535))
                widget.set_color(color)
                widget.set_alpha(int(c[3]*65535))
            else:
                widget.set_active(gw_config_set[name])


    def close_window(self, widget, data = None):
        self.window1.hide()
        Gtk.main_quit()

    def save_settings(self, widget, event=None):
        if state_lock:
            return
        global gw_config_set
        value = None
        w_type = widget.get_name()
        w_name = Gtk.Buildable.get_name(widget)
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
        if name == 'delay_start_time':
            if WIN:
                autorun.add("gis-weather", os.path.join(work_path, 'gis-weather.exe'))
            else:
                autorun.add("gis-weather", os.path.join(work_path, 'gis-weather.py'), gw_config_set['delay_start_time'])

    def clear_settings(self, widget):
        global gw_config_set
        w_name = Gtk.Buildable.get_name(widget)
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
        font_desc = Pango.FontDescription(self.fontbutton_font.get_font_name())
        font = font_desc.get_family()
        gw_config_set['font'] = font
        Save_Config()
        drawing_area_set.redraw(False, False, load_config = True)

    def set_icon_bg(self, widget):
        if state_lock:
            return
        global gw_config_set
        w_name = Gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        i = widget.get_active()
        if name == 'icons_name':
            gw_config_set[name] = icons_list_set[i]
        else:
            gw_config_set[name] = backgrounds_list_set[i]
        Save_Config()
        drawing_area_set.redraw(False, False, load_config = True)

    def set_weather_lang(self, widget):
        if state_lock:
            return
        global gw_config_set
        w_name = Gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        i = widget.get_active()
        gw_config_set[name] = weather_lang_list[i]
        Save_Config()
        drawing_area_set.redraw(False, True, load_config = True)

    def set_app_lang(self, widget):
        if state_lock:
            return
        global gw_config_set
        w_name = Gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        i = widget.get_active()
        gw_config_set[name] = available_lang[i]
        Save_Config()
        localization.set()
        self.dict_o = localization.translate_ui(self.list_o, self.dict_o)
        self.window1.set_title(_('Preferences')+' Gis Weather')
        self.load_config_into_form()
        drawing_area_set.redraw(False, False, load_config = True)


    def set_color(self, widget):
        if state_lock:
            return
        global gw_config_set
        w_name = Gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        alpha = (widget.get_alpha()*100)/65535.0
        alpha = alpha/100.0
        color = widget.get_color()
        gw_config_set[name] = (color.red_float, color.green_float, color.blue_float, alpha)
        Save_Config()
        drawing_area_set.redraw(False, False, load_config = True)

    def set_autorun(self, widget, event):
        if state_lock:
            return
        if widget.get_active() == True:
            if WIN:
                autorun.add("gis-weather", os.path.join(work_path, 'gis-weather.exe'))
            else:
                autorun.add("gis-weather", os.path.join(work_path, 'gis-weather.py'), gw_config_set['delay_start_time'])
        else:
            autorun.remove("gis-weather")

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
    Gtk.main()
