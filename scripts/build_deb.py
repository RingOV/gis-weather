#!/usr/bin/env python3

import os
import sys
from shutil import copy, copytree, rmtree, ignore_patterns
import changelog

PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
GW_PATH = os.path.split(PATH)[0]
DEB_PATH = GW_PATH+'/DEB'
BUILD_PATH = DEB_PATH+'/build'
print('Build to %s'%DEB_PATH)

f = open('%s/gis-weather.py'%GW_PATH, 'r')
count = 1
for line in f:
    if count == 4:
        break
    count=count+1
VERSION = line.split("'")[1]
f.close()

SIZE_DIR = None

print('VERSION =', VERSION)

def main():
    if os.path.exists(DEB_PATH):
        print('Removing ', DEB_PATH)
        try:
            rmtree(DEB_PATH)
        except:
            print("Can't remove "+DEB_PATH)

    create_path(['DEBIAN',
        'usr/bin',
        'usr/share',
        'usr/share/applications',
        'usr/share/doc/gis-weather',
        '/usr/share/pixmaps/'])

    create_desktop_file(BUILD_PATH+'/usr/share/applications/gis-weather.desktop')

    create_bin_file(BUILD_PATH+'/usr/bin/gis-weather')

    create_copyright(BUILD_PATH+'/usr/share/doc/gis-weather/copyright')

    create_changelog(BUILD_PATH+'/usr/share/doc/gis-weather/changelog')
    # Copy all
    IGNORE_PATTERNS = ('__pycache__', '*~', 'DEB', 'scripts', '.git', '.gitignore', 'setup.py', 'icon.ico', 'po')
    copytree(GW_PATH, BUILD_PATH+'/usr/share/gis-weather', ignore=ignore_patterns(*IGNORE_PATTERNS))
    copy(GW_PATH+'/icon.png', BUILD_PATH+'/usr/share/pixmaps/gis-weather.png')

    create_package_file(BUILD_PATH+'/usr/share/gis-weather/package', 'deb')
    # Calculate size
    global SIZE_DIR
    SIZE_DIR = os.popen('du -s -BK %s'%(BUILD_PATH)).readlines()
    SIZE_DIR = SIZE_DIR[0].split()[0][:-1]

    create_control(BUILD_PATH+'/DEBIAN/control')
    # Change modes
    os.popen('find '+BUILD_PATH+' -type d -exec chmod 755 {} \;')
    os.popen('find '+BUILD_PATH+' -type f -exec chmod 644 {} \;')

    os.popen('fakeroot chmod 755 '+BUILD_PATH+'/usr/bin/gis-weather')
    # os.popen('fakeroot chmod +x '+BUILD_PATH+'/usr/bin/gis-weather')
    
    #### Build DEB ####
    a = os.popen('fakeroot dpkg-deb --build %s %s'%(BUILD_PATH, DEB_PATH+'/gis-weather_'+VERSION+'_all1.deb')).readlines()
    print(a[0])

    if len(sys.argv) > 1:
        #### Build RPM ####
        create_package_file(BUILD_PATH+'/usr/share/gis-weather/package', 'rpm')
        a = os.popen('fakeroot dpkg-deb --build %s %s'%(BUILD_PATH, DEB_PATH+'/gis-weather_'+VERSION+'_all.deb')).readlines()
        print(a[0])
        a = os.popen('cd %s; fakeroot alien -r %s; cd ..'%(DEB_PATH, 'gis-weather_'+VERSION+'_all.deb')).readlines()
        print(a[0])
        os.popen('rm %s'%(DEB_PATH+'/gis-weather_'+VERSION+'_all.deb'))

    os.popen('mv %s %s'%(DEB_PATH+'/gis-weather_'+VERSION+'_all1.deb', DEB_PATH+'/gis-weather_'+VERSION+'_all.deb'))

    
def create_path(path):
    for i in path:
        if not os.path.exists(BUILD_PATH+'/'+i):
            os.makedirs(BUILD_PATH+'/'+i)
            print('Creating path ', BUILD_PATH+'/'+i)

def write_to_file(path, lines):
    f = open(path, 'w')
    for l in lines:
        f.write(l+'\n')
    f.close()

def create_desktop_file(path):
    lines = ['[Desktop Entry]',
        'Name=Gis Weather',
        'Comment=Weather widget',
        'Categories=GNOME;Utility;',
        'Exec=/usr/bin/gis-weather',
        'Icon=gis-weather',
        'Terminal=false',
        'Type=Application']
    write_to_file(path, lines)

def create_bin_file(path):
    lines = ['#!/bin/bash',
        'exec python3 /usr/share/gis-weather/gis-weather.py $*']
    write_to_file(path, lines)

def create_copyright(path):
    lines = [' ']
    write_to_file(path, lines)

def create_changelog(path):
    lines = changelog.get(GW_PATH)
    write_to_file(path, lines)
    write_to_file(DEB_PATH+'/Changelog', lines)
    os.popen('gzip -9 %s'%(path))

def create_package_file(path, text):
    lines = [text]
    write_to_file(path, lines)

def create_control(path):
    lines = ['Package: gis-weather', 
        'Version: %s'%VERSION,
        'Priority: optional',
        'Architecture: all',
        'Depends: python3-gi, python3-gi-cairo, gir1.2-gtk-3.0',
        'Recommends: gir1.2-rsvg-2.0',
        'Maintainer: Alexander Koltsov <ringov@mail.ru>',
        'Section: utils',
        'Installed-Size: %s'%SIZE_DIR,
        'Description: Customizable weather widget',
        ' Features:',
        ' - View weather for several days;',
        ' - Detailed weather forecast for today and tomorrow;',
        ' - Fast switching between cities;',
        ' - Select the background and theme weather icons;',
        ' - "Compass" with the wind direction, with adjustable angle of rotation;',
        ' - Highlighting the high wind;',
        ' - Supported weather services:',
        ' - > Gismeteo.com',
        ' - > AccuWeather.com',
        ' - > OpenWeatherMap.org',
        ' - > Yr.no',
        ' - Support SVG, SVGZ and widget scale',
        ' - Indicator to panel',
        ' - Presets']
    write_to_file(path, lines)


if __name__ == '__main__':
    main()
