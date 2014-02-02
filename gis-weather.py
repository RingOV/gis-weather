#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  gis_weather.py
v = '0.4'
#  Copyright 2013-2014 Alexander Koltsov
#
#  draw_scaled_image, draw_text_Whise copyright by Helder Fraga
#  aka Whise <helder.fraga@hotmail.com>

license = '''This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can find the full text of the license under
http://www.gnu.org/licenses/gpl.txt'''

import gtk
import cairo
import pango
import re
import time
import math
from urllib import urlretrieve
from urllib2 import urlopen
from gobject import timeout_add
import os
import json
import Gtk_city_id
import Gtk_update_dialog
import sys
import subprocess
import settings

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')

if not os.path.exists(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)
if not os.path.exists(os.path.join(CONFIG_PATH, 'color_schemes')):
    os.makedirs(os.path.join(CONFIG_PATH, 'color_schemes'))
if not os.path.exists(os.path.join(CONFIG_PATH, 'icons')):
    os.makedirs(os.path.join(CONFIG_PATH, 'icons'))
if not os.path.exists(os.path.join(CONFIG_PATH, 'backgrounds')):
    os.makedirs(os.path.join(CONFIG_PATH, 'backgrounds'))

# Default values
gw_config_default = {
    'angel': 0,                        # Угол поворота по часовой стрелке в градусах
    'city_id': 0,                      # Код города
    'city_id_add': [],                 # Словарь дополнительных городов
    'upd_time': 30,                    # Обновлять через (в минутах)
    'n': 7,                            # Количество отображаемых дней от 1 до 13
    'x_pos': 60,                       # Позиция слева
    'y_pos': 60,                       # Позиция сверху
    't_feel': False,                   # Температура как ощущается
    'font': 'Ubuntu',                  # Шрифт
    'color_text': (0, 0, 0, 1), #RGBa  # Цвет текста
    'color_text_week': (0.5, 0, 0, 1), # Цвет Сб и Вс
    'color_bg': (0.8, 0.8, 0.8, 1),    # Цвет фона
    'color_shadow': (1, 1, 1, 0.7),    # Цвет тени
    'draw_shadow': True,               # Рисовать тень
    'opacity': 1,                      # Прозрачность всего окна 0..1
    'show_time_receive': False,        # Время получения погоды
    'show_block_wind_direct': True,    # Блок направление ветра
    'block_wind_direct_left': -170,    # Позиция слева относительно центра
    'wind_direct_small': False,        # Маленький блок направления ветра
    'show_block_add_info': True,       # Блок с дополнительной информацией
    'block_add_info_left': 70,         # Позиция слева относительно центра
    'show_block_tomorrow': True,       # Блок с погодой на завтра
    'block_tomorrow_left': 180,        # Позиция слева относительно центра
    'show_block_today': True,          # Блок с погодой на сегодня
    'block_today_left': -310,          # Позиция слева относительно центра
    'r': 0,                            # Радиус углов фона (только, если фон не изображение)
    'show_splash_screen': 2,           # Загрузочная заставка 0 - нет, 1 - только фон, 2 - есть
    'max_try_show': 30,                # После этого количества попыток загрузочная заставка исчезнет, 0 - будет видна всегда
    'sticky': True,                    # На всех рабочих столах
    'show_bg_png': True,               # Если True, то в фоне картинка
    'bg_custom': 'bg_light.png',       # А вот, собственно, и она
    'margin': 20,                      # Отступ от всех сторон виджета
    'output_display': 0,               # Номер дисплея, в который выводится виджет (нумерация в терминале, * - выбранный дисплей)
    'high_wind': 10,                   # Ветер больше или равен этого значения выделяется цветом (-1 не выделять)
    'color_high_wind': (0, 0, 0.6, 1), # Цвет сильного ветра
    'icons_name': 'default',           # Имя папки с иконками погоды
    'fix_BadDrawable': False,          # Если выскакивает ошибка 'BadDrawable', то в конфиге исправьте на true
    'color_scheme_number': 0,
    'check_for_updates': 2,            # 0 - нет, 1 - только при запуске, 2 - всегда
    'fix_position': False
}
gw_config = {}
for i in gw_config_default.keys():
    gw_config[i] = gw_config_default[i]

color_scheme = [
    {   'color_text': (0, 0, 0, 1), #RGBa    # Цвет текста
        'color_text_week': (0.5, 0, 0, 1),   # Цвет Сб и Вс
        'color_shadow': (1, 1, 1, 0.7),      # Цвет тени
        'color_high_wind': (0, 0, 0.6, 1)# Цвет сильного ветра
    },
    {   'color_text': (0.9, 0.9, 0.9, 1),    # Цвет текста
        'color_text_week': (1, 0.5, 0.5, 1), # Цвет Сб и Вс
        'color_shadow': (0, 0, 0, 0.7),      # Цвет тени
        'color_high_wind': (0.5, 0.5, 1, 1)  # Цвет сильного ветра
    },
    {   'color_text': (0.2, 0.2, 0.2, 1),    # Цвет текста
        'color_text_week': (0.5, 0, 0, 1),   # Цвет Сб и Вс
        'color_shadow': (0, 0, 0, 0),        # Цвет тени
        'color_high_wind': (0, 0, 0, 1)      # Цвет сильного ветра
    }
    ]

print 'Путь к файлу конфигурации:\n    '+os.path.join(CONFIG_PATH, 'gw_config.json')

def Save_Config():
    for i in gw_config.keys():
        gw_config[i] = globals()[i]
    json.dump(gw_config, open(os.path.join(CONFIG_PATH, 'gw_config.json'), "w"), sort_keys=True, indent=4, separators=(', ', ': '))

def Save_Color_Scheme(number = 0):
    json.dump(color_scheme[number], open(os.path.join(CONFIG_PATH, 'color_schemes', 'color_sheme_%s.json' %number), "w"), sort_keys=True, indent=4, separators=(', ', ': '))

for i in range(len(color_scheme)):
    if not os.path.exists(os.path.join(CONFIG_PATH, 'color_schemes', 'color_sheme_%s.json' %i)):
        Save_Color_Scheme(i)

def Load_Config():
    try:
        gw_config_loaded=json.load(file(os.path.join(CONFIG_PATH, 'gw_config.json')))
        for i in gw_config_loaded.keys():
            gw_config[i] = gw_config_loaded[i] # Присваиваем новые значения
    except:
        print '[!] Произошла ошибка при загрузке конфигурационного файла'

    # Создаем переменные
    for i in gw_config.keys():
        globals()[i] = gw_config[i]

# Загружаем конфиг
Load_Config()
def Load_Color_Scheme(number = 0):
    try:
        scheme_loaded=json.load(file(os.path.join(CONFIG_PATH, 'color_schemes', 'color_sheme_%s.json' %number)))
        for i in scheme_loaded.keys():
            gw_config[i] = scheme_loaded[i]
        gw_config['color_scheme_number'] = number
    except:
        print '[!] Произошла ошибка при загрузке цветовой схемы # %s' %number

    # Создаем переменные
    for i in gw_config.keys():
        globals()[i] = gw_config[i]

