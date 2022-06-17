#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  9 04:02:01 2022

@author: jasonpbu
"""

### read and rewrite file ###

# file_in = open('../GTM/1.spenvis/spenvis_tri.txt', 'r')
# file_out = open('../GTM/1.spenvis/spenvis_tri_rescale.txt', 'w')
file_in = open('../MASS/1.spenvis/spenvis_tri.txt', 'r')
file_out = open('../MASS/1.spenvis/spenvis_tri_rescale.txt', 'w')

normal = True
process = False
# time_rescale = 5699/959
time_rescale = 5699/1080

line_in = file_in.readline()
line_out = file_in.readline()
while line_in:
    
    if normal:
        file_out.write(line_in)
        
    if line_in[0:14] == "'End of Block'" or line_in[0:13] == "'End of File'":
        normal = True
        process = False
        file_out.write(line_in)
        
    if process:
        temp_list = []
        
        for i in line_in.split():
            temp_list.append(i.split(",")[0])
            
        temp_list[1] = str("{:E}".format(float(temp_list[1]) * time_rescale))
        temp_list[2] = str("{:E}".format(float(temp_list[2]) * time_rescale))
        file_out.write("  ")
        file_out.write(temp_list[0])
        file_out.write(",")
        file_out.write("  ")
        file_out.write(temp_list[1])
        file_out.write(",")
        file_out.write("  ")
        file_out.write(temp_list[2])
        file_out.write("\n")
        
    if line_in[0:7] == "'DFlux'":
        normal = False
        process = True
         
    line_in = file_in.readline()

file_in.close()
file_out.close()
