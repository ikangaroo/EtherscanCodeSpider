#!/bin/python3
import re


def Date2path(dt):
    dts = dt.split('/')
    return dts[2]+'_'+dts[0]+'_'+dts[1]


def Code_rm_black(code):
    return re.sub('\\r\\n\s{0,}(\\r\\n){1,}', '\r\n', code)
