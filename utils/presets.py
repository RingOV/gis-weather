#!/usr/bin/env python3

import os
import json

list = [
    #  Default
    {   'bg_left': 0,
        'bg_top': 0,
        'bg_width': -1,
        'bg_height': -1,
        'icon_now_top': 0,
        'icon_now_left': 0,
        'block_icons_left': 0,
        'block_icons_top': 0,
        'city_name_left': 0,
        'city_name_top':0,
        'day_left': 0,
        'day_top': 0,
        'icon_now_size': 0,
        't_now_left': 0,
        't_now_top': 0,
        't_now_size': 0,
        'text_now_left': 0,
        'text_now_top': 0,
        'height_fix': 0,
        'n': 7,
        'show_block_wind_direct': True,
        'block_wind_direct_left': -170,
        'wind_direct_small': False,
        'show_block_add_info': True,
        'block_add_info_left': 70,
        'show_block_tomorrow': True,
        'block_tomorrow_left': 180,
        'show_block_today': True,
        'block_today_left': -310,
        'splash_icon_top': 0,
        'splash_version_top': 0
    },

    #  Small
    {   'bg_left': 0,
        'bg_top': 40,
        'bg_width': -1,
        'bg_height': 170,
        'block_now_left': 0,
        'icon_now_top': -70,
        'icon_now_left': 1100,
        'icon_now_size': 80,
        'block_icons_left': 199,
        'block_icons_top': 7,
        'city_name_left': 200,
        'city_name_top': 24,
        'day_left': 0,
        'day_top': -80,
        't_now_left': 1132,
        't_now_top': 35,
        't_now_size': 6,
        'text_now_left': 1141,
        'text_now_top': -2,
        'height_fix': -110,
        'n': 3,
        'show_block_wind_direct': False,
        'show_block_add_info': False,
        'show_block_tomorrow': False,
        'show_block_today': False,
        'splash_icon_top': 25,
        'splash_version_top': 20
    },
    ]

names = {
    0: 'Default',
    1: 'Small'
}

def save_to_file(CONFIG_PATH):
    for i in range(len(list)):
        #if not os.path.exists(os.path.join(CONFIG_PATH, 'presets', 'preset_%s.json' %i)):  FIXME after testing uncomment this
        json.dump(list[i], open(os.path.join(CONFIG_PATH, 'presets', 'preset_%s.json' %i), "w"), sort_keys=True, indent=4, separators=(', ', ': '))