import os
import pandas as pd 
import calculate
import numpy as np 

import constants as C

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199


class Record:
    def __init__(self, path_gps, path_sensor, label = "", sublabel = "", subsublabel = ""):
        self.path_gps = path_gps
        self.path_sensor = path_sensor
        self.label = label
        self.sublabel = sublabel
        self.subsublabel = subsublabel
        self.splitted_gps = []
        self.splitted_sensor = []
        
    def __str__(self):
        print("### Record Object ###")
        print("GPS-Path: ", self.path_gps)
        print("Sensor-Path: ", self.sensor_gps)
        print("Label: ", self.label)
        print("Sublabel: ", self.sublabel)
        print("SubSubLabel: ", self.subsublabel)
        print("#####################")

def csv_import(path):
    """
    Task: Importieren und Verarbeiten einer CSV Datei
    
    Parameters
    ----------
    path : String
        Dateipfad der zu verarbeitenden CSV Datei.
        
    Returns
    -------
    Pandas Dataframe.
        Pandas Dataframe mit allen GPS-Features
    """
    csv = pd.read_csv(path, sep = ",")    
    ml_csv = calculate.ml_csv(csv)    
    return(ml_csv)
    
def data_import(path):
    """
    Task: Sammelt alle CSV (GPS) Dateien und verarbeitet diese

    Returns
    -------
    None.

    """
    records = []
    # Durchläuft alle User-Ordner
    for files in os.listdir(path):
        # Durchläuft alle Dateien in den User-Ordnern
        for data in os.listdir(path + files + "/"):
            
            # Labels extrahieren
            split = data.split(".")     # Entfernen der Dateiendung
            split = split[0].split("_") # Splitten bei _
            split = split[1:]           # Wegschneiden der Dateinummer

            # Prüfe ob Dateiendung "csv" und Datentyp "GPS"
            if str(data[-7:]) == "GPS.csv":
                
                # DataFrame erstellen
                try:
                    # print(path+files+"/"+data)
                    dataFrame = csv_import(path+files+"/"+data)
                except: 
                    print("INVALID DATA: " +path+files+"/"+data)
                    dataFrame = pd.DataFrame(columns=["Average speed", "Maximum speed", "Average speed without waiting","Minimum acceleration", "Maximum acceleration", "Duration", "Distance"])

                # Labels einfügen
                dataFrame["label"] = None
                dataFrame["sublabel"] = None
                dataFrame["subsublabel"] = None
                try: 
                    dataFrame["label"] = split[0]
                    dataFrame["sublabel"] = split[1]
                    dataFrame["subsublabel"] = split[2]
                except:
                    None

                # ML-CSV erstellen
                try:             
                    ml_csv = pd.concat([ml_csv, dataFrame])
                except:
                    ml_csv = dataFrame
        
            else:
                # Ab hier Verarbeitung Sensordaten
                pass
                

    return(ml_csv)
    # return(records)
    # print(ml_csv) 

def preperate_gps(record):
# =============================================================================
# Alles was mit GPS Dateien zu tun hat - schneiden der Dateien, Berechnen der
# Features etc
# =============================================================================
    
    # DataFrame erstellen
    try:
        # print(path+files+"/"+data)
        dataFrame = csv_import(record.path_gps)
    except: 
        print("INVALID DATA: ", record.path_gps)
        dataFrame = pd.DataFrame(columns=["Average speed", "Maximum speed", "Average speed without waiting","Minimum acceleration", "Maximum acceleration", "Duration", "Distance"])


