#!/usr/bin/env python3

import shlex
import subprocess
import re

import sys
if sys.platform.startswith("win"):
    WIN = True
else:
    WIN = False

def count():
    if WIN:
        return 0
    try:
        cmd_line = 'ps -C gis-weather'
        args = shlex.split(cmd_line)
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        out, err = p.communicate()
        instances = re.findall('gis-weather', out.decode(encoding='UTF-8'))
        return len(instances)
    except:
        return 0

def set_procname(newname):
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(newname)+1)
    buff.value = newname
    libc.prctl(15, byref(buff), 0, 0, 0)

def get_config_file():
    if WIN:
        return 'gw_config.json'
    INSTANCE_NO = count()
    if INSTANCE_NO == 0:
        return 'gw_config.json'
    else:
        return 'gw_config%s.json'%str(INSTANCE_NO)