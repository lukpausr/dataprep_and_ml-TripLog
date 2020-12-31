import pandas as pd 
import os 
import visualize_sensor as vs
import calculate as c


seconds = 60

path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/FirebaseStorageTripData/trips/Development_2_johanna/"


def gps_spliter(path, seconds):
    csv = pd.read_csv(path)
    times_total, _, _, _ = c.get_data(csv)
    avg_time = times_total[-1]/len(times_total)
    try:
        step = seconds / avg_time
        for i in range(0, len(csv) - step, step):
            csvs.append(csv.values[i : i+step])
    except:
        csvs = [csv]
    
    return(csvs)


def sensor_spliter(path, seconds):
    csv = pd.read_csv(path)
    avg_time = vs.average_time(csv, "Time_in_ns")

    #NEIN STOP HIER MUSS MAN SPLINEN
    try:
        step = seconds /(avg_time/1000)
        for i in range(0,len(csv), step):
            csvs.append(csv.values[i : i+step])
    except:
        csvs = [csv]





for csv_file in os.listdir(path):
    
    if "GPS" not in csv_file and "SENSOR" not in csv_file:
        None
    else:
        if "GPS" in csv_file:
            gps_spliter(path + "/" + csv_file, seconds)
        if "SENSOR" in csv_file:
            sensor_spliter(path+"/"+csv_file, seconds)