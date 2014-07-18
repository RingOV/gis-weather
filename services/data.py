#!/usr/bin/env python3

import os

from services import gismeteo, weather_com, accuweather

services_list = [
    'gismeteo',
    'weather.com',
    'accuweather'
    ]

def get(service):
    if service == 0:
        return gismeteo.data
    if service == 1:
        return weather_com.data
    if service == 2:
        return accuweather.data

def get_city_list(service):
    if service == 0:
        return 'city_list_gismeteo'
    if service == 1:
        return 'city_list_weather_com'
    if service == 2:
        return 'city_list_accuweather'

def get_city_name(service, city_id, weather_lang):
    if service == 0:
        return  gismeteo.get_city_name(city_id, weather_lang)
    if service == 1:
        return  weather_com.get_city_name(city_id, weather_lang)
    if service == 2:
        return  accuweather.get_city_name(city_id, weather_lang)

def get_max_days(service):
    if service == 0:
        return gismeteo.max_days
    if service == 1:
        return weather_com.max_days
    if service == 2:
        return accuweather.max_days

def get_weather(service, weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name, indicator_only):
    if service == 0:
        return gismeteo.get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name, indicator_only)
    if service == 1:
        return weather_com.get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name, indicator_only)
    if service == 2:
        return accuweather.get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name, indicator_only)