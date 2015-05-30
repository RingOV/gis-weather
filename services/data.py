#!/usr/bin/env python3

import os

from services import gismeteo, accuweather, openweathermap

services_list = [
    'Gismeteo',
    'AccuWeather',
    'OpenWeatherMap'
    ]

def get_index(service):
    for i in range(len(services_list)):
        if services_list[i] == service:
            return i

def get(service):
    if service == 'Gismeteo':
        return gismeteo.data
    if service == 'AccuWeather':
        return accuweather.data
    if service == 'OpenWeatherMap':
        return openweathermap.data

def get_city_list(service):
    if service == 'Gismeteo':
        return 'city_list_gismeteo'
    if service == 'AccuWeather':
        return 'city_list_accuweather'
    if service == 'OpenWeatherMap':
        return 'city_list_openweathermap'

def get_city_name(service, city_id, weather_lang):
    if service == 'Gismeteo':
        return  gismeteo.get_city_name(city_id)
    if service == 'AccuWeather':
        return  accuweather.get_city_name(city_id)
    if service == 'OpenWeatherMap':
        return  openweathermap.get_city_name(city_id)

def get_max_days(service):
    if service == 'Gismeteo':
        return gismeteo.max_days
    if service == 'AccuWeather':
        return accuweather.max_days
    if service == 'OpenWeatherMap':
        return openweathermap.max_days

def get_weather(service, weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name):
    if service == 'Gismeteo':
        return gismeteo.get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name)
    if service == 'AccuWeather':
        return accuweather.get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name)
    if service == 'OpenWeatherMap':
        return openweathermap.get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name)