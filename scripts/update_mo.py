#!/usr/bin/env python3

import os
import sys

PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
GW_PATH = os.path.split(PATH)[0]

out = os.popen('pocount --short %s/po/*.po'%GW_PATH).readlines()
for line in out:
    if line.split()[0][-5:-3] != 'en':
        infile = line.split()[0]
        outfile = line.split()[0][:-2]+'mo'
        o = os.popen('msgfmt %s -o %s'%(infile, outfile)).readlines()

out = os.popen('pocount --short %s/po/*.mo'%GW_PATH).readlines()
count = len(out)
i = 0
for line in out:
    lang = line.split()[0].split('/')[-1][:-3]
    if lang != 'en':
        i += 1
        print(str(i)+'/'+str(count), lang)
        o = os.popen('mkdir -p %s/i18n/%s/LC_MESSAGES/'%(GW_PATH, lang)).readlines()
        o = os.popen('mv %s %s/i18n/%s/LC_MESSAGES/gis-weather.mo'%(line.split()[0], GW_PATH, lang)).readlines()