import os
import pandas as pd 
import calculate
import numpy as np 
import multiprocessing
import asyncio

import constants as C

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', None)  # or 199


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
        
class SensorDatapoint:
    def __init__(self, acc_path, lacc_path, gyro_path, label, sublabel, subsublabel):
        self.acc_path = acc_path
        self.lacc_path = lacc_path
        self.gyro_path = gyro_path
        self.label = label
        self.sublabel = sublabel
        self.subsublabel = subsublabel

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


def interpolate_data(df):
    # =========================================================================
    # Resampling der Daten
    # https://stackoverflow.com/questions/47148446/pandas-resample-interpolate-is-producing-nans?noredirect=1&lq=1
    # =========================================================================
    oidx = df.index
    nidx = pd.date_range(oidx.min(), oidx.max(), freq = C.INTERPOLATE_FREQUENCY)
    df_res = df.reindex(oidx.union(nidx)).interpolate('index').reindex(nidx)
    return df_res

async def reindex_and_interpolate(df):
    oidx = df.index
    nidx = pd.date_range(oidx.min(), oidx.max(), freq='20ms')
    df_res = df.reindex(oidx.union(nidx)).interpolate('index').reindex(nidx)
    return df_res

async def preperate_sensor(record):
# =============================================================================
# Alles was mit Sensor Dateien zu tun hat - Resampling, Berechnen von
# Features etc
# =============================================================================

    if os.path.isfile(record.path_sensor):
        df = pd.read_csv(record.path_sensor, sep = ",")
                
        # =====================================================================
        # Prepare Data for Resampling
        # =====================================================================
        df = df[:-2]
        
        start_time = df['Time_in_ns'].iloc[0]
        df['Time_in_ns'] = df['Time_in_ns'] - start_time
        
        start_time = df['Time_in_ns.1'].iloc[0]
        df['Time_in_ns.1'] = df['Time_in_ns.1'] - start_time
        
        start_time = df['Time_in_ns.2'].iloc[0]
        df['Time_in_ns.2'] = df['Time_in_ns.2'] - start_time
        

        df_accData = df[['ACC_X', 'ACC_Y', 'ACC_Z']].copy()
        df_accData.index = pd.to_datetime(df['Time_in_ns'], unit = 'ns')
        
        df_laccData = df[['LINEAR_ACC_X', 'LINEAR_ACC_Y', 'LINEAR_ACC_Z']].copy()
        df_laccData.index = pd.to_datetime(df['Time_in_ns.1'], unit = 'ns')
        
        df_gyroData = df[['w_X', 'w_Y', 'w_Z']].copy()
        df_gyroData.index = pd.to_datetime(df['Time_in_ns.2'], unit = 'ns')
        
        #print("Kopieren erledigt")
        # print(df.head(20))
        # print(df_accData.head(20))
        # print(df_laccData.head(20))
        # print(df_gyroData.head(20))
        
        # =====================================================================
        # Resampling der Daten
        # https://stackoverflow.com/questions/47148446/pandas-resample-interpolate-is-producing-nans?noredirect=1&lq=1
        # =====================================================================
        import time        
        
        start = time.time()
        print("Start Interpolation")
        
        acc = asyncio.create_task(reindex_and_interpolate(df_accData))
        lacc = asyncio.create_task(reindex_and_interpolate(df_laccData))
        gyro = asyncio.create_task(reindex_and_interpolate(df_gyroData))
        
        df_res_acc = await acc
        df_res_lacc = await lacc
        df_res_gyro = await gyro
        
        end = time.time()
        print("--> Finished: ", end - start)
        
        # =====================================================================
        # Abschneiden von Start und Ende der Daten      
        # =====================================================================
        ptbc_s = C.SECONDS_CUT_START * 50           # Points to be cut (start)
        ptbc_e = C.SECONDS_CUT_END * 50             # Points to be cut (end)
        pt_seg = C.SECONDS_SENSOR_SEGMENT * 50      # Points per segment
                                                    # 50 Points per second
                                            
        df_res_acc = df_res_acc[ptbc_s:len(df_res_gyro)-ptbc_e]
        df_res_lacc = df_res_lacc[ptbc_s:len(df_res_gyro)-ptbc_e]
        df_res_gyro = df_res_gyro[ptbc_s:len(df_res_gyro)-ptbc_e]
        
        # =====================================================================
        # Speichern von Datensegmenten mit festgelegter Segmentgröße und
        # Überlappung von 50 Prozent als Pickle Files und Ablegen der
        # Dateipfade in CSV Datei
        # =====================================================================
                
        label = record.label
        sublabel = record.sublabel
        subsublabel = record.subsublabel     
        
        for i in range(0, len(df_res_acc)-pt_seg, int(pt_seg/2)):
            
            path = str(time.time_ns())
            path = C.SENSOR_DATA_SEGMENT_FOLDER + path
            
            df_toSave_acc = pd.DataFrame()
            df_toSave_acc = df_res_acc[i:i+pt_seg]
            df_toSave_acc.to_pickle(path + "_acc.pkl", protocol = 2)
            
            df_toSave_lacc = pd.DataFrame()
            df_toSave_lacc = df_res_lacc[i:i+pt_seg]   
            df_toSave_acc.to_pickle(path + "_lacc.pkl", protocol = 2)
            
            df_toSave_gyro = pd.DataFrame()
            df_toSave_gyro = df_res_gyro[i:i+pt_seg] 
            df_toSave_acc.to_pickle(path + "_gyro.pkl", protocol = 2)
            
            obj = SensorDatapoint(
                path + "_acc.pkl", 
                path + "_lacc.pkl", 
                path + "_gyro.pkl", 
                label, sublabel, subsublabel
            )
                     
            record.splitted_sensor.append(obj)
            
