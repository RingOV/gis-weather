#!/usr/bin/env python3

# temperature convert
def F_to_C(t_F):
    t_C = str(round((int(t_F)-32)/1.8))
    if t_C[0] not in ('+', '-', '0'):
        t_C = "+"+t_C
    return t_C

def C_to_F(t_C):
    t_F = str(round(int(t_C)*1.8+32))
    return t_F

def F_to_K(t_F):
    return str(round((int(t_F)+459.67)*5/9))

def C_to_K(t_C):
    return str(int(t_C)+273)

def add_plus(t):
    if t[0] not in ('+', '-', '0'):
        t = "+"+t
    return t

# wind convert
def ms_to_kmh(ms):
    return str(round(int(ms)*3.6))+' '+_('km/h')

def ms_to_mph(ms):
    return str(round(int(ms)*2.237))+' '+_('mph')

def ms_to_Bft(ms):
    return str(round((int(ms)/0.836)**(2/3)))+' '+_('Bft')

def convert_from_ms(ms):
    return ';'.join([ms+' '+_('m/s'), ms_to_kmh(ms), ms_to_mph(ms), ms_to_Bft(ms)])


def kmh_to_ms(kmh):
    return str(round(int(kmh)*0.278))+' '+_('m/s')

def kmh_to_mph(kmh):
    return str(round(int(kmh)*0.621))+' '+_('mph')

def kmh_to_Bft(kmh):
    return str(round((int(kmh)*0.278/0.836)**(2/3)))+' '+_('Bft')

def convert_from_kmh(kmh):
    return ';'.join([kmh_to_ms(kmh), kmh+' '+_('km/h'), kmh_to_mph(kmh), kmh_to_Bft(kmh)])