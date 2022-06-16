#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 01:09:33 2022

@author: jasonpbu
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

def rk4(n, derive, y, t, dt):

    dt2   = 0.5*dt
    y2    = y + dt2 * derive(n, y, t)
    y3    = y + dt2 * derive(n, y2, t+dt2)
    y4    = y + dt  * derive(n, y3, t+dt2)
    ynext = y + dt  * (derive(n, y, t) + 2.0*derive(n, y2, t+dt2) + 2.0*derive(n, y3, t+dt2) + derive(n, y4, t))/6.0

    return ynext

def derive(n, y, t):

    dydt = np.zeros(n)

    dydt[0] = -Ω     # α1/dt
    dydt[1] = 0.0   # α2/dt
    dydt[2] = ω     # α3/dt

    return dydt

time      = 0.0
time_step = 10
end_time  = 5700.0 * 3

Altitude    = 520e3
Inclination = 30.0
Ascending   = 260.0
Perigee     = 0.0
Anomaly     = 0.0

Ω = (2*np.pi) / (23*60*60 + 56*60 + 4.1) * (180/np.pi)
M = 5.972e24
R = 6371e3
G = 6.674e-11
ω = np.sqrt(G*M / (R+Altitude)**3) * (180/np.pi)

n               = 3
EulerAngles_rk4 = np.array([Ascending, Inclination, (Perigee+Anomaly)]) # [α1, α2, α3]

traj_rk4 = {"time": [], "longitude": [], "latitude": []}

while (time <= end_time):

    α1 = EulerAngles_rk4[0] * (np.pi/180)
    α2 = EulerAngles_rk4[1] * (np.pi/180)
    α3 = EulerAngles_rk4[2] * (np.pi/180)

    P1 = np.array([[np.cos(α1), -np.sin(α1), 0.0],
                   [np.sin(α1), np.cos(α1), 0.0],
                   [0.0, 0.0, 1.0]])
    P2 = np.array([[1.0, 0.0, 0.0],
                   [0.0, np.cos(α2), -np.sin(α2)],
                   [0.0, np.sin(α2), np.cos(α2)]])
    P3 = np.array([[np.cos(α3), -np.sin(α3), 0.0],
                   [np.sin(α3), np.cos(α3), 0.0],
                   [0.0, 0.0, 1.0]])

    V = np.dot(np.dot(P1,np.dot(P2,P3)), np.array([[R+Altitude], [0.0], [0.0]]))

    latitude  = np.arcsin(V[2][0] / (R+Altitude)) * (180/np.pi)
    longitude = np.sign(V[1][0]) * abs(np.arccos(V[0][0] / ((R+Altitude) * np.cos(latitude * (np.pi/180))))) * (180/np.pi) #+ Ascending

    # record
    traj_rk4["time"].append(time)
    traj_rk4["longitude"].append(longitude)
    traj_rk4["latitude"].append(latitude)

    # perturbation
    EulerAngles_rk4 = rk4(n, derive, EulerAngles_rk4, time, time_step)
    time += time_step

plt.figure(dpi=500)
plt.plot(traj_rk4["time"], traj_rk4["longitude"])
plt.show()

plt.figure(dpi=500)
plt.plot(traj_rk4["time"], traj_rk4["latitude"])
plt.show()

df_orbit = pd.DataFrame.from_dict(traj_rk4)

fig = go.Figure(data=go.Scattergeo(lat = df_orbit["latitude"],
                                   lon = df_orbit["longitude"],
                                   text = df_orbit["time"], 
                                   mode = 'markers',
                                   marker_color = '#d91e4d'))

fig.update_layout(title = 'World Map', title_x = 0.5)
fig.write_html('RK4_orbit.html')
