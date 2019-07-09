#!/usr/bin/env python3

from utils import weather_vars, wind_direct_convert, gw_vars
from utils.opener import urlopener
from utils.convert import C_to_F, C_to_K, add_plus, convert_from_ms, convert_from_C, convert_from_hPa
import time
import os
import json
from datetime import datetime

data = {
    'url': "http://openweathermap.org/find?q=",  # url
    'example': "http://openweathermap.org/city/<b>1234</b>",  # example
    'code': "<b>1234</b>   <a href='http://openweathermap.org/appid#get'>%s API key (APPID)</a>"%_('How to get'),  # code
    'dict_weather_lang':
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
        },  # dict_weather_lang
    'weather_lang_list': ('en', 'ru', 'it', 'es', 'uk', 'de', 'pt', 'ro', 'pl', 'fi', 'nl', 'fr', 'bg', 'sv', 'zh_tw', 'zh', 'tr', 'hr', 'ca'),  # weather_lang_list
    'max_days': 5,
    'need_appid': True
}

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


def convert(icon):
    try:
        icon_converted = dict_icons[os.path.split(icon)[1]]
    except:
        icon_converted = os.path.split(icon)[1]
    return icon+';'+icon_converted

# APPID = 'dde83a2bee572cb5467f58af45a7987a'


def get_city_name(city_id):
    weather_lang = gw_vars.get('weather_lang')
    APPID = gw_vars.get('appid')
    source = urlopener('http://api.openweathermap.org/data/2.5/weather?id=%s&lang=%s&appid=%s'%(str(city_id), weather_lang, APPID), 2)
    if source:
        source = json.loads(source)
        c_name = source['name']
        return c_name
    else:
        print('\033[1;31m[!]\033[0m '+_('Failed to get the name of the location'))
        if not APPID:
            print('\033[1;31m[!]\033[0m Empty API key. Please enter API key')
        return 'None'


def get_time(source):
    return source['dt_txt'].split()[1][:-3]


def get_day(source):
    return int(source['dt_txt'].split()[0].split('-')[-1])


