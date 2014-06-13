#!/usr/bin/env python3

import os

from services import gismeteo, weather_com

services_list = [
    'gismeteo',
    'weather.com'
    ]

def get(service):
    if service == 0:
        return gismeteo.data
    if service == 1:
        return weather_com.data

def get_city_list(service):
    if service == 0:
        return 'city_list_gismeteo'
    if service == 1:
        return 'city_list_weather_com'

def get_city_name(service, city_id, weather_lang):
    if service == 0:
        return  gismeteo.get_city_name(city_id, weather_lang)
    if service == 1:
        return  weather_com.get_city_name(city_id, weather_lang)

def get_max_days(service):
    if service == 0:
        return gismeteo.max_days
    if service == 1:
        return weather_com.max_days