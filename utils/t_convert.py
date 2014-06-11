#!/usr/bin/env python3

def F_to_C(t_F):
    t_C = str(round((int(t_F)-32)/1.8))
    if t_C[0] not in ('+', '-', '0'):
        t_C = "+"+t_C
    return t_C

def C_to_F(t_C):
    t_F = str(round(int(t_C)*1.8+32))
    if t_F[0] not in ('+', '-', '0'):
        t_F = "+"+t_F
    return t_F