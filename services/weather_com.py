#!/usr/bin/env python3

from urllib.request import urlopen
from utils.t_convert import F_to_C
import re
import time
import os

data = [
    "http://www.weather.com", # url
    "http://www.weather.com/weather/today/<b>ARTF0105</b>:1", # example
    "<b>ARTF0105</b>", #code
    {
        'http://www.weather.com/weather/tenday/': 'English'
    }, # dict_weather_lang
    ('http://www.weather.com/weather/tenday/', '') # weather_lang_list
]

# переменные, в которые записывается погода
city_name = []       # Город
t_now = []           # Температура сейчас
wind_speed_now = []  # Скорость ветра сейчас
wind_direct_now = [] # Направление ветра сейчас
icon_now = []        # Иконка погоды сейчас
icon_wind_now = []   # Иконка ветра сейчас
time_update = []     # Время обновления погоды на сайте
text_now = []        # Текст погоды сейчас
press_now = []       # Давление сейчас
hum_now = []         # Влажность сейчас
t_water_now = []     # Температура воды сейчас

t_night = []         # Температура ночью
t_night_feel = []    # Температура ночью ощущается
day = []             # День недели
date = []            # Дата
t_day = []           # Температура днем
t_day_feel = []      # Температура днем ощущается
icon = []            # Иконка погоды
icon_wind = []       # Иконка ветра
wind_speed = []      # Скорость ветра
wind_direct = []     # Направление ветра
text = []            # Текст погоды

t_tomorrow = []      # Температура завтра
t_tomorrow_feel = [] # Температура завтра ощущается
icon_tomorrow = []   # Иконка погоды завтра
wind_speed_tom = []  # Скорость ветра завтра
wind_direct_tom = [] # Направление ветра завтра

t_today = []         # Температура сегодня
t_today_feel = []    # Температура сегодня ощущается
icon_today = []      # Иконка погоды сегодня
wind_speed_tod = []  # Скорость ветра сегодня
wind_direct_tod = [] # Направление ветра сегодня

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


def get_city_name(c_id, weather_lang):
    try:
        source = urlopen(weather_lang + str(c_id), timeout=10).read()
        source = source.decode(encoding='UTF-8')
        c_name = re.findall('data-location-presentation-name="(.*)"', source)
    except:
        print ('[!] '+_('Failed to get the name of the location'))
        return 'None'
    return c_name[0]

