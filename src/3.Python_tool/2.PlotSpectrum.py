#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 12 15:16:46 2022

@author: jasonpbu
"""

import numpy as np
import matplotlib.pyplot as plt

# mission = 'GTM'
mission = 'MASS'
directory = '../'+mission+'/3.megalib/spectrum/'

file_list = ['AlbedoElectronsAlcarazMizuno.spectrum.dat',
             'AlbedoNeutronsKole.spectrum.dat',
             'AlbedoPhotonsTuerlerMizunoAbdo.spectrum.dat',
             'AlbedoPositronsAlcarazMizuno.spectrum.dat',
             'AlbedoProtonMizuno.spectrum.dat',
             'CosmicAlphasSpenvis.spectrum.dat',
             'CosmicElectronsMizuno.spectrum.dat',
             'CosmicPhotonsGruber.spectrum.dat',
             'CosmicPositronsMizuno.spectrum.dat',
             'CosmicProtonsSpenvis.spectrum.dat',
             'TrappedElectronsSpenvis.spectrum.dat',
             'TrappedProtonsSpenvis.spectrum.dat']

AngleFactor_list = [3.97905,
                    3.97905,
                    3.97905,
                    3.97905,
                    3.97905,
                    8.58732,
                    8.58732,
                    8.58732,
                    8.58732,
                    8.58732,
                    12.5664,
                    12.5664]

label_list = ['Albedo Electrons',
             'Albedo Neutrons',
             'Albedo Photons',
             'Albedo Positrons',
             'Albedo Proton',
             'Cosmic Alphas',
             'Cosmic Electrons',
             'Cosmic Photons',
             'Cosmic Positrons',
             'Cosmic Protons',
             'Trapped Electrons',
             'Trapped Protons']

color_list = ['yellow',
             'gold',
             'orange',
             'lightcoral',
             'red',
             'lightskyblue',
             'deepskyblue',
             'dodgerblue',
             'royalblue',
             'blue',
             'limegreen',
             'darkgreen']

### per sr ###

plt.figure(dpi=500)

plot_pointer = 0
for filename in file_list:

    file = open(directory+filename,'r')
    line = file.readline()
    
    EnergyBins_keV = []
    Spectrum_cm_MeV = []
    
    while line:
        if line[0] == 'D' and line[1] == 'P':
            EnergyBins_keV.append(float(line.split()[1]))
            Spectrum_cm_MeV.append(1000*float(line.split()[2]))
        line = file.readline()
    file.close()
    
    plt.plot(EnergyBins_keV, Spectrum_cm_MeV,
             label = label_list[plot_pointer],
             color = color_list[plot_pointer])
    plot_pointer += 1

plt.vlines(x = 511, ymin = 1e-20, ymax = 1000*0.00527448, label = 'Annihilation Line', color = 'black')

plt.xlim([10, 1e9])
plt.xscale('log')
plt.xlabel(r'Energy [$keV$]')

plt.ylim([1e-15, 1e12])
plt.yscale('log')
plt.yticks(np.logspace(-15, 12, 28))
plt.ylabel(r'Flux [$\# / (cm^2 \cdot s \cdot MeV \cdot sr)$]')

plt.grid()
plt.legend(loc = 'upper right', fontsize = 8, ncol=2)
plt.show()

### having consider angle! ###

plt.figure(dpi=500)

plot_pointer = 0
for filename in file_list:

    file = open(directory+filename,'r')
    line = file.readline()
    
    EnergyBins_keV = []
    Spectrum_cm_MeV = []
    
    while line:
        if line[0] == 'D' and line[1] == 'P':
            EnergyBins_keV.append(float(line.split()[1]))
            Spectrum_cm_MeV.append(1000*float(line.split()[2])*AngleFactor_list[plot_pointer])
        line = file.readline()
    file.close()
    
    plt.plot(EnergyBins_keV, Spectrum_cm_MeV,
             label = label_list[plot_pointer],
             color = color_list[plot_pointer])
    plot_pointer += 1

plt.vlines(x = 511, ymin = 1e-20, ymax = 1000*0.0209874, label = 'Annihilation Line', color = 'black')

plt.xlim([10, 1e9])
plt.xscale('log')
plt.xlabel(r'Energy [$keV$]')

plt.ylim([1e-15, 1e12])
plt.yscale('log')
plt.yticks(np.logspace(-15, 12, 28))
plt.ylabel(r'Flux [$\# / (cm^2 \cdot s \cdot MeV)$]')

plt.grid()
plt.legend(loc = 'upper right', fontsize = 8, ncol=2)
plt.show()
