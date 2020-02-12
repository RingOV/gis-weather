#!/usr/bin/env python3

from utils import weather_vars, gw_vars, wind_direct_convert
from utils.opener import urlopener
from utils.convert import C_to_F, C_to_K, convert_from_ms, convert_from_mmHg, convert_from_C
import re
import time
import os
from datetime import datetime, timezone

data = {
    'url': "http://www.gismeteo.com",  # url
    'example': "https://www.gismeteo.com/weather-alphen-<b>1234</b>",  # example
    'code': "<b>1234</b>",  # code
    'dict_weather_lang':
        {
            'en': 'English',
            'ru': 'Русский',
            'uk': 'Українська',
            'pl': 'Polski',
        },  # dict_weather_lang
    'weather_lang_list': ('en', 'ru', 'uk', 'pl'),  # weather_lang_list
    'max_days': 6,
    'need_appid': False
}

# weather variables
w = weather_vars.weather
# create variables
for i in w.keys():
    globals()[i] = w[i]

CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.config', 'gis-weather')

dict_icons = {
    "d": "32.png",

    "d.c1": "34.png",
    "d.c2": "30.png",
    "d.c3": "28.png",
    "d.c4": "26.png",
    "c4": "26.png",

    "d.c1.s1": "41.png",
    "d.c1.s2": "41.png",
    "d.c1.s3": "41.png",
    "d.c1.s4": "41.png",
    "d.c2.s1": "41.png",
    "d.c2.s2": "41.png",
    "d.c2.s3": "41.png",
    "d.c2.s4": "41.png",
    "d.c3.s1": "41.png",
    "d.c3.s2": "41.png",
    "d.c3.s3": "41.png",
    "d.c3.s4": "41.png",
    "d.c4.s1": "13.png",
    "d.c4.s2": "14.png",
    "d.c4.s3": "16.png",
    "d.c4.s4": "16.png",
    "c4.s1": "13.png",
    "c4.s2": "14.png",
    "c4.s3": "16.png",
    "c4.s4": "16.png",

    "d.c1.r1": "39.png",
    "d.c1.r2": "39.png",
    "d.c1.r3": "39.png",
    "d.c1.r4": "40.png",
    "d.c2.r1": "39.png",
    "d.c2.r2": "39.png",
    "d.c2.r3": "39.png",
    "d.c2.r4": "40.png",
    "d.c3.r1": "39.png",
    "d.c3.r2": "39.png",
    "d.c3.r3": "39.png",
    "d.c3.r4": "40.png",
    "d.c4.r1": "11.png",
    "d.c4.r2": "40.png",
    "d.c4.r3": "40.png",
    "d.c4.r4": "40.png",
    "c4.r1": "11.png",
    "c4.r2": "40.png",
    "c4.r3": "40.png",
    "c4.r4": "40.png",

    "d.c1.r1.st": "37.png",
    "d.c1.r2.st": "37.png",
    "d.c1.r3.st": "37.png",
    "d.c1.r4.st": "37.png",
    "d.c2.r1.st": "37.png",
    "d.c2.r2.st": "37.png",
    "d.c2.r3.st": "37.png",
    "d.c2.r4.st": "37.png",
    "d.c3.r1.st": "37.png",
    "d.c3.r2.st": "37.png",
    "d.c3.r3.st": "37.png",
    "d.c3.r4.st": "37.png",
    "d.c4.r1.st": "35.png",
    "d.c4.r2.st": "35.png",
    "d.c4.r3.st": "35.png",
    "d.c4.r4.st": "35.png",
    "c4.r1.st": "35.png",
    "c4.r2.st": "35.png",
    "c4.r3.st": "35.png",
    "c4.r4.st": "35.png",

    "d.c1.s1.st": "35.png",
    "d.c1.s2.st": "35.png",
    "d.c1.s3.st": "35.png",
    "d.c1.s4.st": "35.png",
    "d.c2.s1.st": "35.png",
    "d.c2.s2.st": "35.png",
    "d.c2.s3.st": "35.png",
    "d.c2.s4.st": "35.png",
    "d.c3.s1.st": "35.png",
    "d.c3.s2.st": "35.png",
    "d.c3.s3.st": "35.png",
    "d.c3.s4.st": "35.png",
    "d.c4.s1.st": "35.png",
    "d.c4.s2.st": "35.png",
    "d.c4.s3.st": "35.png",
    "d.c4.s4.st": "35.png",
    "c4.s1.st": "35.png",
    "c4.s2.st": "35.png",
    "c4.s3.st": "35.png",
    "c4.s4.st": "35.png",

    "d.c3.rs1": "41.png",
    "d.c3.rs2": "41.png",
    "d.c3.rs3": "41.png",
    "d.c3.rs4": "41.png"

    "d.c2.rs1": "41.png",
    "d.c2.rs2": "41.png",
    "d.c2.rs3": "41.png",
    "d.c2.rs4": "41.png",

    "c4.rs1": "05.png",
    "c4.rs2": "05.png",
    "c4.rs3": "05.png",
    "c4.rs4": "05.png",

    "n": "31.png",
    "n.c1": "33.png",
    "n.c2": "29.png",
    "n.c3": "27.png",
    "n.c4": "26.png",

    "n.c1.s1": "46.png",
    "n.c1.s2": "46.png",
    "n.c1.s3": "46.png",
    "n.c1.s4": "46.png",
    "n.c2.s1": "46.png",
    "n.c2.s2": "46.png",
    "n.c2.s3": "46.png",
    "n.c2.s4": "46.png",
    "n.c3.s1": "46.png",
    "n.c3.s2": "46.png",
    "n.c3.s3": "46.png",
    "n.c3.s4": "46.png",
    "n.c4.s1": "13.png",
    "n.c4.s2": "15.png",
    "n.c4.s3": "16.png",
    "n.c4.s4": "16.png",

    "n.c1.r1": "45.png",
    "n.c1.r2": "45.png",
    "n.c1.r3": "45.png",
    "n.c1.r4": "40.png",
    "n.c2.r1": "45.png",
    "n.c2.r2": "45.png",
    "n.c2.r3": "45.png",
    "n.c2.r4": "40.png",
    "n.c3.r1": "45.png",
    "n.c3.r2": "45.png",
    "n.c3.r3": "45.png",
    "n.c3.r4": "40.png",
    "n.c4.r1": "11.png",
    "n.c4.r2": "40.png",
    "n.c4.r3": "40.png",
    "n.c4.r4": "40.png",

    "n.c1.r1.st": "47.png",
    "n.c1.r2.st": "47.png",
    "n.c1.r3.st": "47.png",
    "n.c1.r4.st": "47.png",
    "n.c2.r1.st": "47.png",
    "n.c2.r2.st": "47.png",
    "n.c2.r3.st": "47.png",
    "n.c2.r4.st": "47.png",
    "n.c3.r1.st": "47.png",
    "n.c3.r2.st": "47.png",
    "n.c3.r3.st": "47.png",
    "n.c3.r4.st": "47.png",
    "n.c4.r1.st": "35.png",
    "n.c4.r2.st": "35.png",
    "n.c4.r3.st": "35.png",
    "n.c4.r4.st": "35.png",

    "n.c1.s1.st": "47.png",
    "n.c1.s2.st": "47.png",
    "n.c1.s3.st": "47.png",
    "n.c1.s4.st": "47.png",
    "n.c2.s1.st": "47.png",
    "n.c2.s2.st": "47.png",
    "n.c2.s3.st": "47.png",
    "n.c2.s4.st": "47.png",
    "n.c3.s1.st": "47.png",
    "n.c3.s2.st": "47.png",
    "n.c3.s3.st": "47.png",
    "n.c3.s4.st": "47.png",
    "n.c4.s1.st": "35.png",
    "n.c4.s2.st": "35.png",
    "n.c4.s3.st": "35.png",
    "n.c4.s4.st": "35.png",

    "d.c1.st": "38.png",
    "d.c2.st": "38.png",
    "d.c3.st": "38.png",
    "d.c4.st": "35.png",
    "n.c1.st": "47.png",
    "n.c2.st": "47.png",
    "n.c3.st": "47.png",
    "n.c4.st": "35.png",
    "d.st": "22.png",
    "d.st.r1": "22.png",
    "d.st.r2": "22.png",
    "d.st.r3": "22.png",
    "d.st.r4": "22.png",
    "n.st": "21.png",
    "n.st.r1": "21.png",
    "n.st.r2": "21.png",
    "n.st.r3": "21.png",
    "n.st.r4": "21.png",
    "d.st.s1": "13.png",
    "d.st.s2": "14.png",
    "d.st.s3": "16.png",
    "d.st.s4": "16.png",
    "n.st.s1": "13.png",
    "n.st.s2": "14.png",
    "n.st.s3": "16.png",
    "n.st.s4": "16.png"
    }


