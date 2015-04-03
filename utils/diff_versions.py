#!/usr/bin/env python3

def diff(cur_ver, new_ver):
    cur_ver = fix_length(cur_ver)
    cur_ver = fix_digits(cur_ver)
    new_ver = fix_length(new_ver)
    new_ver = fix_digits(new_ver)
    if int(''.join(new_ver)) > int(''.join(cur_ver)):
        return True
    else:
        return False

def fix_length(ver):
    while len(ver)<4:
        ver.append('0')
    return ver

def fix_digits(ver):
    fixed_ver = []
    for i in ver:
        if len(i) < 2:
            fixed_ver.append('0'+i)
        else:
            fixed_ver.append(i)
    return fixed_ver