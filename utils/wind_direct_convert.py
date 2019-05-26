#!/usr/bin/env python3

def convert(deg):
    direct = 'N'
    if deg>22.5: direct = _('N')+_('E')
    if deg>67.5: direct = _('E')
    if deg>112.5: direct = _('S')+_('E')
    if deg>157.5: direct = _('S')
    if deg>202.5: direct = _('S')+_('W')
    if deg>247.5: direct = _('W')
    if deg>292.5: direct = _('N')+_('W')
    if deg>337.5: direct = _('N')
    return direct

def convert2(d):
    direct = ''
    if d == '1': direct = _('N')
    if d == '2': direct = _('N')+_('E')
    if d == '3': direct = _('E')
    if d == '4': direct = _('S')+_('E')
    if d == '5': direct = _('S')
    if d == '6': direct = _('S')+_('W')
    if d == '7': direct = _('W')
    if d == '8': direct = _('N')+_('W')
    return direct
    