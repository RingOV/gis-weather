#!/usr/bin/env python3

import os

from services import gismeteo, openweathermap, yr, accuweather

services_list = [
    'Gismeteo',
    # 'AccuWeather',
    'OpenWeatherMap',
    'Yr'
    ]

def get_index(service):
    for i in range(len(services_list)):
        if services_list[i] == service:
            return i

def get(service):
    if service == 'Gismeteo':
        return gismeteo.data
    # if service == 'AccuWeather':
    #     return accuweather.data
    if service == 'OpenWeatherMap':
        return openweathermap.data
    if service == 'Yr':
        return yr.data

def get_city_list(service):
    if service == 'Gismeteo':
        return 'city_list_gismeteo'
    # if service == 'AccuWeather':
    #     return 'city_list_accuweather'
    if service == 'OpenWeatherMap':
        return 'city_list_openweathermap'
    if service == 'Yr':
        return 'city_list_yr'

def get_appid(service):
    if service == 'OpenWeatherMap':
        return 'appid_openweathermap'
    return ''

def get_city_name(service, city_id):
    if service == 'Gismeteo':
        return  gismeteo.get_city_name(city_id)
    # if service == 'AccuWeather':
    #     return  accuweather.get_city_name(city_id)
    if service == 'OpenWeatherMap':
        return  openweathermap.get_city_name(city_id)
    if service == 'Yr':
        return yr.get_city_name(city_id)

# def get_max_days(service):
#     if service == 'Gismeteo':
#         return gismeteo.max_days
#     # if service == 'AccuWeather':
#     #     return accuweather.max_days
#     if service == 'OpenWeatherMap':
#         return openweathermap.max_days
#     if service == 'Yr':
#         return yr.max_days

# def get_need_appid(service):
#     if service == 'Gismeteo':
#         return gismeteo.need_appid
#     # if service == 'AccuWeather':
#     #     return accuweather.need_appid
#     if service == 'OpenWeatherMap':
#         return openweathermap.need_appid
#     if service == 'Yr':
#         return yr.need_appid

def get_weather(service):
    if service == 'Gismeteo':
        return gismeteo.get_weather()
    # if service == 'AccuWeather':
    #     return accuweather.get_weather()
    if service == 'OpenWeatherMap':
        return openweathermap.get_weather()
    if service == 'Yr':
        return yr.get_weather()