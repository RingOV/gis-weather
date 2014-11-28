#!/usr/bin/env python3

from urllib.request import urlopen
from utils.t_convert import F_to_C, F_to_K
import re
import time
import os

data = [
    "http://www.weather.com",  # url
    "http://www.weather.com/weather/today/<b>ARTF0105</b>:1",  # example
    "<b>ARTF0105</b>",  # code
    {
        'http://www.weather.com/weather/tenday/': 'English'
    },  # dict_weather_lang
    ('http://www.weather.com/weather/tenday/', '')  # weather_lang_list
]
max_days = 8
# weather variables
city_name = []
t_now = []
wind_speed_now = []
wind_direct_now = []
icon_now = []
icon_wind_now = []
time_update = []
text_now = []
press_now = []
hum_now = []
t_water_now = []

t_night = []
t_night_feel = []
day = []
date = []
t_day = []
t_day_feel = []
icon = []
icon_wind = []
wind_speed = []
wind_direct = []
text = []

t_tomorrow = []
t_tomorrow_feel = []
icon_tomorrow = []
wind_speed_tom = []
wind_direct_tom = []

t_today = []
t_today_feel = []
icon_today = []
wind_speed_tod = []
wind_direct_tod = []
chance_of_rain = []
t_today_low=[]
t_tomorrow_low=[]

dict_icons = {
    "0.png": "00.png",
    "1.png": "01.png",
    "2.png": "02.png",
    "3.png": "03.png",
    "4.png": "04.png",
    "5.png": "05.png",
    "6.png": "06.png",
    "7.png": "07.png",
    "8.png": "08.png",
    "9.png": "09.png",
    "10.png": "10.png",
    "11.png": "11.png",
    "12.png": "12.png",
    "13.png": "13.png",
    "14.png": "14.png",
    "15.png": "15.png",
    "16.png": "16.png",
    "17.png": "17.png",
    "18.png": "18.png",
    "19.png": "19.png",
    "20.png": "20.png",
    "21.png": "21.png",
    "22.png": "22.png",
    "23.png": "23.png",
    "24.png": "24.png",
    "25.png": "25.png",
    "26.png": "26.png",
    "27.png": "27.png",
    "28.png": "28.png",
    "29.png": "29.png",
    "30.png": "30.png",
    "31.png": "31.png",
    "32.png": "32.png",
    "33.png": "33.png",
    "34.png": "34.png",
    "35.png": "35.png",
    "36.png": "36.png",
    "37.png": "37.png",
    "38.png": "38.png",
    "39.png": "39.png",
    "40.png": "40.png",
    "41.png": "41.png",
    "42.png": "42.png",
    "43.png": "43.png",
    "44.png": "44.png",
    "45.png": "45.png",
    "46.png": "46.png",
    "47.png": "47.png"
}


def convert(icon_list, icons_name):
    for i in range(len(icon_list)):
        try:
            icon_converted = dict_icons[os.path.split(icon_list[i])[1]]
        except:
            icon_converted = os.path.split(icon_list[i])[1]
        icon_list[i] = icon_list[i]+';'+icon_converted
    return icon_list


def wind_degree(s):
    wind_dict = {
        'W': 0,
        'WNW': 23,
        'NW': 45,
        'NNW': 68,
        'N': 90,
        'NNE': 113,
        'NE': 135,
        'ENE': 158,
        'E': 180,
        'ESE': 203,
        'SE': 225,
        'SSE': 248,
        'S': 270,
        'SSW': 293,
        'SW': 315,
        'WSW': 338        
    }
    return wind_dict[s]


def get_city_name(c_id, weather_lang):
    try:
        source = urlopen(weather_lang + str(c_id), timeout=10).read()
        source = source.decode(encoding='UTF-8')
        c_name = re.findall('data-location-presentation-name="(.*)"', source)
    except:
        print('\033[1;31m[!]\033[0m '+_('Failed to get the name of the location'))
        return 'None'
    return c_name[0]


