#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gtk
import os

def create(v, APP_PATH, license):
    about = gtk.AboutDialog()
    about.set_icon_from_file(os.path.join(APP_PATH, "icon.png"))
    about.set_program_name("Gis Weather")
    about.set_version(v)
    about.set_copyright("(С) 2013 - 2014 Alexander Koltsov")
    about.set_comments("Погодный виджет")
    about.set_website("http://sourceforge.net/projects/gis-weather/")
    about.set_logo(gtk.gdk.pixbuf_new_from_file_at_size(os.path.join(APP_PATH, "icon.png"), 128, 128))
    about.set_license(license)
    about.set_wrap_license(False)
    about.set_authors(["Alexander Koltsov <ringov@mail.ru>\n",
        "Помощь и идеи:\n    Karbunkul\n    Haron Prime\n    Yuriy_Y\n",
        "draw_scaled_image, draw_text_Whise\nby Helder Fraga aka Whise <helder.fraga@hotmail.com>\n",
        "autostart helper\nby Jonas Wagner\n",
        "Sloth 0.2\nby Mikhail Valkov"])
    about.set_artists(["backgrounds:",
        "LightEasyShadow, LightWhiteShadow, DarkEasyShadow, DarkWithFlare",
        "by wfedin",
        "-------------------------------\n"
        "icons:",
        "colorful, flat_colorful, light, flat_white, dark, flat_black",
        "by ~MerlinTheRed",
        "http://merlinthered.deviantart.com/art/plain-weather-icons-157162192\n",
        "tick by xiao4",
        "http://www.deviantart.com/art/tick-weather-icons-96294478\n",
        "weezle by d3stroy",
        "http://www.deviantart.com/art/Weezle-Weather-Icons-187306753\n"])
    #about.set_translator_credits("")
    #about.set_documenters("")
    return about