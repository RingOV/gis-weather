#!/usr/bin/env python3

import re

def find_separator(date):
    separator = re.findall('\d+(.)\d+', date)
    if separator:
        return separator[0]
    else:
        return False

def fix_digits(date):
    if len(date) == 1:
        return '0'+date
    else:
        return date

def main(date, date_separator, swap_d_and_m):
    if date_separator == 'Default' and swap_d_and_m == False:
        return date

    old_separator = find_separator(date[0])
    if not old_separator:
        print('Can\'t found old date separator')
        return date

    if swap_d_and_m:
        for i in range(len(date)):
            date[i] = fix_digits(date[i].split(old_separator)[-1])+old_separator+fix_digits(date[i].split(old_separator)[0])

    if date_separator != 'Default':
        for i in range(len(date)):
            date[i] = fix_digits(date[i].split(old_separator)[0])+date_separator+fix_digits(date[i].split(old_separator)[-1])
    
    return date