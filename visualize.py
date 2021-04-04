#from gpx_csv_converter import Converter
import calculate
#import pandas as pd
#import os
import gpxpy
import numpy as np

def readPoints(path, jumpSize = 1):
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
            if i % jumpSize == 0:
                lats.append(point.latitude)
                lons.append(point.longitude)
                times.append(point.time)
                elev.append(point.elevation)
            i = i+1
    print(len(lats))
    return lats, lons, times, elev

def calculateDistance(lats, lons):
    #Distanzen in Listen speichern
    distances_total = [0]
    distances_diff = [0]
    
    total = 0
    for i in range(1, len(lats)):
        dist = calculate.calc_distance(lats[i], lons[i], lats[i-1], lons[i-1])
        total = total + dist
        distances_total.append(total)
        distances_diff.append(dist)
        
    return distances_total, distances_diff

def calculateTime(times):
    #Startzeitpunkt ermitteln
    begin = (times[0].second + times[0].minute * 60 + times[0].hour * 3600)
    
    #Zeitpunkte in Listen speichern
    times_total = [0]
    times_diff = [0]        
           
    for i in range(1,len(times)):
        times_total.append((times[i].second + times[i].minute * 60 + times[i].hour * 3600) - begin)
        times_diff.append((times[i].second + times[i].minute * 60 + times[i].hour * 3600)-(times[i-1].second + times[i-1].minute * 60 + times[i-1].hour * 3600))
    
    return begin, times_total, times_diff

def calculateElevation(distances_diff, elev):
    #Steigungen berechnen
    slopes = [0]
    for i in range(1, len(distances_diff)-1):
        m = (elev[i] - elev[i-1]) / (distances_diff[i])
        slopes.append(np.arctan(m)*100)
    slopes.append(0)
    
    return slopes
    
def calculateVelocity(distances_diff, times_diff):
    #Berechnen der Geschwindigkeiten
    velocities = [0]
    #in km/h
    for i in range(1, len(distances_diff)):
        velocities.append(distances_diff[i]*3.6/(times_diff[i]))
        
    return velocities

def calculateAcceleration(velocities, times_diff):
    #Berechnen der Beschleunigungen
    accelerations = [0]
    #in m/s^2
    for i in range(1, len(velocities)):
        accelerations.append((velocities[i] - velocities[i-1]) / (3.6*(times_diff[i])))
        
    return accelerations

def calculateValues(path, jumpSize = 1):
    
    lats, lons, times, elev = readPoints(path, jumpSize)    
    distances_total, distances_diff = calculateDistance(lats, lons)   
    begin, times_total, times_diff = calculateTime(times)  
    slopes = calculateElevation(distances_diff, elev)  
    velocities = calculateVelocity(distances_diff, times_diff)
    accelerations = calculateAcceleration(velocities, times_diff)
    
    return Result(lats, lons, times, elev, distances_total, distances_diff, begin, times_total, times_diff, slopes, velocities, accelerations)

def printMultiplot(x_axis, y_axis, x_label, y_label, label, save_path=None):
    
    from matplotlib import pyplot as plt
    plt.rcParams["figure.figsize"] = (20,10)
    
    for i in range(len(x_axis)):
        plt.plot(x_axis[i], y_axis[i], label=label[i])
        
    plt.ylabel(y_label, fontsize =20)
    plt.xlabel(x_label, fontsize =20)
    plt.legend(loc='best')

    if save_path is None:
        plt.show()
    else:
        destination = save_path + "/" + x_label + y_label + ".pdf"
        print(destination)
        plt.savefig(destination, dpi=1200, bbox_inches='tight')
    
    plt.show()
        

class Result:    
    def __init__(self, lats, lons, times, elev, distances_total, distances_diff, begin, times_total, times_diff, slopes, velocities, accelerations):
        self.lats = lats
        self.lons = lons
        self.times = times
        self.elev = elev
        self.distances_total = distances_total
        self.distances_diff = distances_diff
        self.begin = begin
        self.times_total = times_total
        self.times_diff = times_diff
        self.slopes = slopes
        self.velocities = velocities
        self.accelerations = accelerations
    

if __name__ == "__MAIN__":
    
    path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/Messfahrt2.gpx"
    save_path = "B:\Privat\Studium\Studienarbeit\dataprep_TripLog-main" 
    
    values = []
    
    values.append(calculateValues(path, 1))
    values.append(calculateValues(path, 2))
    values.append(calculateValues(path, 5))
    
    jump_sizes = ["Alle 3s", "Alle 6s", "Alle 15s"]
    
    
    speed = []
    distance = []
    times = []
    acceleration = []
    for i in range(len(values)):
        speed.append(values[i].velocities)
        times.append(values[i].times_total)
        distance.append(values[i].distances_total)
        acceleration.append(values[i].accelerations)
        
    printMultiplot(times, speed, "Zeit", "Geschwindigkeit", jump_sizes)
    
    printMultiplot(times, distance, "Zeit", "Strecke", jump_sizes)
    
    printMultiplot(distance, speed, "Strecke", "Geschwindigkeit", jump_sizes)
    
    printMultiplot(times, acceleration, "Zeit", "Beschleunigung", jump_sizes, save_path)






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