def get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name):
    global city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod, chance_of_rain
    print('\033[34m>\033[0m '+_('Getting weather for')+' '+str(n)+' '+_('days'))
    print('\033[34m>\033[0m '+_('Downloading')+' '+weather_lang + str(city_id))
    try:
        source = urlopen(weather_lang + str(city_id), timeout=10).read()
        source = source.decode(encoding='UTF-8')
        print ('\033[1;32mOK\033[0m')
    except:
        print ('\033[1;31m[!]\033[0m '+_('Unable to download page, check the network connection'))
        if timer_bool:
            print ('\033[1;31m[!]\033[0m '+_('Next try in 10 seconds'))
        return False
    #### current weather ####
    w_now = re.findall('data-location-presentation-name=.*<ul class="wx-conditions">', source, re.DOTALL)
    
    # city
    city_name = re.findall('data-location-presentation-name="(.*)"', w_now[0])

    # temperature
    t = re.findall('"temperature-fahrenheit">(.*)</span', w_now[0])
    t_fill = re.findall('"feels-like-temperature-fahrenheit">(.*)</span', w_now[0])
    if t[0][0] not in ('+', '-', '0'):
            t[0] = '+'+t[0]
    if t_fill[0][0] not in ('+', '-', '0'):
            t_fill[0] = '+'+t_fill[0]
    t_c = F_to_C(t[0])
    t_c_fill = F_to_C(t_fill[0])
    t_k = F_to_K(t[0])
    t_k_fill = F_to_K(t_fill[0])
    t_now = ['']
    t_now[0] = t_c+'°;'+t_c_fill+'°;'+t[0]+'°;'+t_fill[0]+'°;'+t_k+';'+t_k_fill


    # wind
    wind_speed_now = re.findall('"wind-speed">(\d+)<', w_now[0])
    if wind_speed_now:
        wind_speed_now[0] = str(round(int(wind_speed_now[0])*0.447))+' m/s;'+str(round(int(wind_speed_now[0])*1.609))+' km/h;'+wind_speed_now[0]+' mph'
    wind_direct_now = re.findall('"wx-dir-arrow wind-dir-(.+)"', w_now[0])
    if not wind_direct_now:
        wind_direct_now = ['C']

    # icon
    icon_now = re.findall('itemprop="weather-icon">(.*)<', w_now[0])
    icon_now = convert(icon_now, icons_name)

    # wind icon
    icon_wind_now = ['']
    try:
        icon_wind_now[0] = wind_degree(wind_direct_now[0])
    except:
        icon_wind_now[0] = 'None'

    # update time
    time_update = re.findall(' wx-timestamp">(.*)</div>', source)
    time_update[0] = time_update[0].split()[-3].strip()
    
    # weather text now
    text_now = re.findall('"weather-phrase">(.*)<', w_now[0])
    
    # pressure now
    press_now = re.findall('"barometric-pressure.*>(.*) ', w_now[0])
    if press_now:
        press_now[0] = str(round(float(press_now[0])*25.4))+' mmHg;'+press_now[0]+' inHg;'+str(round(float(press_now[0])*25.4*1.333))+' hPa'
    
    # humidity now
    hum_now = re.findall('"humidity">(.*)</span>', w_now[0])
    
    #### weather to several days ####
    # all days
    w_all = re.findall('<ul class="wx-conditions">.*"WX_Driver1"', source, re.DOTALL)
    w_all = w_all[0]

    # day temperature
    t_day = re.findall('"wx-temp"> (-*\d+)<', w_all)
    for i in range(len(t_day)):
        if t_day[i][0] not in ('+', '-', '0'):
            t_day[i] = '+'+t_day[i]
        t_day[i] = F_to_C(t_day[i])+'°;'+F_to_C(t_day[i])+'°;'+t_day[i]+'°;'+t_day[i]+'°;'+F_to_K(t_day[i])+';'+F_to_K(t_day[i])

    # night temperature
    t_night = re.findall('"wx-temp-alt"> (-*\d+)<', w_all)
    for i in range(len(t_night)):
        if t_night[i][0] not in ('+', '-', '0'):
            t_night[i] = '+'+t_night[i]
        t_night[i] = F_to_C(t_night[i])+'°;'+F_to_C(t_night[i])+'°;'+t_night[i]+'°;'+t_night[i]+'°;'+F_to_K(t_night[i])+';'+F_to_K(t_night[i])
    
    # day of week, date
    day = re.findall('<h3>(.*)', w_all)
    day[0] = day[7]
    date = re.findall('<span class="wx-label">(.+)</span>', w_all)
    if len(date) == 12:
        date.pop(1)
        date.pop(1)

    # weather icon day
    icon = re.findall('src=\"(.*png)\" ', w_all)
    icon = convert(icon, icons_name)
    
    # wind
    wind = re.findall('<dt>Wind:</dt>\n<dd>\n(.*)\n</dd>', w_all)
    wind_speed = []
    wind_direct = []
    for i in wind:
        if i.split()[0]==i.split()[-1]:
            wind_speed.append('0')
            wind_direct.append('C')
        else:
            wind_speed.append(i.split()[-2])
            wind_direct.append(i.split()[0])
    if wind_speed:
        for i in range(len(wind_speed)):
            wind_speed[i] = str(round(int(wind_speed[i])*0.447))+' m/s;'+str(round(int(wind_speed[i])*1.609))+' km/h;'+wind_speed[i]+' mph'

    # weather text
    text = re.findall('"wx-phrase">(.*)<', w_all)

    chance_of_rain = re.findall('<dd>(\d+%)</dd>', w_all)

    if time_update:
        print ('\033[34m>\033[0m '+_('updated on server')+' '+time_update[0]) 
    print ('\033[34m>\033[0m '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # write variables
    for i in weather.keys():
        weather[i] = globals()[i]
    return weather