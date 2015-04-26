#!/usr/bin/env python3

from utils import weather_vars, wind_direct_convert
from utils.opener import urlopen, urlopener
from utils.t_convert import C_to_F, C_to_K, add_plus
import re
import time
import os
import json
from datetime import datetime

data = [
    "http://openweathermap.org/find?q=", # url
    "http://openweathermap.org/city/<b>1234</b>", # example
    "<b>1234</b>", #code
    { 
        'en': 'English',
        'ru': 'Russian',
        'it': 'Italian',
        'es': 'Spanish',
        'uk': 'Ukrainian',
        'de': 'German',
        'pt': 'Portuguese',
        'ro': 'Romanian',
        'pl': 'Polish',
        'fi': 'Finnish',
        'nl': 'Dutch',
        'fr': 'French',
        'bg': 'Bulgarian',
        'sv': 'Swedish',
        'zh_tw': 'ChineseTraditional',
        'zh': 'ChineseSimplified',
        'tr': 'Turkish',
        'hr': 'Croatian',
        'ca': 'Catalan'
    }, # dict_weather_lang
    ('en', 'ru', 'it', 'es', 'uk', 'de', 'pt', 'ro', 'pl', 'fi', 'nl', 'fr', 'bg', 'sv', 'zh_tw', 'zh', 'tr', 'hr', 'ca') # weather_lang_list
]
max_days = 15

# weather variables
w = weather_vars.weather
# create variables
for i in w.keys():
    globals()[i] = w[i]

dict_icons = {
    "01d.png": "32.png",
    "02d.png": "34.png",
    "03d.png": "30.png",
    "04d.png": "26.png",
    "09d.png": "12.png",
    "10d.png": "39.png",
    "11d.png": "37.png",
    "13d.png": "15.png",
    "50d.png": "20.png",
    "01n.png": "31.png",
    "02n.png": "33.png",
    "03n.png": "29.png",
    "04n.png": "27.png",
    "09n.png": "12.png",
    "10n.png": "45.png",
    "11n.png": "47.png",
    "13n.png": "15.png",
    "50n.png": "20.png"
}

def convert(icon, icons_name):
    try:
        icon_converted = dict_icons[os.path.split(icon)[1]]
    except:
        icon_converted = os.path.split(icon)[1]
    return icon+';'+icon_converted

def get_city_name(c_id, weather_lang):
    try:

        source = urlopen('http://api.openweathermap.org/data/2.5/weather?id=%s&lang=%s&APPID=%s'%(str(c_id), weather_lang, APPID))
        source = json.loads(source.decode(encoding='UTF-8'))
        c_name = source['name']
    except:
        print ('\033[1;31m[!]\033[0m '+_('Failed to get the name of the location'))
        return 'None'
    return c_name

def get_time(source):
    return source['dt_txt'].split()[1][:-3]

def get_day(source):
    return int(source['dt_txt'].split()[0].split('-')[-1])

APPID = 'dde83a2bee572cb5467f58af45a7987a'

