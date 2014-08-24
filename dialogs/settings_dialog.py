#!/usr/bin/env python3

from gi.repository import Gtk, Pango, Gdk
from utils import autorun, localization, desktop
import os
import json
import sys
from services import data
from services.data import services_list
import re

if sys.platform.startswith("win"):
    WIN = True
else:
    WIN = False

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')
# if WIN:
#     CONFIG_PATH = CONFIG_PATH.decode(sys.getfilesystemencoding())

work_path = os.path.abspath(os.path.dirname(__file__))
# if WIN:
#     work_path = work_path.decode(sys.getfilesystemencoding())

gw_config_default_set = {}
gw_config_set = {}
drawing_area_set = None
state_lock = True
App_gw = None
icons_list_set = []
backgrounds_list_set = []
BGS_PATH_SET = None
ICONS_PATH_SET = None
service_set = None
dict_weather_lang = None
weather_lang_list = None

dict_app_lang = {
    'auto': 'Auto',
    'en': 'English'
}

for root, dirs, files in os.walk(os.path.join(os.path.split(work_path)[0], 'po')):
    break
files.remove('README.md')
for item in files:
    if item[-2:] == 'po':
        f = open(os.path.join(root, item), 'rb')
        l = f.read().decode(encoding='UTF-8')
        language = re.findall('"Language: (.*)"', l)
        dict_app_lang[item.split('_')[-1][:-3]] = language[0][:-2]

# find all available lang
available_lang = ['auto', 'en']
for root, dirs, files in os.walk(os.path.join(os.path.split(work_path)[0], 'i18n')):
    break
