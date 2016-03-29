#!/usr/bin/env python3

from gi.repository import Gtk, GdkPixbuf
import os
import re

def create(v, APP_PATH):
    license = _('''This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You can find the full text of the license under
http://www.gnu.org/licenses/gpl.txt''')
    about = Gtk.AboutDialog()
    about.set_icon_from_file(os.path.join(APP_PATH, "icon.png"))
    about.set_program_name("Gis Weather")
    about.set_version(v)
    about.set_copyright("Copyright © 2013 - 2016 Alexander Koltsov")
    about.set_comments(_('Weather widget'))
    about.set_website("http://sourceforge.net/projects/gis-weather/")
    about.set_logo(GdkPixbuf.Pixbuf.new_from_file_at_size(os.path.join(APP_PATH, "icon.png"), 128, 128))
    about.set_license(license)
    about.set_wrap_license(False)
    about.set_authors(["Alexander Koltsov <ringov@mail.ru>",
        "    "+_('Help and Ideas')+":",
        "Karbunkul",
        "Haron Prime",
        "Yuriy_Y",
        "Alain-Olivier Breysse\n",
        "    autostart helper",
        "by Jonas Wagner\n"])
    about.set_artists(["    "+_('Backgrounds')+":",
        "LightEasyShadow, LightWhiteShadow, DarkEasyShadow, DarkWithFlare",
        "by wfedin\n",
        "Grey",
        "by DeadMetaler\n",
        "    "+_('Icons')+":",
        "colorful, flat_colorful, light, flat_white, dark, flat_black",
        "by ~MerlinTheRed",
        "http://merlinthered.deviantart.com/art/plain-weather-icons-157162192\n",
        "Sticker",
        "by KorToIk",
        "http://kortoik.deviantart.com/art/Sticker-Weather-Icons-78827487\n",
        "Simple",
        "by LavAna",
        "http://lavana.deviantart.com/art/Simple-Weather-Icons-23626765\n",
        "Sketchy",
        "by AzureSol",
        "http://azuresol.deviantart.com/art/Sketchy-Weather-Icons-135079063\n"
        ])
    about.set_translator_credits(_("translator-credits"))
    #about.set_documenters("")
    return about