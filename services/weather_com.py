#!/usr/bin/env python3

from urllib.request import urlopen
from utils.t_convert import F_to_C, F_to_K
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
max_days = 8
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
chance_of_rain = []

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
        print ('[!] '+_('Failed to get the name of the location'))
        return 'None'
    return c_name[0]

def get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, timer_bool, weather_lang, icons_name):
    global city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod, chance_of_rain
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
    t_k = F_to_K(t[0])
    t_k_fill = F_to_K(t_fill[0])
    t_now = ['']
    t_now[0] = t_c+'°;'+t_c_fill+'°;'+t[0]+'°;'+t_fill[0]+'°;'+t_k+';'+t_k_fill


    # Ветер
    wind_speed_now = re.findall('"wind-speed">(\d+)<', w_now[0])
    if wind_speed_now:
        wind_speed_now[0] = str(round(int(wind_speed_now[0])*0.447))+' m/s;'+str(round(int(wind_speed_now[0])*1.609))+' km/h;'+wind_speed_now[0]+' mph'
    wind_direct_now = re.findall('"wx-dir-arrow wind-dir-(.+)"', w_now[0])
    if not wind_direct_now:
        wind_direct_now = ['C']
    # wind_direct_now[0] = wind_direct_now[1]

    # Иконка
    icon_now = re.findall('itemprop="weather-icon">(.*)<', w_now[0])
    icon_now = convert(icon_now, icons_name)
    
    # Иконка ветра
    #icon_wind_now = re.findall('wind(\d)', w_now[0])
    icon_wind_now = ['']
    try:
        icon_wind_now[0] = wind_degree(wind_direct_now[0])
    except:
        icon_wind_now[0] = 'None'

    # Время обновления
    #time_update = re.findall('"last-updated">(.*)<', w_now[0])
    #time_update[0] = time_update[0].split(',')[-1].strip()
    time_update = re.findall(' wx-timestamp">(.*)</div>', source)
    time_update[0] = time_update[0].split()[-3].strip()
    
    # Текст погоды сейчас
    text_now = re.findall('"weather-phrase">(.*)<', w_now[0])
    
    # Давление сейчас
    press_now = re.findall('"barometric-pressure.*>(.*) ', w_now[0])
    if press_now:
        press_now[0] = str(round(float(press_now[0])*25.4))+' mmHg;'+press_now[0]+' inHg;'+str(round(float(press_now[0])*25.4*1.333))+' hPa'
    
    # Влажность сейчас
    hum_now = re.findall('"humidity">(.*)</span>', w_now[0])
    
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
        t_day[i] = F_to_C(t_day[i])+'°;'+F_to_C(t_day[i])+'°;'+t_day[i]+'°;'+t_day[i]+'°;'+F_to_K(t_day[i])+';'+F_to_K(t_day[i])
    #t_day_feel = t_day
    # температура ночью
    t_night = re.findall('"wx-temp-alt"> (-*\d+)<', w_all)
    for i in range(len(t_night)):
        if t_night[i][0] not in ('+', '-', '0'):
            t_night[i] = '+'+t_night[i]
        t_night[i] = F_to_C(t_night[i])+'°;'+F_to_C(t_night[i])+'°;'+t_night[i]+'°;'+t_night[i]+'°;'+F_to_K(t_night[i])+';'+F_to_K(t_night[i])
    #t_night = f_to_c(t_night)
    #t_night_feel = t_night
    
    # День недели и дата
    day = re.findall('<h3>(.*)', w_all)
    day[0] = day[7]
    date = re.findall('<span class="wx-label">(.+)</span>', w_all)
    if len(date) == 12:
        date.pop(1)
        date.pop(1)

    # Иконка погоды днем
    icon = re.findall('src=\"(.*png)\" ', w_all)
    icon = convert(icon, icons_name)
    
    # Иконка ветра
    # icon_wind_list = re.findall('wind(\d)', w_all)
    # icon_wind = icon_wind_list[2::4]
    
    # Ветер
    #wind_speed_list = re.findall('m_wind ms.>(\d+)', w_all)
    wind = re.findall('<dt>Wind:</dt>\n<dd>\n(.*)\n</dd>', w_all)
    wind_speed = []
    #wind_direct_list = re.findall('>(.+)</dt', w_all)
    wind_direct = []
    for i in wind:
        if i.split()[0]==i.split()[-1]:
            wind_speed.append('0')
            wind_direct.append('C')
        else:
            wind_speed.append(i.split()[-2])
            wind_direct.append(i.split()[0])
    if wind_speed:
        print(wind_speed)
        for i in range(len(wind_speed)):
            wind_speed[i] = str(round(int(wind_speed[i])*0.447))+' m/s;'+str(round(int(wind_speed[i])*1.609))+' km/h;'+wind_speed[i]+' mph'
    # for i in range(len(wind_direct)):
    #     wind_direct[i] = wind_direct[i].split('>')[-1]

    # Текст погоды
    text = re.findall('"wx-phrase">(.*)<', w_all)

    chance_of_rain = re.findall('<dd>(\d+%)</dd>', w_all)
    
    if show_block_tomorrow:
        print ('> '+_('Uploading page to a variable')+' http://www.weather.com/weather/tomorrow/' + str(city_id))
        try:
            source = urlopen('http://www.weather.com/weather/tomorrow/' + str(city_id), timeout=10).read()
            source = source.decode(encoding='UTF-8')
            print ('OK')
        except:
            print ('[!] '+_('Unable to download page, check the network connection'))
        t=re.findall('"wx-temp"> (.+)<sup>', source)
        t_tomorrow=[]
        for i in range(len(t)):
            if t[i][0] not in ('+', '-', '0'):
                t[i] = '+'+t[i]
        t_tomorrow.append(F_to_C(t[1])+'°;'+F_to_C(t[1])+'°;'+t[1]+'°;'+t[1]+'°;'+F_to_K(t[1])+';'+F_to_K(t[1]))
        t_tomorrow.append('');
        t_tomorrow.append(F_to_C(t[0])+'°;'+F_to_C(t[0])+'°;'+t[0]+'°;'+t[0]+'°;'+F_to_K(t[0])+';'+F_to_K(t[0]))
        t_tomorrow.append('')
        ic = re.findall('src=\"(.*png)\" ', source)
        ic = convert(ic, icons_name)
        icon_tomorrow=[]
        icon_tomorrow.append(ic[2])
        icon_tomorrow.append('None')
        icon_tomorrow.append(ic[1])
        icon_tomorrow.append('None')
        wind = re.findall('<dt>Wind:</dt>\n<dd>\n(.*)\n</dd>', source)
        wind_speed_tom1=[]
        wind_direct_tom1=[]
        for i in wind:
            if i.split()[0]==i.split()[-1]:
                wind_speed_tom1.append('0')
                wind_direct_tom1.append('C')
            else:
                wind_speed_tom1.append(i.split()[-2])
                wind_direct_tom1.append(i.split()[0])
        wind_direct_tom=[]
        wind_direct_tom.append(wind_direct_tom1[1])
        wind_direct_tom.append('')
        wind_direct_tom.append(wind_direct_tom1[0])
        wind_direct_tom.append('')
        wind_speed_tom=[]
        wind_speed_tom.append(str(round(int(wind_speed_tom1[1])*0.447))+' m/s;'+str(round(int(wind_speed_tom1[1])*1.609))+' km/h;'+wind_speed_tom1[1]+' mph')
        wind_speed_tom.append('')
        wind_speed_tom.append(str(round(int(wind_speed_tom1[0])*0.447))+' m/s;'+str(round(int(wind_speed_tom1[0])*1.609))+' km/h;'+wind_speed_tom1[0]+' mph')
        wind_speed_tom.append('')


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