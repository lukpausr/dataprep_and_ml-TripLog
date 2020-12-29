from gpx_csv_converter import Converter
import calculate
import pandas as pd
import os
import gpxpy
import numpy as np

path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/Messfahrt2.gpx"

gpx_file = open(path, 'r')
gpx = gpxpy.parse(gpx_file)
i = 1
lats = []
lons = []
times = []
elev = []
track = gpx.tracks[0]
for segment in track.segments:
    for point in segment.points:
        if True: #i % 2 == 1:
            lats.append(point.latitude)
            lons.append(point.longitude)
            times.append(point.time)
            elev.append(point.elevation)
        i = i+1

print(len(lats))

#Distanzen in Listen speichern
distances_total = [0]
distances_diff = [0]

total = 0
for i in range(1, len(lats)):
    dist = calculate.calc_distance(lats[i], lons[i], lats[i-1], lons[i-1])
    total = total + dist
    distances_total.append(total)
    distances_diff.append(dist)


#Startzeitpunkt ermitteln
begin = (times[0].second + times[0].minute * 60 + times[0].hour * 3600)

#Zeitpunkte in Listen speichern
times_total = [0]
times_diff = [0]        
       
for i in range(1,len(times)):
    times_total.append((times[i].second + times[i].minute * 60 + times[i].hour * 3600) - begin)
    times_diff.append((times[i].second + times[i].minute * 60 + times[i].hour * 3600)-(times[i-1].second + times[i-1].minute * 60 + times[i-1].hour * 3600))


#Steigungen berechnen
slopes = [0]
for i in range(1, len(distances_diff)-1):
    m = (elev[i] - elev[i-1]) / (distances_diff[i])
    slopes.append(np.arctan(m)*100)
slopes.append(0)


#Berechnen der Geschwindigkeiten
velocities = [0]
#in km/h
for i in range(1, len(distances_diff)):
    velocities.append(distances_diff[i]*3.6/(times_diff[i]))

#Berechnen der Beschleunigungen
accelerations = [0]
#in m/s^2
for i in range(1, len(velocities)):
    accelerations.append((velocities[i] - velocities[i-1]) / (3.6*(times_diff[i])))


import matplotlib.pyplot as plt # v 3.0.3
# #v_s
# plt.figure(figsize=(15, 6), dpi=80)
# plt.subplot(111)
# plt.plot(distances_total, velocities)
# plt.xlabel("Strecke [m]", fontsize =14, fontweight = "bold")
# plt.ylabel("Geschwindigkeit [m/s]", fontsize =14, fontweight = "bold")
# plt.savefig("Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/GPS/fünftel/v_s.png")

# #v_t
# plt.figure(figsize=(15, 6), dpi=80)
# plt.subplot(111)
# plt.plot(times_total, velocities) 
# plt.xlabel("Zeit [s]", fontsize =14, fontweight = "bold")
# plt.ylabel("Geschwindigkeit [m/s]", fontsize =14, fontweight = "bold")
# plt.savefig("Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/GPS/fünftel/v_t.png")

# #a_s
# plt.figure(figsize=(15, 6), dpi=80)
# plt.subplot(111)
# plt.plot(distances_total, accelerations) 
# plt.xlabel("Strecke [m]", fontsize =14, fontweight = "bold")
# plt.ylabel("Beschleunigung [m/s^2]", fontsize =14, fontweight = "bold")
# plt.savefig("Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/GPS/fünftel/a_s.png")

# #a_t
# plt.figure(figsize=(15, 6), dpi=80)
# plt.subplot(111)
# plt.plot(times_total, accelerations) 
# plt.xlabel("Zeit [s]", fontsize =14, fontweight = "bold")
# plt.ylabel("Beschleunigung [m/s^2]", fontsize =14, fontweight = "bold")
# plt.savefig("Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/GPS/fünftel/a_t.png")

# #h_s
# plt.figure(figsize=(15, 6), dpi=80)
# plt.subplot(111)
# plt.plot(distances_total, elev) 
# plt.xlabel("Strecke [m]", fontsize =14, fontweight = "bold")
# plt.ylabel("Höhe [m]", fontsize =14, fontweight = "bold")
# plt.savefig("Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/GPS/fünftel/h_s.png")

# #h_t
# plt.figure(figsize=(15, 6), dpi=80)
# plt.subplot(111)
# plt.plot(times_total, elev) 
# plt.xlabel("Zeit [s]", fontsize =14, fontweight = "bold")
# plt.ylabel("Höhe [m]", fontsize =14, fontweight = "bold")
# plt.savefig("Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/GPS/fünftel/h_t.png")

# #e_s
# plt.figure(figsize=(15, 6), dpi=80)
# plt.subplot(111)
# plt.plot(distances_total, slopes) 
# plt.xlabel("Strecke [m]", fontsize =14, fontweight = "bold")
# plt.ylabel("Steigung [%]", fontsize =14, fontweight = "bold")
# plt.savefig("Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/GPS/fünftel/e_s.png")

# #e_t
# plt.figure(figsize=(15, 6), dpi=80)
# plt.subplot(111)
# plt.plot(times_total, slopes)
# plt.xlabel("Zeit [s]", fontsize =14, fontweight = "bold") 
# plt.ylabel("Steigung [%]", fontsize =14, fontweight = "bold")
# plt.savefig("Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/GPS/fünftel/e_t.png")

# #s_t
# plt.figure(figsize=(15, 6), dpi=80)
# plt.subplot(111)
# plt.plot(times_total, distances_total)
# plt.xlabel("Zeit [s]", fontsize =14, fontweight = "bold") 
# plt.ylabel("Strecke [m]", fontsize =14, fontweight = "bold")
# plt.savefig("Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/99-Ausarbeitung/Grafiken/GPS/fünftel/m_s.png")