def preperate_sensor(record):
# =============================================================================
# Alles was mit Sensor Dateien zu tun hat - Resampling, Berechnen von
# Features etc
# =============================================================================

    if os.path.isfile(record.path_sensor):
        df = pd.read_csv(record.path_sensor, sep = ",")
        
        # =====================================================================
        # Convert ns-Timestamp to Timedelta   
        # =====================================================================
        #df['td_acc'] = pd.to_datetime(df['Time_in_ns'], unit='ns')
        #df['td_linearAcc'] = pd.to_timedelta(df['Time_in_ns.1'], 'ns')
        #df['td_gyro'] = pd.to_timedelta(df['Time_in_ns.1'], 'ns')
        # print(df.head(20))
        
        # =====================================================================
        # Prepare Data for Resampling
        # =====================================================================
        start_time = df['Time_in_ns'].iloc[0]
        df['Time_in_ns'] = df['Time_in_ns'] - start_time

        df_accData = df[['ACC_X', 'ACC_Y', 'ACC_Z']].copy()
        df_accData.index = pd.to_datetime(df['Time_in_ns'], unit = 'ns')
        
        df_laccData = df[['LINEAR_ACC_X', 'LINEAR_ACC_Y', 'LINEAR_ACC_Z']].copy()
        df_laccData.index = pd.to_datetime(df['Time_in_ns.1'], unit = 'ns')
        
        df_gyroData = df[['w_X', 'w_Y', 'w_Z']].copy()
        df_gyroData.index = pd.to_datetime(df['Time_in_ns.2'], unit = 'ns')
        
        print(df.head(20))
        print(df_accData.head(20))
        print(df_laccData.head(20))
        print(df_gyroData.head(20))
        
        # =====================================================================
        # Resampling der Daten
        # https://stackoverflow.com/questions/47148446/pandas-resample-interpolate-is-producing-nans?noredirect=1&lq=1
        # =====================================================================
        oidx = df_accData.index
        nidx = pd.date_range(oidx.min(), oidx.max(), freq='20ms')
        df_res_acc = df_accData.reindex(oidx.union(nidx)).interpolate('index').reindex(nidx)
        
        oidx = df_laccData.index
        nidx = pd.date_range(oidx.min(), oidx.max(), freq='20ms')
        df_res_lacc = df_accData.reindex(oidx.union(nidx)).interpolate('index').reindex(nidx)
        
        oidx = df_gyroData.index
        nidx = pd.date_range(oidx.min(), oidx.max(), freq='20ms')
        df_res_gyro = df_accData.reindex(oidx.union(nidx)).interpolate('index').reindex(nidx)
        
        # res.to_excel('Test.xlsx')
        
        # =====================================================================
        # Abschneiden von Start und Ende der Daten      
        # =====================================================================
        
  
    
def preperate_data(records):
    for record in records:
        
        ### GPS Preperation ###
        # preperate_gps(record)
        
        ### Sensor Preperation ###
        preperate_sensor(record)
    
def read_labels(file):
    label = ["", "", ""]
    
    # Labels extrahieren
    split = file.split(".")     # Entfernen der Dateiendung
    split = split[0].split("_") # Splitten bei _
    split = split[1:]           # Wegschneiden der Dateinummer
    
    try: 
        label[0] = split[0]
        label[1] = split[1]
        label[2] = split[2]
    except:
        None
        
    return label
      
def collect_files(path):
    records = []
    
    # Durchläuft alle User-Ordner
    for folder in os.listdir(path):
        # Durchläuft alle Dateien in den User-Ordnern
        for file in os.listdir(path + folder + "/"):
            
            # Prüfe ob Dateiendung "csv" und Datentyp "GPS"
            if str(file[-7:]) == "GPS.csv":
                path_gps = path + folder + "/" + file
                path_sensor = path + folder + "/" + file[:-7] + "SENSOR.csv"
                
                labels = read_labels(file)
                
                records.append(
                    Record(
                        path_gps= path_gps, 
                        path_sensor= path_sensor, 
                        label= labels[0],
                        sublabel= labels[1],
                        subsublabel= labels[2]
                    )
                )
    
    return records
    

# =============================================================================
# Hauptprogramm
# =============================================================================
path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/FirebaseStorageTripData/trips/"
save_path_gps = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/06-Datenaufbereitung/processedData/ml_gps.csv"

if(__name__ == "__main__"):
    
    records = collect_files(path)
    
    # Anzahl der aufgenommenen Datensätze
    print(len(records))
    
    preperate_data(records)
    
    # ml_csv = data_import(path)
    # ml_csv.to_csv(save_path_gps)