if not os.path.exists(os.path.join(CONFIG_PATH, 'gw_config.json')):
    Save_Config()
# ------------------------------------------------------------------------------

# Путь к виджету
#APP_PATH = os.path.dirname(__file__)

APP_PATH = os.path.dirname(sys.argv[0])
if APP_PATH == '':
    print 'Указывайте полный путь к скрипту\nВыход.'
    exit()

THEMES_PATH = os.path.join(APP_PATH, 'themes')
ICONS_PATH = os.path.join(THEMES_PATH, 'icons')
BGS_PATH = os.path.join(THEMES_PATH, 'backgrounds')
ICONS_USER_PATH = os.path.join(CONFIG_PATH, 'icons')
BGS_USER_PATH = os.path.join(CONFIG_PATH, 'backgrounds')

if not os.path.exists(os.path.join(ICONS_USER_PATH, 'default', 'weather')):
    os.makedirs(os.path.join(ICONS_USER_PATH, 'default', 'weather'))

# Вспомогательные переменные
height = None
width = None
cr = None
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

# переменные, в которые записывается погода
city_name = []       # Город
t_now = []           # Температура сейчас
wind_speed_now = []  # Скорость ветра сейчас
wind_direct_now = [] # Направление ветра сейчас
icon_now = []        # Иконка погоды сейчас
icon_wind_now = []   # Иконка ветра сейчас
time_update = []     # Время обновления погоды на сайте
text_now = []        # Текст погоды сейчас
press_now = []       # Давление сейчас
hum_now = []         # Влажность сейчас
t_water_now = []     # Температура воды сейчас

t_night = []         # Температура ночью
t_night_feel = []    # Температура ночью ощущается
day = []             # День недели
date = []            # Дата
t_day = []           # Температура днем
t_day_feel = []      # Температура днем ощущается
icon = []            # Иконка погоды
icon_wind = []       # Иконка ветра
wind_speed = []      # Скорость ветра
wind_direct = []     # Направление ветра
text = []            # Текст погоды

t_tomorrow = []      # Температура завтра
icon_tomorrow = []   # Иконка погоды завтра
wind_speed_tom = []  # Скорость ветра завтра
wind_direct_tom = [] # Направление ветра завтра

t_today = []         # Температура сегодня
icon_today = []      # Иконка погоды сегодня
wind_speed_tod = []  # Скорость ветра сегодня
wind_direct_tod = [] # Направление ветра сегодня


def get_city_name(c_id):
    try:
        source = urlopen('http://www.gismeteo.ru/city/weekly/' + str(c_id), timeout=10).read()
        c_name = re.findall('type[A-Z].*\">(.*)<', source)
    except:
        print '[!] Не удалось получить название местоположения'
        return 'None'
    return c_name[0]


def check_updates():
    print '> Проверяю наличие новой версии'
    try:
        source = urlopen('http://sourceforge.net/projects/gis-weather/files/gis-weather/', timeout=10).read()
    except:
        print '[!] Невозможно проверить обновления'
        print '-'*40
        return False
    new_ver1 = re.findall('<a href="/projects/gis-weather/files/gis-weather/(.+)/"', source)
    new_ver = new_ver1[0].split('.')
    while len(new_ver)<4:
        new_ver.append('0')
    cur_ver = v.split('.')
    while len(cur_ver)<4:
        cur_ver.append('0')

    new_v = None
    for i in range(4):
        if int(new_ver[i])>int(cur_ver[i]):
            new_v = new_ver1[0]
            break
    if new_v:
        print '>>> Доступна новая версия', new_v, '<<<'
        print '-'*40
        Gtk_update_dialog.show(v, new_v, CONFIG_PATH, APP_PATH)
        global check_for_updates_local
        check_for_updates_local = False
    else:
        print '> Текущая версия актуальна'
        print '-'*40
        if check_for_updates == 1 and check_for_updates_local:
            check_for_updates_local = False


def get_weather():
    global err_connect, splash
    global city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, icon_today, wind_speed_tod, wind_direct_tod 
    print '> Получаю погоду на', n, 'дней'
    print '> Загружаю в переменную страницу', 'http://www.gismeteo.ru/city/weekly/' + str(city_id)
    try:
        source = urlopen('http://www.gismeteo.ru/city/weekly/' + str(city_id), timeout=10).read()
        err_connect = False
        print 'OK'
    except:
        print '[!] Невозможно скачать страницу, проверьте интернет соединение'
        if timer_bool:
            print '[!] Следующая попытка через 10 секунд'
        err_connect = True
        return
    #### Текущая погода ####
    w_now = re.findall("type[A-Z].*>вода", source, re.DOTALL)
    
    # Город
    city_name = re.findall('type[A-Z].*\">(.*)<', w_now[0])

    # Температура
    t_now = re.findall('m_temp c.>([&minus;+]*\d+)<', w_now[0])
    for i in range(0, len(t_now)):
        if t_now[i][0] == '&':
            t_now[i] = '-' + t_now[i][7:]

    # Ветер
    wind_speed_now = re.findall('m_wind ms.*>(\d+)<', w_now[0])
    wind_direct_now = re.findall('<dt>([СЮЗВШ]+)</dt>', w_now[0])

    # Иконка
    icon_now = re.findall('url\(.*?new\/(.+)\)', w_now[0])
    
    #Иконка ветра
    icon_wind_now = re.findall('wind(\d)', w_now[0])

    # Время обновления
    time_update = re.findall('data-hr.* (\d?\d:\d\d)\s*</span>', source, re.DOTALL)
    
    # Текст погоды сейчас
    text_now = re.findall('title=\"(.*?)\"', w_now[0])
    
    # Давление сейчас
    press_now = re.findall('m_press torr\'>(\d+)<', w_now[0])
    
    # Влажность сейчас
    hum_now = re.findall('Влажность">(\d+)<', w_now[0])
    
    # Температура воды сейчас
    try:
        t_water_now = t_now[1]
    except:
        pass
    
    #### Погода на неделю ####
    # Погода ночью
    w_night_list = re.findall('Ночь</th>.*?>Утро</th>', source, re.DOTALL)
    w_night = '\n'.join(w_night_list)
    
    # Температура ночью
    t_night = re.findall('m_temp c.>([&minus;+]*\d+)<', w_night)
    for i in range(0, len(t_night)):
        if t_night[i][0] == '&':
            t_night[i] = '-' + t_night[i][7:]
    t_night_feel = t_night[1::2]
    t_night = t_night[::2]
    
    # День недели и дата
    day = re.findall('weekday.>(.*?)<', source)
    date = re.findall('s_date.>(.*?)<', source)
    
    # Погода днем
    w_day_list = re.findall('День</th>.*?>Вечер</th>', source, re.DOTALL)
    w_day = '\n'.join(w_day_list)
    
    # Температура днем
    t_day = re.findall('m_temp c.>([&minus;+]*\d+)<', w_day) 
    for i in range(0, len(t_day)):
        if t_day[i][0] == '&':
            t_day[i] = '-' + t_day[i][7:]
    t_day_feel = t_day[1::2]
    t_day = t_day[::2]
    
    # Иконка погоды днем
    icon = re.findall('src=\".*?new\/(.*?)\"', w_day)
    
    # Иконка ветра
    icon_wind = re.findall('wind(\d)', w_day)
    
    # Ветер
    wind_speed = re.findall('m_wind ms.>(\d+)', w_day)
    wind_direct = re.findall('>([СЮЗВШ]+)<', w_day)

    # Текст погоды
    text = re.findall('cltext.>(.*?)<', w_day)

    if show_block_tomorrow:
        #### Погода завтра ####
        w_tomorrow = re.findall('Ночь</th>.*?>Ночь</div>', source, re.DOTALL)
        
        # Температура
        t_tomorrow = re.findall('m_temp c.>([&minus;+]*\d+)<', w_tomorrow[1])
        for i in range(0, len(t_tomorrow)):
            if t_tomorrow[i][0] == '&':
                t_tomorrow[i] = '-' + t_tomorrow[i][7:]

        # Иконка погоды
        icon_tomorrow = re.findall('src=\".*?new\/(.*?)\"', w_tomorrow[1])

        # Ветер
        wind_speed_tom = re.findall('m_wind ms.>(\d+)', w_tomorrow[1])
        wind_direct_tom = re.findall('>([СЮЗВШ]+)<', w_tomorrow[1])
        
    if show_block_today:
        #### Погода сегодня ####
        if not show_block_tomorrow:
            w_tomorrow = re.findall('Ночь</th>.*?>Ночь</div>', source, re.DOTALL)
        
        # Температура
        t_today = re.findall('m_temp c.>([&minus;+]*\d+)<', w_tomorrow[0])
        for i in range(0, len(t_today)):
            if t_today[i][0] == '&':
                t_today[i] = '-' + t_today[i][7:]
        
        # Иконка погоды
        icon_today = re.findall('src=\".*?new\/(.*?)\"', w_tomorrow[0])

        # Ветер
        wind_speed_tod = re.findall('m_wind ms.>(\d+)', w_tomorrow[0])
        wind_direct_tod = re.findall('>([СЮЗВШ]+)<', w_tomorrow[0])
    ########
    
    if time_update:
        print '> Обновление на сервере в', time_update[0]
    print '> Погода получена в', time.strftime('%H:%M', time.localtime())

    if splash:
        splash = False


