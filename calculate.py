import pandas as pd
import numpy as np
#from gpx_csv_converter import Converter
from math import sin, cos, sqrt, atan2, radians
from scipy.spatial import distance as dis

import matplotlib.pyplot as plt

import visualize as v
import tikzplotlib
import triplog_constants as C

# Funktion um Distanz (m) zw. zwei GPS-Punkten zu bestimmen
def calc_distance(lat1, lon1, lat2, lon2):
    """
    Berechnet die Distanz zwischen zwei GPS Punkten in m.
    
    Parameters
    ----------
    lat1 : Numpy.Float
        Breitengrad von GPS-Punkt 1.
    lon1 : Numpy.Float
        Längengrad von GPS-Punkt 1.
    lat2 : Numpy.Float
        Breitengrad von GPS-Punkt 2.
    lon2 : Numpy.Float
        Längengrad von GPS-Punkt 2.

    Returns
    -------
    Distanz in m.

    """
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine Formula
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Abschätzung der Strecke auf Basis des Erdradius in km
    R = 6373.0
    distance = R * c
    distance = 1000*distance

    # Return Meter
    return(distance)

def get_data(csv):
    """
    Aus der übergebenen csv-Datei werden die relevanten Werte (Zeiten, Distanzen)
    entnommen und in Listen gespeichert.

    Parameters
    ----------
    csv : Pandas DataFrame
        DataFrame einer csv-Datei.

    Returns
    -------
    list[float]: Liste mit den Zeiten (total)
    List[float]: Liste mit den Zeitdifferenzen
    List[float]: Liste mit der Gesamtstrecke
    List[float]: Liste mit den Streckendifferenzen        

    """
    # Startzeitpunkt ermitteln
    time_in_s = csv["Time_in_s"]
    begin = time_in_s[0]

    # Zeitpunkte in Listen speichern
    times_total = [0]
    times_diff = [0]        
       
    for i in range(1,len(time_in_s)):
        times_total.append(time_in_s[i] - begin)
        times_diff.append(time_in_s[i]-time_in_s[i-1])

    # Distanzen
    lats = csv["Latitude"]
    lons = csv["Longitude"]
    
    # print(type(lats[0]))
    # Distanzen in Listen speichern
    distances_total = [0]
    distances_diff = [0]

    total = 0
    for i in range(1, len(lats)):
        dist = calc_distance(lats[i], lons[i], lats[i-1], lons[i-1])
        total = total + dist
        distances_total.append(total)
        distances_diff.append(dist)
    # Zeiten in Sekunden
    
    speedGoogle = list(csv["Speed"].values)
    
    return(times_total, times_diff, distances_total, distances_diff, speedGoogle)