def get_weather():
    global city_name, URL, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod, chance_of_rain, time_of_day_list, sunrise, sunset, sun_duration
    APPID = gw_vars.get('appid')
    if not APPID:
        print('\033[1;31m[!]\033[0m Empty API key. Please enter API key')
    n = gw_vars.get('n')
    city_id = gw_vars.get('city_id')
    show_block_tomorrow = gw_vars.get('show_block_tomorrow')
    show_block_today = gw_vars.get('show_block_today')
    show_block_add_info = gw_vars.get('show_block_add_info')
    weather_lang = gw_vars.get('weather_lang')
    URL = 'https://openweathermap.org/city/%s'%str(city_id)
    URL_CURRENT = 'http://api.openweathermap.org/data/2.5/weather?id=%s&lang=%s&units=metric&appid=%s'%(str(city_id), weather_lang, APPID)
    URL_SEVERAL_DAYS = 'http://api.openweathermap.org/data/2.5/forecast?id=%s&lang=%s&units=metric&appid=%s'%(str(city_id), weather_lang, APPID)

    print ('\033[34m>\033[0m '+_('Getting weather for')+' '+str(n)+' '+_('days'))

    source = urlopener(URL_CURRENT, 2)
    if not source:
        return False
    source = json.loads(source)

    #### current weather ####
    # city
    city_name = [source['name']]

    # temperature
    t_now = [add_plus(str(round(source['main']['temp'])))]
    t_now[0] = convert_from_C(t_now[0])

    # wind
    wind_speed_now = [str(round(source['wind']['speed']))]
    if wind_speed_now:
        wind_speed_now[0] = convert_from_ms(wind_speed_now[0])
    try:
        wind_direct_now = [wind_direct_convert.convert(source['wind']['deg'])]
    except:
        wind_direct_now = []

    # icon
    icon_now = ['http://openweathermap.org/img/w/'+source['weather'][0]['icon']+'.png']
    icon_now[0] = convert(icon_now[0])

    # wind icon
    try:
        icon_wind_now = [round(source['wind']['deg'])+90]
        if icon_wind_now[0] == '0':
            icon_wind_now[0] = 'None'
    except:
        icon_wind_now = ['None']

    # update time
    dt = datetime.utcfromtimestamp(source['dt']+source['timezone'])
    time_update = [dt.strftime('%H:%M')]
    day = [dt.strftime('%a')]
    date = [dt.strftime('%d.%m')]

    # weather text now
    text_now = [source['weather'][0]['description']]

    # pressure now
    press_now = [str(round(source['main']['pressure']))]
    if press_now:
        press_now[0] = convert_from_hPa(press_now[0])

    # humidity now
    hum_now = [str(source['main']['humidity'])]

    dt1 = datetime.utcfromtimestamp(source['sys']['sunrise']+source['timezone'])
    dt2 = datetime.utcfromtimestamp(source['sys']['sunset']+source['timezone'])
    dt3 = dt2-dt1
    sunrise = dt1.strftime('%H:%M')
    sunset = dt2.strftime('%H:%M')
    sun_duration = ':'.join(str(dt3).split(':')[:2])

    #### weather to several days ####
    source = urlopener(URL_SEVERAL_DAYS, 2)
    if not source:
        return False
    source = json.loads(source)

    wt2 = []
    for data in source['list']:
        t=str(round(data['main']['temp']))
        dt = datetime.utcfromtimestamp(data['dt']+source['city']['timezone'])
        _day=dt.strftime('%a')
        _date=dt.strftime('%d.%m')
        _time=dt.strftime('%H:%M')
        icon='http://openweathermap.org/img/w/'+data['weather'][0]['icon']+'.png'
        text=data['weather'][0]['description']
        wind_speed=str(round(data['wind']['speed']))
        wind_direct=wind_direct_convert.convert(data['wind']['deg'])
        wt2.append({
            't':t,
            'day': _day,
            'date': _date,
            'time': _time,
            'icon': icon,
            'text': text,
            'wind_speed': wind_speed,
            'wind_direct': wind_direct
            })

    wt = [[]]
    i = 0
    _date = date[0]
    # true sort by date for local time
    for item in wt2:
        if _date != item['date']:
            i+=1
            wt.append([])
            _date = item['date']
        wt[i].append(item)

    t_day = ['']
    t_night = ['']
    icon = ['']
    text = ['']
    wind_speed = ['']
    wind_direct = ['']

    for i in range(1, len(wt)):
        max_t = None
        min_t = None
        w_s = 0
        # find max min temp
        for item in wt[i]:
            if max_t == None:
                max_t = item['t']
                min_t = item['t']
            if int(item['t']) > int(max_t):
                max_t = item['t']
            if int(item['t']) < int(min_t):
                min_t = item['t']
            w_s += int(item['wind_speed'])
        t_day.append(convert_from_C(max_t))
        t_night.append(convert_from_C(min_t))
        day.append(wt[i][0]['day'])
        date.append(wt[i][0]['date'])
        index = -1 if len(wt[i])<5 else 4
        icon.append(convert(wt[i][index]['icon']))
        text.append(wt[i][index]['text'])
        # avg wind_speed, may be best max-min
        wind_speed.append(convert_from_ms(str(round(w_s/len(wt[i])))))
        wind_direct.append(wt[i][index]['wind_direct'])

    if show_block_tomorrow or show_block_today:
        t_today = [';;;;;', ';;;;;', ';;;;;', ';;;;;']
        icon_today = ['clear.png;clear.png', 'clear.png;clear.png', 'clear.png;clear.png', 'clear.png;clear.png']
        wind_speed_tod = [';;', ';;', ';;', ';;']
        wind_direct_tod = ['', '', '', '']
        
        t_tomorrow = []
        icon_tomorrow = []
        wind_speed_tom = []
        wind_direct_tom = []

        time_of_day_list = (_('Night'), _('Morning'), _('Day'), _('Evening'))

        # today weather
        w_tod = []
        j = 0
        for i in (-7, -5, -3, -1):
            try:
                t_today[j] = convert_from_C(wt[0][i]['t'])
                icon_today[j] = convert(wt[0][i]['icon'])
                wind_speed_tod[j] = convert_from_ms(wt[0][i]['wind_speed'])
                wind_direct_tod[j] = wt[0][i]['wind_direct']
            except:
                pass
            j+=1

        # tomorrow weather
        for i in (1, 3, 5, 7):
            t_tomorrow.append(convert_from_C(wt[1][i]['t']))
            icon_tomorrow.append(convert(wt[1][i]['icon']))
            wind_speed_tom.append(convert_from_ms(wt[1][i]['wind_speed']))
            wind_direct_tom.append(wt[1][i]['wind_direct'])

    if time_update:
        print ('\033[34m>\033[0m '+_('updated on server')+' '+time_update[0]) 
    print ('\033[34m>\033[0m '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # write variables
    for i in w.keys():
        w[i] = globals()[i]
    return w
    