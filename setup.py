import sys
if sys.platform != "win32":
    exit()

# v = '0.6.4'
f = open('gis-weather.py', 'r')
count = 1
for line in f:
    if count == 4:
        break
    count=count+1
v = line.split("'")[1]

import site, os
from cx_Freeze import setup, Executable

siteDir = site.getsitepackages()[1]
includeDllPath = os.path.join(siteDir, 'gnome')

missingDll = ['libatk-1.0-0.dll',
    'libcairo-gobject-2.dll',
    'libffi-6.dll',
    'libfontconfig-1.dll',
    'libfreetype-6.dll',
    'libgailutil-3-0.dll',
    'libgdk_pixbuf-2.0-0.dll',
    'libgdk-3-0.dll',
    'libgio-2.0-0.dll',
    'libgirepository-1.0-1.dll',
    'libglib-2.0-0.dll',
    'libgmodule-2.0-0.dll',
    'libgobject-2.0-0.dll',
    'libgthread-2.0-0.dll',
    'libgtk-3-0.dll',
    'libharfbuzz-gobject-0.dll',
    'libintl-8.dll',
    'libjpeg-8.dll',
    'libpango-1.0-0.dll',
    'libpangocairo-1.0-0.dll',
    'libpangoft2-1.0-0.dll',
    'libpangowin32-1.0-0.dll',
    'libpng16-16.dll',
    'libpyglib-gi-2.0-python34-0.dll',
    'librsvg-2-2.dll',
    'libwebp-4.dll',
    'libwinpthread-1.dll',
    'libxml2-2.dll',
    'libzzz.dll']

includeFiles = []
for dll in missingDll:
    includeFiles.append((os.path.join(includeDllPath, dll), dll))

gtkLibs = ['lib\\gdk-pixbuf-2.0',
    'lib\\girepository-1.0',
    'share\\glib-2.0',
    'lib\\gtk-3.0']


for lib in gtkLibs:
    includeFiles.append((os.path.join(includeDllPath, lib), lib))

addFiles = ['utils',
    'services',
    'dialogs',
    'themes',
    'i18n',
    'po',
    'icon.png',
    'icon.ico']


for files in addFiles:
    includeFiles.append((files, files))

buildOptions = dict(
    compressed = False,
    includes = ["gi"],
    excludes = ['wx', 'pydoc_data', 'curses', 'pygtkcompat','utils', 'dialogs', 'services'],
    packages = ["gi"],
    include_files = includeFiles)

base = "Win32GUI"

setup(name = "Gis Weather",
    version = v,
    description = "Weather widget",
    options = {"build_exe": buildOptions},
    executables = [Executable("gis-weather.py", base=base, icon="icon.ico")])