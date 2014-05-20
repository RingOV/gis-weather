#!/usr/bin/env python3

import os

user_applications_folder = os.path.join(os.path.expanduser("~"), ".local", "share", "applications")

def exists():
    return os.path.exists(os.path.join(user_applications_folder, "gis-weather.desktop"))

def main_exists():
    return os.path.exists("/usr/share/applications/gis-weather.desktop")

def remove():
    os.unlink(os.path.join(user_applications_folder, "gis-weather.desktop"))

def create(application):
    desktop_entry = "[Desktop Entry]\n"\
        "Name=Gis Weather\n"\
        "Exec=python3 \"%s\"\n"\
        "Type=Application\n"\
        "Terminal=false\n"\
        "Icon=%s\n"\
        "Comment=%s" % (application, os.path.join(os.path.dirname(application),'icon.png'), _("Weather widget"))
    with open(os.path.join(user_applications_folder, "gis-weather.desktop"), "w") as f:
        f.write(desktop_entry)