async def totalSensorSegments(records):
    counter = 0
    for record in records:
        counter = counter + len(record.splitted_sensor)  
    return counter
    
async def preperate_data(records):
        
    count = list(range(len(records)))
        
    for record, i in zip(records, count):
        
        if(True):
            
            #print("File: ", record.path_sensor)
            ### GPS Preperation ###
            # preperate_gps(record)
            
            ### Sensor Preperation ###
            #print(record.path_sensor)
            
            
            
            print("Dateipfad: ", record.path_sensor)
            print("File ", i, " of ", len(records))
            try:
                size = os.path.getsize(record.path_sensor)
                print('File size: ' + str(round(size / (1024 * 1024), 3)) + ' Megabytes')
            except:
                print("Datei nicht verfügbar!")
            
            try:
                await preperate_sensor(record)
            except:
                pass
        
    segment_count = await totalSensorSegments(records)
    print("Total sensor segments: ", segment_count)
    
async def read_labels(file):
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
      
async def collect_files(path):
    records = []
    
    # Durchläuft alle User-Ordner
    for folder in os.listdir(path):
        # Durchläuft alle Dateien in den User-Ordnern
        for file in os.listdir(path + folder + "/"):
            
            # Prüfe ob Dateiendung "csv" und Datentyp "GPS"
            if str(file[-7:]) == "GPS.csv":
                path_gps = path + folder + "/" + file
                path_sensor = path + folder + "/" + file[:-7] + "SENSOR.csv"
                
                labels = await read_labels(file)
                
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
async def main():
    records = await collect_files(path)
    
    # Anzahl der aufgenommenen Datensätze
    print(len(records))
    
    await preperate_data(records)
    
    # ml_csv = data_import(path)
    # ml_csv.to_csv(save_path_gps)
    
path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/FirebaseStorageTripData/trips/"
save_path_gps = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/06-Datenaufbereitung/processedData/ml_gps.csv"

if(__name__ == "__main__"):
    import nest_asyncio
    nest_asyncio.apply()
    
    asyncio.run(main())
    
    
    