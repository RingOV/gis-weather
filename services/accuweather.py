#!/usr/bin/env python3

from utils import weather_vars, gw_vars
from utils.opener import urlopener
from utils.convert import C_to_F, C_to_K, F_to_C, convert_from_kmh, convert_from_C, convert_from_inHg, convert_from_hPa
import re
import time
import os

data = [
    "http://www.accuweather.com", # url
    "http://www.accuweather.com/en/<b>us/new-york-ny/10017</b>/weather-forecast/<b>349727</b>", # example
    "<b>us/new-york-ny/10017,349727</b>\n"+_("If the city code is wrong, please read")+" <a href='https://github.com/RingOV/gis-weather/wiki/How-to:-AccuWeather-city-code'>How to: AccuWeather city code</a>", #code
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
need_appid = False

# weather variables
w = weather_vars.weather
# create variables
for i in w.keys():
    globals()[i] = w[i]

encode_list = {
    'i-1-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/01.svg',
    'i-2-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/02.svg',
    'i-3-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/03.svg',
    'i-4-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/04.svg',
    'i-5-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/05.svg',
    'i-6-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/06.svg',
    'i-7-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/07.svg',
    'i-8-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/08.svg',
    'i-9-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/09.svg',
    'i-10-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/10.svg',
    'i-11-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/11.svg',
    'i-12-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/12.svg',
    'i-13-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/13.svg',
    'i-14-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/14.svg',
    'i-15-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/15.svg',
    'i-16-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/16.svg',
    'i-17-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/17.svg',
    'i-18-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/18.svg',
    'i-19-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/19.svg',
    'i-20-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/20.svg',
    'i-21-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/21.svg',
    'i-22-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/22.svg',
    'i-23-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/23.svg',
    'i-24-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/24.svg',
    'i-25-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/25.svg',
    'i-26-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/26.svg',
    'i-27-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/27.svg',
    'i-28-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/28.svg',
    'i-29-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/29.svg',
    'i-30-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/30.svg',
    'i-31-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/31.svg',
    'i-32-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/32.svg',
    'i-33-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/33.svg',
    'i-34-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/34.svg',
    'i-35-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/35.svg',
    'i-36-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/36.svg',
    'i-37-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/37.svg',
    'i-38-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/38.svg',
    'i-39-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/39.svg',
    'i-40-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/40.svg',
    'i-41-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/41.svg',
    'i-42-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/42.svg',
    'i-43-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/43.svg',
    'i-44-': 'http://vortex.accuweather.com/adc2010/images/slate/icons/44.svg',  
    }

dict_icons = {
    'i-1-': '32.png',
    'i-2-': '34.png',
    'i-3-': '30.png',
    'i-4-': '28.png',
    'i-5-': '22.png',
    'i-6-': '26.png',
    'i-7-': '26.png',
    'i-8-': '26.png',
    'i-11-': '20.png',
    'i-12-': '40.png',
    'i-13-': '39.png',
    'i-14-': '39.png',
    'i-15-': '03.png',
    'i-16-': '37.png',
    'i-17-': '37.png',
    'i-18-': '40.png',
    'i-19-': '14.png',
    'i-20-': '13.png',
    'i-21-': '41.png',
    'i-22-': '16.png',
    'i-23-': '41.png',
    'i-24-': '06.png',
    'i-25-': '06.png',
    'i-26-': '06.png',
    'i-29-': '05.png',
    'i-30-': '36.png',
    'i-31-': '25.png',
    'i-32-': '23.png',
    'i-33-': '31.png',
    'i-34-': '33.png',
    'i-35-': '29.png',
    'i-36-': '27.png',
    'i-37-': '21.png',
    'i-38-': '27.png',
    'i-39-': '45.png',
    'i-40-': '45.png',
    'i-41-': '47.png',
    'i-42-': '47.png',
    'i-43-': '46.png',
    'i-44-': '46.png',
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
    return encode_list[icon]+';'+icon_converted

def get_city_name(city_id):
    weather_lang = gw_vars.get('weather_lang')
    try:
        if city_id.split(',')[0]==city_id.split(',')[-1]:
            city_number = city_id.split('/')[-1]
        else:
            city_number = city_id.split(',')[-1].strip()
            city_id = city_id.split(',')[0].strip()
        source = urlopener('http://www.accuweather.com/%s/%s/current-weather/%s'%(weather_lang, city_id, city_number))
        c_name = re.findall('"current-city"><h1>(.*),', source)
    except:
        print ('\033[1;31m[!]\033[0m '+_('Failed to get the name of the location'))
        return 'None'
    return c_name[0]

def get_weather():
    global w, sunrise, sunset, sun_duration, moonrise, moonset, moon_duration, URL, URL_HOURLY, URL_DAILY, city_name, t_now, wind_speed_now, wind_direct_now, icon_now, icon_wind_now, time_update, text_now, press_now, hum_now, t_water_now, t_night, t_night_feel, day, date, t_day, t_day_feel, icon, icon_wind, wind_speed, wind_direct, text, t_tomorrow, t_tomorrow_feel, icon_tomorrow, wind_speed_tom, wind_direct_tom, t_today, t_today_feel, icon_today, wind_speed_tod, wind_direct_tod, chance_of_rain, t_today_low, t_tomorrow_low
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

    URL = URL_CURRENT
    URL_HOURLY = 'http://www.accuweather.com/%s/%s/hourly-weather-forecast/%s'%(weather_lang, city_id, city_number)
    URL_DAILY = 'http://www.accuweather.com/%s/%s/daily-weather-forecast/%s?day='%(weather_lang, city_id, city_number)

    print ('\033[34m>\033[0m '+_('Getting weather for')+' '+str(n)+' '+_('days'))

    source = urlopener(URL_CURRENT, 5)
    if not source:
        return False
    # time.sleep(1)

    # sun/moon
    sun_moon = re.findall('<span>(.*)</span></li>', source)

    if sun_moon:
        sunrise = sun_moon[1]
        sunset = sun_moon[2]
        sun_duration = sun_moon[3][:-3]
        moonrise = sun_moon[4]
        moonset = sun_moon[5]
        moon_duration = sun_moon[6][:-3]

    #### current weather ####
    # city
    city_name = re.findall('"current-city"><h1>(.*),', source)

    celsius = re.findall('\d\&deg;C', source)

    # temperature
    w_now = re.findall('detail-now.*', source, re.DOTALL)
    t_now = re.findall('<span class="large-temp">(.?\d+)', w_now[0])
    t_now_f = re.findall('<em>RealFeel&#174;</em>\s?(.?\d+)', w_now[0])
    if not celsius:
        t_now[0] = F_to_C(t_now[0])
        t_now_f[0] = F_to_C(t_now_f[0])
    t_now[0] = convert_from_C(t_now[0], t_now_f[0])

    # wind
    wind_speed_now = re.findall('<li class="wind"><strong>(\d*)', source)
    if wind_speed_now:
        wind_speed_now[0] = convert_from_kmh(wind_speed_now[0])
    wind_direct_now = re.findall('<div class="wind-point (.*)"', w_now[0])

    # icon
    icon_now = re.findall('<div class="icon (.*)xl"', w_now[0])
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
    text_now = re.findall('<span class="cond">(.*)<', w_now[0])
    text_now[0]=text_now[0].split('<')[0]
    
    # if show_block_add_info:
    source = urlopener(URL_ADD_INFO, 5)
    if not source:
        return False
    # time.sleep(1)

    # pressure now
    press = re.findall('Pressure.*>(.+?)<', source)
    if press:
        press_now = [press[0].split()[0]]
        press_scale = press[0].split()[1]
        if press_scale == 'mb':
            press_now[0] = convert_from_hPa(press_now[0])
        if press_scale == 'in':
            press_now[0] = convert_from_inHg(press_now[0])
    else:
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
    w_all = re.findall('<tr class="today lo calendar.*</table>', source, re.DOTALL)

    # day temperature
    t_day = re.findall('<td>(.*)&#176;/', w_all[0])
    t_day = t_day[::2]
    for i in range(len(t_day)):
        if not celsius:
            t_day[i] = F_to_C(t_day[i])
        t_day[i] = convert_from_C(t_day[i])

    # night temperature
    t_night = re.findall('<td>.*/(.*)&#176;', w_all[0])
    t_night = t_night[::2]
    for i in range(len(t_night)):
        if not celsius:
            t_night[i] = F_to_C(t_night[i])
        t_night[i] = convert_from_C(t_night[i])


    # day of week, date
    day = re.findall('<a.*>(.*)[.| ]*<time>', w_all[0])
    date = re.findall('<time>(.*)</time>', w_all[0])
    # try:
    #     int(date[0][:4])
    #     for i in range(len(date)):
    #         date[i]=date[i][5:]
    # except:
    #     for i in range(len(date)):
    #         date[i]=date[i][:-5]

    # weather icon day
    icon = re.findall('<div class="icon (.*)s"', w_all[0])
    for i in range(len(icon)):
        icon[i] = convert(icon[i], icons_name)


    # weather text
    text = re.findall('<p>(.*)</p>', w_all[0])

    chance_of_rain = re.findall('<td>(.*?)\s*<span class="small">(.*?)<', w_all[0])
    for i in range(len(chance_of_rain)):
        chance_of_rain[i] = ' '.join(chance_of_rain[i])
    chance_of_rain = chance_of_rain[::2]


    # if end of month, get days from next month
    if len(t_day)-1<n:
        try:
            next_month = re.findall('href="(.*)&amp;.*next-month', source)
            next_month[0] = next_month[0]+'&view=table'
            source = urlopener(next_month[0], 5)
            if not source:
                return False

            # all days
            w_all = re.findall('<tr class="lo calendar-list-cl-tr.*</table>', source, re.DOTALL)

            # day temperature
            t_day2 = re.findall('<td>(.*)&#176;/', w_all[0])
            t_day2 = t_day2[::2]
            for i in range(len(t_day2)):
                if not celsius:
                    t_day2[i] = F_to_C(t_day2[i])
                t_day2[i] = convert_from_C(t_day2[i])
            t_day.extend(t_day2)

            # night temperature
            t_night2 = re.findall('<td>.*/(.*)&#176;', w_all[0])
            t_night2 = t_night2[::2]
            for i in range(len(t_night2)):
                if not celsius:
                    t_night2[i] = F_to_C(t_night2[i])
                t_night2[i] = convert_from_C(t_night2[i])
            t_night.extend(t_night2)


            # day of week, date
            day2 = re.findall('<a.*>(.*)[.| ]*<time>', w_all[0])
            date2 = re.findall('<time>(.*)</time>', w_all[0])
            # try:
            #     int(date2[0][:4])
            #     for i in range(len(date2)):
            #         date2[i]=date2[i][5:]
            # except:
            #     for i in range(len(date2)):
            #         date2[i]=date2[i][:-5]
            day.extend(day2)
            date.extend(date2)


            # weather icon day
            icon2 = re.findall('<div class="icon (.*)s"', w_all[0])
            for i in range(len(icon2)):
                icon2[i] = convert(icon2[i], icons_name)
            icon.extend(icon2)


            # weather text
            text2 = re.findall('<p>(.*)</p>', w_all[0])
            # if text[-1] == '': # Need or not?
            #     del text[-1]
            text.extend(text2)


            chance_of_rain2 = re.findall('<td>(\d+)\s*<span class="small">(.*)</td>', w_all[0])
            for i in range(len(chance_of_rain2)):
                chance_of_rain2[i] = ' '.join(chance_of_rain2[i])
            if chance_of_rain2[1][-1] == '>':
                chance_of_rain2 = chance_of_rain2[::2]
            chance_of_rain.extend(chance_of_rain2)

        except:
            print('Can\'t get weather for next month')
            pass

    if show_block_tomorrow:
        #### weather tomorrow ####
        source = ['', '', '', '']
        for i, w_time in zip(range(4), ['morning', 'afternoon', 'evening', 'overnight']):
            source[i] = urlopener('http://www.accuweather.com/en/%s/%s-weather-forecast/%s?day=2'%(city_id, w_time, city_number), 5)
            if not source[i]:
                return False

        t_tomorrow=[]
        t_tomorrow_low = []
        icon_tomorrow = []
        
        for s in source:
            w_now = re.findall('detail-now.*', s, re.DOTALL)
            
            t = re.findall('<span class="large-temp">(.?\d+)', w_now[0])
            t_feel = re.findall('<em>RealFeel&#174;</em>\s?(.?\d+).*;/(.?\d+)', w_now[0])
            t_f = ['', '']
            if not celsius:
                t[0] = F_to_C(t[0])
                t_f[0] = F_to_C(t_feel[0][0])
                t_f[1] = F_to_C(t_feel[0][1])
            t[0] = convert_from_C(t[0], t_f[0])
            t_tomorrow.append(t[0])
            
            t = re.findall('<span class="small-temp">/(.?\d+)', w_now[0])
            if not celsius:
                t[0] = F_to_C(t[0])
            t[0] = convert_from_C(t[0], t_f[1])
            t_tomorrow_low.append(t[0])
            
            i = re.findall('<div class="icon (.*)xl"', w_now[0])
            i[0] = convert(i[0], icons_name)
            icon_tomorrow.append(i[0])
        

    if show_block_today:
        #### weather today ####
        source = ['', '', '', '']
        for i, w_time in zip(range(4), ['morning', 'afternoon', 'evening', 'overnight']):
            source[i] = urlopener('http://www.accuweather.com/en/%s/%s-weather-forecast/%s?day=1'%(city_id, w_time, city_number), 5)
            if not source[i]:
                return False

        t_today=[]
        t_today_low = []
        icon_today = []
        
        for s in source:
            w_now = re.findall('detail-now.*', s, re.DOTALL)
            
            t = re.findall('<span class="large-temp">(.?\d+)', w_now[0])
            t_feel = re.findall('<em>RealFeel&#174;</em>\s?(.?\d+).*;/(.?\d+)', w_now[0])
            t_f = ['', '']
            if not celsius:
                t[0] = F_to_C(t[0])
                t_f[0] = F_to_C(t_feel[0][0])
                t_f[1] = F_to_C(t_feel[0][1])
            t[0] = convert_from_C(t[0], t_f[0])
            t_today.append(t[0])
            
            t = re.findall('<span class="small-temp">/(.?\d+)', w_now[0])
            if not celsius:
                t[0] = F_to_C(t[0])
            t[0] = convert_from_C(t[0], t_f[1])
            t_today_low.append(t[0])
            
            i = re.findall('<div class="icon (.*)xl"', w_now[0])
            i[0] = convert(i[0], icons_name)
            icon_today.append(i[0])


    if time_update:
        print ('\033[34m>\033[0m '+_('updated on server')+' '+time_update[0]) 
    print ('\033[34m>\033[0m '+_('weather received')+' '+time.strftime('%H:%M', time.localtime()))

    # write variables
    for i in w.keys():
        w[i] = globals()[i]
    return w
