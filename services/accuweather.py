#!/usr/bin/env python3

from utils import weather_vars, gw_vars
from utils.opener import urlopener
from utils.convert import C_to_F, C_to_K, F_to_C, convert_from_kmh
import re
import time
import os

data = [
    "http://www.accuweather.com", # url
    "http://www.accuweather.com/vi/<b>za/sun-city/306096</b>/weather-forecast/306096", # example
    "<b>za/sun-city/306096</b>\n"+_("If the city code is wrong, please read")+" <a href='https://github.com/RingOV/gis-weather/wiki/How-to:-AccuWeather-city-code'>How to: AccuWeather city code</a>", #code
    { 
    'en': 'English',
    'es': 'Español',
    'fr': 'Français',
    'da': 'Dansk',
    'pt': 'Português',
    'nl': 'Nederlands',
    'no': 'Norsk',
    'it': 'Italiano',
    'de': 'Deutsch',
    'sv': 'Svenska',
    'fi': 'Suomi',
    'zh': '中文',
    'es': 'Español',
    'sk': 'Slovenčinu',
    'ro': 'Română',
    'cs': 'Čeština',
    'hu': 'Magyar',
    'pl': 'Polski',
    'ca': 'Català',
    'pt': 'Português',
    'hi': 'हिन्दी',
    'ru': 'Русский',
    'ar': 'عربي',
    'el': 'Ελληνικά',
    'ja': '日本語',
    'ko': '한국어',
    'tr': 'TÜRKÇE',
    'he': 'עברית',
    'sl': 'Slovenski',
    'uk': 'Українська',
    'id': 'Bahasa Indonesia',
    'bg': 'български',
    'et': 'Eesti keeles',
    'hr': 'Hrvatski',
    'kk': 'Қазақша',
    'lt': 'Lietuvių',
    'lv': 'Latviski',
    'mk': 'Македонски',
    'ms': 'Bahasa Melayu',
    'tl': 'Tagalog',
    'sr': 'Srpski',
    'th': 'ไทย',
    'vi': 'Tiếng Việt'
    }, # dict_weather_lang
    ('en', 'ru', 'es', 'fr', 'da', 'pt', 'nl', 'no', 'it', 'de', 'sv', 'fi', 'zh', 'es', 'sk', 'ro', 'cs', 'hu', 'pl', 'ca', 'pt', 'hi', 'ar', 'el', 'ja', 'ko', 'tr', 'he', 'sl', 'uk', 'id', 'bg', 'et', 'hr', 'kk', 'lt', 'lv', 'mk', 'ms', 'tl', 'sr', 'th', 'vi') # weather_lang_list
]

max_days = 14

# weather variables
w = weather_vars.weather
# create variables
for i in w.keys():
    globals()[i] = w[i]

dict_icons = {
    "01-h.png": "32.png",
    "02-h.png": "34.png",
    "03-h.png": "30.png",
    "04-h.png": "28.png",
    "05-h.png": "22.png",
    "06-h.png": "26.png",
    "07-h.png": "26.png",
    "08-h.png": "26.png",
    "11-h.png": "20.png",
    "12-h.png": "40.png",
    "13-h.png": "39.png",
    "14-h.png": "39.png",
    "15-h.png": "03.png",
    "16-h.png": "37.png",
    "17-h.png": "37.png",
    "18-h.png": "40.png",
    "19-h.png": "14.png",
    "20-h.png": "13.png",
    "21-h.png": "41.png",
    "22-h.png": "16.png",
    "23-h.png": "41.png",
    "24-h.png": "06.png",
    "25-h.png": "06.png",
    "26-h.png": "06.png",
    "29-h.png": "05.png",
    "30-h.png": "36.png",
    "31-h.png": "25.png",
    "32-h.png": "23.png",
    "33-h.png": "31.png",
    "34-h.png": "33.png",
    "35-h.png": "29.png",
    "36-h.png": "27.png",
    "37-h.png": "21.png",
    "38-h.png": "27.png",
    "39-h.png": "45.png",
    "40-h.png": "45.png",
    "41-h.png": "47.png",
    "42-h.png": "47.png",
    "43-h.png": "46.png",
    "44-h.png": "46.png",

    "01-xl.png": "32.png",
    "02-xl.png": "34.png",
    "03-xl.png": "30.png",
    "04-xl.png": "28.png",
    "05-xl.png": "22.png",
    "06-xl.png": "26.png",
    "07-xl.png": "26.png",
    "08-xl.png": "26.png",
    "11-xl.png": "20.png",
    "12-xl.png": "40.png",
    "13-xl.png": "39.png",
    "14-xl.png": "39.png",
    "15-xl.png": "03.png",
    "16-xl.png": "37.png",
    "17-xl.png": "37.png",
    "18-xl.png": "40.png",
    "19-xl.png": "14.png",
    "20-xl.png": "13.png",
    "21-xl.png": "41.png",
    "22-xl.png": "16.png",
    "23-xl.png": "41.png",
    "24-xl.png": "06.png",
    "25-xl.png": "06.png",
    "26-xl.png": "06.png",
    "29-xl.png": "05.png",
    "30-xl.png": "36.png",
    "31-xl.png": "25.png",
    "32-xl.png": "23.png",
    "33-xl.png": "31.png",
    "34-xl.png": "33.png",
    "35-xl.png": "29.png",
    "36-xl.png": "27.png",
    "37-xl.png": "21.png",
    "38-xl.png": "27.png",
    "39-xl.png": "45.png",
    "40-xl.png": "45.png",
    "41-xl.png": "47.png",
    "42-xl.png": "47.png",
    "43-xl.png": "46.png",
    "44-xl.png": "46.png"
}

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

