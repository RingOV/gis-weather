#!/usr/bin/python3
#
#  gis_weather.py
v = '0.7.7.8'
#  Copyright (C) 2013-2015 Alexander Koltsov <ringov@mail.ru>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

print('Gis Weather '+v)

import sys
if sys.platform.startswith("win"):
    WIN = True
else:
    WIN = False

from utils import instance
if not WIN:
    try:
        instance.set_procname(b'gis-weather')
        multInstances = True
    except:
        multInstances = False
else:
    multInstances = False
    
from utils import localization
localization.set()

if not multInstances:
    print(_('Running multiple instances is not supported'))

import argparse
parser = argparse.ArgumentParser(description='Customizable weather widget')
parser.add_argument('-i', '--instances', nargs=1, metavar='N', default=['0'],
                    help=_('number of instances'))
parser.add_argument('-v','--version', action='version', version='Gis Weather '+v)

args = parser.parse_args()

INSTANCE_NO = instance.count()

from gi.repository import Gtk, GObject, Pango, PangoCairo, Gdk, GdkPixbuf, GLib

try:
    from gi.repository import AppIndicator3
    HAS_INDICATOR=True
except:
    HAS_INDICATOR=False
    print('Not found gir1.2-appindicator3-0.1 (libappindicator3)')

try:
    from gi.repository import Rsvg
    HAS_RSVG=True
except:
    HAS_RSVG=False
    print('Not found gir1.2-rsvg-2.0 (librsvg)')

from dialogs import about_dialog, city_id_dialog, update_dialog, settings_dialog, help_dialog
from services import data
from utils import gw_menu, presets, date_convert, diff_versions, weather_vars
from utils.opener import urlopen
import cairo
import re
import os
import time
import math
from urllib.request import urlretrieve
import json
import subprocess
import gzip
import shutil

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')
CONFIG_PATH_FILE = os.path.join(CONFIG_PATH, instance.get_config_file())

def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)

make_dirs(CONFIG_PATH)
make_dirs(os.path.join(CONFIG_PATH, 'color_schemes'))
make_dirs(os.path.join(CONFIG_PATH, 'icons'))
make_dirs(os.path.join(CONFIG_PATH, 'backgrounds'))
make_dirs(os.path.join(CONFIG_PATH, 'presets'))

presets.save_to_file(CONFIG_PATH)

# Default values
gw_config_default = {
    'angel': 0,                        # angle of clockwise rotation in degrees 
    'city_id': 0,                      # location code
    'upd_time': 30,                    # Update by (in minutes) 
    'n': 7,                            # Display days
    'x_pos': 60,                       # left position
    'y_pos': 60,                       # top position
    't_feel': False,                   # temperature as feel
    'font': 'Sans',                    # font
    'color_text': (0, 0, 0, 1), #RGBa  # color text
    'color_text_week': (0.5, 0, 0, 1), # color weekend
    'weekend': 'Sa, Su',
    'color_bg': (0.8, 0.8, 0.8, 1),    # color background
    'color_shadow': (1, 1, 1, 0.7),    # color shadow
    'draw_shadow': True,               # draw shadow
    'opacity': 1,                      # opacity window
    'show_time_receive': True,         # time of receipt of weather 
    'show_block_wind_direct': True,    # block wind direct
    'block_wind_direct_left': -170,    # position
    'wind_direct_small': False,        # small block wind direct
    'show_block_add_info': True,       # block with additional information
    'block_add_info_left': 70,         # position
    'show_block_tomorrow': True,       # block with the weather for tomorrow
    'block_tomorrow_left': 180,        # position
    'show_block_today': True,          # block with the weather for today
    'block_today_left': -310,          # position
    'r': 0,                            # border radius
    'show_splash_screen': 2,           # splash creen 0 - no, 1 - only backdround, 2 - yes
    'max_try_show': 30,                # hide splash, 0 - show always
    'sticky': True,                    # on all desktops
    'show_bg_png': True,               # picture in background
    'bg_custom': 'Light50',            # this picture
    'margin': 20,                      # inside padding
    'high_wind': 10,                   # wind greater or equal to this value is highlighted (-1 do not allocate) 
    'color_high_wind': (0, 0, 0.6, 1), # color
    'icons_name': 'default',           # name folder with icon
    'fix_BadDrawable': False,           # if BadDrawable error
    'color_scheme_number': 0,
    'check_for_updates': 2,            # 0 - no, 1 - only when startup, 2 - always
    'fix_position': False,
    'app_lang': 'auto',
    'weather_lang': 'com',
    'delay_start_time': 0,
    'block_now_left': 0,
    't_scale': 0,                      # 0 - °C, 1 - °F, 2 - K
    'service': 'Gismeteo',
    'max_days': 12,
    'show_chance_of_rain': False,
    'wind_units': 0,
    'press_units': 0,
    'show_indicator': 0,               # 0 - widget only, 1 - indicator only, 2 - widget + indicator
    'indicator_is_appindicator': 'None',
    'indicator_icons_name': 'default',
    'indicator_font': 'Sans',
    'indicator_font_size': 9,
    'indicator_color_text': (0, 0, 0, 1),
    'indicator_color_shadow': (1, 1, 1, 0.7),
    'indicator_draw_shadow': True,
    'indicator_top': 0,
    'indicator_width': 30,
    'app_indicator_fix_size': False,
    'app_indicator_size': 22,
    'scale': 1,
    'instances_count': 1,
    'date_separator': 'default',
    'swap_d_and_m': False,
    'save_cur_temp': False,
    'save_cur_temp_add_scale': False,
    'show_indicator_text': True,
    # customizable options
    'preset_number':0,
    'bg_left': 0,
    'bg_top': 0,
    'bg_width': -1,
    'bg_height': -1,
    'icon_now_top': 0,
    'icon_now_left': 0,
    'icon_now_size': 0,
    'block_icons_left': 0,
    'block_icons_top': 0,
    'city_name_left': 0,
    'city_name_top': 0,
    'day_left': 0,
    'day_top': 0,
    't_now_left': 0,
    't_now_top': 0,
    't_now_size': 0,
    't_now_alignment': 'right',
    'text_now_left': 0,
    'text_now_top': 0,
    'height_fix': 0,
    'splash_icon_top': 0,
    'splash_version_top': 0,
    'block_wind_direct_small_left': 0,
    'block_today_top': 0,
    'block_tomorrow_top': 0,
    'block_wind_direct_small_top': 0,
    'splash_block_top': 0,
    'desc_style': 0 # 0 - Normal, 1 - Italic
}
gw_config = {}
for i in gw_config_default.keys():
    gw_config[i] = gw_config_default[i]

color_scheme = [
    {   'color_text': (0, 0, 0, 1), #RGBa    # text color
        'color_text_week': (0.5, 0, 0, 1),   # color weekend
        'color_shadow': (1, 1, 1, 0.7),      # color shadow
        'color_high_wind': (0, 0, 0.6, 1)    # color high wind
    },
    {   'color_text': (0.9, 0.9, 0.9, 1),    # text color
        'color_text_week': (1, 0.5, 0.5, 1), # color weekend
        'color_shadow': (0, 0, 0, 0.7),      # color shadow
        'color_high_wind': (0.5, 0.5, 1, 1)  # color high wind
    },
    {   'color_text': (0.2, 0.2, 0.2, 1),    # text color
        'color_text_week': (0.5, 0, 0, 1),   # color weekend
        'color_shadow': (0, 0, 0, 0),        # color shadow
        'color_high_wind': (0, 0, 0, 1)      # color high wind
    }
    ]

def create_variables():
    for i in gw_config.keys():
        globals()[i] = gw_config[i]

print (_('Configuration folder')+':\n    '+CONFIG_PATH_FILE)

def Save_Config():
    for i in gw_config.keys():
        try:
            gw_config[i] = globals()[i]
        except:
            pass
    json.dump(gw_config, open(CONFIG_PATH_FILE, "w"), sort_keys=True, indent=4, separators=(', ', ': '))

def Save_Color_Scheme(number = 0):
    json.dump(color_scheme[number], open(os.path.join(CONFIG_PATH, 'color_schemes', 'color_sheme_%s.json' %number), "w"), sort_keys=True, indent=4, separators=(', ', ': '))

for i in range(len(color_scheme)):
    if not os.path.exists(os.path.join(CONFIG_PATH, 'color_schemes', 'color_sheme_%s.json' %i)):
        Save_Color_Scheme(i)