dirs.sort()
available_lang.extend(dirs)

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
        self.label_add_icon = self.ui.get_object('label_add_icon')
        self.switch_add_icon = self.ui.get_object('switch_add_icon')
        self.switch_add_icon.connect("notify::active", self.set_desktop)
        self.combobox_service = self.ui.get_object('combobox_service')
        self.combobox_service.connect("changed", self.set_service)
        self.liststore8 = self.ui.get_object('liststore8')
        self.button_refresh = self.ui.get_object('button_refresh')
        self.button_refresh.connect("clicked", self.refresh)

        
        self.clear_upd_time = self.ui.get_object('clear_upd_time')
        self.clear_upd_time.connect("clicked", self.clear_settings)
        self.clear_fix_BadDrawable = self.ui.get_object('clear_fix_BadDrawable')
        self.clear_fix_BadDrawable.connect("clicked", self.clear_settings)
        self.clear_check_for_updates = self.ui.get_object('clear_check_for_updates')
        self.clear_check_for_updates.connect("clicked", self.clear_settings)
        self.clear_delay_start_time = self.ui.get_object('clear_delay_start_time')
        self.clear_delay_start_time.connect("clicked", self.clear_settings)


        # Units
        self.combobox_t_scale = self.ui.get_object('combobox_t_scale')
        self.combobox_t_scale.connect("changed", self.save_settings)
        self.liststore7 = self.ui.get_object('liststore7')
        self.switch_t_feel = self.ui.get_object('switch_t_feel')
        self.switch_t_feel.connect("notify::active", self.save_settings)
        self.combobox_wind_units = self.ui.get_object('combobox_wind_units')
        self.combobox_wind_units.connect("changed", self.save_settings)
        self.liststore9 = self.ui.get_object('liststore9')
        self.combobox_press_units = self.ui.get_object('combobox_press_units')
        self.combobox_press_units.connect("changed", self.save_settings)
        self.liststore10 = self.ui.get_object('liststore10')

        self.clear_t_scale = self.ui.get_object('clear_t_scale')
        self.clear_t_scale.connect("clicked", self.clear_settings)
        self.clear_t_feel = self.ui.get_object('clear_t_feel')
        self.clear_t_feel.connect("clicked", self.clear_settings)
        self.clear_wind_units = self.ui.get_object('clear_wind_units')
        self.clear_wind_units.connect("clicked", self.clear_settings)
        self.clear_press_units = self.ui.get_object('clear_press_units')
        self.clear_press_units.connect("clicked", self.clear_settings)


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
        self.spinbutton_scale = self.ui.get_object('spinbutton_scale')
        self.spinbutton_scale.connect("value-changed", self.save_settings)


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
        self.clear_scale = self.ui.get_object('clear_scale')
        self.clear_scale.connect("clicked", self.clear_settings)

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
        self.switch_show_chance_of_rain = self.ui.get_object('switch_show_chance_of_rain')
        self.switch_show_chance_of_rain.connect("notify::active", self.save_settings)
        self.combobox_show_splash_screen = self.ui.get_object('combobox_show_splash_screen')
        self.combobox_show_splash_screen.connect("changed", self.save_settings)
        self.spinbutton_max_try_show = self.ui.get_object('spinbutton_max_try_show')
        self.spinbutton_max_try_show.connect("value-changed", self.save_settings)
        self.liststore2 = self.ui.get_object('liststore2')
        self.spinbutton_block_now_left = self.ui.get_object('spinbutton_block_now_left')
        self.spinbutton_block_now_left.connect("value-changed", self.save_settings)


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
        self.clear_show_chance_of_rain = self.ui.get_object('clear_show_chance_of_rain')
        self.clear_show_chance_of_rain.connect("clicked", self.clear_settings)
        self.clear_show_splash_screen = self.ui.get_object('clear_show_splash_screen')
        self.clear_show_splash_screen.connect("clicked", self.clear_settings)
        self.clear_max_try_show = self.ui.get_object('clear_max_try_show')
        self.clear_max_try_show.connect("clicked", self.clear_settings)
        self.clear_block_now_left = self.ui.get_object('clear_block_now_left')
        self.clear_block_now_left.connect("clicked", self.clear_settings)

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
        self.frame_image = self.ui.get_object('frame_image')
        self.frame_not_image = self.ui.get_object('frame_not_image')

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


        # Indicator
        self.combobox_show_indicator = self.ui.get_object('combobox_show_indicator')
        self.combobox_show_indicator.connect("changed", self.save_settings)
        self.liststore11 = self.ui.get_object('liststore11')
        self.combobox_indicator_is_appindicator = self.ui.get_object('combobox_indicator_is_appindicator')
        self.combobox_indicator_is_appindicator.connect("changed", self.save_settings)
        self.liststore12 = self.ui.get_object('liststore12')
        self.combobox_indicator_icons_name = self.ui.get_object('combobox_indicator_icons_name')
        self.combobox_indicator_icons_name.connect("changed", self.set_icon_bg)
        self.liststore13 = self.ui.get_object('liststore13')
        self.switch_indicator_draw_shadow = self.ui.get_object('switch_indicator_draw_shadow')
        self.switch_indicator_draw_shadow.connect("notify::active", self.save_settings)
        self.fontbutton_indicator_font = self.ui.get_object('fontbutton_indicator_font')
        self.fontbutton_indicator_font.connect("font-set", self.set_font)
        self.colorbutton_indicator_color_text = self.ui.get_object('colorbutton_indicator_color_text')
        self.colorbutton_indicator_color_text.connect("color-set", self.set_color)
        self.colorbutton_indicator_color_shadow = self.ui.get_object('colorbutton_indicator_color_shadow')
        self.colorbutton_indicator_color_shadow.connect("color-set", self.set_color)
        self.frame_status_icon = self.ui.get_object('frame_status_icon')
        self.spinbutton_indicator_top = self.ui.get_object('spinbutton_indicator_top')
        self.spinbutton_indicator_top.connect("value-changed", self.save_settings)
        self.spinbutton_indicator_width = self.ui.get_object('spinbutton_indicator_width')
        self.spinbutton_indicator_width.connect("value-changed", self.save_settings)
        self.frame_app_indicator = self.ui.get_object('frame_app_indicator')
        self.spinbutton_app_indicator_size = self.ui.get_object('spinbutton_app_indicator_size')
        self.spinbutton_app_indicator_size.connect("value-changed", self.save_settings)
        self.switch_app_indicator_fix_size = self.ui.get_object('switch_app_indicator_fix_size')
        self.switch_app_indicator_fix_size.connect("notify::active", self.save_settings)

        self.clear_show_indicator = self.ui.get_object('clear_show_indicator')
        self.clear_show_indicator.connect("clicked", self.clear_settings)
        self.clear_indicator_draw_shadow = self.ui.get_object('clear_indicator_draw_shadow')
        self.clear_indicator_draw_shadow.connect("clicked", self.clear_settings)
        self.clear_indicator_font = self.ui.get_object('clear_indicator_font')
        self.clear_indicator_font.connect("clicked", self.clear_settings)
        self.clear_indicator_top = self.ui.get_object('clear_indicator_top')
        self.clear_indicator_top.connect("clicked", self.clear_settings)
        self.clear_indicator_width = self.ui.get_object('clear_indicator_width')
        self.clear_indicator_width.connect("clicked", self.clear_settings)
        self.clear_app_indicator_size = self.ui.get_object('clear_app_indicator_size')
        self.clear_app_indicator_size.connect("clicked", self.clear_settings)
        self.clear_app_indicator_fix_size = self.ui.get_object('clear_app_indicator_fix_size')
        self.clear_app_indicator_fix_size.connect("clicked", self.clear_settings)
        
        if WIN:
            self.clear_delay_start_time.hide()
            self.spinbutton_delay_start_time.hide()
            self.label_delay_start_time.hide()

            self.switch_add_icon.hide()
            self.label_add_icon.hide()

        self.button_close = self.ui.get_object('button_close')
        self.button_close.connect("clicked", self.close_window)

        self.window1.connect("delete_event", self.close_window)
        self.window1.show()

    def load_config_into_form(self):
        global state_lock
        state_lock = True
        wind_units_list = [_('m/s'), _('km/h'), _('mph')]
        press_units_list = [_('mmHg'), _('inHg'), _('hPa')]

        self.liststore1.clear()
        self.liststore1.append([_('Never')])
        self.liststore1.append([_('Only at start')])
        self.liststore1.append([_('Always')])

        self.liststore2.clear()
        self.liststore2.append([_('No')])
        self.liststore2.append([_('Only background')])
        self.liststore2.append([_('Yes')])

        self.liststore7.clear()
        self.liststore7.append(['°C'])
        self.liststore7.append(['°F'])
        self.liststore7.append(['K'])

        self.liststore11.clear()
        self.liststore11.append(['Widget only'])
        self.liststore11.append(['Indicator only'])
        self.liststore11.append(['Widget + Indicator'])

        self.liststore12.clear()
        self.liststore12.append(['Gtk.StatusIcon'])
        self.liststore12.append(['AppIndicator3'])

        self.liststore9.clear()
        for i in wind_units_list:
            self.liststore9.append([i])

        self.liststore10.clear()
        for i in press_units_list:
            self.liststore10.append([i])

        self.liststore8.clear()
        for i in range(len(services_list)):
            self.liststore8.append([services_list[i]])
        self.combobox_service.set_active(service_set)

        self.load(self.combobox_wind_units)
        self.load(self.combobox_press_units)
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
        self.load(self.switch_show_chance_of_rain)
        self.load(self.combobox_check_for_updates)
        self.load(self.combobox_show_splash_screen)
        self.load(self.combobox_t_scale)
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
        self.load(self.spinbutton_block_now_left)
        self.load(self.combobox_show_indicator)
        self.load(self.combobox_indicator_is_appindicator)
        self.load(self.switch_indicator_draw_shadow)
        self.fontbutton_indicator_font.set_font_name(gw_config_set['indicator_font']+' '+str(gw_config_set['indicator_font_size']))
        self.load(self.colorbutton_indicator_color_text)
        self.load(self.colorbutton_indicator_color_shadow)
        self.load(self.spinbutton_indicator_top)
        self.load(self.spinbutton_indicator_width)
        self.load(self.spinbutton_scale)
        self.load(self.spinbutton_app_indicator_size)
        self.load(self.switch_app_indicator_fix_size)

        if gw_config_set['show_bg_png'] == True:
            self.frame_not_image.hide()
        else:
            self.frame_image.hide()

        if gw_config_set['indicator_is_appindicator'] == 0:
            self.frame_app_indicator.hide()
        else:
            self.frame_status_icon.hide()

        self.liststore3.clear()
        for i in range(len(icons_list_set)):
            author = ""
            if os.path.exists(os.path.join(ICONS_PATH_SET, icons_list_set[i], 'author')):
                f = open(os.path.join(ICONS_PATH_SET, icons_list_set[i], 'author'),"r")
                author = "\n"+"<i>"+_('Author')+": "+f.readline().strip()+"</i>"
            self.liststore3.append(["<b>"+icons_list_set[i]+"</b>"+author])
            if icons_list_set[i] == gw_config_set['icons_name']: 
                self.combobox_icons_name.set_active(i)

        self.liststore13.clear()
        for i in range(len(icons_list_set)):
            author = ""
            if os.path.exists(os.path.join(ICONS_PATH_SET, icons_list_set[i], 'author')):
                f = open(os.path.join(ICONS_PATH_SET, icons_list_set[i], 'author'),"r")
                author = "\n"+"<i>"+_('Author')+": "+f.readline().strip()+"</i>"
            self.liststore13.append(["<b>"+icons_list_set[i]+"</b>"+author])
            if icons_list_set[i] == gw_config_set['indicator_icons_name']: 
                self.combobox_indicator_icons_name.set_active(i)

        self.liststore4.clear()
        for i in range(len(backgrounds_list_set)):
            author = ""
            if os.path.exists(os.path.join(BGS_PATH_SET, backgrounds_list_set[i], 'author')):
                f = open(os.path.join(BGS_PATH_SET, backgrounds_list_set[i], 'author'),"r")
                author = "\n"+"<i>"+_('Author')+": "+f.readline().strip()+"</i>"
            self.liststore4.append(["<b>"+backgrounds_list_set[i]+"</b>"+author])
            if backgrounds_list_set[i] == gw_config_set['bg_custom']: 
                self.combobox_bg_custom.set_active(i)

        if autorun.exists("gis-weather"):
            self.switch_autostart.set_active(True)

        if desktop.main_exists():
            self.switch_add_icon.hide()
            self.label_add_icon.hide()
        else:
            if desktop.exists():
                self.switch_add_icon.set_active(True)

        self.liststore5.clear()
        for i in range(len(available_lang)):
            try:
                self.liststore5.append([dict_app_lang[available_lang[i]]])
            except:
                self.liststore5.append([available_lang[i]])
            if available_lang[i] == gw_config_set['app_lang']:
                self.combobox_app_lang.set_active(i)
        self.load_available_service_lang(service_set)

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
            if name in ('opacity', 'scale'):
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
                autorun.add("gis-weather", os.path.join(os.path.split(work_path)[0], 'gis-weather.exe'))
            else:
                autorun.add("gis-weather", os.path.join(os.path.split(work_path)[0], 'gis-weather.py'), gw_config_set['delay_start_time'])
        if name == 'indicator_is_appindicator':
            if value:
                self.frame_status_icon.hide()
                self.frame_app_indicator.show()
            else:
                self.frame_status_icon.show()
                self.frame_app_indicator.hide()

        if name == 'show_bg_png':
            if value:
                self.frame_image.show()
                self.frame_not_image.hide()
            else:
                self.frame_image.hide()
                self.frame_not_image.show()

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
        font_desc = Pango.FontDescription(widget.get_font_name())
        font = font_desc.get_family()
        w_name = Gtk.Buildable.get_name(widget)
        w_name = w_name.split('_')
        name = '_'.join(w_name[1:])
        if name == 'font':
            gw_config_set['font'] = font
        if name == 'indicator_font':
            gw_config_set['indicator_font'] = font
            gw_config_set['indicator_font_size'] = font_desc.get_size()//Pango.SCALE
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
        if name == 'bg_custom':
            gw_config_set[name] = backgrounds_list_set[i]
        if name == 'indicator_icons_name':
            gw_config_set[name] = icons_list_set[i]
        Save_Config()
        drawing_area_set.redraw(False, False, load_config = True)

    def set_weather_lang(self, widget):
        if state_lock:
            return
        global gw_config_set
        i = widget.get_active()
        gw_config_set['weather_lang'] = weather_lang_list[i]
        Save_Config()
        #drawing_area_set.redraw(False, True, load_config = True)

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
                autorun.add("gis-weather", os.path.join(os.path.split(work_path)[0], 'gis-weather.exe'))
            else:
                autorun.add("gis-weather", os.path.join(os.path.split(work_path)[0], 'gis-weather.py'), gw_config_set['delay_start_time'])
        else:
            autorun.remove("gis-weather")

    def set_desktop(self, widget, event):
        if state_lock:
            return
        if widget.get_active() == True:
            desktop.create(os.path.join(os.path.split(work_path)[0], 'gis-weather.py'))
        else:
            desktop.remove()

    def set_service(self, widget):
        if state_lock:
            return
        global gw_config_set
        i = widget.get_active()
        gw_config_set['service'] = i
        try:
            city_list = gw_config_set[data.get_city_list(i)]
        except:
            city_list = []
        if city_list:
            gw_config_set['city_id'] = city_list[0].split(';')[0]
        else:
            gw_config_set['city_id'] = 0
        gw_config_set['max_days'] = data.get_max_days(i)
        if gw_config_set['n'] > gw_config_set['max_days']:
            gw_config_set['n'] = gw_config_set['max_days']
        self.spinbutton_n.set_value(gw_config_set['n'])
        self.spinbutton_n.set_range(3, gw_config_set['max_days'])
        Save_Config()
        self.load_available_service_lang(i)

    def load_available_service_lang(self, i):
        global dict_weather_lang, weather_lang_list
        url, example, code, dict_weather_lang, weather_lang_list = data.get(gw_config_set['service'])
        self.liststore6.clear()
        for i in range(len(weather_lang_list)):
            try:
                self.liststore6.append([dict_weather_lang[weather_lang_list[i]]])
            except:
                if weather_lang_list[i] != '':
                    self.liststore6.append([weather_lang_list[i]])
            if weather_lang_list[i] == gw_config_set['weather_lang']:
                self.combobox_weather_lang.set_active(i)
            if self.combobox_weather_lang.get_active() == -1:
                self.combobox_weather_lang.set_active(0)

    def refresh(self, widget):
        drawing_area_set.redraw(False, True, load_config = True)




def main(gw_config_default, gw_config, drawing_area, app_gw, icons_list, backgrounds_list, ICONS_PATH, BGS_PATH, service):
    global gw_config_default_set, gw_config_set, drawing_area_set, App_gw, icons_list_set, backgrounds_list_set, ICONS_PATH_SET, BGS_PATH_SET, service_set
    for i in gw_config_default.keys():
        gw_config_default_set[i] = gw_config_default[i]
    for i in gw_config.keys():
        gw_config_set[i] = gw_config[i]

    ICONS_PATH_SET = ICONS_PATH
    BGS_PATH_SET = BGS_PATH
    service_set = service
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