def get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, show_block_add_info, timer_bool, weather_lang, icons_name):
    global city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod, chance_of_rain
    URL_CURRENT = 'http://api.openweathermap.org/data/2.5/weather?id=%s&lang=%s&units=metric'%(str(city_id), weather_lang)
    URL_SEVERAL_DAYS = 'http://api.openweathermap.org/data/2.5/forecast/daily?id=%s&lang=%s&units=metric&cnt=%s'%(str(city_id), weather_lang, n+1)
    URL_TODAY_TOMORROW = 'http://api.openweathermap.org/data/2.5/forecast?id=%s&lang=%s&units=metric'%(str(city_id), weather_lang)
    print ('\033[34m>\033[0m '+_('Getting weather for')+' '+str(n)+' '+_('days'))
    # print ('\033[34m>\033[0m '+_('Downloading')+' '+URL_CURRENT)
    # try:
    #     source = urlopen('http://api.openweathermap.org/data/2.5/weather?id=%s&lang=%s&units=metric&APPID=%s'%(str(city_id), weather_lang, APPID))
    #     source = json.loads(source.decode(encoding='UTF-8'))
    #     
    # except:
    #     print ('\033[1;31m[!]\033[0m '+_('Unable to download page, check the network connection'))
    #     if timer_bool:
    #         print ('\033[1;31m[!]\033[0m '+_('Next try in 10 seconds'))
    #     return False
    source = urlopener(URL_CURRENT, 5)
    if not source:
        if timer_bool:
            print ('\033[1;31m[!]\033[0m '+_('Next try in 10 seconds'))
        return False
    source = json.loads(source)


    #### current weather ####
    
    # city
    city_name = [source['name']]

    # temperature
    t_now = [add_plus(str(round(source['main']['temp'])))]
    t_now[0] = t_now[0]+'°;'+t_now[0]+'°;'+C_to_F(t_now[0])+'°;'+C_to_F(t_now[0])+'°;'+C_to_K(t_now[0])+';'+C_to_K(t_now[0])

    # wind
    wind_speed_now = [str(round(source['wind']['speed']))]
    if wind_speed_now:
        wind_speed_now[0] = wind_speed_now[0]+' m/s;'+str(round(int(wind_speed_now[0])*3.6))+' km/h;'+str(round(int(wind_speed_now[0])*2.237))+' mph'
    wind_direct_now = [wind_direct_convert.convert(source['wind']['deg'])]
    a=''
    for i in range(len(wind_direct_now[0])):
        a=a+_(wind_direct_now[0][i])
    wind_direct_now[0]=a

    # icon
    icon_now = ['http://openweathermap.org/img/w/'+source['weather'][0]['icon']+'.png']
    icon_now[0] = convert(icon_now[0], icons_name)
    
    # wind icon
    icon_wind_now = [round(source['wind']['deg'])+90]
    if icon_wind_now[0] == '0':
        icon_wind_now[0] = 'None'

    # update time
    dt = datetime.fromtimestamp(source['dt'])
    time_update = [dt.strftime('%H:%M')]
    
    # weather text now
    text_now = [source['weather'][0]['description']]
    
    # pressure now
    press_now = [str(round(source['main']['pressure']))]
    if press_now:
        press_now[0] = str(round(int(press_now[0])*0.75))+' mmHg;'+str(round(int(press_now[0])*0.0295))+' inHg;'+press_now[0]+' hPa'
    
    # humidity now
    hum_now = [str(source['main']['humidity'])]
    
    # water temperature now
    # try:
    #     t_water_now = t_now[1]+';'+str(int(C_to_F(t_now[1])))+';'+C_to_K(t_now[1])
    # except:
    #     pass
    
    #### weather to several days ####
    # all days
    # print ('\033[34m>\033[0m '+_('Downloading')+' '+URL_SEVERAL_DAYS)
    # try:
    #     source = urlopen('http://api.openweathermap.org/data/2.5/forecast/daily?id=%s&lang=%s&units=metric&cnt=%s&APPID=%s'%(str(city_id), weather_lang, n+1, APPID))
    #     source = json.loads(source.decode(encoding='UTF-8'))
    #     print ('\033[1;32mOK\033[0m')
    # except:
    #     print ('\033[1;31m[!]\033[0m '+_('Unable to download page, check the network connection'))
    #     if timer_bool:
    #         print ('\033[1;31m[!]\033[0m '+_('Next try in 10 seconds'))
    #     return False
    source = urlopener(URL_SEVERAL_DAYS, 5)
    if not source:
        if timer_bool:
            print ('\033[1;31m[!]\033[0m '+_('Next try in 10 seconds'))
        return False
    source = json.loads(source)
    
    t_day = []
    t_night = []
    day = []
    date = []
    icon = []
    text = []
    wind_speed = []
    wind_direct = []
    chance_of_rain = []

    for data in source['list']:
        t_day.append(add_plus(str(round(data['temp']['day']))))
        t_night.append(add_plus(str(round(data['temp']['night']))))
        dt = datetime.fromtimestamp(data['dt'])
        day.append(dt.strftime('%a'))
        date.append(dt.strftime('%d.%m'))
        icon.append('http://openweathermap.org/img/w/'+data['weather'][0]['icon']+'.png')
        text.append(data['weather'][0]['description'])
        wind_speed.append(str(round(data['speed'])))
        wind_direct.append(wind_direct_convert.convert(data['deg']))
        chance_of_rain.append(str(data['rain']) if 'rain' in data.keys() else '')

    for j in range(len(wind_direct)):
        a=''
        for i in range(len(wind_direct[j])):
            a=a+_(wind_direct[j][i])
        wind_direct[j]=a

    for i in range(len(t_day)):
        t_day[i] = t_day[i]+'°;'+t_day[i]+'°;'+C_to_F(t_day[i])+'°;'+C_to_F(t_day[i])+'°;'+C_to_K(t_day[i])+';'+C_to_K(t_day[i])

    for i in range(len(t_night)):
        t_night[i] = t_night[i]+'°;'+t_night[i]+'°;'+C_to_F(t_night[i])+'°;'+C_to_F(t_night[i])+'°;'+C_to_K(t_night[i])+';'+C_to_K(t_night[i])

    for i in range(len(icon)):
        icon[i] = convert(icon[i], icons_name)

    if wind_speed:
        for i in range(len(wind_speed)):
            wind_speed[i] = wind_speed[i]+' m/s;'+str(round(int(wind_speed[i])*3.6))+' km/h;'+str(round(int(wind_speed[i])*2.237))+' mph'
    
    if show_block_tomorrow or show_block_today:
        # print ('\033[34m>\033[0m '+_('Downloading')+' '+)
        # try:
        #     source = urlopen('http://api.openweathermap.org/data/2.5/forecast?id=%s&lang=%s&units=metric&APPID=%s'%(str(city_id), weather_lang, APPID))
        #     source = json.loads(source.decode(encoding='UTF-8'))
        #     print ('\033[1;32mOK\033[0m')
        # except:
        #     print ('\033[1;31m[!]\033[0m '+_('Unable to download page, check the network connection'))
        #     if timer_bool:
        #         print ('\033[1;31m[!]\033[0m '+_('Next try in 10 seconds'))
        #     return False
        source = urlopener(URL_TODAY_TOMORROW, 5)
        if not source:
            if timer_bool:
                print ('\033[1;31m[!]\033[0m '+_('Next try in 10 seconds'))
            return False
        source = json.loads(source)


        t_tomorrow = ['', '', '', '']
        t_today = ['', '', '', '']
        icon_today = ['', '', '', '']
        icon_tomorrow = ['', '', '', '']
        wind_speed_tod = ['', '', '', '']
        wind_direct_tod = ['', '', '', '']
        wind_speed_tom = ['', '', '', '']
        wind_direct_tom = ['', '', '', '']

        day_today = get_day(source['list'][0])

        for data in source['list']:
            day_tommorow = get_day(data)
            if day_tommorow != day_today:
                break

        for data in source['list']:
            day_after_tommorow = get_day(data)
            if day_after_tommorow != day_today and day_after_tommorow != day_tommorow:
                break

        a_dict = {'00:00':3, '06:00':0, '12:00':1, '18:00':2}

        for data in source['list']:
            if get_time(data) in a_dict.keys():
                if get_day(data) == day_today:
                    t_today[a_dict[get_time(data)]] = add_plus(str(round(data['main']['temp'])))
                    icon_today[a_dict[get_time(data)]] = 'http://openweathermap.org/img/w/'+data['weather'][0]['icon']+'.png'
                    wind_speed_tod[a_dict[get_time(data)]] = str(round(data['wind']['speed']))
                    wind_direct_tod[a_dict[get_time(data)]] = wind_direct_convert.convert(data['wind']['deg'])
                if get_day(data) == day_tommorow:
                    t_tomorrow[a_dict[get_time(data)]] = add_plus(str(round(data['main']['temp'])))
                    icon_tomorrow[a_dict[get_time(data)]] = 'http://openweathermap.org/img/w/'+data['weather'][0]['icon']+'.png'
                    wind_speed_tom[a_dict[get_time(data)]] = str(round(data['wind']['speed']))
                    wind_direct_tom[a_dict[get_time(data)]] = wind_direct_convert.convert(data['wind']['deg'])
                    if get_time(data) == '00:00':
                        t_today[3] = add_plus(str(round(data['main']['temp'])))
                        icon_today[3] = 'http://openweathermap.org/img/w/'+data['weather'][0]['icon']+'.png'
                        wind_speed_tod[3] = str(round(data['wind']['speed']))
                        wind_direct_tod[3] = wind_direct_convert.convert(data['wind']['deg'])
                if get_day(data) == day_after_tommorow and get_time(data) == '00:00':
                    t_tomorrow[3] = add_plus(str(round(data['main']['temp'])))
                    icon_tomorrow[3] = 'http://openweathermap.org/img/w/'+data['weather'][0]['icon']+'.png'
                    wind_speed_tom[3] = str(round(data['wind']['speed']))
                    wind_direct_tom[3] = wind_direct_convert.convert(data['wind']['deg'])

        for i in range(len(t_today)):
            if t_today[i] != '':
                t_today[i] = t_today[i]+'°;'+t_today[i]+'°;'+C_to_F(t_today[i])+'°;'+C_to_F(t_today[i])+'°;'+C_to_K(t_today[i])+';'+C_to_K(t_today[i])
            else:
                t_today[i] = ';;;;;'

        for i in range(len(t_tomorrow)):
            if t_tomorrow[i] != '':
                t_tomorrow[i] = t_tomorrow[i]+'°;'+t_tomorrow[i]+'°;'+C_to_F(t_tomorrow[i])+'°;'+C_to_F(t_tomorrow[i])+'°;'+C_to_K(t_tomorrow[i])+';'+C_to_K(t_tomorrow[i])
            else:
                t_tomorrow[i] = ';;;;;'
        for i in range(len(icon_today)):
            if icon_today[i] != '':
                icon_today[i] = convert(icon_today[i], icons_name)
            else:
                icon_today[i] = 'na.png;na.png'
        for i in range(len(icon_tomorrow)):
            if icon_tomorrow[i] != '':
                icon_tomorrow[i] = convert(icon_tomorrow[i], icons_name)
            else:
                icon_tomorrow[i] = 'na.png;na.png'
        for i in range(len(wind_speed_tod)):
            if wind_speed_tod[i] != '':
                wind_speed_tod[i] = wind_speed_tod[i]+' m/s;'+str(round(int(wind_speed_tod[i])*3.6))+' km/h;'+str(round(int(wind_speed_tod[i])*2.237))+' mph'
            else:
                wind_speed_tod[i] = ';;'
        for i in range(len(wind_speed_tom)):
            if wind_speed_tom[i] != '':
                wind_speed_tom[i] = wind_speed_tom[i]+' m/s;'+str(round(int(wind_speed_tom[i])*3.6))+' km/h;'+str(round(int(wind_speed_tom[i])*2.237))+' mph'
        for j in range(len(wind_direct_tod)):
            a=''
            for i in range(len(wind_direct_tod[j])):
                a=a+_(wind_direct_tod[j][i])
            wind_direct_tod[j]=a
        for j in range(len(wind_direct_tom)):
            a=''
            for i in range(len(wind_direct_tom[j])):
                a=a+_(wind_direct_tom[j][i])
            wind_direct_tom[j]=a
    
    if time_update:
        print ('\033[34m>\033[0m '+_('updated on server')+' '+time_update[0]) 
    print ('\033[34m>\033[0m '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # write variables
    for i in weather.keys():
        weather[i] = globals()[i]
    return weather
    