#!/usr/bin/env python3

from utils import weather_vars, gw_vars
from utils.opener import urlopener
from utils.convert import convert_from_ms, convert_from_hPa, convert_from_C
import re
import time
import os

# data = [
#     "http://www.yr.no",  # url
#     "www.yr.no/sted/<b>South_Africa/North-West/Sun_City</b>",  # example
#     "<b>South_Africa/North-West/Sun_City</b>",  # code
#     {
#         'en': 'English'
#     },  # dict_weather_lang
#     ('en', '')  # weather_lang_list
# ]

data = {
    'url': "http://www.yr.no",  # url
    'example': "www.yr.no/sted/<b>South_Africa/North-West/Sun_City</b>",  # example
    'code': "<b>South_Africa/North-West/Sun_City</b>",  # code
    'dict_weather_lang': {
            'en': 'English'
        },  # dict_weather_lang
    'weather_lang_list': ('en', ''),  # weather_lang_list
    'max_days': 8,
    'need_appid': False
}

# weather variables
w = weather_vars.weather
# create variables
for i in w.keys():
    globals()[i] = w[i]

dict_icons = {
    "01d": "32.png",
    "02d": "30.png",
    "03d": "28.png",
    "05d": "39.png",
    "04": "26.png",
    "01n": "31.png",
    "02n": "29.png",
    "03n": "27.png",
    "05n": "45.png",
    "46": "09.png",
    "40n": "45.png",
    "40d": "39.png",
    "09": "11.png",
    "10": "12.png"
}


def convert(icon, icons_name):
    try:
        icon_converted = dict_icons[os.path.split(icon)[1]]
    except:
        try:
            icon_converted = dict_icons[os.path.split(icon)[1].split('.')[0]]
        except:
            icon_converted = os.path.split(icon)[1]+'.png'
    return 'http://symbol.yr.no/grafikk/sym/b38/'+icon+'.png;'+icon_converted


def get_city_name(city_id):
    try:
        source = urlopener('http://www.yr.no/place/%s/forecast.xml'%(str(city_id)), 2)
        c_name = re.findall('<name>(.+)</name>', source)
    except:
        print('\033[1;31m[!]\033[0m '+_('Failed to get the name of the location'))
        return 'None'
    return c_name[0]


def get_weather():
    global time_of_day_list, URL, city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod, chance_of_rain
    n = gw_vars.get('n')
    city_id = gw_vars.get('city_id')
    icons_name = gw_vars.get('icons_name')
    URL = 'http://www.yr.no/place/%s/forecast.xml' % str(city_id)
    print ('\033[34m>\033[0m '+_('Getting weather for')+' '+str(n)+' '+_('days'))

    source = urlopener(URL, 2)
    if not source:
        return False

    URL = 'http://www.yr.no/sted/%s' % str(city_id)

    latitude = re.findall('<location.*latitude="(.+?)"', source)
    longitude = re.findall('<location.*longitude="(.+?)"', source)
    URL_CURRENT = "http://api.met.no/weatherapi/locationforecast/1.9/?lat=%s;lon=%s" %(latitude[0], longitude[0])

    # city
    city_name = re.findall('<name>(.+?)</name>', source)

    # temperature
    temp = re.findall('<temperature unit="celsius" value="(.+?)"', source)
    for i in range(len(temp)):
        temp[i] = convert_from_C(temp[i])
    t_now = [temp[0]]

    # wind
    wind_speed_now = re.findall('<windSpeed mps="(.+?)"', source)
    if wind_speed_now:
        for i in range(len(wind_speed_now)):
            wind_speed_now[i] = convert_from_ms(wind_speed_now[i])

    wind_direct_now = re.findall('<windDirection.*code="(.*?)"', source)

    # icon
    icons = re.findall('<symbol.*var="([mf/]*.+?)"', source)
    for i in range(len(icons)):
        icons[i] = convert(icons[i], icons_name)
    icon_now = [icons[0]]

    # weather text now
    text_now = re.findall('<symbol.*name="(.+?)"', source)

    #### weather to several days ####
    # all days
    dates = re.findall('<time from="\d\d\d\d-(.+?)T', source)

    t_night = ['']
    t_day = ['']
    icon = []
    text = []
    date = [dates[0]]
    wind_speed = ['']
    wind_direct = ['']
    all_periods = re.findall('<time.*period="(\d)"', source)
    for i in range(1, len(all_periods)):
        if all_periods[i] == '0':
            # night
            t_night.append(temp[i])
            pass
        if all_periods[i] == '2':
            # day
            t_day.append(temp[i])
            icon.append(icons[i])
            text.append(text_now[i])
            date.append(dates[i])
            wind_speed.append(wind_speed_now[i])
            wind_direct.append(wind_direct_now[i])
            pass

    #### today tomorrow weather ####
    t_today = [';;;;;', ';;;;;', ';;;;;', ';;;;;']
    t_tomorrow = []
    icon_today = ['clear.png;clear.png', 'clear.png;clear.png', 'clear.png;clear.png', 'clear.png;clear.png']
    icon_tomorrow = []
    wind_speed_tod = ['', '', '', '']
    wind_speed_tom = []
    wind_direct_tod = ['', '', '', '']
    wind_direct_tom = []
    time_of_day_list = ( _('Night'), _('Morning'), _('Day'), _('Evening'))
    a1 = ['0', '1', '2', '3']
    a2 = ['0', '1', '2', '3']
    for i in range(len(all_periods)):
        if all_periods[i] in a1:
            t_today[int(all_periods[i])] = temp[i]
            icon_today[int(all_periods[i])] = icons[i]
            wind_speed_tod[int(all_periods[i])] = wind_speed_now[i]
            wind_direct_tod[int(all_periods[i])] = wind_direct_now[i]
            if all_periods[i] == '3':
                a1 = []
        else:
            if all_periods[i] in a2:
                t_tomorrow.append(temp[i])
                icon_tomorrow.append(icons[i])
                wind_speed_tom.append(wind_speed_now[i])
                wind_direct_tom.append(wind_direct_now[i])
                if all_periods[i] == '3':
                    break

    #### current weather ####
    source = urlopener(URL_CURRENT, 2)
    if not source:
        return False

    # pressure now
    press_now = re.findall('<pressure.*value="(.+?)"', source)
    if press_now:
        press_now[0] = convert_from_hPa(press_now[0])

    hum_now = re.findall('<humidity value="(.+?)"', source)
    hum_now[0] = str(round(float(hum_now[0])))

    t_now = re.findall('<temperature.*unit="celsius" value="(.+?)"', source)
    t_now[0] = convert_from_C(t_now[0])

    wind_speed_now = re.findall('<windSpeed.*mps="(.+?)"', source)
    wind_speed_now[0] = convert_from_ms(wind_speed_now[0])
    wind_direct_now = re.findall('<windDirection.*name="(.+?)"', source)

    icon_wind_now = re.findall('<windDirection.*deg="(.+?)"', source)
    if icon_wind_now[0] == '0':
        icon_wind_now[0] = 'None'
    else:
        icon_wind_now[0] = round(float(icon_wind_now[0]))+90

    print ('\033[34m>\033[0m '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # write variables
    for i in w.keys():
        w[i] = globals()[i]
    return w
