#!/usr/bin/python3

import subprocess
import os
import sys

PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
GW_PATH = os.path.split(PATH)[0]

f = open('%s/gis-weather.py'%GW_PATH, 'r')
count = 1
for line in f:
    if count == 4:
        break
    count=count+1
VERSION = line.split("'")[1]

# VERSION = []
# VERSION.extend(OLD_VERSION)

# if len(VERSION)<4:
#     VERSION.append('1')
# else:
#     VERSION[-1] = str(int(VERSION[-1])+1)

# OLD_VERSION = '.'.join(OLD_VERSION)
# VERSION = '.'.join(VERSION)

# subprocess.Popen(['%s/write_version_changes.sh'%PATH, OLD_VERSION, VERSION, '%s/gis-weather.py'%GW_PATH], stdout=subprocess.PIPE)


subprocess.Popen(['%s/git_tag.sh'%PATH, VERSION], stdout=subprocess.PIPE)