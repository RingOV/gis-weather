#!/usr/bin/env python3

def convert(deg):
    direct = 'N'
    if deg>22.5: direct = 'NE'
    if deg>67.5: direct = 'E'
    if deg>112.5: direct = 'SE'
    if deg>157.5: direct = 'S'
    if deg>202.5: direct = 'SW'
    if deg>247.5: direct = 'W'
    if deg>292.5: direct = 'NW'
    if deg>337.5: direct = 'N'

    return direct