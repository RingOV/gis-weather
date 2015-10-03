#!/usr/bin/env python3

import os
import json

list = [
    #  Default
    {   'n': 7,                            # Display days
        'color_text': (0, 0, 0, 1), #RGBa  # color text
        'color_text_week': (0.5, 0, 0, 1), # color weekend
        'color_shadow': (1, 1, 1, 0.7),    # color shadow
        'draw_shadow': True,               # draw shadow
        'show_block_wind_direct': True,    # block wind direct
        'block_wind_direct_left': -170,    # position
        'wind_direct_small': False,        # small block wind direct
        'show_block_add_info': True,       # block with additional information
        'block_add_info_left': 70,         # position
        'show_block_tomorrow': True,       # block with the weather for tomorrow
        'block_tomorrow_left': 180,        # position
        'show_block_today': True,          # block with the weather for today
        'block_today_left': -310,          # position
        'bg_custom': 'Light50',            # this picture
        'margin': 20,                      # inside padding
        'block_now_left': 0,
        # customizable options
        'preset_number':0,
        'bg_left': 0,
        'bg_top': 0,
        'bg_width': -1,
        'bg_height': -1,
        'block_icons_left': 0,
        'block_icons_top': 0,
        'day_left': 0,
        'day_top': 0,
        'height_fix': 0,
        'width_fix': 0,
        'splash_icon_top': 0,
        'splash_version_top': 0,
        'block_wind_direct_small_left': 0,
        'block_today_top': 0,
        'block_tomorrow_top': 0,
        'block_wind_direct_small_top': 0,
        'splash_block_top': 0,
        # day icon customization
        'day_icon_attr': {'x':30, 'y':16, 'size':36, 'show':True},
        'day_date_fmt': '{day}, {date}',
        'day_date_attr': {'x':0, 'y':-2, 'font_weight':' Bold', 'font_size':9, 'align':'left', 'show':True},
        't_fmt': '{t_day}\n{t_night}',
        't_attr': {'x':0, 'y':15, 'font_weight':' Normal', 'font_size':10, 'align':'left', 'show':True},
        'wind_fmt': '{wind_direct}, {wind_speed}',
        'wind_attr': {'x':0, 'y':50, 'font_weight':' Normal', 'font_size':8, 'align':'left', 'show':True},
        'text_attr': {'x':0, 'y':55, 'font_size':7, 'align':'left', 'show':True},
        # now icon customization
        'city_name_attr': {'x':0, 'y':0, 'font_weight':' Bold', 'font_size':14, 'align':'center', 'show':True},
        'text_now_attr': {'x':0, 'y':0, 'font_weight':' Normal', 'font_size':10, 'align':'center', 'show':True},
        't_now_attr': {'x':0, 'y':30, 'font_weight':' Normal', 'font_size':18, 'align':'right', 'show':True},
        'icon_now_attr': {'x':0, 'y':30, 'size':80, 'show':True},
        'custom_text1_attr': {'text':'Now', 'x':65, 'y':3, 'font_weight':' Bold', 'font_size':9, 'align':'left', 'show':False},
        'block_h_offset': 12,
    },

    #  Small
    {   'bg_left': 0,
        'bg_top': 80,#38,
        'bg_width': -1,
        'bg_height': 185,
        'block_icons_left': 199,
        'block_icons_top': -1,
        'day_top': -75,
        'height_fix': -95,
        'n': 3,
        'show_block_wind_direct': False,
        'show_block_add_info': False,
        'show_block_tomorrow': False,
        'show_block_today': False,
        'splash_icon_top': 25,
        'splash_version_top': 20,
        'splash_block_top': 25,
        'margin': 20,
        'city_name_attr': {'x':200, 'y':27, 'font_weight':' Bold', 'font_size':14, 'align':'center', 'show':True},
        'text_now_attr': {'x':1161, 'y':9, 'font_weight':' Normal', 'font_size':10, 'align':'center', 'show':True},
        't_now_attr': {'x':1125, 'y':70, 'font_weight':' Normal', 'font_size':24, 'align':'left', 'show':True},
        'icon_now_attr': {'x':1120, 'y':-40, 'size':160, 'show':True},
    },

    #  Wood
    {   'bg_left': 0,
        'day_top': 126,
        'height_fix': 120,
        'n': 5,
        'show_block_wind_direct': True,
        'block_wind_direct_left': -170,
        'wind_direct_small': True,
        'show_block_add_info': False,
        'block_add_info_left': 70,
        'show_block_tomorrow': True,
        'block_tomorrow_left': 90,
        'show_block_today': True,
        'block_today_left': -220,
        'bg_custom': 'Wood',
        'margin': 15,
        'block_today_top': 120,
        'block_tomorrow_top': 120,
        'block_wind_direct_small_top': 120,
        'splash_block_top': 70,
        'color_text': (0.18, 0.18, 0.18, 1),
        'draw_shadow': False,
        'icons_name': 'Sketchy',
        'show_bg_png': True,
        'city_name_attr': {'x':0, 'y':126, 'font_weight':' Bold', 'font_size':14, 'align':'center', 'show':True},
        'text_now_attr': {'x':0, 'y':120, 'font_weight':' Normal', 'font_size':10, 'align':'center', 'show':True},
        't_now_attr': {'x':0, 'y':150, 'font_weight':' Normal', 'font_size':18, 'align':'right', 'show':True},
        'icon_now_attr': {'x':0, 'y':150, 'size':80, 'show':True},
    },

    #  NotePaper
    {   'bg_left': 0,
        'block_now_left': 20,
        'block_icons_left': 50,
        'block_icons_top': 0,
        'day_left': 20,
        'n': 4,
        'show_block_wind_direct': True,
        'show_block_add_info': True,
        'show_block_tomorrow': False,
        'show_block_today': False,
        'margin': 20,
        'block_wind_direct_left': -150,
        'block_add_info_left': 90,
        'bg_custom': 'NotePaper',
        'wind_direct_small': False,
        'show_bg_png': True,
        'city_name_attr': {'x':20, 'y':0, 'font_weight':' Bold', 'font_size':14, 'align':'center', 'show':True}
    },

    #  Winter
    {   'bg_custom': 'Winter',            # this picture
        'margin': 50,                      # inside padding
    },

    #  Compact
    {   'bg_left': 0,
        'bg_top': 0,
        'bg_height': 145,
        'block_now_left': -125,
        'block_icons_left': 49,
        'block_icons_top': 30,
        'day_top': -75,
        'height_fix': -180,
        'width_fix': 20,
        'n': 3,
        'show_block_wind_direct': False,
        'show_block_add_info': False,
        'show_block_tomorrow': False,
        'show_block_today': False,
        'splash_icon_top': 25,
        'splash_version_top': 20,
        'splash_block_top': 25,
        'margin': 20,
        'day_icon_attr': {'x':22, 'y':16, 'size':36},
        'day_date_fmt': '{day}',
        'day_date_attr': {'x':0, 'y':-2, 'font_weight':' Bold', 'font_size':9, 'align':'center', 'show':True},
        't_fmt': '{t_night}/{t_day}',
        't_attr': {'x':0, 'y':55, 'font_weight':' Normal', 'font_size':10, 'align':'center', 'show':True},
        'wind_fmt': '{wind_direct}, {wind_speed}',
        'wind_attr': {'x':0, 'y':50, 'font_weight':' Normal', 'font_size':8, 'align':'left', 'show':False},
        'text_attr': {'x':0, 'y':55, 'font_size':7, 'align':'left', 'show':False},
        'city_name_attr': {'x':164, 'y':-18, 'font_weight':' Normal', 'font_size':11, 'align':'left', 'show':True},
        'text_now_attr': {'x':1161, 'y':9, 'font_weight':' Normal', 'font_size':10, 'align':'center', 'show':False},
        't_now_attr': {'x':1230, 'y':60, 'font_weight':' Normal', 'font_size':10, 'align':'right', 'show':True},
        'icon_now_attr': {'x':1200, 'y':21, 'size':36, 'show':True},
        'custom_text1_attr': {'text':'Now', 'x':40, 'y':3, 'font_weight':' Bold', 'font_size':9, 'align':'left', 'show':True},
        'block_h_offset': -5,
    },
    ]

names = {
    0: 'Default',
    1: 'Small',
    2: 'Wood',
    3: 'NotePaper',
    4: 'Winter',
    5: 'Compact'
}

def save_to_file(CONFIG_PATH):
    for i in range(len(list)):
        #if not os.path.exists(os.path.join(CONFIG_PATH, 'presets', 'preset_%s.json' %i)):  FIXME after testing uncomment this
        json.dump(list[i], open(os.path.join(CONFIG_PATH, 'presets', 'preset_%s.json' %i), "w"), sort_keys=True, indent=4, separators=(', ', ': '))