def convert(icon, icons_name):
    try:
        icon_converted = dict_icons[os.path.split(icon)[1]]
    except:
        icon_converted = os.path.split(icon)[1]
    return icon_converted+';'+icon_converted


def get_city_name(city_id):
    weather_lang = gw_vars.get('weather_lang')
    if weather_lang == 'ua/ru':
        weather_lang = 'ru'
    try:
        source = urlopener('https://services.gismeteo.ru/inform-service/inf_chrome/forecast/?lang=%s&city=%s'%(weather_lang, str(city_id)))
        c_name = re.findall(' name="(.*?)"', source)
    except:
        print ('\033[1;31m[!]\033[0m '+_('Failed to get the name of the location'))
        return 'None'
    return c_name[0]


def get_weather():
    global time_of_day_list, w, sunrise, sunset, sun_duration, URL, URL_HOURLY, URL_DAILY, city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod, chance_of_rain, t_today_low, t_tomorrow_low
    n = gw_vars.get('n')
    city_id = gw_vars.get('city_id')
    show_block_tomorrow = gw_vars.get('show_block_tomorrow')
    show_block_today = gw_vars.get('show_block_today')
    show_block_add_info = gw_vars.get('show_block_add_info')
    weather_lang = gw_vars.get('weather_lang')
    if weather_lang == 'ua/ru':
        weather_lang = 'ru'
    icons_name = gw_vars.get('icons_name')

    URL_ALL = 'https://services.gismeteo.ru/inform-service/inf_chrome/forecast/?lang=%s&city=%s'%(weather_lang, str(city_id))
    
    URL = 'https://www.gismeteo.%s/city/weekly/'%weather_lang + str(city_id)
    URL_HOURLY = 'https://www.gismeteo.%s/city/hourly/%s'%(weather_lang, str(city_id))
    # URL_DAILY = 'https://www.gismeteo.%s/city/weekly/%s/#wweekly'%(weather_lang, str(city_id))

    print ('\033[34m>\033[0m '+_('Getting weather for')+' '+str(n)+' '+_('days'))

    source = urlopener(URL_ALL, 2)
    if not source:
        return False

    # city
    city_name = re.findall(' name="(.*?)"', source)

    # sun
    dt1 = datetime.utcfromtimestamp(int(re.findall('<fact.*?sunrise="(.*?)"', source)[0]))
    dt2 = datetime.utcfromtimestamp(int(re.findall('<fact.*?sunset="(.*?)"', source)[0]))
    dt3 = dt2 - dt1
    sunrise = dt1.strftime('%H:%M')
    sunset = dt2.strftime('%H:%M')
    sun_duration = ':'.join(str(dt3).split(':')[:2])

    # temperature
    t_now = re.findall('<fact.*? t="(.*?)"',source)
    t_now[0] = convert_from_C(t_now[0])

    # wind
    wind_speed_now = re.findall('<fact.*? ws="(.*?)"', source)
    wind_speed_now[0] = convert_from_ms(wind_speed_now[0])
    s = re.findall('<fact.*? wd="(.*?)"', source)[0]
    wind_direct_now = [wind_direct_convert.convert2(s)]
    if s == '0':
        icon_wind_now = ['None']
    else:
        icon_wind_now = [int(s)*45+45]

    # icon
    icon_now = re.findall('<fact.*? icon="(.*?)"', source)
    icon_now[0] = convert(icon_now[0], icons_name)

    # update time
    time_update = re.findall('<fact.*? valid="(.*?)"', source)
    time_update[0] = time_update[0][-8:-3]

    # weather text now
    text_now = re.findall('<fact.*? descr="(.*?)"', source)

    # pressure now
    press_now = re.findall('<fact.*? p="(.*?)"', source)
    press_now[0] = convert_from_mmHg(press_now[0])

    # humidity now
    hum_now = re.findall('<fact.*? hum="(.*?)"', source)

    # water temperature now
    t_water_now = re.findall('<fact.*? water_t="(.*?)"', source)
    t_water_now = t_water_now[0]+';'+str(int(C_to_F(t_water_now[0])))+';'+C_to_K(t_water_now[0])

    #### weather to several days ####
    # night temperature
    t_night = re.findall('<day.*? tmin="(.*?)"', source)
    for i in range(len(t_night)):
        t_night[i] = convert_from_C(t_night[i], t_night[i])
    # day temperature
    t_day = re.findall('<day.*? tmax="(.*?)"', source)
    for i in range(len(t_day)):
        t_day[i] = convert_from_C(t_day[i], t_day[i])

    # day of week, date
    day = re.findall('<day.*? date="(.*?)"', source)
    day.pop(0)
    for i in range(len(day)):
        dt1 = datetime.strptime(day[i], '%Y-%m-%d')
        day[i] = dt1.strftime('%a')
    date = re.findall('<day.*? date=".*?-(.*?)"', source)
    date.pop(0)
    for i in range(len(date)):
        s = date[i].split('-')
        date[i] = s[1]+'.'+s[0]

    # weather icon day
    icon = re.findall('<day.*? icon="(.*?)"', source, re.DOTALL)
    for i in range(len(icon)):
        icon[i] = convert(icon[i], icons_name)

    # wind
    wind_speed = re.findall('<day.*? ws="(.*?)"', source, re.DOTALL)
    for i in range(len(wind_speed)):
        wind_speed[i] = convert_from_ms(wind_speed[i])
    wind_direct = re.findall('<day.*? wd="(.*?)"', source, re.DOTALL)
    icon_wind = []
    for i in range(len(wind_direct)):
        if wind_direct[i] == '0':
            icon_wind.append('None')
        else:
            icon_wind.append(int(wind_direct[i])*45+45)
        wind_direct[i] = wind_direct_convert.convert2(wind_direct[i])

    # weather text
    text = re.findall('<day.*? descr="(.*?)"', source,  re.DOTALL)

    time_of_day_list = ( _('Night'), _('Morning'), _('Day'), _('Evening'))

    w_today_tomorrow = re.findall('<forecast(.*?)</day>', source,  re.DOTALL)
    
    if show_block_today:
        #### weather today ####
        w_today = w_today_tomorrow[0]
        # temperature
        t_today = re.findall(' t="(.*?)"', w_today)[::2]
        for i in range(len(t_today)):
            t_today[i] = convert_from_C(t_today[i], t_today[i])

        # weather icon
        icon_today = re.findall(' icon="(.*?)"', w_today)[::2]
        for i in range(len(icon_today)):
            icon_today[i] = convert(icon_today[i], icons_name)
        # wind
        wind_speed_tod = re.findall(' ws="(.*?)"', w_today)[::2]
        if wind_speed_tod:
            for i in range(len(wind_speed_tod)):
                wind_speed_tod[i] = convert_from_ms(wind_speed_tod[i])
        wind_direct_tod = re.findall(' wd="(.*?)"', w_today)[::2]
        for i in range(len(wind_direct_tod)):
            wind_direct_tod[i] = wind_direct_convert.convert2(wind_direct_tod[i])

    if show_block_tomorrow:
        #### weather tomorrow ####
        w_tomorrow = w_today_tomorrow[1]
        # temperature
        t_tomorrow = re.findall(' t="(.*?)"', w_tomorrow)[::2]
        for i in range(len(t_tomorrow)):
            t_tomorrow[i] = convert_from_C(t_tomorrow[i], t_tomorrow[i])

        # weather icon
        icon_tomorrow = re.findall(' icon="(.*?)"', w_tomorrow)[::2]
        for i in range(len(icon_tomorrow)):
            icon_tomorrow[i] = convert(icon_tomorrow[i], icons_name)
        # wind
        wind_speed_tom = re.findall(' ws="(.*?)"', w_tomorrow)[::2]
        if wind_speed_tom:
            for i in range(len(wind_speed_tom)):
                wind_speed_tom[i] = convert_from_ms(wind_speed_tom[i])
        wind_direct_tom = re.findall(' wd="(.*?)"', w_tomorrow)[::2]
        for i in range(len(wind_direct_tom)):
            wind_direct_tom[i] = wind_direct_convert.convert2(wind_direct_tom[i])

    ########

    if time_update:
        print ('\033[34m>\033[0m '+_('updated on server')+' '+time_update[0]) 
    print ('\033[34m>\033[0m '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # write variables
    for i in w.keys():
        w[i] = globals()[i]
    return w