def calculate_data(times_total, times_diff, distances_total, distances_diff, speedGoogle, printReq=False):
    """
    Berechnet aus den Daten von get_data() die Features der GPS-Daten.

    Parameters
    ----------
    times_total : List[float]
    times_diff : List[float]
    distances_total : List[float]
    distances_diff : List[float]
    
    Returns
    -------
    DataFrame mit den ml-Features der GPS-Daten.

    """
    #Berechnen der Geschwindigkeiten
    if C.USE_GOOGLE_SPEEDS is True:
        velocities = speedGoogle
    else:
        velocities = [0]
        #in km/h
        for i in range(1, len(distances_diff)):
            velocities.append(distances_diff[i]/(times_diff[i]))

    #Berechnen der Beschleunigungen
    accelerations = [0]
    #in m/s^2
    for i in range(1, len(velocities)):
        accelerations.append( (velocities[i] - velocities[i-1]) / (times_diff[i]))

    #Durchschnitt- und Maximalgeschwindigkeit
    max_velocity = max(velocities)
    avg_velocity = sum(velocities)/len(velocities)

    #Durchschnittsgeschwindigkeit ohne Geschwindigkeiten < 2km/h (Wartezeiten)
    times_wo_waiting = []
    velocities_wo_waiting = []
    for i in range(len(velocities)):
        if velocities[i] > (2/3.6):
            velocities_wo_waiting.append(velocities[i])
            times_wo_waiting.append(times_diff[i])
    try:
        avg_velocity_wo_waiting = sum(velocities_wo_waiting)/len(velocities_wo_waiting)
    except:
        avg_velocity_wo_waiting = 0

    if times_wo_waiting == []:
        times_wo_waiting = [0] 
    
    if avg_velocity_wo_waiting == None: 
        avg_velocity_wo_waiting = 0
        
    #Wartezeiten
    waiting_duration = times_total[-1] - sum(times_wo_waiting)

    #Maximal- und Minimalbeschleunigung
    max_acceleration = max(accelerations)
    min_acceleration = min(accelerations)
 
    #Dauer
    duration = times_total[-1]

    #Entfernung
    distance = distances_total[-1]
    
    #Standardabweichung und Varianz
    stdSpeed = np.std(velocities, dtype=np.float64)
    varSpeed = np.var(velocities, dtype=np.float64)
    stdAcc = np.std(accelerations, dtype=np.float64)
    varAcc = np.var(accelerations, dtype=np.float64)
    
    #Daten zusammenfassen
    #dauer einer Beschleunigung, bremsweg
    data = [avg_velocity, max_velocity, min_acceleration, max_acceleration, 
            duration, distance, waiting_duration, avg_velocity_wo_waiting,
            stdSpeed, varSpeed, stdAcc, varAcc]
    data = pd.DataFrame(
        data=[data], columns = [
            "Average speed", 
            "Maximum speed",
            "Minimum acceleration", 
            "Maximum acceleration", 
            "Duration", 
            "Distance",
            "Time of waiting", 
            "Average speed without waiting",
            "STDSPEED",
            "VARSPEED",
            "STDACC",
            "VARACC"
        ]
    )
    
    if printReq is True:
        import time
        # Test for median filtering
        #from pandas.core.window import Rolling
        #threshold = 3
        fig = plt.figure(figsize =(20, 10)) 
        plt.ylim(0, 60)
        plt.xlim(0, 2000)
        plt.ylabel("Geschwindigkeit in $m/s$")
        plt.xlabel("Zeit in $s$")
        df = pd.DataFrame()
        df['vel'] = velocities
        df['median'] = df['vel'].rolling(window = 10, center=True).median()
        df['median'] = df['median'].fillna(method='bfill').fillna(method='ffill')
        #(median(df['vel'], window = 3, center=True).fillna(method='bfill').fillna(method='ffill'))        
        
        plt.plot(times_total, df['vel'], linewidth=3, label="Ohne Vorverarbeitung")
        plt.plot(times_total, list(df['median'].values), linewidth=3, label="Medianfilter")     
        plt.plot(times_total, speedGoogle, linewidth=3, label="Google")
        plt.legend(loc="upper left")
        
        tikzplotlib.save(
            "C:/Users/Lukas/Desktop/Studienarbeit/T3200/images/plots/" + str(time.time_ns()) + ".tex",
            axis_width = "18cm",
            axis_height = "6cm",
            textsize = 10.0,
            flavor = "latex"
        )

    return(data)

def meanNearestInfrastructure(df, dbInfrastructure):  
    points = pd.DataFrame()
    points['Latitude'] = df['Latitude'] 
    points['Longitude'] = df['Longitude']
    allPoints = list(points.itertuples(index=False, name=None))
    
    # tl_point = ((df['Latitude'].max + 0.5), (df['Longitude'].min - 0.5))
    # tr_point = ((df['Latitude'].max + 0.5), (df['Longitude'].max + 0.5))
    # bl_point = ((df['Latitude'].min - 0.5), (df['Longitude'].min - 0.5))
    # br_point = ((df['Latitude'].min - 0.5), (df['Longitude'].max + 0.5))  
        
    distance = 0.0
    for point in allPoints:
        node = closest_node(point, dbInfrastructure)
        distance = distance + calc_distance(point[0], point[1], node[0], node[1])
 
    distance = distance / len(allPoints)
    return distance

# https://codereview.stackexchange.com/questions/28207/finding-the-closest-point-to-a-list-of-points
def closest_node(node, nodes):
    closest_index = dis.cdist([node], nodes).argmin()
    return nodes[closest_index]

def ml_csv(df, printReq=False):
    """
    Erstellt aus dem DataFrame einer csv-Datei ein DataFrame mit den ML-Features.

    Parameters
    ----------
    df : Pandas.DataFrame
        Eine GPS-Datei, die in einem DataFrame eingelesen wurde.

    Returns
    -------
    DataFrame mit ML-Features.

    """
    times_total, times_diff, distances_total, distances_diff, speedGoogle = get_data(df)
    data = calculate_data(times_total, times_diff, distances_total, distances_diff, speedGoogle, printReq) 

    return(data)

if __name__ == "__MAIN__":
    path = r"C:\Studium\5.Semester\Studienarbeit\1608195983032_Car_Electric.csv"
    csv = pd.read_csv(path, sep = ",")    
    times_total, times_diff, distances_total, distances_diff = get_data(csv) 
    calculate_data(times_total, times_diff, distances_total, distances_diff)