def get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, timer_bool, weather_lang, icons_name):
    global city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod 
    print ('> '+_('Getting weather for')+' '+str(n)+' '+_('days'))
    print ('> '+_('Uploading page to a variable')+' '+weather_lang + str(city_id))
    try:
        source = urlopen(weather_lang + str(city_id), timeout=10).read()
        source = source.decode(encoding='UTF-8')
        print ('OK')
    except:
        print ('[!] '+_('Unable to download page, check the network connection'))
        if timer_bool:
            print ('[!] '+_('Next try in 10 seconds'))
        return False
    #### Текущая погода ####
    w_now = re.findall('data-location-presentation-name=.*<ul class="wx-conditions">', source, re.DOTALL)
    
    # Город
    city_name = re.findall('data-location-presentation-name="(.*)"', w_now[0])
    print (city_name[0])

    # Температура
    t = re.findall('"temperature-fahrenheit">(.*)</span', w_now[0])
    t_fill = re.findall('"feels-like-temperature-fahrenheit">(.*)</span', w_now[0])
    # for i in range(0, len(t_now)):
    #     if t_now[i][0] == '&':
    #         t_now[i] = '-' + t_now[i][7:]
    if t[0][0] not in ('+', '-', '0'):
            t[0] = '+'+t[0]
    if t_fill[0][0] not in ('+', '-', '0'):
            t_fill[0] = '+'+t_fill[0]
    t_c = F_to_C(t[0])
    t_c_fill = F_to_C(t_fill[0])
    t_now = ['']
    t_now[0] = t_c+';'+t_c_fill+';'+t[0]+';'+t_fill[0]

    print(t_now[0])

    # Ветер
    wind_speed_now = re.findall('"wind-speed">(\d+)<', w_now[0])
    wind_speed_now[0] = str(round(int(wind_speed_now[0])*10/36))
    wind_direct_now = re.findall('"wx-dir-arrow wind-dir-(.+)"', w_now[0])
    # wind_direct_now[0] = wind_direct_now[1]
    print (wind_speed_now[0])
    print (wind_direct_now[0])

    # Иконка
    icon_now = re.findall('itemprop="weather-icon">(.*)<', w_now[0])
    icon_now = convert(icon_now, icons_name)
    print (icon_now[0])
    
    # Иконка ветра
    #icon_wind_now = re.findall('wind(\d)', w_now[0])
    icon_wind_now = ['1']

    # Время обновления
    #time_update = re.findall('"last-updated">(.*)<', w_now[0])
    #time_update[0] = time_update[0].split(',')[-1].strip()
    time_update = re.findall(' wx-timestamp">(.*)</div>', source)
    time_update[0] = time_update[0].split()[-3].strip()
    print(time_update[0])
    
    # Текст погоды сейчас
    text_now = re.findall('"weather-phrase">(.*)<', w_now[0])
    print(text_now[0])
    
    # Давление сейчас
    press_now = re.findall('"barometric-pressure.*>(.*)', w_now[0])
    print(press_now[0])
    
    # Влажность сейчас
    hum_now = re.findall('"humidity">(.*)</span>', w_now[0])
    print(hum_now[0])
    
    # Температура воды сейчас
    # try:
    #     t_water_now = t_now[1]
    # except:
    #     pass
    
    #### Погода на 10 дней ####
    # все дни с погодой
    w_all = re.findall('<ul class="wx-conditions">.*"WX_Driver1"', source, re.DOTALL)
    #w_all[0] = w_all[0].split('\n')
    #w_all = ''.join(w_all[0])
    w_all = w_all[0]
    # температура днем
    t_day = re.findall('"wx-temp"> (-*\d+)<', w_all)
    for i in range(len(t_day)):
        if t_day[i][0] not in ('+', '-', '0'):
            t_day[i] = '+'+t_day[i]
        t_day[i] = F_to_C(t_day[i])+';'+F_to_C(t_day[i])+';'+t_day[i]+';'+t_day[i]
    #t_day_feel = t_day
    # температура ночью
    t_night = re.findall('"wx-temp-alt"> (-*\d+)<', w_all)
    for i in range(len(t_night)):
        if t_night[i][0] not in ('+', '-', '0'):
            t_night[i] = '+'+t_night[i]
        t_night[i] = F_to_C(t_night[i])+';'+F_to_C(t_night[i])+';'+t_night[i]+';'+t_night[i]
    #t_night = f_to_c(t_night)
    #t_night_feel = t_night

    print(t_day)
    print(t_night)
    
    # День недели и дата
    day = re.findall('<h3>(.*)', w_all)
    day[0] = day[7]
    print(day)
    date = re.findall('<span class="wx-label">(.+)</span>', w_all)
    #date.pop(1)
    #date.pop(1)
    print(date)

    # Иконка погоды днем
    icon = re.findall('src=\"(.*png)\" ', w_all)
    icon = convert(icon, icons_name)
    print(icon)
    
    # Иконка ветра
    # icon_wind_list = re.findall('wind(\d)', w_all)
    # icon_wind = icon_wind_list[2::4]
    
    # Ветер
    #wind_speed_list = re.findall('m_wind ms.>(\d+)', w_all)
    wind = re.findall('<dd>\n(.*)\n</dd>', w_all)
    wind_speed = []
    #wind_direct_list = re.findall('>(.+)</dt', w_all)
    wind_direct = []
    for i in wind:
        wind_speed.append(str(round(int(i.split()[-2])*10/36)))
        wind_direct.append(i.split()[0])
    # for i in range(len(wind_direct)):
    #     wind_direct[i] = wind_direct[i].split('>')[-1]
    print(wind_speed)
    print(wind_direct)

    # Текст погоды
    text = re.findall('"wx-phrase">(.*)<', w_all)
    print(text)
    
    # if show_block_tomorrow:
    #     #### Погода завтра ####
    #     w_tomorrow = w_all_list[1]
        
    #     # Температура
    #     t_tomorrow = t[4:8]
    #     t_tomorrow_feel = t_feel[4:8]
    #     # Иконка погоды
    #     icon_tomorrow = re.findall('src=\"(.*?new\/.*?)\"', w_tomorrow)
    #     for i in range(len(icon_tomorrow)):
    #         icon_tomorrow[i] = convert(icon_tomorrow[i], icons_name)
    #     # Ветер
    #     wind_speed_tom = re.findall('m_wind ms.>(\d+)', w_tomorrow)
    #     wind_direct_tom = re.findall('>(.+)</dt', w_tomorrow)
    #     for i in range(len(wind_direct_tom)):
    #         wind_direct_tom[i] = wind_direct_tom[i].split('>')[-1]
        
    # if show_block_today:
    #     #### Погода сегодня ####
    #     w_today = w_all_list[0]
    #     # Температура
    #     t_today = t[0:4]
    #     t_today_feel = t_feel[0:4]
    #     # Иконка погоды
    #     icon_today = re.findall('src=\"(.*?new\/.*?)\"', w_today)
    #     for i in range(len(icon_today)):
    #         icon_today[i] = convert(icon_today[i], icons_name)
    #     # Ветер
    #     wind_speed_tod = re.findall('m_wind ms.>(\d+)', w_today)
    #     wind_direct_tod = re.findall('>(.+)</dt', w_today)
    #     for i in range(len(wind_direct_tod)):
    #         wind_direct_tod[i] = wind_direct_tod[i].split('>')[-1]
    ########
    
    if time_update:
        print ('> '+_('updated on server')+' '+time_update[0]) 
    print ('> '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # записываем переменные
    for i in weather.keys():
        weather[i] = globals()[i]
    return weather


#get_weather('weather', 7, 'RSXX6905', True, True, True, 'http://www.weather.com/weather/tenday/', 'icons_name')