class MyDrawArea(gtk.DrawingArea):
    p_layout = None
    p_fdesc = None

    def __init__(self):
        self.timer = timeout_add(1000, self.redraw)
        gtk.DrawingArea.__init__(self)
        self.set_app_paintable(True)
        self.connect('expose_event', self.expose)

    def splash_screen(self, state = 0):
        if show_splash_screen == 0:
            return
        global try_no
        if max_try_show != 0 and try_no >= max_try_show:
            return
        self.draw_bg()
        if show_splash_screen != 1:
            self.draw_scaled_image(width/2 - 64, height/2 - 128, os.path.join(APP_PATH, 'icon.png'), 128, 128)
            self.draw_text('Gis Weather v ' + v, 0, height/2 - 8, font+' Normal', 14, width, pango.ALIGN_CENTER)
            if state == 0:
                self.draw_text('Получаю погоду...', 0, height/2 + 40, font+' Normal', 10, width, pango.ALIGN_CENTER)
            else:
                try_no += 1
                self.draw_text('Ошибка при получении погоды. Попытка № ' + str(try_no), 0, height/2 + 40, font+' Normal', 10, width, pango.ALIGN_CENTER)
                if city_id == 0:
                    self.draw_text('Местоположение не настроено', 0, height/2 + 60, font+' Normal', 10, width, pango.ALIGN_CENTER)


    def redraw(self, timer1 = True, get_weather1 = True, load_config = False):
        global first_start, on_redraw, timer_bool, get_weather_bool
        if load_config:
            Load_Config()
            app.set_window_properties()
        timer_bool = timer1
        get_weather_bool = get_weather1
        on_redraw = True
        expose_event = gtk.gdk.Event(gtk.gdk.EXPOSE)
        expose_event.window = self.window
        if first_start:
            first_start = False
        self.send_expose(expose_event)
        while gtk.events_pending():
            gtk.main_iteration_do(True)
        if get_weather1 and check_for_updates_local and not err_connect:
            check_updates()

    
    def clear_draw_area(self, widget):
        self.cr = widget.window.cairo_create()
        self.cr.save()
        if fix_BadDrawable:
            self.cr.set_source_rgba(1, 1, 1, 0.01)
        else:
            self.cr.set_source_rgba(1, 1, 1, 0)
        self.cr.set_operator(cairo.OPERATOR_SOURCE)
        self.cr.paint()
        
        self.cr.restore()
    
    
    def expose(self, widget, event):
        global err, on_redraw, get_weather_bool
        if err == False:
            self.clear_draw_area(widget)
        if first_start:
            self.splash_screen()
            return
        if get_weather_bool:
            get_weather()
            get_weather_bool = False
            if not timer_bool:
                print '-'*40
        if err_connect:
            if on_redraw:
                on_redraw = False
                if timer_bool:
                    self.timer = timeout_add(10000, self.redraw)
            print '-'*40
            if splash:
                self.splash_screen(1)
            else:
                if err == False:
                    self.Draw_Weather()
                    self.draw_scaled_image(margin + 10, margin + 10, os.path.join(THEMES_PATH, 'error.png'),24,24)
                    self.draw_text('Ошибка соединения', margin + 35, margin + 14, font+' Normal', 10, color = color_text_week)
                    err = True
        else:
            if err == True:
                err = False
                self.clear_draw_area(widget)
            if on_redraw:
                on_redraw = False
                if timer_bool:
                    self.timer = timeout_add(upd_time*60*1000, self.redraw)
                    print '> Следующее обновление через', upd_time, 'минут'
                    print '-'*40
            self.Draw_Weather()

    
    def Draw_Weather(self):
        self.draw_bg()
        self.draw_weather_icon_now(0, 20 + margin)
        
        for i in range(1, n+1):
            self.draw_weather_icon(i, margin + block_margin + (i-1)*w_block + (i-1)*(10+10/(n-2)), height-h_block-10 - margin)
        

    def draw_weather_icon_now(self, x, y):
        if day != []:
            center = x+width/2
            
            if (day and date):
                if day[0] in ('Сб', 'Вс'):
                    self.draw_text(day[0]+', '+date[0], 0, y-15, font+' Bold', 12, width, pango.ALIGN_CENTER, color_text_week)
                else:
                    self.draw_text(day[0]+', '+date[0], 0, y-15, font+' Bold', 12, width, pango.ALIGN_CENTER)
            
            if show_time_receive:
                if time_update: self.draw_text('обновление на сервере '+time_update[0], x-margin, x+18+margin, font+' Normal', 8, width-10,pango.ALIGN_RIGHT)
                self.draw_text('погода получена '+time.strftime('%H:%M', time.localtime()), x-margin, x+8+margin, font+' Normal', 8, width-10,pango.ALIGN_RIGHT)
            if city_name: self.draw_text(city_name[0], x+0, y, font+' Bold', 14, width, pango.ALIGN_CENTER)
            self.draw_scaled_icon(center-40, y+30, os.path.join(ICONS_PATH, icons_name, 'weather', icon_now[0]),80,80)
            if t_now: self.draw_text(t_now[0]+'°', center-100, y+30, font+' Normal', 18, 60, pango.ALIGN_RIGHT)
            if text_now: self.draw_text(text_now[0], center-70, y+106, font+' Normal', 10, 140, pango.ALIGN_CENTER)
            
            if show_block_wind_direct:
                ####-Блок направление ветра-####
                left = block_wind_direct_left
                top = y + 30 #50 + margin
                r = 31     #радиус окружности
                a = 36     #ширина и высота стрелки (a < 2*r)
                font_NS = 8 # шрифт сторон горизонта
                font_wind = 10
                if wind_direct_small:
                    left = block_wind_direct_left+90#-85
                    top = y + 55 #75 + margin
                    r = 16    #радиус окружности
                    a = 20     #ширина и высота стрелки (a < 2*r)
                    font_NS = 6 # шрифт сторон горизонта
                    font_wind = 7
                ################################

                NS = ('В', 'Ю', 'З', 'С')
                x0 = center + left+a
                y0 = top + r
                angel_rad = angel*math.pi/180
                if (wind_direct_now and wind_speed_now):
                    for i in range(0, 8):
                        if i % 2 == 0:
                            self.draw_text(NS[i/2], x0+r*math.cos(i*0.25*math.pi+angel_rad), y0+r*math.sin(i*0.25*math.pi+angel_rad), font+' Bold', font_NS, 10, pango.ALIGN_LEFT)
                    if int(wind_speed_now[0]) >= high_wind:
                        self.draw_text(wind_direct_now[0]+', '+wind_speed_now[0]+' м/с', x0-r-5, y0+r+font_wind+4, font+' Normal', font_wind, 2*r+10+font_NS,pango.ALIGN_CENTER, color_high_wind)
                    else:
                        self.draw_text(wind_direct_now[0]+', '+wind_speed_now[0]+' м/с', x0-r-5, y0+r+font_wind+4, font+' Normal', font_wind, 2*r+10+font_NS,pango.ALIGN_CENTER)
                wind_icon = 0
                if icon_wind_now[0] != '0': 
                    wind_icon = int(icon_wind_now[0])*45+45
                    if os.path.exists(os.path.join(ICONS_PATH, icons_name, 'wind.png')):
                        self.draw_scaled_image(x0-a/2+font_NS/2, y0-a/2+1+font_NS/2, os.path.join(ICONS_PATH, icons_name, 'wind.png'), a, a, wind_icon+angel)
                    else:
                        self.draw_scaled_image(x0-a/2+font_NS/2, y0-a/2+1+font_NS/2, os.path.join(ICONS_PATH, 'default', 'wind.png'), a, a, wind_icon+angel)
            
            if show_block_add_info:    
                ####-Блок с доп инфо-####
                left = block_add_info_left
                top = y + 30 # 50 + margin
                line_height = 25  #отступ между строк
                #########################
                
                x0 = center + left
                y0 = top
                
                if not show_block_wind_direct:
                    wind_icon = 0
                    if icon_wind_now[0] != '0': 
                        wind_icon = int(icon_wind_now[0])*45+45
                if wind_icon != 0:
                    if os.path.exists(os.path.join(ICONS_PATH, icons_name, 'wind_small.png')):
                        self.draw_scaled_image(x0, y0, os.path.join(ICONS_PATH, icons_name, 'wind_small.png'), 16, 16, wind_icon+angel)
                    else:
                        self.draw_scaled_image(x0, y0, os.path.join(ICONS_PATH, 'default', 'wind_small.png'), 16, 16, wind_icon+angel)
                if (wind_direct_now and wind_speed_now):
                    if int(wind_speed_now[0]) >= high_wind:
                        self.draw_text(wind_speed_now[0]+"<span size='x-small'> м/с</span>  <span size='small'>%s</span>"%wind_direct_now[0], x0+20, y0-1, font+' Normal', 12, 100,pango.ALIGN_LEFT, color_high_wind)
                    else:
                        self.draw_text(wind_speed_now[0]+"<span size='x-small'> м/с</span>  <span size='small'>%s</span>"%wind_direct_now[0], x0+20, y0-1, font+' Normal', 12, 100,pango.ALIGN_LEFT)
                if os.path.exists(os.path.join(ICONS_PATH, icons_name, 'press.png')):
                    self.draw_scaled_image(x0, y0+line_height, os.path.join(ICONS_PATH, icons_name, 'press.png'), 16, 16)
                else:
                    self.draw_scaled_image(x0, y0+line_height, os.path.join(ICONS_PATH, 'default', 'press.png'), 16, 16)
                if press_now:
                    self.draw_text(press_now[0]+"<span size='x-small'> мм рт.ст.</span>", x0+20, y0+line_height-1, font+' Normal', 12, 100,pango.ALIGN_LEFT)
                if os.path.exists(os.path.join(ICONS_PATH, icons_name, 'hum.png')):
                    self.draw_scaled_image(x0, y0+line_height*2, os.path.join(ICONS_PATH, icons_name, 'hum.png'), 16, 16)
                else:
                    self.draw_scaled_image(x0, y0+line_height*2, os.path.join(ICONS_PATH, 'default', 'hum.png'), 16, 16)
                if hum_now:
                    self.draw_text(hum_now[0]+"<span size='x-small'> % влажн.</span>", x0+20, y0+line_height*2-1, font+' Normal', 12, 100,pango.ALIGN_LEFT)
                if os.path.exists(os.path.join(ICONS_PATH, icons_name, 't_water.png')):
                    self.draw_scaled_image(x0, y0+line_height*3, os.path.join(ICONS_PATH, icons_name, 't_water.png'), 16, 16)
                else:
                    self.draw_scaled_image(x0, y0+line_height*3, os.path.join(ICONS_PATH, 'default', 't_water.png'), 16, 16)
                if t_water_now:
                    self.draw_text(t_water_now+"<span size='x-small'> °C вода</span>", x0+20, y0+line_height*3-1, font+' Normal', 12, 100,pango.ALIGN_LEFT)
            
            if show_block_tomorrow:
                ####-Блок погоды на завтра-####
                left = block_tomorrow_left
                top = y + 30 # 50 + margin
                a = 70
                b = 53
                b_width = a+60
                ###############################
                
                x0 = center + left
                y0 = top
                c = ('Ночь', 'Утро', 'День', 'Вечер')
                
                self.draw_text('Завтра', x0, y0-13, font+' Bold', 8, a+60,pango.ALIGN_CENTER)
                for i in range(0, 4):
                    j = i
                    if j > 1: j = j-2
                    self.draw_text(c[i], x0+a*((j+1)/2), y0+b*(i/2), font+' Bold', 7, 50,pango.ALIGN_LEFT)
                    if t_tomorrow:
                        if t_feel:
                            self.draw_text(t_tomorrow[1::2][i]+'°', x0+a*((j+1)/2), y0+13+b*(i/2), font+' Normal', 8, 50,pango.ALIGN_LEFT)
                        else:
                            self.draw_text(t_tomorrow[::2][i]+'°', x0+a*((j+1)/2), y0+13+b*(i/2), font+' Normal', 8, 50,pango.ALIGN_LEFT)
                    self.draw_scaled_icon(x0+32+a*((j+1)/2), y0+b*(i/2), os.path.join(ICONS_PATH, icons_name, 'weather', icon_tomorrow[i]), 28, 28)
                    if (wind_direct and wind_speed): 
                        if int(wind_speed_tom[i]) >= high_wind:
                            self.draw_text(wind_direct_tom[i]+', '+wind_speed_tom[i]+' м/с', x0+a*((j+1)/2), y0+27+b*(i/2), font+' Normal', 7, 50,pango.ALIGN_LEFT, color_high_wind)
                        else:
                            self.draw_text(wind_direct_tom[i]+', '+wind_speed_tom[i]+' м/с', x0+a*((j+1)/2), y0+27+b*(i/2), font+' Normal', 7, 50,pango.ALIGN_LEFT)


            if show_block_today:
                ####-Блок погоды на сегодня-####
                left = block_today_left
                top = y + 30 # 50 + margin
                a = 70
                b = 53
                b_width = a+60
                ###############################
                
                x0 = center + left
                y0 = top
                c = ('Ночь', 'Утро', 'День', 'Вечер')
                
                self.draw_text('Сегодня', x0, y0-13, font+' Bold', 8, a+60,pango.ALIGN_CENTER)
                for i in range(0, 4):
                    j = i
                    if j > 1: j = j-2
                    self.draw_text(c[i], x0+a*((j+1)/2), y0+b*(i/2), font+' Bold', 7, 50,pango.ALIGN_LEFT)
                    if t_tomorrow:
                        if t_feel:
                            self.draw_text(t_today[1::2][i]+'°', x0+a*((j+1)/2), y0+13+b*(i/2), font+' Normal', 8, 50,pango.ALIGN_LEFT)
                        else:
                            self.draw_text(t_today[::2][i]+'°', x0+a*((j+1)/2), y0+13+b*(i/2), font+' Normal', 8, 50,pango.ALIGN_LEFT)
                    self.draw_scaled_icon(x0+32+a*((j+1)/2), y0+b*(i/2), os.path.join(ICONS_PATH, icons_name, 'weather', icon_today[i]), 28, 28)
                    if (wind_direct and wind_speed): 
                        if int(wind_speed_tod[i]) >= high_wind:
                            self.draw_text(wind_direct_tod[i]+', '+wind_speed_tod[i]+' м/с', x0+a*((j+1)/2), y0+27+b*(i/2), font+' Normal', 7, 50,pango.ALIGN_LEFT, color_high_wind)
                        else:
                            self.draw_text(wind_direct_tod[i]+', '+wind_speed_tod[i]+' м/с', x0+a*((j+1)/2), y0+27+b*(i/2), font+' Normal', 7, 50,pango.ALIGN_LEFT)


    def draw_weather_icon(self, index, x, y):
        if day != []:
            a = 30
            if t_feel:
                if math.fabs(int(t_day_feel[index])) < 10: a = 20
            else:
                if math.fabs(int(t_day[index])) < 10: a = 20
            self.draw_scaled_icon(x+a, y+16, os.path.join(ICONS_PATH, icons_name, 'weather', icon[index]), 36, 36)
            if (day and date): 
                if day[index] in ('Сб', 'Вс'):
                    self.draw_text(day[index]+', '+date[index], x, y-2, font+' Bold', 9, w_block,pango.ALIGN_LEFT, color_text_week)
                else:
                    self.draw_text(day[index]+', '+date[index], x, y-2, font+' Bold', 9, w_block,pango.ALIGN_LEFT)
            self.cr.set_source_rgba(color_text[0], color_text[1], color_text[2], color_text[3])
            if t_feel:
                if t_day_feel: self.draw_text(t_day_feel[index]+'°', x, y+15, font+' Normal', 10, w_block-45,pango.ALIGN_LEFT)
                if t_night_feel: self.draw_text(t_night_feel[index]+'°', x, y+30, font+' Normal', 8, w_block-45,pango.ALIGN_LEFT)
            else:
                if t_day: self.draw_text(t_day[index]+'°', x, y+15, font+' Normal', 10, w_block-45,pango.ALIGN_LEFT)
                if t_night: self.draw_text(t_night[index]+'°', x, y+30, font+' Normal', 8, w_block-45,pango.ALIGN_LEFT)
            if (wind_direct and wind_speed): 
                if int(wind_speed[index]) >= high_wind:
                    self.draw_text(wind_direct[index]+', '+wind_speed[index]+' м/с', x, y+50, font+' Normal', 8, 80,pango.ALIGN_LEFT, color_high_wind)
                else:
                    self.draw_text(wind_direct[index]+', '+wind_speed[index]+' м/с', x, y+50, font+' Normal', 8, 80,pango.ALIGN_LEFT)
            if text: self.draw_text(text[index], x, y+65, font+' Italic', 7, w_block, pango.ALIGN_LEFT)


    def draw_bg(self):
        if show_bg_png:
            if not_composited:
                if os.path.exists(os.path.join(CONFIG_PATH, 'screenshot.png')):
                    self.draw_scaled_image(0, 0, os.path.join(CONFIG_PATH, 'screenshot.png'), width, height)
            if os.path.exists(os.path.join(BGS_USER_PATH, bg_custom)):
                self.draw_scaled_image(0, 0, os.path.join(BGS_USER_PATH, bg_custom), width, height)
            else: 
                if os.path.exists(os.path.join(BGS_PATH, bg_custom)):
                    self.draw_scaled_image(0, 0, os.path.join(BGS_PATH, bg_custom), width, height)
                else:
                    print 'Не найдено фоновое изображение:', bg_custom
        else:
            w = width
            h = height
            self.cr.set_source_rgba(color_bg[0], color_bg[1], color_bg[2], color_bg[3])
            self.cr.rectangle(r, 0, w-2*r, h)
            self.cr.rectangle(0, r, w, h-2*r)
            self.cr.arc(w-r, 0+r, r, 0 , 8)
            self.cr.arc(w-r, 0+r, r, 0 , 8)
            self.cr.arc(w-r, h-r, r, 0, 8)
            self.cr.arc(0+r, h-r, r, 0, 8)
            self.cr.arc(0+r, 0+r, r, 0, 8)
            self.cr.fill()
    
    def draw_text(self, text, x, y,  font, size = None, width = 200, allignment=pango.ALIGN_LEFT, color = (-1, -1, -1, -1)):
        if color == (-1, -1, -1, -1):
            color = color_text
        if draw_shadow:
            self.cr.set_source_rgba(color_shadow[0], color_shadow[1], color_shadow[2], color_shadow[3])
            self.draw_text_Whise(text, x+1, y+1,  font, size , width, allignment)
        self.cr.set_source_rgba(color[0], color[1], color[2], color[3])
        self.draw_text_Whise(text, x, y,  font, size , width, allignment)
        
    def draw_text_Whise(self, text, x, y,  font, size = None, width = 200, allignment=pango.ALIGN_LEFT,alignment=None,justify = False,weight = None, ellipsize = pango.ELLIPSIZE_NONE):
        """Draws text"""
        if size is not None:
            size = int(size)

        self.cr.save()
        self.cr.translate(x, y)
        if self.p_layout == None :
    
            self.p_layout = self.cr.create_layout()
        else:
            
            self.cr.update_layout(self.p_layout)
        if self.p_fdesc == None:self.p_fdesc = pango.FontDescription(font)
        else: pass
        # using "Ubuntu Bold 12" is new standard, detecting spaces is lousy, but no better idea
        if font.find(" ") >= 0:
            self.p_fdesc = pango.FontDescription(font)
        # but we should keep old standard describing just font family "Ubuntu"
        # this is probably not needed, but max compatibility!!!
        else:
            self.p_fdesc.set_family_static(font)
        if size is not None:
            self.p_fdesc.set_size(size * pango.SCALE)
        if weight is not None:
            self.p_fdesc.set_weight(weight)
        self.p_layout.set_font_description(self.p_fdesc)
        self.p_layout.set_width(width * pango.SCALE)
        self.p_layout.set_alignment(allignment)
        if alignment != None:self.p_layout.set_alignment(alignment)
        self.p_layout.set_justify(justify)
        self.p_layout.set_ellipsize(ellipsize)
        self.p_layout.set_markup(text)
        self.cr.show_layout(self.p_layout)
        self.cr.restore()


    def draw_scaled_icon(self, x, y, pix, w, h):
        if icons_name == 'default':
            pix = os.path.join(ICONS_USER_PATH, 'default', 'weather', os.path.split(pix)[1])
        if icons_name == 'default' and not os.path.exists(pix):
            try:
                print '> скачиваю', os.path.split(pix)[1]
                urlretrieve('http://st8.gisstatic.ru/static/images/icons/new/'+os.path.split(pix)[1], pix)
            except:
                print 'Не удалось скачать', 'http://st8.gisstatic.ru/static/images/icons/new/'+os.path.split(pix)[1]
            if not os.path.exists(pix):
                pix = os.path.join(THEMES_PATH, 'na.png')
            self.draw_scaled_image(x, y, pix, w, h)
            return
        
        if not os.path.exists(pix):
            pix_convert = pix.split('.')
            for i in range(2, 5):
                try:
                    a = int(pix_convert[-i][1])
                    a = (a+1)/2+(a+1)/2
                    pix_convert[-i] = pix_convert[-i][0]+str(a) # вместо четырех состояний, делаем два: 2 и 4
                except:
                    pass    
            pix = '.'.join(pix_convert)
            
            pix_convert = os.path.split(pix)
            pix_convert = pix_convert[1].split('.')
            if pix_convert[2] == 'c4': # за тучами не видно: солнце там или луна (иконки только для солнца)
                pix_convert[0] = 'd'
                pix_convert[1] = 'sun'
            if pix_convert[-2] == 'st' and pix_convert[-3] == 'r4': #гроза и дождь 2 и 4 - одинаковая иконка
                pix_convert[-3] = 'r2'
            if pix_convert[-3] == 'c2' and pix_convert[-2] != 'st': #при облаках c2 дождь 2 и 4 одинаковый
                pix_convert[-2] = pix_convert[-2][0] +'2'
            if pix_convert[1] == 'mist' and pix_convert[2] != 'png':
                pix_convert[0] = 'd.sun'
                pix_convert[1] = 'c4'
            
            pix = os.path.join(ICONS_PATH, icons_name, 'weather', '.'.join(pix_convert))
            
            
            if not os.path.exists(pix):
                pix = os.path.join(ICONS_USER_PATH, icons_name, 'weather', '.'.join(pix_convert))
                if not os.path.exists(pix):
                    print '[!] отсутстует иконка:\n>', os.path.join(icons_name, 'weather', '.'.join(pix_convert))
                    if os.path.exists(os.path.join(ICONS_PATH, icons_name, 'weather', 'na.png')):
                        pix = os.path.join(ICONS_PATH, icons_name, 'weather', 'na.png')
                    else:
                        if os.path.exists(os.path.join(ICONS_USER_PATH, icons_name, 'weather', 'na.png')):
                            pix = os.path.join(ICONS_USER_PATH, icons_name, 'weather', 'na.png')
                        else:
                            pix = os.path.join(THEMES_PATH, 'na.png')
            
        self.draw_scaled_image(x, y, pix, w, h)
    
    def draw_scaled_image(self, x, y, pix, w, h, ang = 0):
        """Draws a picture from specified path with a certain width and height"""
        w = int(w)
        h = int(h)

        self.cr.save()
        
        if ang !=0:
            self.cr.translate(x+w/2, y+h/2)
            self.cr.rotate(math.radians(ang))
            self.cr.translate(-w/2, -h/2)
        else:
            self.cr.translate(x, y)    
        pixbuf = gtk.gdk.pixbuf_new_from_file(pix).scale_simple(w,h,gtk.gdk.INTERP_HYPER)
        format = cairo.FORMAT_RGB24
        if pixbuf.get_has_alpha():
            format = cairo.FORMAT_ARGB32

        iw = pixbuf.get_width()
        ih = pixbuf.get_height()
        image = cairo.ImageSurface(format, iw, ih)

        matrix = cairo.Matrix(xx=iw/w, yy=ih/h)
        self.cr.set_operator(cairo.OPERATOR_OVER)
        image = self.cr.set_source_pixbuf(pixbuf, 0, 0)
        if image != None :image.set_matrix(matrix)
        
        self.cr.paint()
        puxbuf = None
        image = None
        self.cr.restore()


