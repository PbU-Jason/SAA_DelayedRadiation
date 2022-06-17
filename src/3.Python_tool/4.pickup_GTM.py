#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 18:58:55 2022

@author: jasonpbu
"""

### used package ###

import pickle
import numpy as np 
import matplotlib.pyplot as plt
import re

### load output file ###

mission = 'GTM'
Area = 100
directory_1 = '../'+mission+'/4.python/'
filename = 'GTM_SAA_5700s_smaller50_oneMudule.pickle'

with open(directory_1+filename, 'rb') as f:
    data = pickle.load(f)
    
ExcitedTime = data['ExcitedTime']
IdealDecayTime = data['IdealDecayTime']
RealDecayTime_IA = data['RealDecayTime_IA']
RealDecayTime_IAandHTsim = data['RealDecayTime_IAandHTsim']
EventList = data['EventList']

ExcitedTime_sorted = [E for I, E in sorted(zip(IdealDecayTime, ExcitedTime))]
IdealDecayTime_sorted = [I for I, E in sorted(zip(IdealDecayTime, ExcitedTime))]

### rule out should but no decay event !!! (Tl188[0.000]) ###

for i in range(len(IdealDecayTime_sorted)-len(RealDecayTime_IA)):
    for j in range(len(IdealDecayTime_sorted)):
        if abs(RealDecayTime_IA[j] - IdealDecayTime_sorted[j]) >= 1e-5:
            print('weird index: ', j)
            print('weird ExcitedTime: ', ExcitedTime_sorted[j])
            print('weird IdealDecayTime: ', IdealDecayTime_sorted[j])
            del ExcitedTime_sorted[j]
            del IdealDecayTime_sorted[j]
            break      

### pickup decay produced in 1000s but occur after 1000s ###

wanted_RealDecayTime_IA = []
for i in range(len(ExcitedTime_sorted)):
    if ExcitedTime_sorted[i] <= 1000 and RealDecayTime_IA[i] > 1000:
        wanted_RealDecayTime_IA.append(RealDecayTime_IA[i])
        
wanted_RealDecayTime_IAandHTsim = []
wanted_EventList = []
for i in range(len(RealDecayTime_IAandHTsim)):
    if RealDecayTime_IAandHTsim[i] > 1000:
        for j in range(len(wanted_RealDecayTime_IA)):
            if RealDecayTime_IAandHTsim[i] == wanted_RealDecayTime_IA[j]:
                wanted_RealDecayTime_IAandHTsim.append(RealDecayTime_IAandHTsim[i])
                wanted_EventList.append(EventList[i])
                del wanted_RealDecayTime_IA[0:j+1] # delete 0~j 
                break   
            
### plot time curve ###

time_bin = 50
bins = np.linspace(1000, 5700, int(((5700-1000)/time_bin) + 1))
(counts_bin, bins) = np.histogram(wanted_RealDecayTime_IAandHTsim, bins) 

plt.figure(dpi=500)
plt.scatter(bins[:-1], counts_bin, s=2, label = "outside SAA", color = "blue")

SAA_x = np.array([0, 1000])
SAA_y_down = np.array([0, 0])
SAA_y_up = np.array([np.ceil(max(counts_bin)/10)*10, np.ceil(max(counts_bin)/10)*10])
plt.fill_between(SAA_x, SAA_y_down, SAA_y_up, label = "inside SAA", color='C1', alpha=0.3)

plt.title('SAA Delay Radiaiton')

plt.xlim([0, 5700])
plt.xticks([0, 1000, 2000, 3000, 4000, 5000, 5700])
plt.xlabel(r'Time [$s$] (bin = '+str(time_bin)+'s)')

plt.ylim([0, np.ceil(max(counts_bin)/10)*10])
plt.ylabel(r'Event Rate [$\# / bin$]')

plt.grid()
plt.legend(loc = 'upper right', fontsize = 10)
plt.show()

### sum energy of each hit into event ###

energy_event_list = []

for event in wanted_EventList:
    
    energy_event = 0
    for hit in event:
        energy_event += float(hit[0][4])
        
    energy_event_list.append(energy_event)

bins = np.logspace(1, 9, 100) # keV unit form 10keV~1GeV separated to 10000 bins
(counts_bin, bins) = np.histogram(energy_event_list, bins) # allocate energy into bins

flux_bin = []
for i in range(0,len(counts_bin),1):
    flux_bin.append((counts_bin[i]*1000*time_bin)/(Area*float(4700)*(bins[i+1]-bins[i]))) #!!! (# in OneBin) to (#/(MeV*cm^2*s))
bins_MeV = bins/1000 # keV to MeV

### plot depsition energy ###

# SAA deleay decay
plt.figure(dpi=500)
plt.scatter(bins_MeV[:-1], flux_bin, s=2,
            label = "SAA delay radiation", color = 'darkgreen')

# bkg components

directory_2 = '../'+mission+'/3.megalib/output/'

file_list = ['ActivationStep1_AlbedoElectrons.inc1.id1.sim',
             'ActivationStep1_AlbedoNeutrons.inc1.id1.sim',
             'ActivationStep1_AlbedoPhotons.inc1.id1.sim',
             'ActivationStep1_AlbedoPositrons.inc1.id1.sim',
             'ActivationStep1_AlbedoProton.inc1.id1.sim',
             'ActivationStep1_AnnihilationLine.inc1.id1.sim',
             'ActivationStep1_CosmicAlphas.inc1.id1.sim',
             'ActivationStep1_CosmicElectrons.inc1.id1.sim',
             'ActivationStep1_CosmicPhotons.inc1.id1.sim',
             'ActivationStep1_CosmicPositrons.inc1.id1.sim',
             'ActivationStep1_CosmicProtons.inc1.id1.sim']

label_list = ['Albedo Electrons',
              'Albedo Neutrons',
              'Albedo Photons',
              'Albedo Positrons',
              'Albedo Proton',
              'AnnihilationLine',
              'Cosmic Alphas',
              'Cosmic Electrons',
              'Cosmic Photons',
              'Cosmic Positrons',
              'Cosmic Protons']

color_list = ['yellow',
              'gold',
              'orange',
              'lightcoral',
              'red',
              'black',
              'lightskyblue',
              'deepskyblue',
              'dodgerblue',
              'royalblue',
              'blue'] # 'darkgreen'

### find SE, HTsim, EN & TE ###

pattern_SE = re.compile(r"SE")
pattern_HTsim = re.compile(r"""
    HTsim\s(\d+);              # label
    \s*(-?\d+\.\d+);           # x
    \s*(-?\d+\.\d+);           # y
    \s*(-?\d+\.\d+);           # z
    \s*(-?\d+\.\d+);           # energy
    \s*(\d\.\d{5}e[+-]\d{2});  # time
    """, re.VERBOSE)
pattern_EN = re.compile(r"EN")
pattern_TE = re.compile(r"TE (\d+\.*\d*)")

for file_index in range(len(file_list)):
    
    ### read file ###
    
    file = open(directory_2+file_list[file_index], 'r')
    line = file.readline()
    
    event_list_temp = []
    event_list = []
    
    totalT = 0
    ACS_hit = 0
    onlyACSevent = 0
    
    while line:
        
        ### fist SE & onlyACSevent do nothing, the others store HTsims to one event ###
        
        if_SE = re.match(pattern_SE, line)
        if if_SE and len(event_list_temp) != 0:
            event_list.append(event_list_temp)
            event_list_temp = []
        
        ### HTsim infomations ###
        
        line_list = re.findall(pattern_HTsim, line)
        if len(line_list) != 0: # skip empty results
            
            if int(line_list[0][0]) == 4: # GAGG HTsim
                event_list_temp.append(line_list)
        
        ### final EN stores HTsims to one event ###
        
        if_EN = re.match(pattern_EN, line)
        if if_EN:
            event_list.append(event_list_temp)
            event_list_temp = []
        
        TE = re.findall(pattern_TE, line)
        if len(TE) != 0: # skip empty results
            totalT = TE[0]
            
        line = file.readline()
        
    file.close()
    
    ### count rate ###
    
    print(file_list[file_index])
    print('event number: ', len(event_list))
    print('total time: ', float(totalT))
    print('count rate: ', len(event_list)/float(totalT))
    
    ### sum energy of each hit into event ###
    
    energy_event_list = []
    
    for event in event_list:
        
        energy_event = 0
        for hit in event:
            energy_event += float(hit[0][4])
            
        energy_event_list.append(energy_event)
    
    bins = np.logspace(1, 9, 500) # keV unit form 10keV~1GeV separated to 10000 bins
    (counts_bin, bins) = np.histogram(energy_event_list, bins) # allocate energy into bins
    
    flux_bin = []
    for i in range(0,len(counts_bin),1):
        flux_bin.append((counts_bin[i]*1000)/(Area*float(totalT)*(bins[i+1]-bins[i]))) #!!! (# in OneBin) to (#/(MeV*cm^2*s))
    bins_MeV = bins/1000 # keV to MeV
    
    ### plot ###
    
    plt.scatter(bins_MeV[:-1], flux_bin, s=2,
                label = label_list[file_index], color = color_list[file_index])

plt.title('Deposition Energy Spectrum')

plt.xlim([1e-2, 1e+3])
plt.xscale('log')
plt.xlabel(r'Energy [$MeV$]')

plt.ylim([1e-6, 1e3])
plt.yscale('log')
plt.yticks(np.logspace(-6, 3, 10))
plt.ylabel(r'Flux [$\# / (cm^2 \cdot s \cdot MeV)$]')

plt.grid()
plt.legend(loc = 'upper right', fontsize = 8, ncol=2)
plt.show()
