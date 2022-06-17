#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 13:36:01 2022

@author: jasonpbu
"""

### used package ###

import re
import pickle

### find SE, TI, CC, IA DECA, HTsim & TE ###

pattern_SE = re.compile(r"SE")
pattern_TI = re.compile(r"TI (\d+\.*\d*)")
# pattern_CC_isotope = re.compile(r"CC Future decay: ([a-zA-Z]+)([0-9]+)")
pattern_CC_time = re.compile(r"t=(\d+\.*\d*) sec")
pattern_IA_DECA = re.compile(r"""
                             IA\s\DECA\s\s(\d+);      # current label
                             \s(\d+);                 # source label
                             """, re.VERBOSE)
pattern_HTsim = re.compile(r"""
                           HTsim\s(\d+);              # label
                           \s*(-?\d+\.\d+);           # x
                           \s*(-?\d+\.\d+);           # y
                           \s*(-?\d+\.\d+);           # z
                           \s*(-?\d+\.\d+);           # energy
                           \s*(\d\.\d{5}e[+-]\d{2});  # time
                           """, re.VERBOSE)
pattern_TE = re.compile(r"TE (\d+\.*\d*)")

### read input file ###

filename = 'GTM_SAA_5700s_smaller50_oneMudule'

file = open('./ActivationStep1_Buildup_SAA_5700s_smaller50_KeepIA_oneMudule.inc1.id1.sim', 'r')
line = file.readline()

Time_temp = 0
# Isotope_temp = 0
StableTime_temp = []

ExcitedTime_list = []
# Isotope_list = []
# StableTime_list = []

IdealDecayTime_list = []
RealDecayTime_IAandHTsim_list = []
RealDecayTime_IA_list = []

DECA_temp_list = []
# DECA_IAandHTsim_list = []
# DECA_IA_list = []

Event_temp_list = []
Event_list = []

while line:

    ### TI infomations ###

    Time_temp_list = re.findall(pattern_TI, line)
    if len(Time_temp_list) != 0: # skip empty results
        Time_temp = Time_temp_list[0]

    ### CC infomations ###

    # Isotope_temp_list = re.findall(pattern_CC_isotope, line)
    # print(Isotope_temp_list)
    # if len(Isotope_temp_list) != 0: # skip empty results
    #     Isotope_temp = Isotope_temp_list[0]

    StableTime_temp_list = re.findall(pattern_CC_time, line)
    if len(StableTime_temp_list) != 0: # skip empty results
        StableTime_temp.append(StableTime_temp_list[0]) # list here!!!

    ### IA infomations ###

    IA_DECA_temp_list = re.findall(pattern_IA_DECA, line)
    if len(IA_DECA_temp_list) != 0: # skip empty results
        if int(IA_DECA_temp_list[0][1]) == 1: # decay event
            DECA_temp_list.append(IA_DECA_temp_list)

    ### HTsim infomations ###

    HTsim_temp_list = re.findall(pattern_HTsim, line)
    if len(HTsim_temp_list) != 0: # skip empty results
        if int(HTsim_temp_list[0][0]) == 4: # GAGG HTsim
            Event_temp_list.append(HTsim_temp_list)

    ### No match then do nothing, ortherwise store info. for one event ###

    if_SE = re.match(pattern_SE, line)

    if if_SE and len(StableTime_temp) != 0:
        for i in StableTime_temp:
            IdealDecayTime = float(Time_temp) + float(i)
            if IdealDecayTime <= 5700: # save all first
                ExcitedTime_list.append(float(Time_temp))
                # Isotope_list.append(Isotope_temp)
                # StableTime_list.append(StableTime_temp)
                IdealDecayTime_list.append(IdealDecayTime)

    if if_SE and len(DECA_temp_list) != 0:
        RealDecayTime_IA_list.append(float(Time_temp))
        # DECA_IA_list.append(DECA_temp_list)
        if len(Event_temp_list) != 0:
            RealDecayTime_IAandHTsim_list.append(float(Time_temp))
            # DECA_IAandHTsim_list.append(DECA_temp_list)
            Event_list.append(Event_temp_list)

    if if_SE: # clear above work logical label
        StableTime_temp = []
        DECA_temp_list = []
        Event_temp_list = []

    ### final time ###

    TotalTime_temp = re.findall(pattern_TE, line)
    if len(TotalTime_temp) != 0: # skip empty results
        TotalTime = float(TotalTime_temp[0])

    line = file.readline()

file.close()

# IdealDecayTime_list = sorted(IdealDecayTime_list) # sort ideal decay time

### save output file ###

my_dict = {
    'ExcitedTime': ExcitedTime_list,
    'IdealDecayTime': IdealDecayTime_list,
    'RealDecayTime_IA': RealDecayTime_IA_list,
    'RealDecayTime_IAandHTsim': RealDecayTime_IAandHTsim_list,
    'EventList': Event_list
}

# Save
with open(filename+'.pickle', 'wb') as f:
    pickle.dump(my_dict, f)

# # Load
# with open(filename+'.pickle', 'rb') as f:
#     new_dict = pickle.load(f)
