import pandas as pd
from gpx_csv_converter import Converter
from math import sin, cos, sqrt, atan2, radians

#Funktion um Distanz (m) zw. zwei GPS-Punkten zu bestimmen
def calc_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # approximate radius of earth in km
    R = 6373.0
    distance = R * c
    distance = 1000*distance

    #returns Meter
    return(distance)

def get_data(csv):
    #Startzeitpunkt ermitteln
    time_in_s = csv["Time_in_s"]
    begin = time_in_s[0]

    #Zeitpunkte in Listen speichern
    times_total = [0]
    times_diff = [0]        
       
    for i in range(1,len(time_in_s)):
        times_total.append(time_in_s[i] - begin)
        times_diff.append(time_in_s[i]-time_in_s[i-1])

    #Distanzen
    lats = csv["Latitude"]
    lons = csv["Longitude"]

    #Distanzen in Listen speichern
    distances_total = [0]
    distances_diff = [0]

    total = 0
    for i in range(1, len(lats)):
        dist = calc_distance(lats[i], lons[i], lats[i-1], lons[i-1])
        total = total + dist
        distances_total.append(total)
        distances_diff.append(dist)
    
    return(times_total, times_diff, distances_total, distances_diff)

def calculate_data(times_total, times_diff, distances_total, distances_diff):
    
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

    #Durchschnitt- und Maximalgeschwindigkeit
    max_velocity = max(velocities)
    avg_velocity = sum(velocities)/len(velocities)

    #Durchschnittsgeschwindigkeit ohne Geschwindigkeiten < 2km/h (Wartezeiten)
    times_wo_waiting = []
    velocities_wo_waiting = []
    for i in range(len(velocities)):
        if velocities[i] > 2:
            velocities_wo_waiting.append(velocities[i])
            times_wo_waiting.append(times_diff[i])
    try:
        avg_velocity_wo_waiting = sum(velocities_wo_waiting)/len(velocities_wo_waiting)
    except:
        avg_velocity_wo_waiting = None

    #Wartezeiten
    waiting_duration = times_total[-1] - sum(times_wo_waiting)

    #Maximal- und Minimalbeschleunigung
    max_acceleration = max(accelerations)
    min_acceleration = min(accelerations)
 
    #Dauer
    duration = times_total[-1]

    #Entfernung
    distance = distances_total[-1]
   
    #Daten zusammenfassen
    #dauer einer Beschleunigung, bremsweg
    data = [avg_velocity, max_velocity, min_acceleration, max_acceleration, duration, distance, waiting_duration, avg_velocity_wo_waiting]
    data = pd.DataFrame(data=[data], columns = ["Average speed", "Maximum speed","Minimum acceleration", "Maximum acceleration", "Duration", "Distance","Time of waiting", "Average speed without waiting"])
    return(data)

def ml_csv(csv):

    times_total, times_diff, distances_total, distances_diff = get_data(csv)
    data = calculate_data(times_total, times_diff, distances_total, distances_diff) 

    return(data)

#a = r"Z:\2020-JG18-T31Bewegungsanalyse-Pelz-Kroener\05-Messfahrten_Daten\FirebaseStorageTripData\trips\\"


#path = r"C:\Studium\5.Semester\Studienarbeit\1608195983032_Car_Electric.csv"
#csv = pd.read_csv(path, sep = ",")    
#times_total, times_diff, distances_total, distances_diff = get_data(csv) 
#calculate_data(times_total, times_diff, distances_total, distances_diff)

