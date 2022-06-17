#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 04:02:01 2022

@author: jasonpbu
"""

from datetime import datetime, timedelta

def mdj2StrTime(mdj):
    t0 = datetime(1950, 1, 1, 0, 0, 0, 0) # %Y, %m, %d, %H, %M, %S
    time = t0 + timedelta(days = mdj)
    return time.strftime("%Y/%m/%d,%H:%M:%S:%f")

print(mdj2StrTime(25567.04306))
