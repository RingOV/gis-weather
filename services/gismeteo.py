#!/usr/bin/env python3

from urllib.request import urlopen
import re
import time

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


def get_city_name(c_id, weather_lang):
    try:
        source = urlopen('http://www.gismeteo.%s/city/weekly/'%weather_lang + str(c_id), timeout=10).read()
        source = source.decode(encoding='UTF-8')
        c_name = re.findall('type[A-Z].*\">(.*)<', source)
    except:
        print ('[!] '+_('Failed to get the name of the location'))
        return 'None'
    return c_name[0]

def get_weather(weather, n, city_id, show_block_tomorrow, show_block_today, timer_bool, weather_lang):
    #global err_connect, splash
    global city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod 
    print ('> '+_('Getting weather for')+' '+str(n)+' '+_('days'))
    print ('> '+_('Uploading page to a variable')+' '+'http://www.gismeteo.%s/city/weekly/'%weather_lang + str(city_id))
    try:
        source = urlopen('http://www.gismeteo.%s/city/weekly/'%weather_lang + str(city_id), timeout=10).read()
        source = source.decode(encoding='UTF-8')
        print ('OK')
    except:
        print ('[!] '+_('Unable to download page, check the network connection'))
        if timer_bool:
            print ('[!] '+_('Next try in 10 seconds'))
        return False
    #### Текущая погода ####
    w_now = re.findall("type[A-Z].*wrap f_link", source, re.DOTALL)
    
    # Город
    city_name = re.findall('type[A-Z].*\">(.*)<', w_now[0])

    # Температура
    t_now = re.findall('m_temp c.>([&minus;+]*\d+)<', w_now[0])
    for i in range(0, len(t_now)):
        if t_now[i][0] == '&':
            t_now[i] = '-' + t_now[i][7:]

    # Ветер
    wind_speed_now = re.findall('m_wind ms.*>(\d+)<', w_now[0])
    #wind_direct_now1 = re.findall('<dt>([СЮЗВШ]+)</dt>', w_now[0])
    wind_direct_now = re.findall('>(.+)</dt', w_now[0])
    wind_direct_now[0] = wind_direct_now[1]

    # Иконка
    icon_now = re.findall('url\(.*?new\/(.+)\)', w_now[0])
    
    #Иконка ветра
    icon_wind_now = re.findall('wind(\d)', w_now[0])

    # Время обновления
    time_update = re.findall('data-hr.* (\d?\d:\d\d)\s*</span>', source, re.DOTALL)
    
    # Текст погоды сейчас
    text_now = re.findall('title=\"(.*?)\"', w_now[0])
    
    # Давление сейчас
    press_now = re.findall('m_press torr\'>(\d+)<', w_now[0])
    
    # Влажность сейчас
    hum_now = re.findall('wicon hum".*>(\d+)<span class="unit"', w_now[0])
    
    # Температура воды сейчас
    try:
        t_water_now = t_now[1]
    except:
        pass
    
    #### Погода на 2 недели ####
# ------------------------ NEW ------------------------------------
    # все дни с погодой
    w_all_list = re.findall('tbwdaily1.*?rframe wblock wdata', source, re.DOTALL)
    w_all = '\n'.join(w_all_list)
    t_all = re.findall('m_temp c.>([&minus;+]*\d+)<', w_all)
    for i in range(len(t_all)):
        if t_all[i][0] == '&':
            t_all[i] = '-' + t_all[i][7:]
    # все температуры
    t = t_all[::2]
    # все температуры как ощущается
    t_feel = t_all[1::2]