class Weather_Widget:

    menu = None

    def __init__(self):
        #global x_pos, y_pos
        #global output_display
        #global margin

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_accept_focus(False)

        self.set_window_properties()
        # width = w_block*n + block_margin*2 + 10*(n - 1) + 2*margin
        # height = 260 + block_margin + 2*margin
        print 'Размеры виджета:'
        print '    ширина =', width, 'высота =', height, 'в т.ч. отступ =', margin
        # self.window.resize(width, height)

        # Нужно ли?
        # try:
        #     screen = subprocess.Popen('xrandr | grep " connected"', shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        #     screen = screen.stdout.readlines()
        #     if output_display < 0: output_display = 0
        #     if output_display >= len(screen): output_display = len(screen) - 1
        #     print 'Найденные дисплеи:'
        #     for i in range (0, len(screen)):
        #         if i == output_display:
        #             print '  * '+str(i)+':', screen[i].split()[0], screen[i].split()[2].split('+')[0]
        #         else:
        #             print '    '+str(i)+':', screen[i].split()[0], screen[i].split()[2].split('+')[0]
        #     screen_width = int(screen[output_display].split()[2].split('x')[0])
        #     screen_height = int(screen[output_display].split()[2].split('x')[1].split('+')[0])
        #     hoffset = int(screen[output_display].split()[2].split('+')[1])
        #     voffset = int(screen[output_display].split()[2].split('+')[2])
        # except:
        #     screen_width = gtk.gdk.screen_width()
        #     screen_height = gtk.gdk.screen_height()
        #     voffset = 0
        #     hoffset = 0
        # if x_pos >= 0: x_pos1 = hoffset + x_pos
        # else: x_pos1 = hoffset + screen_width - width + x_pos + margin
        
        # if y_pos >= 0: y_pos1 = voffset + y_pos
        # else: y_pos1 = voffset + screen_height - height + y_pos + margin
        
        
        self.window.set_decorated(False)

        global not_composited

        if not self.window.is_composited():
            not_composited = True
            self.screenshot(x_pos, y_pos, width, height)

        self.window.set_events(gtk.gdk.ALL_EVENTS_MASK)
        self.window.connect('button-press-event', self.button_press)
        self.window.connect("configure-event", self.configure_event)

        self.window.connect("destroy", gtk.main_quit)
        self.window.connect("screen-changed", self.screen_changed)
        self.window.set_role('')
        self.window.set_app_paintable(True)
        if os.environ.get('DESKTOP_SESSION') == "ubuntu":
            self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DOCK)
        else:
            self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_UTILITY)
        self.window.set_keep_above(False)
        self.window.set_keep_below(True)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_skip_pager_hint(True)

        self.drawing_area = MyDrawArea()
        self.window.add(self.drawing_area)
        self.screen_changed(self.window)

    def set_window_properties(self):
        global n
        global width, height

        if n > 13: n = 13
        if n < 1: n = 1
        width = w_block*n + block_margin*2 + 10*(n - 1) + 2*margin
        height = 260 + block_margin + 2*margin
        self.window.resize(width, height)
        self.window.move(x_pos, y_pos)
        if sticky:
            self.window.stick()
        else:
            self.window.unstick()
        self.window.set_opacity(opacity)

    def create_menu(self):
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
        global icons_list, backgrounds_list
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
        menu_items.connect("activate", self.redraw_icons, 'default')
        menu_items.show()
        for i in range(len(icons_list)):
            buf = icons_list[i].split('_') # из _ делаем __ (отображается как _)
            buf = '__'.join(buf)
            menu_items = gtk.RadioMenuItem(group, str(i+1)+'. '+buf)
            if icons_name == icons_list[i]:
                menu_items.set_active(True)
            group = menu_items
            sub_menu_icons.append(menu_items)
            menu_items.connect("activate", self.redraw_icons, icons_list[i])
            menu_items.show()

        # Фоны
        group = None
        menu_items = gtk.RadioMenuItem(group, '0. Нет')
        if show_bg_png == False and color_bg[3]==0:
            menu_items.set_active(True)
        group = menu_items
        sub_menu_bgs.append(menu_items)
        menu_items.connect("activate", self.redraw_bg, 'Нет')
        menu_items.show()
        for i in range(len(backgrounds_list)):
            buf = backgrounds_list[i].split('_')
            buf = '__'.join(buf)
            menu_items = gtk.RadioMenuItem(group, str(i+1)+'. '+buf)
            if bg_custom == backgrounds_list[i]:
                menu_items.set_active(True)
            group = menu_items
            sub_menu_bgs.append(menu_items)
            menu_items.connect("activate", self.redraw_bg, backgrounds_list[i])
            menu_items.show()

        # Цвет текста
        group = None
        for i in range(len(color_scheme)):
            menu_items = gtk.RadioMenuItem(group, 'Цветовая схема #' + str(i))
            if i == color_scheme_number:
                menu_items.set_active(True)
            group = menu_items
            sub_menu_color_text.append(menu_items)
            menu_items.connect("activate", self.redraw_text, i)
            menu_items.show()
        # menu_items = gtk.SeparatorMenuItem()
        # sub_menu_color_text.append(menu_items)
        # menu_items.show()
        # menu_items = gtk.MenuItem('Выбрать шрифт...')
        # sub_menu_color_text.append(menu_items)
        # menu_items.connect("activate", self.menu_response, 'choose_font')
        # menu_items.show()

        # sub_menu_place
        group = None
        if len(city_id_add) > 0:
            for i in range(len(city_id_add)):
                menu_items = gtk.RadioMenuItem(group, city_id_add[i].split(';')[1])
                if city_id_add[i].split(';')[0] == str(city_id):
                    menu_items.set_active(True)
                group = menu_items
                sub_menu_place.append(menu_items)
                menu_items.connect("activate", self.reload, city_id_add[i])
                menu_items.show()
            menu_items = gtk.SeparatorMenuItem()
            sub_menu_place.append(menu_items)
            menu_items.show()

        menu_items = gtk.MenuItem('Настроить...')
        sub_menu_place.append(menu_items)
        menu_items.connect("activate", self.edit_city_id)
        menu_items.show()

        sub_menu_window
        menu_items = gtk.CheckMenuItem('Зафиксировать')
        menu_items.set_active(fix_position)
        menu_items.connect("activate", self.menu_response, 'fix')
        sub_menu_window.append(menu_items)
        menu_items.show()

        menu_items = gtk.CheckMenuItem('На всех рабочих столах')
        menu_items.set_active(sticky)
        menu_items.connect("activate", self.menu_response, 'sticky')
        sub_menu_window.append(menu_items)
        menu_items.show()

        # main menu
        menu_items = gtk.ImageMenuItem(gtk.STOCK_REFRESH)
        menu.append(menu_items)
        menu_items.connect("activate", self.reload)
        menu_items.show()

        menu_items = gtk.SeparatorMenuItem()
        menu.append(menu_items)
        menu_items.show()

        menu_items = gtk.MenuItem('Местоположение')
        menu.append(menu_items)
        menu_items.set_submenu(sub_menu_place)
        menu_items.show()

        menu_items = gtk.MenuItem('Иконки')
        menu.append(menu_items)
        menu_items.set_submenu(sub_menu_icons)
        menu_items.show()
        
        menu_items = gtk.MenuItem('Фон')
        menu.append(menu_items)
        menu_items.set_submenu(sub_menu_bgs)
        menu_items.show()
        
        menu_items = gtk.MenuItem('Текст')
        menu.append(menu_items)
        menu_items.set_submenu(sub_menu_color_text)
        menu_items.show()

        menu_items = gtk.MenuItem('Окно')
        menu.append(menu_items)
        menu_items.set_submenu(sub_menu_window)
        menu_items.show()

        menu_items = gtk.ImageMenuItem(gtk.STOCK_PROPERTIES)
        menu.append(menu_items)
        menu_items.connect("activate", self.menu_response, 'setup')
        menu_items.show()
        
        # menu_items = gtk.MenuItem('Редактировать...')
        # menu.append(menu_items)
        # menu_items.connect("activate", self.menu_response, 'edit')
        # menu_items.show()

        menu_items = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        menu.append(menu_items)
        menu_items.connect("activate", self.menu_response, 'about')
        menu_items.show()

        menu_items = gtk.SeparatorMenuItem()
        menu.append(menu_items)
        menu_items.show()

        menu_items = gtk.ImageMenuItem(gtk.STOCK_CLOSE)
        menu.append(menu_items)
        menu_items.connect("activate", gtk.main_quit)
        menu_items.show()
        return menu

    def screenshot(self, left, top, width, height):
        w = gtk.gdk.get_default_root_window()
        #sz = w.get_size()
        #print "The size of the window is %d x %d" % sz
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,True,8,width,height)
        pb = pb.get_from_drawable(w,w.get_colormap(),left,top,0,0,width,height)
        if (pb != None):
            pb.save(os.path.join(CONFIG_PATH, "screenshot.png"),"png")
            print "Screenshot saved to", os.path.join(CONFIG_PATH, "screenshot.png")
        else:
            print "Unable to get the screenshot."


    def menu_response(self, widget, event, value=None):
        if event == 'about':
            about = gtk.AboutDialog()
            about.set_program_name('Gis Weather')
            about.set_version(v)
            about.set_copyright('(С) 2013 - 2014 Alexander Koltsov')
            about.set_comments('Погодный виджет')
            about.set_website('http://sourceforge.net/projects/gis-weather/')
            about.set_logo(gtk.gdk.pixbuf_new_from_file_at_size(os.path.join(APP_PATH, 'icon.png'), 128, 128))
            about.set_license(license)
            about.set_wrap_license(False)
            about.set_authors(['Alexander Koltsov <ringov@mail.ru>\n',
                'draw_scaled_image, draw_text_Whise\nby Helder Fraga aka Whise <helder.fraga@hotmail.com>\n',
                'Помощь и идеи:\n    Karbunkul\n    Haron Prime\n    Yuriy_Y'])
            about.set_artists(['backgrounds:',
                'LightEasyShadow, LightWhiteShadow, DarkEasyShadow, DarkWithFlare',
                'by wfedin',
                '-------------------------------\n'
                'icons:',
                'colorful, flat_colorful, light, flat_white, dark, flat_black',
                'by ~MerlinTheRed',
                'http://merlinthered.deviantart.com/art/plain-weather-icons-157162192\n',
                'tick by xiao4',
                'http://www.deviantart.com/art/tick-weather-icons-96294478\n',
                'weezle by d3stroy',
                'http://www.deviantart.com/art/Weezle-Weather-Icons-187306753\n'])
            #about.set_translator_credits('')
            #about.set_documenters('')
            about.run()
            about.destroy()
            return
        # if event == 'choose_font':
        #     global font
        #     fdia = gtk.FontSelectionDialog('Выберите шрифт')
        #     fdia.set_font_name(font)
        #     response = fdia.run()

        #     if response == gtk.RESPONSE_OK:
        #         font_desc = pango.FontDescription(fdia.get_font_name())
        #         font = font_desc.get_family()
        #         Save_Config()
        #         self.drawing_area.redraw(False, False)
        #     fdia.destroy()
        #     return
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
                self.window.unstick()
            else:
                sticky = True
                self.window.stick()
            Save_Config()
        if event == 'setup':
            settings.main(gw_config_default, gw_config, self.drawing_area, app, icons_list, backgrounds_list)

    def button_press(self, widget, event):
        if event.button == 1 and not fix_position:
            self.window.begin_move_drag(1, int(event.x_root), int(event.y_root), event.time)
            return True
        if event.button == 3:
            self.menu = self.create_menu()
            self.menu.popup(None, None, None, event.button, event.time)
            return True
        return False

    def configure_event(self, widget, event):
        global x_pos, y_pos
        if event.x != x_pos or event.y != y_pos:
            x_pos = event.x
            y_pos = event.y
            Save_Config()

    def redraw_icons(self, widget, string):
        global icons_name
        icons_name = string
        self.drawing_area.redraw(False, False)
        Save_Config()

    def redraw_bg(self, widget, string):
        global bg_custom, show_bg_png, color_bg
        show_bg_png = True
        if string == 'Нет':
            show_bg_png = False
            color_bg = (1, 1, 1, 0)
        bg_custom = string
        self.drawing_area.redraw(False, False)
        Save_Config()
    
    def redraw_text(self, widget, i):
        Load_Color_Scheme(i)
        self.drawing_area.redraw(False, False)
        Save_Config()

    def reload(self, widget, c_id = 0):
        # если radio, то обновлялось 2 раза, фикс
        if type(widget) == gtk.RadioMenuItem:
            if not widget.get_active():
                return

        global city_id
        Load_Config()
        if c_id != 0:
            city_id = c_id.split(';')[0]
            Save_Config()
        self.drawing_area.redraw(False)

    def show_edit_dialog(self):
        global city_id, city_id_add
        dialog, entrybox, treeview, bar_err, bar_ok, bar_label = Gtk_city_id.create_gtk_city_id(self.window, city_id, city_id_add);
        dialog.show_all()
        bar_err.hide()
        bar_ok.hide()
        response = dialog.run()

        while response == gtk.RESPONSE_ACCEPT or response == gtk.RESPONSE_OK:
            bar_err.hide()
            bar_ok.hide()
            if response == gtk.RESPONSE_ACCEPT:
                try:
                    selection = treeview.get_selection()
                    model, iter = selection.get_selected()
                    abc, cde =  selection.get_selected_rows()
                    del_index=cde[0]
                    if iter:
                        model.remove(iter)
                    bar_label.set_text('Удалено: %s'%city_id_add[int(del_index[0])].split(';')[1])
                    if str(city_id) == city_id_add[int(del_index[0])].split(';')[0]:
                        del city_id_add[int(del_index[0])]
                        if len(city_id_add) != 0:
                            city_id = int(city_id_add[0].split(';')[0])
                        else:
                            city_id = 0
                    else:
                        del city_id_add[int(del_index[0])]
                    Save_Config()
                    bar_ok.show()
                except:
                    pass
            if response == gtk.RESPONSE_OK:
                try:
                    city_id = int(entrybox.get_text())
                    c_name = get_city_name(city_id)
                    if c_name == 'None':
                        if len(city_id_add) != 0:
                            city_id = int(city_id_add[0].split(';')[0])
                        else:
                            city_id = 0
                        raise
                    city_id_add.append(str(city_id) + ';' + c_name)
                    model = treeview.get_model()
                    model.append([city_id_add[-1].split(';')[0], city_id_add[-1].split(';')[1]])
                    treeview.set_model(model)
                    Save_Config()
                    bar_label.set_text('Добавлено: %s'%city_id_add[-1].split(';')[1])
                    bar_ok.show()
                except:
                    bar_err.show()
                    print '[!] Не верно введен код местоположения'
            response = dialog.run()

        dialog.hide()
        return True

    def edit_city_id(self, widget):
        if self.show_edit_dialog():
            Save_Config()
            while gtk.events_pending():
                gtk.main_iteration_do(True)
            self.drawing_area.redraw(False)

    def main(self):
        self.window.show_all()
        x = self.window.get_size()
        self.window.resize(width, height-(x[1]-height))
        if city_id == 0:
            if self.show_edit_dialog():
                Save_Config()
        gtk.main()
        

    def screen_changed(self, widget, old_screen = None):
        screen = widget.get_screen()
        colormap = screen.get_rgba_colormap()
        if colormap == None or not widget.is_composited():
            print 'Your screen does not support alpha'
            colormap = screen.get_rgb_colormap()
        else:
            print 'Your screen supports alpha'
        widget.set_colormap(colormap)
        return True


if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = Weather_Widget()
    app.main()
