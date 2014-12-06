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
        'splash_block_top': 0
    },

    #  Small
    {   'bg_left': 0,
        'bg_top': 80,#38,
        'bg_width': -1,
        'bg_height': 185,
        'block_now_left': 0,
        'icon_now_top': -70,
        'icon_now_left': 1120,
        'icon_now_size': 80,
        'block_icons_left': 199,
        'block_icons_top': -1,
        'city_name_left': 200,
        'city_name_top': 27,
        'day_left': 0,
        'day_top': -75,
        't_now_left': 1125,
        't_now_top': 40,
        't_now_size': 6,
        't_now_alignment': 'left',
        'text_now_left': 1161,
        'text_now_top': 9,
        'height_fix': -95,
        'n': 3,
        'show_block_wind_direct': False,
        'show_block_add_info': False,
        'show_block_tomorrow': False,
        'show_block_today': False,
        'splash_icon_top': 25,
        'splash_version_top': 20,
        'splash_block_top': 25,
        'margin': 20
    },

    #  Wood
    {   'bg_left': 0,
        'bg_top': 0,
        'bg_width': -1,
        'bg_height': -1,
        'icon_now_top': 120,
        'icon_now_left': 0,
        'block_icons_left': 0,
        'block_icons_top': 0,
        'city_name_left': 0,
        'city_name_top':126,
        'day_left': 0,
        'day_top': 126,
        'icon_now_size': 0,
        't_now_left': 0,
        't_now_top': 120,
        't_now_size': 0,
        't_now_alignment': 'right',
        'text_now_left': 0,
        'text_now_top': 120,
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
        'splash_icon_top': 0,
        'splash_version_top': 0,
        'bg_custom': 'Wood',
        'margin': 15,
        'block_wind_direct_small_left': 0,
        'block_today_top': 120,
        'block_tomorrow_top': 120,
        'block_wind_direct_small_top': 120,
        'splash_block_top': 70,
        'color_text': (0.18, 0.18, 0.18, 1),
        'draw_shadow': False,
        'icons_name': 'Sketchy',
        'show_bg_png': True
    },
    #  NotePaper
    {   'bg_left': 0,
        'bg_top': 0,
        'bg_width': -1,
        'bg_height': -1,
        'block_now_left': 20,
        'icon_now_top': 0,
        'icon_now_left': 0,
        'icon_now_size': 0,
        'block_icons_left': 50,
        'block_icons_top': 0,
        'city_name_left': 20,
        'city_name_top': 0,
        'day_left': 20,
        'day_top': 0,
        't_now_left': 0,
        't_now_top': 0,
        't_now_size': 0,
        't_now_alignment': 'right',
        'text_now_left': 0,
        'text_now_top': 0,
        'height_fix': 0,
        'n': 4,
        'show_block_wind_direct': True,
        'show_block_add_info': True,
        'show_block_tomorrow': False,
        'show_block_today': False,
        'splash_block_top': 0,
        'margin': 20,
        'block_wind_direct_left': -150,
        'block_add_info_left': 90,
        'bg_custom': 'NotePaper',
        'wind_direct_small': False,
        'show_bg_png': True
    },
    ]

names = {
    0: 'Default',
    1: 'Small',
    2: 'Wood',
    3: 'NotePaper'
}

def save_to_file(CONFIG_PATH):
    for i in range(len(list)):
        #if not os.path.exists(os.path.join(CONFIG_PATH, 'presets', 'preset_%s.json' %i)):  FIXME after testing uncomment this
        json.dump(list[i], open(os.path.join(CONFIG_PATH, 'presets', 'preset_%s.json' %i), "w"), sort_keys=True, indent=4, separators=(', ', ': '))