def Load_Config():
    try:
        gw_config_loaded=json.load(open(CONFIG_PATH_FILE))
        for i in gw_config_loaded.keys():
            gw_config[i] = gw_config_loaded[i] # new values
    except:
        print ('\033[1;31m[!]\033[0m '+_('Error loading config file'))

    create_variables()

# first start, config missed
if not os.path.exists(CONFIG_PATH_FILE):
    if INSTANCE_NO == 0:
        create_variables()
        Save_Config()
    else:
        if INSTANCE_NO == 1:
            if os.path.exists(os.path.join(CONFIG_PATH, 'gw_config.json')):
                shutil.copy(os.path.join(CONFIG_PATH, 'gw_config.json'), CONFIG_PATH_FILE)
            else:
                create_variables()
                Save_Config()
        else:
            shutil.copy(os.path.join(CONFIG_PATH, 'gw_config%s.json'%str(INSTANCE_NO-1)), CONFIG_PATH_FILE)
# load config
Load_Config()
def Load_Color_Scheme(number = 0):
    try:
        scheme_loaded=json.load(open(os.path.join(CONFIG_PATH, 'color_schemes', 'color_sheme_%s.json' %number)))
        for i in scheme_loaded.keys():
            gw_config[i] = scheme_loaded[i]
        gw_config['color_scheme_number'] = number
    except:
        print ('\033[1;31m[!]\033[0m '+_('Error loading color scheme')+' # '+str(number))

    create_variables()
    

def Load_Preset(number = 0):
    try:
        preset_loaded=json.load(open(os.path.join(CONFIG_PATH, 'presets', 'preset_%s.json' %number)))
        for i in preset_loaded.keys():
            gw_config[i] = preset_loaded[i]
        gw_config['preset_number'] = number
    except:
        print ('\033[1;31m[!]\033[0m '+_('Error loading preset')+' # '+str(number))

    create_variables()

# ------------------------------------------------------------------------------

# path to gis-weather.py
APP_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))

if APP_PATH == '' or APP_PATH.startswith('.'):
    print (_('Enter full path to script'))
    print (_('Exit'))
    exit()

THEMES_PATH = os.path.join(APP_PATH, 'themes')
ICONS_PATH = os.path.join(THEMES_PATH, 'icons')
BGS_PATH = os.path.join(THEMES_PATH, 'backgrounds')
ICONS_USER_PATH = os.path.join(CONFIG_PATH, 'icons')
BGS_USER_PATH = os.path.join(CONFIG_PATH, 'backgrounds')

make_dirs(os.path.join(ICONS_USER_PATH, 'default', 'weather'))

if indicator_is_appindicator == 'None':
    if HAS_INDICATOR:
        indicator_is_appindicator = 1
    else:
        indicator_is_appindicator = 0
    Save_Config()
# additional variables
height = None
width = None
# cr = None
h_block = 95         
w_block = 80         
block_margin = 20 
keep_above = False
keep_below = False
err_connect = False
first_start = True
try_no = 0
splash = True
err = False
on_redraw = False
timer_bool = True
get_weather_bool = True
not_composited = False
if check_for_updates == 0:
    check_for_updates_local = False
else:
    check_for_updates_local = True
icons_list = []
backgrounds_list = []
show_time_receive_local = False
time_receive = None
ind = None
pix_path = None

t_scale_dict = {
    0: "°C",
    1: "°F",
    2: "K"
}
desc_list = (
    " Normal",
    " Italic"
)

# weather variables
weather = weather_vars.weather
# create variables
for i in weather.keys():
    globals()[i] = weather[i]

if int(args.instances[0]) != 0:
    instances_count = int(args.instances[0])
else:
    instances_count = 0

if INSTANCE_NO < instances_count:
    subprocess.Popen(['python3', os.path.join(APP_PATH, 'gis-weather.py'), '-i '+str(instances_count)])

def get_weather():
    global service, weather_lang
    if service not in data.services_list:
        service = data.services_list[0]
        weather_lang = data.get(service)[-1][0]
        Save_Config()
    if city_id == 0:
        if app.show_edit_dialog():
            Save_Config()
    if city_id == 0:
        return False
    else:
        return data.get_weather(service, weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name)

def check_updates():
    package = 'gz'
    if os.path.exists(os.path.join(APP_PATH, 'package')):
        f = open(os.path.join(APP_PATH, 'package'),"r")
        package = f.readline().strip()

    if package not in ('gz', 'deb', 'exe', 'rpm', 'aur', 'ppa'):
        print ('package = '+package)
        return False

    if package in ('aur', 'ppa'):
        global check_for_updates
        check_for_updates = 0
        Save_Config()
        return False

    print ('\033[34m>\033[0m '+_('Check for new version')+' '+'(%s)' % package)
    try:
        source = urlopen('http://sourceforge.net/projects/gis-weather/files/gis-weather/')
        source = source.decode(encoding='UTF-8')
    except:
        print ('\033[1;31m[!]\033[0m '+_('Unable to check for updates'))
        print ('-'*40)
        return False
    new_ver1 = re.findall('<a href="/projects/gis-weather/files/gis-weather/(.+)/"', source)
    new_ver = new_ver1[0].split('.')
    try:
        temp = urlopen('http://sourceforge.net/projects/gis-weather/files/gis-weather/%s/'%new_ver1[0])
        temp = temp.decode(encoding='UTF-8')
    except:
        print ('\033[1;31m[!]\033[0m '+_('Unable to check for updates'))
        print ('-'*40)
        return False
    temp_links = re.findall('http://sourceforge.net/projects/gis-weather/files/gis-weather/%s/(.+)/download'%new_ver1[0], temp)
    update_link = ''
    for i in range(len(temp_links)):
        if temp_links[i].split('.')[-1] == package:
            update_link = 'http://sourceforge.net/projects/gis-weather/files/gis-weather/%s/%s/download'%(new_ver1[0], temp_links[i])
            file_name = temp_links[i]
    if update_link == '':
        new_ver = [0, 0, 0, 0]
    new_v = None
    if diff_versions.diff(v.split('.'), new_ver):
        new_v = new_ver1[0]
    if new_v:
        print ('\033[34m>>>\033[0m '+_('New version available')+' '+str(new_v))
        print ('\033[34m>>>\033[0m '+str(update_link))
        print ('-'*40)
        global check_for_updates_local
        check_for_updates_local = False
        update_dialog.create(v, new_v, CONFIG_PATH, APP_PATH, update_link, file_name, package)
    else:
        print ('\033[34m>\033[0m '+_('You are using the latest version'))
        print ('-'*40)
        if check_for_updates == 1 and check_for_updates_local:
            check_for_updates_local = False

def screenshot():
    w = Gdk.get_default_root_window()
    if WIN:
        import ctypes
        user32 = ctypes.windll.user32
        left, top, width, height = 0, 0, user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    else:
        left, top, width, height = w.get_geometry()
    pb = Gdk.pixbuf_get_from_window(w,left,top,width,height)
    if (pb != None):
        try:
            pb.savev(os.path.join(CONFIG_PATH, "main_screenshot.png"),"png", (), ())
            print (_("Screenshot saved to")+' '+os.path.join(CONFIG_PATH, "main_screenshot.png"))
        except:
            print (">> Pixbuf.savev Error")
    else:
        print (_("Unable to get the screenshot"))

def crop_image(left, top, width, height):
    surface = cairo.ImageSurface.create_from_png(os.path.join(CONFIG_PATH, "main_screenshot.png"))
    pb = Gdk.pixbuf_get_from_surface(surface, left, top, int(width*scale), int(height*scale))
    try:
        pb.savev(os.path.join(CONFIG_PATH, "screenshot.png"),"png", (), ())
    except:
        print (">> Pixbuf.savev Error")