def convert(icon, icons_name):
    try:
        icon_converted = dict_icons[os.path.split(icon)[1]]
    except:
        icon_converted = os.path.split(icon)[1]
    return icon+';'+icon_converted

def get_city_name(city_id):
    weather_lang = gw_vars.get('weather_lang')
    try:
        if city_id.split(',')[0]==city_id.split(',')[-1]:
            city_number = city_id.split('/')[-1]
        else:
            city_number = city_id.split(',')[-1].strip()
            city_id = city_id.split(',')[0].strip()
        source = urlopener('http://www.accuweather.com/%s/%s/weather-forecast/%s'%(weather_lang, city_id, city_number))
        c_name = re.findall('"current-city"><h1>(.*),', source)
    except:
        print ('\033[1;31m[!]\033[0m '+_('Failed to get the name of the location'))
        return 'None'
    return c_name[0]

def get_weather():
    global w, city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod, chance_of_rain, t_today_low, t_tomorrow_low
    n = gw_vars.get('n')
    city_id = gw_vars.get('city_id')
    show_block_tomorrow = gw_vars.get('show_block_tomorrow')
    show_block_today = gw_vars.get('show_block_today')
    show_block_add_info = gw_vars.get('show_block_add_info')
    weather_lang = gw_vars.get('weather_lang')
    icons_name = gw_vars.get('icons_name')
    if city_id.split(',')[0]==city_id.split(',')[-1]:
        city_number = city_id.split('/')[-1]
    else:
        city_number = city_id.split(',')[-1].strip()
        city_id = city_id.split(',')[0].strip()
    URL_CURRENT = 'http://www.accuweather.com/%s/%s/current-weather/%s'%(weather_lang, city_id, city_number)
    URL_ADD_INFO = 'http://www.accuweather.com/en/%s/current-weather/%s'%(city_id, city_number)
    URL_SEVERAL_DAYS = 'http://www.accuweather.com/%s/%s/month/%s?view=table'%(weather_lang, city_id, city_number)

    print ('\033[34m>\033[0m '+_('Getting weather for')+' '+str(n)+' '+_('days'))

    source = urlopener(URL_CURRENT, 5)
    if not source:
        return False
    #### current weather ####
    # city
    city_name = re.findall('"current-city"><h1>(.*),', source)

    celsius = re.findall('celsius.*checked', source)

    # temperature
    t_now = re.findall('<span class="temp">(.?\d+)<', source)
    if not celsius:
        t_now[0] = F_to_C(t_now[0])
    if t_now[0][0] not in ('+', '-', '0'):
            t_now[0] = '+'+t_now[0]
    t_now[0] = t_now[0]+'°;'+t_now[0]+'°;'+C_to_F(t_now[0])+'°;'+C_to_F(t_now[0])+'°;'+C_to_K(t_now[0])+';'+C_to_K(t_now[0])

    # wind
    wind_speed_now = re.findall("<div style=\".+\">(\d*).*</div>", source)
    if wind_speed_now:
        wind_speed_now[0] = convert_from_kmh(wind_speed_now[0])
    wind_direct_now = re.findall("arrow-lg-(.*)\.png", source)

    # icon
    icon_now = re.findall('<div class="forecast">\s*<div class="icon (.*)"></div>', source)
    icon_now[0] = icon_now[0][2:]
    if len(icon_now[0])==4:
        icon_now[0]='0'+icon_now[0]
    icon_now[0] = 'http://vortex.accuweather.com/adc2010/images/icons-numbered/'+icon_now[0]+'.png'
    icon_now[0] = convert(icon_now[0], icons_name)
    
    # wind icon
    icon_wind_now = ['']
    try:
        icon_wind_now[0] = wind_degree(wind_direct_now[0])
    except:
        icon_wind_now[0] = 'None'
    try:
        if wind_direct_now[0]=='CLM':
            wind_direct_now[0]=_('Calm')
        else:
            a=''
            for i in range(len(wind_direct_now[0])):
                a=a+_(wind_direct_now[0][i])
            wind_direct_now[0]=a
    except:
        wind_direct_now = []

    
    # weather text now
    text_now = re.findall('<div class="info"> <span class="cond">(.*)<', source)
    text_now[0]=text_now[0].split('<')[0]

    if show_block_add_info:
        source = urlopener(URL_ADD_INFO, 5)
        if not source:
            return False

        # pressure now
        press_now = re.findall('Pressure.*>(\d+)', source)
        try:
            press_now[0] = str(round(int(press_now[0])*0.75))+' mmHg;'+str(round(int(press_now[0])*0.0295))+' inHg;'+press_now[0]+' hPa'
        except:
            press_now = ['n/a mmHg;n/a inHg;n/a hPa']
        # humidity now
        hum_now = re.findall('Humidity.*>(\d+)', source)
        if not hum_now:
            hum_now=['n/a']

    #### weather to several days ####
    source = urlopener(URL_SEVERAL_DAYS, 5)
    if not source:
        return False

    # all days
    w_all = re.findall('<tr class="lo calendar.*</table>', source, re.DOTALL)

    # day temperature
    t_day = re.findall('<td style="font-weight:bold;">(.*)&#176;', w_all[0])
    for i in range(len(t_day)):
        if t_day[i][0] not in ('+', '-', '0'):
            t_day[i] = '+' + t_day[i]
        if not celsius:
            t_day[i] = F_to_C(t_day[i])
        t_day[i] = t_day[i]+'°;'+t_day[i]+'°;'+C_to_F(t_day[i])+'°;'+C_to_F(t_day[i])+'°;'+C_to_K(t_day[i])+';'+C_to_K(t_day[i]) 

    # night temperature
    t_night = re.findall('<td style="font-weight:bold;">.*\s*<td>(.*)&#176;', w_all[0])
    for i in range(len(t_night)):
        if t_night[i][0] not in ('+', '-', '0'):
            t_night[i] = '+' + t_night[i]
        if not celsius:
            t_night[i] = F_to_C(t_night[i])
        t_night[i] = t_night[i]+'°;'+t_night[i]+'°;'+C_to_F(t_night[i])+'°;'+C_to_F(t_night[i])+'°;'+C_to_K(t_night[i])+';'+C_to_K(t_night[i])


    # day of week, date
    day = re.findall('color:.*>(.*)<br', w_all[0])
    date = re.findall('<br />([\d|.\-/]+)<', w_all[0])
    try:
        int(date[0][:4])
        for i in range(len(date)):
            date[i]=date[i][5:]
    except:    
        for i in range(len(date)):
            date[i]=date[i][:-5]

    # weather icon day
    icon = re.findall('src=\"(.*png)\" ', w_all[0])
    for i in range(len(icon)):
        icon[i] = convert(icon[i], icons_name)


    # weather text
    text = re.findall('src=.*>(.*)\r', w_all[0])

    chance_of_rain = re.findall('<td style="font-weight:bold;">.*\s*<td>.*\s*<td>(.*)<', w_all[0])
    # if end of month, get days from next month
    if len(t_day)-1<n:
        try:
            next_month = re.findall('href="(.*)&amp;view=table".*next-month"', source)
            next_month[0] = next_month[0]+'&view=table'
            source = urlopener(next_month[0], 5)
            if not source:
                return False

            # all days
            w_all = re.findall('<tr class="lo calendar.*</table>', source, re.DOTALL)

            # day temperature
            t_day2 = re.findall('<td style="font-weight:bold;">(.*)&#176;', w_all[0])
            for i in range(len(t_day2)):
                if t_day2[i][0] not in ('+', '-', '0'):
                    t_day2[i] = '+' + t_day2[i]
                if not celsius:
                    t_day2[i] = F_to_C(t_day2[i])
                t_day2[i] = t_day2[i]+'°;'+t_day2[i]+'°;'+C_to_F(t_day2[i])+'°;'+C_to_F(t_day2[i])+'°;'+C_to_K(t_day2[i])+';'+C_to_K(t_day2[i]) 
            t_day.extend(t_day2)

            # night temperature
            t_night2 = re.findall('<td style="font-weight:bold;">.*\s*<td>(.*)&#176;', w_all[0])
            for i in range(len(t_night2)):
                if t_night2[i][0] not in ('+', '-', '0'):
                    t_night2[i] = '+' + t_night2[i]
                if not celsius:
                    t_night2[i] = F_to_C(t_night2[i])
                t_night2[i] = t_night2[i]+'°;'+t_night2[i]+'°;'+C_to_F(t_night2[i])+'°;'+C_to_F(t_night2[i])+'°;'+C_to_K(t_night2[i])+';'+C_to_K(t_night2[i])
            t_night.extend(t_night2)

            # day of week, date
            day2 = re.findall('color:.*>(.*)<br', w_all[0])
            date2 = re.findall('<br />([\d|.\-/]+)<', w_all[0])
            try:
                int(date2[0][:4])
                for i in range(len(date2)):
                    date2[i]=date2[i][5:]
            except:    
                for i in range(len(date2)):
                    date2[i]=date2[i][:-5]
            day.extend(day2)
            date.extend(date2)
            # weather icon day
            icon2 = re.findall('src=\"(.*png)\" ', w_all[0])
            for i in range(len(icon2)):
                icon2[i] = convert(icon2[i], icons_name)
            icon.extend(icon2)

            # weather text
            text2 = re.findall('src=.*>(.*)\r', w_all[0])
            if text[-1] == '':
                del text[-1]
            chance_of_rain2 = re.findall('<td style="font-weight:bold;">.*\s*<td>.*\s*<td>(.*)<', w_all[0])
            text.extend(text2)
            chance_of_rain.extend(chance_of_rain2)
        except:
            pass

    if show_block_tomorrow:
        #### weather tomorrow ####
        w_night = urlopener('http://www.accuweather.com/en/%s/overnight-weather-forecast/%s?day=2'%(city_id, city_number), 5)
        if not w_night:
            return False

        w_morning = urlopener('http://www.accuweather.com/en/%s/morning-weather-forecast/%s?day=2'%(city_id, city_number))
        if not w_morning:
            return False

        w_day = urlopener('http://www.accuweather.com/en/%s/afternoon-weather-forecast/%s?day=2'%(city_id, city_number))
        if not w_day:
            return False
        
        w_evening = urlopener('http://www.accuweather.com/en/%s/evening-weather-forecast/%s?day=2'%(city_id, city_number))
        if not w_evening:
            return False
        
        t_tomorrow=[]

        t = re.findall('<span class="temp">(.?\d+)<', w_morning)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_tomorrow.append(t[0])

        t = re.findall('<span class="temp">(.?\d+)<', w_day)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_tomorrow.append(t[0])

        t = re.findall('<span class="temp">(.?\d+)<', w_evening)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_tomorrow.append(t[0])

        t = re.findall('<span class="temp">(.?\d+)<', w_night)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_tomorrow.append(t[0])


        t_tomorrow_low=[]

        t = re.findall('<span class="lo">Lo (.?\d+)<', w_morning)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_tomorrow_low.append(t[0])

        t = re.findall('<span class="lo">Lo (.?\d+)<', w_day)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_tomorrow_low.append(t[0])

        t = re.findall('<span class="lo">Lo (.?\d+)<', w_evening)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_tomorrow_low.append(t[0])

        t = re.findall('<span class="lo">Lo (.?\d+)<', w_night)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_tomorrow_low.append(t[0])

        
        icon_tomorrow=[]

        i = re.findall('<div class="forecast">\s*<div class="icon (.*)"></div>', w_morning)
        i[0] = i[0][2:-2]
        if len(i[0])==2:
            i[0]='0'+i[0]
        i[0] = 'http://vortex.accuweather.com/adc2010/images/icons-numbered/'+i[0]+'h.png'
        i[0] = convert(i[0], icons_name)
        icon_tomorrow.append(i[0])

        i = re.findall('<div class="forecast">\s*<div class="icon (.*)"></div>', w_day)
        i[0] = i[0][2:-2]
        if len(i[0])==2:
            i[0]='0'+i[0]
        i[0] = 'http://vortex.accuweather.com/adc2010/images/icons-numbered/'+i[0]+'h.png'
        i[0] = convert(i[0], icons_name)
        icon_tomorrow.append(i[0])

        i = re.findall('<div class="forecast">\s*<div class="icon (.*)"></div>', w_evening)
        i[0] = i[0][2:-2]
        if len(i[0])==2:
            i[0]='0'+i[0]
        i[0] = 'http://vortex.accuweather.com/adc2010/images/icons-numbered/'+i[0]+'h.png'
        i[0] = convert(i[0], icons_name)
        icon_tomorrow.append(i[0])

        i = re.findall('<div class="forecast">\s*<div class="icon (.*)"></div>', w_night)
        i[0] = i[0][2:-2]
        if len(i[0])==2:
            i[0]='0'+i[0]
        i[0] = 'http://vortex.accuweather.com/adc2010/images/icons-numbered/'+i[0]+'h.png'
        i[0] = convert(i[0], icons_name)
        icon_tomorrow.append(i[0])

        
    if show_block_today:
        #### weather today ####
        w_night = urlopener('http://www.accuweather.com/en/%s/overnight-weather-forecast/%s?day=1'%(city_id, city_number), 5)
        if not w_night:
            return False

        w_morning = urlopener('http://www.accuweather.com/en/%s/morning-weather-forecast/%s?day=1'%(city_id, city_number))
        if not w_morning:
            return False

        w_day = urlopener('http://www.accuweather.com/en/%s/afternoon-weather-forecast/%s?day=1'%(city_id, city_number))
        if not w_day:
            return False
        
        w_evening = urlopener('http://www.accuweather.com/en/%s/evening-weather-forecast/%s?day=1'%(city_id, city_number))
        if not w_evening:
            return False
        
        t_today=[]

        t = re.findall('<span class="temp">(.?\d+)<', w_morning)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_today.append(t[0])

        t = re.findall('<span class="temp">(.?\d+)<', w_day)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_today.append(t[0])

        t = re.findall('<span class="temp">(.?\d+)<', w_evening)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_today.append(t[0])

        t = re.findall('<span class="temp">(.?\d+)<', w_night)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_today.append(t[0])


        t_today_low=[]

        t = re.findall('<span class="lo">Lo (.?\d+)<', w_morning)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_today_low.append(t[0])

        t = re.findall('<span class="lo">Lo (.?\d+)<', w_day)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_today_low.append(t[0])

        t = re.findall('<span class="lo">Lo (.?\d+)<', w_evening)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_today_low.append(t[0])

        t = re.findall('<span class="lo">Lo (.?\d+)<', w_night)
        if t[0][0] not in ('+', '-', '0'):
                t[0] = '+'+t[0]
        if not celsius:
            t[0] = F_to_C(t[0])
        t[0] = t[0]+'°;'+t[0]+'°;'+C_to_F(t[0])+'°;'+C_to_F(t[0])+'°;'+C_to_K(t[0])+';'+C_to_K(t[0])
        t_today_low.append(t[0])

        
        icon_today=[]

        i = re.findall('<div class="forecast">\s*<div class="icon (.*)"></div>', w_morning)
        i[0] = i[0][2:-2]
        if len(i[0])==2:
            i[0]='0'+i[0]
        i[0] = 'http://vortex.accuweather.com/adc2010/images/icons-numbered/'+i[0]+'h.png'
        i[0] = convert(i[0], icons_name)
        icon_today.append(i[0])

        i = re.findall('<div class="forecast">\s*<div class="icon (.*)"></div>', w_day)
        i[0] = i[0][2:-2]
        if len(i[0])==2:
            i[0]='0'+i[0]
        i[0] = 'http://vortex.accuweather.com/adc2010/images/icons-numbered/'+i[0]+'h.png'
        i[0] = convert(i[0], icons_name)
        icon_today.append(i[0])

        i = re.findall('<div class="forecast">\s*<div class="icon (.*)"></div>', w_evening)
        i[0] = i[0][2:-2]
        if len(i[0])==2:
            i[0]='0'+i[0]
        i[0] = 'http://vortex.accuweather.com/adc2010/images/icons-numbered/'+i[0]+'h.png'
        i[0] = convert(i[0], icons_name)
        icon_today.append(i[0])

        i = re.findall('<div class="forecast">\s*<div class="icon (.*)"></div>', w_night)
        i[0] = i[0][2:-2]
        if len(i[0])==2:
            i[0]='0'+i[0]
        i[0] = 'http://vortex.accuweather.com/adc2010/images/icons-numbered/'+i[0]+'h.png'
        i[0] = convert(i[0], icons_name)
        icon_today.append(i[0])

    
    if time_update:
        print ('\033[34m>\033[0m '+_('updated on server')+' '+time_update[0]) 
    print ('\033[34m>\033[0m '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # write variables
    for i in w.keys():
        w[i] = globals()[i]
    return w
