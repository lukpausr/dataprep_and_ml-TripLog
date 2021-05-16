import pandas as pd
import numpy as np
from math import sin, cos, sqrt, atan2, radians
from scipy.spatial import distance as dis

import matplotlib.pyplot as plt

import visualize as v
import tikzplotlib
import triplog_constants as C

# =============================================================================
# calc_distance
# calculate the distance between two given gps-points
#
# Parameter:
#   lat1, lon1 - gps coordinates of the first point
#   lat2, lon2 - gps coordinates of the second point
#
# Returns:
#   distance - returns the distance in meters
# =============================================================================   
def calc_distance(lat1, lon1, lat2, lon2):

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    ###########################################################################
    ### Using Haversine Formula
    ###########################################################################
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    ###########################################################################
    ### Estimation of the distance based on the earth radius in km
    ###########################################################################
    R = 6373.0
    distance = R * c
    distance = 1000 * distance

    return(distance)

# =============================================================================
# get_data
# basic data for features is being calculated/collected out of dataframe
#
# Parameter:
#   cvs - dataframe of a csv-file
#
# Returns:
#   times_total - list of total times
#   times_diff - list of times differences
#   distances_total - list of total distance
#   distances_diff - list of distance differences
#   speedGoogle - list of speeds calculated by google
# =============================================================================  
def get_data(csv):

    #######################################################################
    ### Creating time lists
    #######################################################################
    time_in_s = csv["Time_in_s"]
    begin = time_in_s[0]

    times_total = [0]
    times_diff = [0]        
       
    for i in range(1,len(time_in_s)):
        times_total.append(time_in_s[i] - begin)
        times_diff.append(time_in_s[i]-time_in_s[i-1])

    #######################################################################
    ### Creating distance lists
    #######################################################################
    lats = csv["Latitude"]
    lons = csv["Longitude"]
    
    distances_total = [0]
    distances_diff = [0]

    total = 0
    for i in range(1, len(lats)):
        dist = calc_distance(lats[i], lons[i], lats[i-1], lons[i-1])
        total = total + dist
        distances_total.append(total)
        distances_diff.append(dist)

    #######################################################################
    ### Creating google speed list
    #######################################################################
    speedGoogle = list(csv["Speed"].values)
    
    return(times_total, times_diff, distances_total, distances_diff, speedGoogle)

# =============================================================================
# calculate_data
# calculate gps features
#
# Parameter:
#   times_total - list of total times
#   times_diff - list of times differences
#   distances_total - list of total distance
#   distances_diff - list of distance differences
#   speedGoogle - list of speeds calculated by google
#
# Returns:
#   data - DataFrame with all features made of gps data
# =============================================================================  
def calculate_data(times_total, times_diff, distances_total, distances_diff, speedGoogle, printReq=False):

    ###########################################################################
    ### Calculate speed features
    ###########################################################################
    if C.USE_GOOGLE_SPEEDS is True:
        velocities = speedGoogle
    else:
        velocities = [0]
        for i in range(1, len(distances_diff)):
            velocities.append(distances_diff[i]/(times_diff[i]))

    # average and maximum speed
    max_velocity = max(velocities)
    avg_velocity = sum(velocities)/len(velocities)

    # Average speed without speeds < 2km/h (waiting times)
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
        
    ###########################################################################
    ### Calculate acceleration features
    ###########################################################################
    accelerations = [0]
    #in m/s^2
    for i in range(1, len(velocities)):
        accelerations.append( (velocities[i] - velocities[i-1]) / (times_diff[i]))       
    
    # Maximum and minimum acceleration
    max_acceleration = max(accelerations)
    min_acceleration = min(accelerations)        
        
    ###########################################################################
    ### Calculate waiting times
    ###########################################################################
    waiting_duration = times_total[-1] - sum(times_wo_waiting)

    # Duration
    duration = times_total[-1]

    # Distance
    distance = distances_total[-1]
    
    # Standard deviation and variance
    stdSpeed = np.std(velocities, dtype=np.float64)
    varSpeed = np.var(velocities, dtype=np.float64)
    stdAcc = np.std(accelerations, dtype=np.float64)
    varAcc = np.var(accelerations, dtype=np.float64)
    
    ###########################################################################
    ### Create DataFrame
    ###########################################################################
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
    
    ###########################################################################
    ### if printReq(required) is set true: 
    ### print comparison between gps calculated speeds, median filtered 
    ### speeds and google speeds (as latex pgf/tikz)
    ###########################################################################
    if printReq is True:
        import time
        velocities = [0]
        for i in range(1, len(distances_diff)):
            velocities.append(distances_diff[i]/(times_diff[i]))
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
            "***:/***/T3200/images/plots/" + str(time.time_ns()) + ".tex",
            axis_width = "18cm",
            axis_height = "10cm",
            textsize = 10.0,
            flavor = "latex"
        )

    return(data)

# =============================================================================
# meanNearestInfrastructure
# Find out mean distance to closest infrastructure of given list of points
# using closest_node
# CAUTION: VERY TIME CONSUMING CALCULATION, FEATURE CALCULATION RISES FROM
# 30MIN TO 12HOURS AND MORE BECAUSE OF THIS CALCULATION!
# See: https://codereview.stackexchange.com/questions/28207/finding-the-closest-point-to-a-list-of-points
#
# Parameter:
#   df - DataFrame of gps-file
#   dbInfrastructure - list of df Infrastructure points (window)
#
# Returns:
#   distance - distance to nearest point in the window
# =============================================================================  
def meanNearestInfrastructure(df, dbInfrastructure):  
    points = pd.DataFrame()
    points['Latitude'] = df['Latitude'] 
    points['Longitude'] = df['Longitude']
    allPoints = list(points.itertuples(index=False, name=None))
            
    ###########################################################################
    ### Calculate mean distance to infrastructure of all given points
    ### USE FEWER POINTS (CALCULATE 1, JUMP 1 ...or sth. like this) TO SAVE
    ### CALCULATION TIME - NOT IMPLEMENTED YET
    ###########################################################################
    distance = 0.0
    for point in allPoints:
        node = closest_node(point, dbInfrastructure)
        distance = distance + calc_distance(point[0], point[1], node[0], node[1])
 
    distance = distance / len(allPoints)
    return distance

# =============================================================================
# closest_node
# Finding the closest point to a list of points
# Parameter:
#   node - point to which the shortest distance is to be determinded
#   nodes - points of the db infrastructure
#
# Returns:
#   node - point with the shortest distance to input node
# =============================================================================  
def closest_node(node, nodes):
    closest_index = dis.cdist([node], nodes).argmin()
    return nodes[closest_index]

# =============================================================================
# ml_csv
# Creates a DataFrame with the ML features from the DataFrame of a csv file 
# Parameter:
#   df - DataFrame of gps-file 
#
# Returns:
#   data - DataFrame with ML features
# =============================================================================  
def ml_csv(df, printReq=False):

    times_total, times_diff, distances_total, distances_diff, speedGoogle = get_data(df)
    data = calculate_data(times_total, times_diff, distances_total, distances_diff, speedGoogle, printReq) 

    return(data)

if __name__ == "__MAIN__":
    path = r"***:\***\1608195983032_Car_Electric.csv"
    csv = pd.read_csv(path, sep = ",")    
    times_total, times_diff, distances_total, distances_diff = get_data(csv) 
    calculate_data(times_total, times_diff, distances_total, distances_diff)