class Indicator:
    if indicator_is_appindicator and HAS_INDICATOR: # AppIndicator3
        def __init__(self):
            self.indicator = AppIndicator3.Indicator.new("gis-weather", "weather-clear", AppIndicator3.IndicatorCategory.APPLICATION_STATUS)
            if show_indicator:
                self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
                self.hiden = False
            else:
                self.indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
                self.hiden = True

        def set_label(self, text):
            self.indicator.set_label(text, '')

        def set_icon(self, icon):
            if app_indicator_fix_size:
                self.set_icon_fixed(icon, app_indicator_size)
            else:
                if icon[-4:] == 'svgz':
                    inF = gzip.open(icon, 'rb')
                    outF = open(os.path.join(CONFIG_PATH, 'cur_icon.svg'), 'wb')
                    outF.write(inF.read())
                    inF.close()
                    outF.close()
                    self.indicator.set_icon(os.path.join(CONFIG_PATH, 'cur_icon.svg'))
                else:
                    self.indicator.set_icon(icon)

        def set_icon_fixed(self, icon, size=None):
            if icon[-4:] == 'svgz':
                inF = gzip.open(icon, 'r')
                loader = GdkPixbuf.PixbufLoader()
                loader.write(inF.read())
                loader.close()
                inF.close()
                pixbuf = loader.get_pixbuf()
            else:
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(icon)
            if size:
                pixbuf = pixbuf.scale_simple(size,size,GdkPixbuf.InterpType.BILINEAR)
            try:
                pixbuf.savev(os.path.join(CONFIG_PATH, "cur_icon.png"),"png", (), ())
                self.indicator.set_icon(os.path.join(CONFIG_PATH, "cur_icon.png"))
            except:
                print (">> Pixbuf.savev Error")

        def set_menu(self, menu):
            self.indicator.set_menu(menu)

        def hide(self):
            if not self.hiden:
                self.indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)
                self.hiden = True

        def show(self):
            if self.hiden:
                self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
                self.indicator.set_menu(app.menu)
                self.hiden = False

    else:  # Gtk.StatusIcon
        def __init__(self):
            self.indicator = Gtk.StatusIcon()
            self.indicator_label = Gtk.StatusIcon()
            self.indicator.set_from_file(os.path.join(APP_PATH, "icon.png"))
            if show_indicator:
                self.indicator.set_visible(True)
                self.indicator_label.set_visible(True)
                self.hiden = False
            else:
                self.indicator.set_visible(False)
                self.indicator_label.set_visible(False)
                self.hiden = True
            
        def set_label(self, text):
            if show_indicator_text:
                self.indicator_label.set_visible(True)
                self.draw_text_to_png(self.indicator.get_size(), text)
                self.indicator_label.set_from_file(os.path.join(CONFIG_PATH, "text.png"))
            else:
                self.indicator_label.set_visible(False)

        def set_icon(self, icon):
            if icon[-4:] == 'svgz':
                inF = gzip.open(icon, 'rb')
                outF = open(os.path.join(CONFIG_PATH, 'cur_icon.svg'), 'wb')
                outF.write(inF.read())
                inF.close()
                outF.close()
                self.indicator.set_from_file(os.path.join(CONFIG_PATH, 'cur_icon.svg'))
            else:
                self.indicator.set_from_file(icon)

        def set_menu(self, menu):
            self.indicator.connect("popup-menu", self.popup_menu)
            self.indicator_label.connect("popup-menu", self.popup_menu)

        def popup_menu(self, icon, widget, time):
            app.create_menu(for_indicator=True)
            app.menu.popup(None, None, None, None, widget, time)

        def hide(self):
            if not self.hiden:
                self.indicator.set_visible(False)
                self.indicator_label.set_visible(False)
                self.hiden = True

        def show(self):
            if self.hiden:
                self.indicator.set_visible(True)
                self.indicator_label.set_visible(True)
                self.hiden = False

        def draw_text_to_png(self, HEIGHT, text):
            WIDTH = indicator_width

            surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, WIDTH, HEIGHT)
            self.cr = cairo.Context(surface)
            if indicator_draw_shadow:
                self.cr.set_source_rgba(indicator_color_shadow[0], indicator_color_shadow[1], indicator_color_shadow[2], indicator_color_shadow[3])
                self.draw_indicator_text(text, 1, indicator_top+HEIGHT//8+1, indicator_font, indicator_font_size, WIDTH)
            self.cr.set_source_rgba(indicator_color_text[0], indicator_color_text[1], indicator_color_text[2], indicator_color_text[3])
            self.draw_indicator_text(text, 0, indicator_top+HEIGHT//8, indicator_font, indicator_font_size, WIDTH)
            surface.write_to_png(os.path.join(CONFIG_PATH, "text.png"))

        def draw_indicator_text(self, text, x, y, font, size, width=200, alignment=Pango.Alignment.LEFT):
            self.cr.save()
            self.cr.translate(x, y)
            
            font_desc = Pango.FontDescription(font)
            font_desc.set_size(size * Pango.SCALE)

            self.p_layout = PangoCairo.create_layout(self.cr)
            self.p_layout.set_font_description(font_desc)
            self.p_layout.set_width(width * Pango.SCALE)
            self.p_layout.set_alignment(alignment)
            self.p_layout.set_markup(text)
            PangoCairo.show_layout(self.cr, self.p_layout)
            self.cr.restore()


class MyDrawArea(Gtk.DrawingArea):
    p_layout = None
    p_fdesc = None
    cr = None

    def __init__(self):
        self.timer = GLib.timeout_add(1000, self.redraw)
        GObject.GObject.__init__(self)
        self.set_app_paintable(True)
        self.connect('draw', self.expose)

    def splash_screen(self, cr, state = 0):
        if show_splash_screen == 0:
            return
        global try_no
        if max_try_show != 0 and try_no >= max_try_show:
            return
        self.draw_bg(cr, bg_left, bg_top, bg_width, bg_height)
        if show_splash_screen != 1:
            self.draw_scaled_image(cr, width/2 - 64, splash_block_top+height/2 - 128, os.path.join(APP_PATH, 'icon.png'), 128, 128)
            self.draw_text(cr, 'Gis Weather v ' + v, 0, splash_block_top+height/2 - 8, font+' Normal', 14, width, Pango.Alignment.CENTER)
            if state == 0:
                self.draw_text(cr, _('Getting weather...'), 0, splash_block_top+height/2 + 20, font+' Normal', 10, width, Pango.Alignment.CENTER)
            else:
                try_no += 1
                self.draw_text(cr, _('Error getting weather')+' '+ str(try_no), 0, splash_block_top+height/2 + 20, font+' Normal', 10, width, Pango.Alignment.CENTER)
                if city_id == 0:
                    self.draw_text(cr, _('Location not set'), 0, splash_block_top+height/2 + 40, font+' Normal', 10, width, Pango.Alignment.CENTER)


    def redraw(self, timer1 = True, get_weather1 = True, load_config = False):
        global first_start, on_redraw, timer_bool, get_weather_bool
        if load_config:
            Load_Config()
            app.set_window_properties()
        timer_bool = timer1
        get_weather_bool = get_weather1
        on_redraw = True
        if first_start:
            first_start = False
        if show_indicator == 0:
            ind.hide()
        else:
            ind.show()
        if show_indicator == 1:
            app.window_main.hide()
        else:
            app.window_main.show()

        if show_indicator == 1:
            self.expose_indicator()

        self.queue_draw()
        while Gtk.events_pending():
            Gtk.main_iteration_do(True)
        if get_weather1 and check_for_updates_local and not err_connect:
            check_updates()

    def expose_indicator(self):
        global err, on_redraw, get_weather_bool, weather, err_connect
        if get_weather_bool:
            weather1 = get_weather()
            if weather1:
                time_receive = time.strftime('%H:%M', time.localtime())
                err_connect = False
                splash = False
                weather = weather1
                for i in weather.keys():
                    globals()[i] = weather[i]
            else:
                err_connect = True
            get_weather_bool = False
            if not timer_bool:
                print ('-'*40)
        if err_connect:
            if on_redraw:
                on_redraw = False
                if timer_bool:
                    self.timer = GLib.timeout_add(10000, self.redraw)         
        else:
            if on_redraw:
                on_redraw = False
                if timer_bool:
                    self.timer = GLib.timeout_add(upd_time*60*1000, self.redraw)
                    print ('\033[34m>\033[0m '+_('Next update in')+' '+str(upd_time)+' '+_('min'))
                    print ('-'*40)
            self.Draw_Weather(self.cr)
    
    def clear_draw_area(self, widget):
        self.cr = Gdk.cairo_create(self.get_window())
        self.cr.save()
        if fix_BadDrawable:
            self.cr.set_source_rgba(0.5, 0.5, 0.5, 0.01)
        else:
            self.cr.set_source_rgba(1, 1, 1, 0)
        self.cr.set_operator(cairo.OPERATOR_SOURCE)
        self.cr.paint()
        self.cr.restore()
        self.cr.scale(scale, scale)
        # self.cr.set_antialias(cairo.ANTIALIAS_SUBPIXEL)
    
    
    def expose(self, widget, event):
        global err, on_redraw, get_weather_bool, weather, err_connect, splash, time_receive, date
        # if err == False:
        self.clear_draw_area(widget)
        if first_start:
            self.splash_screen(self.cr)
            return
        if get_weather_bool:
            weather1 = get_weather()
            if weather1:
                time_receive = time.strftime('%H:%M', time.localtime())
                err_connect = False
                splash = False
                weather = weather1
                for i in weather.keys():
                    globals()[i] = weather[i]
                date = date_convert.main(date, date_separator, swap_d_and_m)
            else:
                err_connect = True
            get_weather_bool = False
            if not timer_bool:
                print ('-'*40)
        if err_connect:
            if on_redraw:
                on_redraw = False
                if timer_bool:
                    self.timer = GLib.timeout_add(10000, self.redraw)
            print ('-'*40)
            if splash:
                self.splash_screen(self.cr, 1)
            else:
                # if err == False:
                self.Draw_Weather(self.cr)
                self.draw_scaled_image(self.cr, margin + 10, margin + 10, os.path.join(THEMES_PATH, 'error.png'),24,24)
                self.draw_text(self.cr, _('Connection error'), margin + 35, margin + 14, font+' Normal', 10, color = color_text_week)
                err = True
        else:
            if err == True:
                err = False
                self.clear_draw_area(widget)
            if on_redraw:
                on_redraw = False
                if timer_bool:
                    self.timer = GLib.timeout_add(upd_time*60*1000, self.redraw)
                    print ('\033[34m>\033[0m '+_('Next update in')+' '+str(upd_time)+' '+_('min'))
                    print ('-'*40)
            self.Draw_Weather(self.cr)

    
    def Draw_Weather(self, cr):
        if show_indicator:
            self.draw_scaled_icon(cr, 0, 0, weather['icon_now'][0],1,1, indicator_icons_name)
            ind.set_icon(pix_path)
            t_index = t_scale*2
            if t_feel:
                t_index += 1
            if weather['t_now']:
                ind.set_label(weather['t_now'][0].split(';')[t_index])
        if show_indicator == 1:
            return

        self.draw_bg(cr, bg_left, bg_top, bg_width, bg_height)
        self.cr.fill()
        self.draw_weather_icon_now(cr, 0, 20 + margin)
        
        for i in range(1, n+1):
            self.draw_weather_icon(cr, i, block_icons_left + margin + block_margin + (i-1)*w_block + (i-1)*(10+10/(n-2)), block_icons_top + height-h_block-10 - margin)
        

    def draw_weather_icon_now(self, cr, x, y):
        if day != []:
            global t_now_left, text_now_left
            center = x+width/2

            if icon_now_left > 999: icon_now_left2 = icon_now_left - 1000 - center
            else: icon_now_left2 = icon_now_left
            
            if t_now_left > 999: t_now_left2 = t_now_left - 1000 - center
            else: t_now_left2 = t_now_left

            if text_now_left > 999: text_now_left2 = text_now_left - 1000 - center
            else: text_now_left2 = text_now_left

            s=''
            if date:
                s=', '+date[0]
            if day:
                weekend1 = []
                for item in weekend.split(','):
                    weekend1.append(item.strip())
                if day[0] in weekend1:
                    self.draw_text(cr, day[0]+s, day_left+0+block_now_left, day_top+y-15, font+' Bold', 12, width-day_left, Pango.Alignment.CENTER, color_text_week)
                else:
                    self.draw_text(cr, day[0]+s, day_left+0+block_now_left, day_top+y-15, font+' Bold', 12, width-day_left, Pango.Alignment.CENTER)
            
            if show_time_receive_local:
                if time_update: self.draw_text(cr, _('Updated on server')+' '+time_update[0], x-margin, x+20+margin, font+' Normal', 8, width-10,Pango.Alignment.RIGHT)
                if time_receive: self.draw_text(cr, _('Weather received')+' '+time_receive, x-margin, x+10+margin, font+' Normal', 8, width-10,Pango.Alignment.RIGHT)
            if city_name: self.draw_text(cr, city_name[0], city_name_left+x+block_now_left, city_name_top+y, font+' Bold', 14, width - city_name_left, Pango.Alignment.CENTER)
            self.draw_scaled_icon(cr, icon_now_left2+center-40+block_now_left, icon_now_top+y+30, icon_now[0],80+icon_now_size,80+icon_now_size)
            t_index = t_scale*2
            if t_feel:
                t_index += 1
            if t_now:
                if t_now_alignment == 'right': pango_align = Pango.Alignment.RIGHT
                else: pango_align = Pango.Alignment.LEFT
                self.draw_text(cr, t_now[0].split(';')[t_index], t_now_left2+center-100+block_now_left, t_now_top+y+30, font+' Normal', 18+t_now_size, 60, pango_align)
                if save_cur_temp:
                    t_now_post = ''
                    if save_cur_temp_add_scale:
                        t_now_post = t_scale_dict[t_scale][-1]
                    cur_temp_file = open(os.path.join(CONFIG_PATH, 'cur_temp'), 'w')
                    cur_temp_file.write(t_now[0].split(';')[t_index]+t_now_post)
                    cur_temp_file.close()
            if text_now: self.draw_text(cr, text_now[0], text_now_left2+center-70+block_now_left, text_now_top+y+106, font+' Normal', 10, 140, Pango.Alignment.CENTER)
            
            if show_block_wind_direct:
                ####-block wind direct-####
                left = block_wind_direct_left
                top = y + 30 # top
                r = 31     # radius
                a = 36     # width and height arrow (a < 2*r)
                font_NS = 8 # font
                font_wind = 10
                if wind_direct_small:
                    left = block_now_left-90+block_wind_direct_small_left
                    top = y + 55 + block_wind_direct_small_top# top
                    r = 16    # radius
                    a = 20     # width and height arrow (a < 2*r)
                    font_NS = 6 # font
                    font_wind = 7
                ################################

                NS = (_('E'), _('S'), _('W'), _('N'))
                x0 = center + left+a
                y0 = top + r
                angel_rad = angel*math.pi/180
                if (wind_direct_now and wind_speed_now):
                    for i in range(0, 8):
                        if i % 2 == 0:
                            self.draw_text(cr, NS[i//2], int(x0+r*math.cos(i*0.25*math.pi+angel_rad)), int(y0+r*math.sin(i*0.25*math.pi+angel_rad)), font+' Bold', font_NS, 10, Pango.Alignment.LEFT)
                    if int(wind_speed_now[0].split(';')[wind_units].split()[0]) >= high_wind and high_wind != -1:
                        self.draw_text(cr, wind_direct_now[0]+', '+wind_speed_now[0].split(';')[wind_units].split()[0]+' '+_(wind_speed_now[0].split(';')[wind_units].split()[-1]), x0-r-15, y0+r+font_wind+4, font+' Normal', font_wind, 2*r+30+font_NS,Pango.Alignment.CENTER, color_high_wind)
                    else:
                        self.draw_text(cr, wind_direct_now[0]+', '+wind_speed_now[0].split(';')[wind_units].split()[0]+' '+_(wind_speed_now[0].split(';')[wind_units].split()[-1]), x0-r-15, y0+r+font_wind+4, font+' Normal', font_wind, 2*r+30+font_NS,Pango.Alignment.CENTER)
                if icon_wind_now[0] != 'None': 
                    if os.path.exists(os.path.join(ICONS_PATH, icons_name, 'wind.png')):
                        self.draw_scaled_image(cr, x0-a/2+font_NS/2, y0-a/2+3+font_NS/2, os.path.join(ICONS_PATH, icons_name, 'wind.png'), a, a, icon_wind_now[0]+angel)
                    else:
                        self.draw_scaled_image(cr, x0-a/2+font_NS/2, y0-a/2+3+font_NS/2, os.path.join(ICONS_PATH, 'default', 'wind.png'), a, a, icon_wind_now[0]+angel)
            
            if show_block_add_info:    
                ####-block with additional info-####
                left = block_add_info_left
                top = y + 30 # top
                line_height = 25  # spacing between rows
                #########################
                
                x0 = center + left
                y0 = top
                
                if icon_wind_now[0] != 'None': 
                    if os.path.exists(os.path.join(ICONS_PATH, icons_name, 'wind_small.png')):
                        self.draw_scaled_image(cr, x0, y0, os.path.join(ICONS_PATH, icons_name, 'wind_small.png'), 16, 16, icon_wind_now[0]+angel)
                    else:
                        self.draw_scaled_image(cr, x0, y0, os.path.join(ICONS_PATH, 'default', 'wind_small.png'), 16, 16, icon_wind_now[0]+angel)
                if (wind_direct_now and wind_speed_now):
                    if int(wind_speed_now[0].split(';')[wind_units].split()[0]) >= high_wind and high_wind != -1:
                        self.draw_text(cr, wind_speed_now[0].split(';')[wind_units].split()[0]+"<span size='x-small'> %s</span>  <span size='small'>%s</span>"%(_(wind_speed_now[0].split(';')[wind_units].split()[-1]), wind_direct_now[0]), x0+20, y0-1, font+' Normal', 12, 100,Pango.Alignment.LEFT, color_high_wind)
                    else:
                        self.draw_text(cr, wind_speed_now[0].split(';')[wind_units].split()[0]+"<span size='x-small'> %s</span>  <span size='small'>%s</span>"%(_(wind_speed_now[0].split(';')[wind_units].split()[-1]), wind_direct_now[0]), x0+20, y0-1, font+' Normal', 12, 100,Pango.Alignment.LEFT)
                if press_now:
                    self.draw_text(cr, press_now[0].split(';')[press_units].split()[0]+"<span size='x-small'> %s</span>"%_(press_now[0].split(';')[press_units].split()[-1]), x0+20, y0+line_height-1, font+' Normal', 12, 150,Pango.Alignment.LEFT)
                    if os.path.exists(os.path.join(ICONS_PATH, icons_name, 'press.png')):
                        self.draw_scaled_image(cr, x0, y0+line_height, os.path.join(ICONS_PATH, icons_name, 'press.png'), 16, 16)
                    else:
                        self.draw_scaled_image(cr, x0, y0+line_height, os.path.join(ICONS_PATH, 'default', 'press.png'), 16, 16)
                if hum_now:
                    self.draw_text(cr, hum_now[0]+"<span size='x-small'> % "+_('humid.')+"</span>", x0+20, y0+line_height*2-1, font+' Normal', 12, 100,Pango.Alignment.LEFT)
                    if os.path.exists(os.path.join(ICONS_PATH, icons_name, 'hum.png')):
                        self.draw_scaled_image(cr, x0, y0+line_height*2, os.path.join(ICONS_PATH, icons_name, 'hum.png'), 16, 16)
                    else:
                        self.draw_scaled_image(cr, x0, y0+line_height*2, os.path.join(ICONS_PATH, 'default', 'hum.png'), 16, 16)
                if t_water_now:
                    self.draw_text(cr, t_water_now.split(';')[t_scale]+"<span size='x-small'> %s %s</span>"%(t_scale_dict[t_scale], _("water")), x0+20, y0+line_height*3-1, font+' Normal', 12, 100,Pango.Alignment.LEFT)
                    if os.path.exists(os.path.join(ICONS_PATH, icons_name, 't_water.png')):
                        self.draw_scaled_image(cr, x0, y0+line_height*3, os.path.join(ICONS_PATH, icons_name, 't_water.png'), 16, 16)
                    else:
                        self.draw_scaled_image(cr, x0, y0+line_height*3, os.path.join(ICONS_PATH, 'default', 't_water.png'), 16, 16)
            
            if show_block_tomorrow:
                ####-block tomorrow-####
                left = block_tomorrow_left
                top = y + 30 + block_tomorrow_top
                a = 70
                b = 53
                b_width = a+60
                ###############################

                x0 = center + left
                y0 = top
                c = ( _('Morning'), _('Day'), _('Evening'), _('Night'))

                if icon_tomorrow and icon_tomorrow[1] == 'None' and icon_tomorrow[3] == 'None':
                    self.draw_text(cr, _('Tomorrow'), x0-40, y0-13, font+' Bold', 8, a+60,Pango.Alignment.CENTER)
                else:
                    self.draw_text(cr, _('Tomorrow'), x0, y0-13, font+' Bold', 8, a+60,Pango.Alignment.CENTER)
                for i in range(0, 4):
                    j = i
                    if j > 1: j = j-2
                    self.draw_text(cr, c[i], x0+a*((j+1)//2), y0+b*(i//2), font+' Bold', 7, 50,Pango.Alignment.LEFT, gradient=True)
                    if t_tomorrow:
                        self.draw_text(cr, t_tomorrow[i].split(';')[t_index], x0+a*((j+1)//2), y0+11+b*(i//2), font+' Normal', 8, 50,Pango.Alignment.LEFT)          
                    if t_tomorrow_low:
                        self.draw_text(cr, t_tomorrow_low[i].split(';')[t_index], x0+a*((j+1)//2)+2, y0+22+b*(i//2), font+' Normal', 7, 50,Pango.Alignment.LEFT)
                    try:
                        self.draw_scaled_icon(cr, x0+32+a*((j+1)//2), y0+b*(i//2), icon_tomorrow[i], 28, 28)
                    except:
                        self.draw_scaled_icon(cr, x0+32+a*((j+1)//2), y0+b*(i//2), 'na.png;na.png', 28, 28)
                    if (wind_direct_tom and wind_speed_tom):
                        try:
                            if int(wind_speed_tom[i].split(';')[wind_units].split()[0]) >= high_wind and high_wind != -1:
                                self.draw_text(cr, wind_direct_tom[i]+', '+wind_speed_tom[i].split(';')[wind_units].split()[0]+' '+_(wind_speed_tom[i].split(';')[wind_units].split()[-1]), x0+a*((j+1)//2), y0+27+b*(i//2), font+' Normal', 7, 64,Pango.Alignment.LEFT, color_high_wind)
                            else:
                                self.draw_text(cr, wind_direct_tom[i]+', '+wind_speed_tom[i].split(';')[wind_units].split()[0]+' '+_(wind_speed_tom[i].split(';')[wind_units].split()[-1]), x0+a*((j+1)//2), y0+27+b*(i//2), font+' Normal', 7, 64,Pango.Alignment.LEFT)
                        except:
                            pass


            if show_block_today:
                ####-block today-####
                left = block_today_left
                top = y + 30 + block_today_top
                a = 70
                b = 53
                b_width = a+60
                ###############################
                
                x0 = center + left
                y0 = top
                c = (_('Morning'), _('Day'), _('Evening'), _('Night'))

                self.draw_text(cr, _('Today'), x0, y0-13, font+' Bold', 8, a+60,Pango.Alignment.CENTER)
                for i in range(0, 4):
                    j = i
                    if j > 1: j = j-2
                    self.draw_text(cr, c[i], x0+a*((j+1)//2), y0+b*(i//2), font+' Bold', 7, 50,Pango.Alignment.LEFT, gradient=True)
                    if t_today:
                        self.draw_text(cr, t_today[i].split(';')[t_index], x0+a*((j+1)//2), y0+11+b*(i//2), font+' Normal', 8, 50,Pango.Alignment.LEFT)
                    if t_today_low:
                        self.draw_text(cr, t_today_low[i].split(';')[t_index], x0+a*((j+1)//2)+2, y0+22+b*(i//2), font+' Normal', 7, 50,Pango.Alignment.LEFT)
                    try:
                        self.draw_scaled_icon(cr, x0+32+a*((j+1)//2), y0+b*(i//2), icon_today[i], 28, 28)
                    except:
                        self.draw_scaled_icon(cr, x0+32+a*((j+1)//2), y0+b*(i//2), 'na.png;na.png', 28, 28)
                    if (wind_direct_tod and wind_speed_tod):
                        try:
                            if int(wind_speed_tod[i].split(';')[wind_units].split()[0]) >= high_wind and high_wind != -1:
                                self.draw_text(cr, wind_direct_tod[i]+', '+wind_speed_tod[i].split(';')[wind_units].split()[0]+' '+_(wind_speed_tod[i].split(';')[wind_units].split()[-1]), x0+a*((j+1)//2), y0+27+b*(i//2), font+' Normal', 7, 64,Pango.Alignment.LEFT, color_high_wind)
                            else:
                                self.draw_text(cr, wind_direct_tod[i]+', '+wind_speed_tod[i].split(';')[wind_units].split()[0]+' '+_(wind_speed_tod[i].split(';')[wind_units].split()[-1]), x0+a*((j+1)//2), y0+27+b*(i//2), font+' Normal', 7, 64,Pango.Alignment.LEFT)
                        except:
                            pass


    def draw_weather_icon(self, cr, index, x, y):
        if day != []:
            try:
                a = 30
                self.draw_scaled_icon(cr, x+a, y+16, icon[index], 36, 36)
                s=''
                if date:
                    s=', '+date[index]
                if day:
                    weekend1 = []
                    for item in weekend.split(','):
                        weekend1.append(item.strip())
                    if day[index] in weekend1:
                        self.draw_text(cr, day[index]+s, x, y-2, font+' Bold', 9, w_block,Pango.Alignment.LEFT, color_text_week)
                    else:
                        self.draw_text(cr, day[index]+s, x, y-2, font+' Bold', 9, w_block,Pango.Alignment.LEFT)
                cr.set_source_rgba(color_text[0], color_text[1], color_text[2], color_text[3])
                t_index = t_scale*2
                if t_feel:
                    t_index += 1
                self.draw_text(cr, t_day[index].split(';')[t_index], x, y+15, font+' Normal', 10, w_block-45,Pango.Alignment.LEFT)
                self.draw_text(cr, t_night[index].split(';')[t_index], x, y+30, font+' Normal', 8, w_block-45,Pango.Alignment.LEFT)
                if chance_of_rain and show_chance_of_rain:
                    self.draw_text(cr, chance_of_rain[index], x+30, y+9, font+' Normal', 7, 36,Pango.Alignment.CENTER)

                if (wind_direct and wind_speed): 
                    if int(wind_speed[index].split(';')[wind_units].split()[0]) >= high_wind and high_wind != -1:
                        self.draw_text(cr, wind_direct[index]+', '+wind_speed[index].split(';')[wind_units].split()[0]+' '+_(wind_speed[index].split(';')[wind_units].split()[-1]), x, y+50, font+' Normal', 8, 80,Pango.Alignment.LEFT, color_high_wind)
                    else:
                        self.draw_text(cr, wind_direct[index]+', '+wind_speed[index].split(';')[wind_units].split()[0]+' '+_(wind_speed[index].split(';')[wind_units].split()[-1]), x, y+50, font+' Normal', 8, 80,Pango.Alignment.LEFT)
                    if text: self.draw_text(cr, text[index], x, y+65, font+desc_list[desc_style], 7, w_block, Pango.Alignment.LEFT)
                else:
                    if text: self.draw_text(cr, text[index], x, y+55, font+desc_list[desc_style], 7, w_block, Pango.Alignment.LEFT)
            except:
                pass

    def draw_bg_l_c_r(self, cr, path, l, t, w, h, ext):
        self.draw_scaled_image(cr, l, t, os.path.join(path, "l.%s"%ext), 60, h)
        self.draw_scaled_image(cr, l+60, t, os.path.join(path, "c.%s"%ext), w-120, h)
        self.draw_scaled_image(cr, l+w-60, t, os.path.join(path, "r.%s"%ext), 60, h)        

    def draw_bg_png_svg(self, cr, path, l, t, w, h):
        if os.path.exists(os.path.join(path, "%s.png"%bg_custom)):
            self.draw_scaled_image(cr, l, t, os.path.join(path, "%s.png"%bg_custom), w, h)
        if os.path.exists(os.path.join(path, "%s.svg"%bg_custom)):
            self.draw_scaled_image(cr, l, t, os.path.join(path, "%s.svg"%bg_custom), w, h)
        if os.path.exists(os.path.join(path, "%s.svgz"%bg_custom)):
            self.draw_scaled_image(cr, l, t, os.path.join(path, "%s.svgz"%bg_custom), w, h)
        if os.path.exists(os.path.join(path, "l.png")):
            self.draw_bg_l_c_r(cr, path, l, t, w, h, "png")
        else:
            if os.path.exists(os.path.join(path, "l.svg")):
                self.draw_bg_l_c_r(cr, path, l, t, w, h, "svg")
            else:
                if os.path.exists(os.path.join(path, "l.svgz")):
                    self.draw_bg_l_c_r(cr, path, l, t, w, h, "svgz")
                else:
                    if os.path.exists(os.path.join(path, "corner.png")):
                        self.draw_scaled_image(cr, l, t, os.path.join(path, "corner.png"), 60, 60)
                        self.draw_scaled_image(cr, l, t+60, os.path.join(path, "border_left.png"), 60, h-120)
                        self.draw_scaled_image(cr, l+w-60, t+60, os.path.join(path, "border_left.png"), 60, h-120, 180)
                        self.draw_scaled_image(cr, l+60, t, os.path.join(path, "border_top.png"), w-120, 60)
                        self.draw_scaled_image(cr, l+w-60, t, os.path.join(path, "corner.png"), 60, 60, 90)
                        self.draw_scaled_image(cr, l+60, t+60, os.path.join(path, "fill.png"), w-120, h-120)
                        self.draw_scaled_image(cr, l, t+h-60, os.path.join(path, "corner.png"), 60, 60, 270)
                        self.draw_scaled_image(cr, l+w-60, t+h-60, os.path.join(path, "corner.png"), 60, 60, 180)
                        self.draw_scaled_image(cr, l+60, t+h-60, os.path.join(path, "border_top.png"), l+w-120, 60, 180)

    def find_image(self, path):
        if path[-4] == '.' or path[-5] == '.':
            return path
        if os.path.exists(os.path.join(path, "%s.png"%bg_custom)):
            return os.path.join(path, "%s.png"%bg_custom)
        if os.path.exists(os.path.join(path, "%s.svg"%bg_custom)):
            return os.path.join(path, "%s.svg"%bg_custom)
        if os.path.exists(os.path.join(path, "%s.svgz"%bg_custom)):
            return os.path.join(path, "%s.svgz"%bg_custom)
        return False

    def draw_bg(self, cr, l, t, w, h, ignore_scale = False):
        if w == -1:
            w = width
        if h == -1:
            h = height
        if not_composited:
            if os.path.exists(os.path.join(CONFIG_PATH, 'main_screenshot.png')):
                crop_image(x_pos, y_pos, w+l, h+t)
                self.draw_scaled_image(cr, 0, 0, os.path.join(CONFIG_PATH, 'screenshot.png'), w+l, h+t)
        if show_bg_png:
            l = l//2
            t = t//2
            if scale == 1 or ignore_scale: 
                if os.path.exists(os.path.join(BGS_USER_PATH, bg_custom)):
                    if self.find_image(os.path.join(BGS_USER_PATH, bg_custom)):
                        self.draw_scaled_image(cr, l, t, self.find_image(os.path.join(BGS_USER_PATH, bg_custom)), w, h)
                    else:
                        self.draw_bg_png_svg(cr, os.path.join(BGS_USER_PATH, bg_custom), l, t, w, h)
                else:
                    if os.path.exists(os.path.join(BGS_PATH, bg_custom)):
                        if self.find_image(os.path.join(BGS_PATH, bg_custom)):
                            self.draw_scaled_image(cr, l, t, self.find_image(os.path.join(BGS_PATH, bg_custom)), w, h)
                        else:
                            self.draw_bg_png_svg(cr, os.path.join(BGS_PATH, bg_custom), l, t, w, h)
                    else:
                        print (_('Background image not found')+': '+str(bg_custom))
                if ignore_scale:
                    return
                # cr.translate(-l, -t)
            if scale != 1:
                if not os.path.exists(os.path.join(CONFIG_PATH, 'bgs_for_scale', str(bg_custom)+'_'+str(preset_number)+'_'+str(n)+'.png')):
                    self.save_widget_bg()
                if os.path.exists(os.path.join(CONFIG_PATH, 'bgs_for_scale', str(bg_custom)+'_'+str(preset_number)+'_'+str(n)+'.png')):
                    self.draw_scaled_image(cr, l, t, os.path.join(CONFIG_PATH, 'bgs_for_scale', str(bg_custom)+'_'+str(preset_number)+'_'+str(n)+'.png'), w, h)
        else:
            cr.set_source_rgba(color_bg[0], color_bg[1], color_bg[2], color_bg[3])
            cr.rectangle(l+r, t+0, w-2*r, h)
            cr.rectangle(l+0, t+r, w, h-2*r)
            cr.arc(l+w-r, t+0+r, r, 0 , 8)
            cr.arc(l+w-r, t+0+r, r, 0 , 8)
            cr.arc(l+w-r, t+h-r, r, 0, 8)
            cr.arc(l+0+r, t+h-r, r, 0, 8)
            cr.arc(l+0+r, t+0+r, r, 0, 8)
            cr.fill()

    
    def draw_text(self, cr, text, x, y, font, size=None, width=200, alignment=Pango.Alignment.LEFT, color=(-1, -1, -1, -1), gradient=False):
        if color == (-1, -1, -1, -1):
            color = color_text
        if draw_shadow:
            cr.set_source_rgba(color_shadow[0], color_shadow[1], color_shadow[2], color_shadow[3])
            self.draw_custom_text(cr, text, x+1, y+1,  font, size , width, alignment, gradient, color_shadow)
        cr.set_source_rgba(color[0], color[1], color[2], color[3])
        self.draw_custom_text(cr, text, x, y,  font, size , width, alignment, gradient, color)
        
    def draw_custom_text(self, cr, text, x, y, font, size, width=200, alignment=Pango.Alignment.LEFT, gradient=False, color=(-1, -1, -1, -1)):
        cr.save()
        cr.translate(x, y)
        
        font_desc = Pango.FontDescription(font)
        font_desc.set_size(size * Pango.SCALE)

        if self.p_layout == None :
            self.p_layout = PangoCairo.create_layout(cr)
        else:
            PangoCairo.update_layout(cr, self.p_layout)
        self.p_layout.set_font_description(font_desc)
        self.p_layout.set_width(width * Pango.SCALE)
        self.p_layout.set_alignment(alignment)
        self.p_layout.set_markup(text)
        if gradient:
            lg = cairo.LinearGradient(0, 0, 45, 0)
            lg.add_color_stop_rgba(0.5, color[0], color[1], color[2], color[3])
            lg.add_color_stop_rgba(0.8, color[0], color[1], color[2], 0)
            cr.set_source(lg)
            cr.fill()
        PangoCairo.show_layout(cr, self.p_layout)
        cr.restore()

    def draw_scaled_icon(self, cr, x, y, pix, w, h, indicator_icon_name=False):
        icons_name1 = icons_name    
        if indicator_icon_name:
            global pix_path
            icons_name1 = indicator_icon_name
        if icons_name1 == 'default':
            pix = pix.split(';')[0]
            pix_path = os.path.join(ICONS_USER_PATH, 'default', 'weather', os.path.split(pix)[1])
            if not os.path.exists(pix_path):
                try:
                    print ('\033[34m>\033[0m '+_('downloading')+' '+os.path.split(pix)[1]+' ('+pix+')')
                    urlretrieve(pix, pix_path)
                    print ('OK')
                except:
                    print (_('Unable to download')+' '+pix)
                if not os.path.exists(pix_path):
                    pix_path = os.path.join(THEMES_PATH, 'na.png')
                if not indicator_icon_name:
                    try:
                        self.draw_scaled_image(cr, x, y, pix_path, w, h)
                    except:
                        pass
                return
        else:
            pix = pix.split(';')[1]
            pix_path = os.path.join(ICONS_PATH, icons_name1, 'weather', pix)
            
            
            if not os.path.exists(pix_path):
                pix_path = pix_path[:-3]+'svg'
                if not os.path.exists(pix_path):
                    pix_path = pix_path[:-3]+'svgz'
                    if not os.path.exists(pix_path):
                        pix_path = os.path.join(ICONS_USER_PATH, icons_name1, 'weather', pix)
                        if not os.path.exists(pix_path):
                            pix_path = pix_path[:-3]+'svg'
                            if not os.path.exists(pix_path):
                                pix_path = pix_path[:-3]+'svgz'
                                if not os.path.exists(pix_path):
                                    print ('\033[1;31m[!]\033[0m '+_('Icon not found')+':\n> '+pix_path)
                                    if os.path.exists(os.path.join(ICONS_PATH, icons_name1, 'weather', 'na.png')):
                                        pix_path = os.path.join(ICONS_PATH, icons_name1, 'weather', 'na.png')
                                    else:
                                        if os.path.exists(os.path.join(ICONS_USER_PATH, icons_name1, 'weather', 'na.png')):
                                            pix_path = os.path.join(ICONS_USER_PATH, icons_name1, 'weather', 'na.png')
                                        else:
                                            pix_path = os.path.join(THEMES_PATH, 'na.png')
        if not indicator_icon_name:    
            self.draw_scaled_image(cr, x, y, pix_path, w, h)

    def draw_scaled_image(self, cr, x, y, pix, w, h, ang = 0):
        if pix.split('.')[-1] == 'svg' or pix.split('.')[-1] == 'svgz' and HAS_RSVG:
            self.draw_scaled_image_svg(cr, x, y, pix, w, h, ang)
        else:
            self.draw_scaled_image_png(cr, x, y, pix, w, h, ang)
 

    def draw_scaled_image_png(self, cr, x, y, pix, w, h, ang = 0):
        cr.save()
        if ang !=0:
            cr.translate(x+w//2, y+h//2)
            cr.rotate(math.radians(ang))
            cr.translate(-w//2, -h//2)
        else:
            cr.translate(x, y)
        if pix[-4:] == 'svgz':
            inF = gzip.open(pix, 'r')
            loader = GdkPixbuf.PixbufLoader()
            loader.write(inF.read())
            loader.close()
            inF.close()
            pixbuf = loader.get_pixbuf()
        else:
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(pix)
        k=1
        if pixbuf.get_width()>pixbuf.get_height() and not re.findall('backgrounds', pix) and os.path.basename(pix)!='screenshot.png' and not re.findall('bgs_for_scale', pix):
            k = pixbuf.get_width()/pixbuf.get_height()
        pixbuf = pixbuf.scale_simple(round(w*k),h,GdkPixbuf.InterpType.BILINEAR)
        if k==1:
            Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        else:
            Gdk.cairo_set_source_pixbuf(cr, pixbuf, (h-round(w*k))/2, 0)
        cr.paint()
        cr.restore()


    def draw_scaled_image_svg(self, cr, x, y, pix, w, h, ang = 0):
        cr.save()
        handle = Rsvg.Handle()
        svg = handle.new_from_file(pix)
        if ang !=0:
            cr.translate(x+w//2, y+h//2)
            cr.rotate(math.radians(ang))
            cr.translate(-w//2, -h//2)
        else:
            cr.translate(x, y)
        cr.scale(w/svg.props.width, h/svg.props.height)
        svg.render_cairo(cr)
        cr.restore()


    def save_widget_bg(self):
        bg_w = width if bg_width == -1 else bg_width
        bg_h = height if bg_height == -1 else bg_height
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, bg_w, bg_h)
        ctx = cairo.Context(surface)
        self.draw_bg(ctx, 0, 0, bg_width, bg_height, ignore_scale = True)
        make_dirs(os.path.join(CONFIG_PATH, 'bgs_for_scale'))
        surface.write_to_png(os.path.join(CONFIG_PATH, 'bgs_for_scale', str(bg_custom)+'_'+str(preset_number)+'_'+str(n)+'.png'))


    def save_widget_screenshot(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(width*scale), int(height*scale))
        ctx = cairo.Context(surface)
        ctx.scale(scale, scale)
        self.Draw_Weather(ctx)
        print(_('Screenshot saved to')+' '+os.path.join(os.path.expanduser('~'), "gis-weather %s.png"%time.strftime('%d-%m-%y %T', time.localtime())))
        surface.write_to_png(os.path.join(os.path.expanduser('~'), "gis-weather %s.png"%time.strftime('%d-%m-%y %T', time.localtime())))

class Weather_Widget:
    def __init__(self):
        self.window_main = Gtk.Window()
        self.window_main.set_accept_focus(False)
        self.window_main.set_has_resize_grip(False)
        self.set_window_properties()
        self.window_main.set_icon_from_file(os.path.join(APP_PATH, "icon.png"))

        print (_('Widget size')+':')
        print ('    '+_('width')+' = '+str(int(width*scale))+' '+_('height')+' = '+str(int(height*scale))+' '+_('including indent')+' = '+str(margin))

        self.window_main.set_decorated(False)

        global not_composited

        if not self.window_main.is_composited():
            not_composited = True
            screenshot()

        self.window_main.set_events(Gdk.EventMask.ALL_EVENTS_MASK)
        self.window_main.connect('button-press-event', self.button_press)
        self.window_main.connect("configure-event", self.configure_event)
        self.window_main.connect("enter-notify-event", self.enter_leave_event, "enter")
        self.window_main.connect("leave-notify-event", self.enter_leave_event, "leave")

        self.window_main.connect("destroy", Gtk.main_quit)
        self.window_main.connect("screen-changed", self.screen_changed)
        self.window_main.set_role('')
        self.window_main.set_app_paintable(True)
        if os.environ.get('DESKTOP_SESSION') == "ubuntu":
            self.window_main.set_type_hint(Gdk.WindowTypeHint.DOCK)
        else:
            self.window_main.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.window_main.set_keep_above(False)
        self.window_main.set_keep_below(True)
        self.window_main.set_skip_taskbar_hint(True)
        self.window_main.set_skip_pager_hint(True)

        self.drawing_area = MyDrawArea()
        self.window_main.add(self.drawing_area)
        self.screen_changed(self.window_main)

    def set_window_properties(self):
        global n
        global width, height

        if n < 1: n = 1
        width = w_block*n + block_margin*2 + 10*(n - 1) + 2*margin + block_icons_left
        height = 260 + block_margin + 2*margin + height_fix
        self.window_main.resize(int(width*scale), int(height*scale))
        self.window_main.move(x_pos, y_pos)
        if sticky:
            self.window_main.stick()
        else:
            self.window_main.unstick()
        self.window_main.set_opacity(opacity)


    def menu_response(self, widget, event, value=None):
        global service
        if event == 'load_preset':
            Load_Preset(value)
            self.set_window_properties()
            self.drawing_area.redraw(False, False)
            Save_Config()
        if event == 'save_screenshot':
            self.drawing_area.save_widget_screenshot()
        if event == 'show_hide_widget':
            global show_indicator
            if show_indicator == 1:
                show_indicator = 2
            else:
                show_indicator = 1
            Save_Config()
            self.drawing_area.redraw(False, False)
        if event == 'help':
            help_dialog.create(APP_PATH)
        if event == 'about':
            about = about_dialog.create(v, APP_PATH)
            about.run()
            about.destroy()
            return
        if event == 'edit':
            if sys.platform.startswith('linux'):
                subprocess.Popen(['xdg-open', CONFIG_PATH])
            else:
                subprocess.Popen(['explorer ', CONFIG_PATH])
            return
        if event == 'fix':
            global fix_position
            if fix_position:
                fix_position = False
            else:
                fix_position = True
            Save_Config()
        if event == 'sticky':
            global sticky
            if sticky:
                sticky = False
                self.window_main.unstick()
            else:
                sticky = True
                self.window_main.stick()
            Save_Config()
        if event == 'setup':
            Load_Config()
            settings_dialog.main(gw_config_default, gw_config, self.drawing_area, app, icons_list, backgrounds_list, ICONS_PATH, BGS_PATH, service)
        if event == 'redraw_icons':
            global icons_name
            icons_name = value
            self.drawing_area.queue_draw()
            Save_Config()
        if event == 'redraw_indicator_icons':
            global indicator_icons_name
            indicator_icons_name = value
            if show_indicator == 1:
                self.drawing_area.redraw(False, False)
            self.drawing_area.queue_draw()
            Save_Config()
        if event == 'redraw_bg':
            global bg_custom, show_bg_png, color_bg
            show_bg_png = True
            if value == 'Нет':
                show_bg_png = False
                color_bg = (1, 1, 1, 0)
            bg_custom = value
            #self.drawing_area.redraw(False, False)
            self.drawing_area.queue_draw()
            # self.drawing_area.create_bg()
            # self.drawing_area.draw_bg(self.drawing_area.cr_bg)
            Save_Config()
        if event == 'redraw_text':
            Load_Color_Scheme(value)
            self.drawing_area.redraw(False, False)
            Save_Config()
        if event == 'reload':
            # if radio, then reloaded 2 time, fix
            if type(widget) == Gtk.RadioMenuItem:
                if not widget.get_active():
                    return

            global city_id, weather_lang
            Load_Config()
            try:
                if value[1] != 0:
                    service = value[0]
                    city_id = value[1].split(';')[0]
                    if service+'_weather_lang' in gw_config.keys():
                        weather_lang = gw_config[service+'_weather_lang']
                    else:
                        weather_lang = value[2]
                    Save_Config()
            except:
                pass
            self.drawing_area.redraw(False)
        if event == 'edit_city_id':
            if self.show_edit_dialog():
                Load_Config()
                while Gtk.events_pending():
                    Gtk.main_iteration_do(True)
                self.drawing_area.redraw(False)

        if indicator_is_appindicator:
            app.create_menu(for_indicator=True)
            ind.set_menu(app.menu)


    def show_edit_dialog(self):
        global city_id, gw_config
        Load_Config()
        dialog, entrybox, treeview, bar_err, bar_ok, bar_label, combobox_weather_lang, weather_lang_list, combobox_service = city_id_dialog.create(self.window_main, APP_PATH, weather_lang, service);
        dialog.show_all()
        response = dialog.run()

        while response == Gtk.ResponseType.ACCEPT or response == Gtk.ResponseType.OK:
            bar_err.hide()
            Load_Config()
            try:
                city_list = gw_config[data.get_city_list(service)]
            except:
                city_list = []
            if response == Gtk.ResponseType.ACCEPT:
                try:
                    selection = treeview.get_selection()
                    model, iter = selection.get_selected()
                    abc, cde =  selection.get_selected_rows()
                    del_index=cde[0]
                    if iter:
                        model.remove(iter)
                    bar_label.set_text(_('Removed')+': %s'%city_list[int(del_index[0])].split(';')[1])
                    del city_list[int(del_index[0])]
                    selection = treeview.get_selection()
                    abc, cde =  selection.get_selected_rows()
                    if cde:
                        city_id = city_list[int(cde[0][0])].split(';')[0]
                    else:
                        city_id = 0
                    gw_config[data.get_city_list(service)] = city_list
                    Save_Config()
                    bar_ok.show()
                except:
                    pass
            if response == Gtk.ResponseType.OK:
                try:
                    city_id = entrybox.get_text()
                    c_name = data.get_city_name(service, city_id, weather_lang)
                    if c_name == 'None':
                        if len(city_list) != 0:
                            city_id = city_list[0].split(';')[0]
                        else:
                            city_id = 0
                        raise
                    city_list.append(str(city_id) + ';' + c_name)
                    model = treeview.get_model()
                    model.append([city_list[-1].split(';')[0], city_list[-1].split(';')[1]])
                    treeview.set_model(model)
                    gw_config[data.get_city_list(service)] = city_list
                    Save_Config()
                    bar_label.set_text(_('Added')+': %s'%city_list[-1].split(';')[1])
                    bar_ok.show()
                except:
                    bar_ok.hide()
                    bar_err.show()
                    print ('\033[1;31m[!]\033[0m '+_('Invalid location code'))
            response = dialog.run()
        Load_Config()
        try:
            city_list = gw_config[data.get_city_list(service)]
        except:
            city_list = []
        selection = treeview.get_selection()
        abc, cde =  selection.get_selected_rows()
        try:
            sel_index=cde[0]
        except:
            sel_index = None
        if sel_index:
            city_id = city_list[int(sel_index.to_string())].split(';')[0]
        else:
            if len(city_list) != 0:
                city_id = city_list[0].split(';')[0]
            else:
                city_id = 0
        Save_Config()
        dialog.hide()
        return True

#---------------------- Event handlers window --------------------------------
    def button_press(self, widget, event):
        if event.button == 1 and not fix_position:
            self.window_main.begin_move_drag(1, int(event.x_root), int(event.y_root), event.time)
            return True
        if event.button == 3:
            self.create_menu()
            self.menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False

    def create_menu(self, for_indicator=False):
        global icons_list, backgrounds_list
        # try:
        #     a = gw_config[data.get_city_list(service)]
        # except:
        #     gw_config[data.get_city_list(service)] = []
        self.menu, icons_list, backgrounds_list = gw_menu.create_menu(app, ICONS_PATH, BGS_PATH, ICONS_USER_PATH, BGS_USER_PATH, color_scheme, gw_config, for_indicator)

    def configure_event(self, widget, event):
        global x_pos, y_pos
        if event.x != x_pos or event.y != y_pos:
            x_pos = event.x
            y_pos = event.y
            Save_Config()
            # if not_composited:
            #     self.drawing_area.draw_bg(cr, bg_left, bg_top, bg_width, bg_height)

    def enter_leave_event(self, widget, event, param):
        global show_time_receive_local
        if param == 'enter' and show_time_receive:
            show_time_receive_local = True
        if param == 'leave' and show_time_receive_local:
            show_time_receive_local = False
        if not err and show_time_receive:
            self.drawing_area.queue_draw()

    def screen_changed(self, widget, old_screen = None):
        screen = widget.get_screen()
        visual = screen.get_rgba_visual()
        if visual == None or not widget.is_composited():
            print (_('Your screen does not support alpha'))
        else:
            print (_('Your screen supports alpha'))
        if not WIN:
            widget.set_visual(visual)
        return True

#--------------------------------------------------------------------------------

    def main(self):
        self.window_main.show_all()
        if show_indicator == 1:
            self.window_main.hide()
        # fix height window
        if WIN:
            x = self.window_main.get_size()
            self.window_main.resize(int(width*scale), int(height*scale-(x[1]-height*scale)))
        Gtk.main()


if __name__ == "__main__":

    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    ind = Indicator()
    app = Weather_Widget()
    app.create_menu(for_indicator=True)
    ind.set_menu(app.menu)
    app.main()
