#!/usr/bin/env python3


# temperature convert
def F_to_C(F):
    C = str(round((float(F)-32)/1.8))
    if C[0] not in ('+', '-', '0'):
        C = "+"+C
    return C


def C_to_F(C):
    F = str(round(float(C)*1.8+32))
    return F


def F_to_K(F):
    return str(round((float(F)+459.67)*5/9))


def C_to_K(C):
    return str(round(float(C)+273))


def add_plus(t):
    if t[0] not in ('+', '-', '0'):
        t = "+"+t
    return t


def convert_from_C(C, C_feel=None):
    if not C_feel:
        C_feel = C
    return add_plus(C)+'°;'+add_plus(C_feel)+'°;'+C_to_F(C)+'°;'+C_to_F(C_feel)+'°;'+C_to_K(C)+';'+C_to_K(C_feel)


def convert_from_F(F, F_feel=None):
    if not F_feel:
        F_feel = F
    return add_plus(F_to_C(F))+'°;'+add_plus(F_to_C(F_feel))+'°;'+F_C+'°;'+F_C_feel+'°;'+F_to_K(F)+';'+F_to_K(F_feel)


# wind convert
def ms_to_kmh(ms):
    return str(round(float(ms)*3.6))+' '+_('km/h')


def ms_to_mph(ms):
    return str(round(float(ms)*2.237))+' '+_('mph')


def ms_to_Bft(ms):
    return str(round((float(ms)/0.836)**(2/3)))+' '+_('bft')


def ms_to_kts(ms):
    return str(round(float(ms)*1.944))+' '+_('kts')


def convert_from_ms(ms):
    return ';'.join([str(round(float(ms)))+' '+_('m/s'), ms_to_kmh(ms), ms_to_mph(ms), ms_to_Bft(ms), ms_to_kts(ms)])


def kmh_to_ms(kmh):
    return str(round(float(kmh)*0.278))+' '+_('m/s')


def kmh_to_mph(kmh):
    return str(round(float(kmh)*0.621))+' '+_('mph')


def kmh_to_Bft(kmh):
    return str(round((float(kmh)*0.278/0.836)**(2/3)))+' '+_('bft')


def kmh_to_kts(kmh):
    return str(round(float(kmh)*0.54))+' '+_('kts')


def convert_from_kmh(kmh):
    return ';'.join([kmh_to_ms(kmh), str(round(float(kmh)))+' '+_('km/h'), kmh_to_mph(kmh), kmh_to_Bft(kmh), kmh_to_kts(kmh)])


# pressure convert
def convert_from_mmHg(mmHg):
    return mmHg+' mmHg;'+str(round(float(mmHg)/25.4))+' inHg;'+str(round(float(mmHg)*1.333))+' hPa'


def convert_from_hPa(hPa):
    return str(round(float(hPa)*0.75))+' mmHg;'+str(round(float(hPa)*0.0295))+' inHg;'+str(round(float(hPa)))+' hPa'