# -----------------------------------------------------------------
    # Погода ночью
    # w_night_list = re.findall('Ночь</th>.*?>Утро</th>', source, re.DOTALL)
    # w_night = '\n'.join(w_night_list)
    
    # Температура ночью
    # t_night = re.findall('m_temp c.>([&minus;+]*\d+)<', w_night)
    # for i in range(0, len(t_night)):
    #     if t_night[i][0] == '&':
    #         t_night[i] = '-' + t_night[i][7:]
    # t_night_feel = t_night[1::2]
    # t_night = t_night[::2]

    # температура ночью
    t_night = t[::4]
    t_night_feel = t_feel[::4]
    
    # День недели и дата
    day = re.findall('weekday.>(.*?)<', source)
    date = re.findall('s_date.>(.*?)<', source)
    
    # Погода днем
    #w_day_list = re.findall('День</th>.*?>Вечер</th>', source, re.DOTALL)
    #w_day = '\n'.join(w_day_list)
    
    # Температура днем
    # t_day = re.findall('m_temp c.>([&minus;+]*\d+)<', w_day) 
    # for i in range(0, len(t_day)):
    #     if t_day[i][0] == '&':
    #         t_day[i] = '-' + t_day[i][7:]
    # t_day_feel = t_day[1::2]
    # t_day = t_day[::2]

    # температура днем
    t_day = t[2::4]
    t_day_feel = t_feel[2::4]
    
    # Иконка погоды днем
    # icon = re.findall('src=\".*?new\/(.*?)\"', w_day)
    icons_list = re.findall('src=\".*?new\/(.*?)\"', w_all)
    icon = icons_list[2::4]
    
    # Иконка ветра
    # icon_wind = re.findall('wind(\d)', w_day)
    icon_wind_list = re.findall('wind(\d)', w_all)
    icon_wind = icon_wind_list[2::4]
    
    # Ветер
    # wind_speed = re.findall('m_wind ms.>(\d+)', w_day)
    # wind_direct = re.findall('>([СЮЗВШ]+)<', w_day)
    wind_speed_list = re.findall('m_wind ms.>(\d+)', w_all)
    wind_speed = wind_speed_list[2::4]
    wind_direct_list = re.findall('>(.+)</dt', w_all)
    wind_direct = wind_direct_list[2::4]
    for i in range(len(wind_direct)):
        wind_direct[i] = wind_direct[i].split('>')[-1]


    # Текст погоды
    #text = re.findall('cltext.>(.*?)<', w_day)
    text_list = re.findall('cltext.>(.*?)<', w_all)
    text = text_list[2::4]

    if show_block_tomorrow:
        #### Погода завтра ####
        #w_tomorrow = re.findall('Ночь</th>.*?>Ночь</div>', source, re.DOTALL)
        w_tomorrow = w_all_list[1]
        
        # Температура
        # t_tomorrow = re.findall('m_temp c.>([&minus;+]*\d+)<', w_tomorrow[1])
        # for i in range(0, len(t_tomorrow)):
        #     if t_tomorrow[i][0] == '&':
        #         t_tomorrow[i] = '-' + t_tomorrow[i][7:]
        t_tomorrow = t[4:8]
        t_tomorrow_feel = t_feel[4:8]
        # Иконка погоды
        #icon_tomorrow = re.findall('src=\".*?new\/(.*?)\"', w_tomorrow[1])
        icon_tomorrow = re.findall('src=\".*?new\/(.*?)\"', w_tomorrow)

        # Ветер
        wind_speed_tom = re.findall('m_wind ms.>(\d+)', w_tomorrow)
        wind_direct_tom = re.findall('>(.+)</dt', w_tomorrow)
        for i in range(len(wind_direct_tom)):
            wind_direct_tom[i] = wind_direct_tom[i].split('>')[-1]
        
    if show_block_today:
        #### Погода сегодня ####
        # if not show_block_tomorrow:
        #     w_tomorrow = re.findall('Ночь</th>.*?>Ночь</div>', source, re.DOTALL)
        w_today = w_all_list[0]
        # Температура
        # t_today = re.findall('m_temp c.>([&minus;+]*\d+)<', w_tomorrow[0])
        # for i in range(0, len(t_today)):
        #     if t_today[i][0] == '&':
        #         t_today[i] = '-' + t_today[i][7:]
        t_today = t[0:4]
        t_today_feel = t_feel[0:4]
        # Иконка погоды
        #icon_today = re.findall('src=\".*?new\/(.*?)\"', w_tomorrow[0])
        icon_today = re.findall('src=\".*?new\/(.*?)\"', w_today)
        # Ветер
        # wind_speed_tod = re.findall('m_wind ms.>(\d+)', w_tomorrow[0])
        # wind_direct_tod = re.findall('>([СЮЗВШ]+)<', w_tomorrow[0])
        wind_speed_tod = re.findall('m_wind ms.>(\d+)', w_today)
        wind_direct_tod = re.findall('>(.+)</dt', w_today)
        for i in range(len(wind_direct_tod)):
            wind_direct_tod[i] = wind_direct_tod[i].split('>')[-1]
    ########
    
    if time_update:
        print ('> '+_('updated on server')+' '+time_update[0]) 
    print ('> '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # if splash:
    #     splash = False
    # записываем переменные
    for i in weather.keys():
        weather[i] = globals()[i]
    return weather