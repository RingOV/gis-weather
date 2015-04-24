#!/usr/bin/env python3

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