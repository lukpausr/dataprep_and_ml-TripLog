import os
import pandas as pd 
import calculate
import numpy as np 
#import multiprocessing
import asyncio

import triplog_constants as C
#import ML.visualisation_ml as vis
import FeatureExtraction.calculate_sensor as calcSensor

pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', None)  # or 199
pd.options.mode.chained_assignment = None  # default='warn'


class Record:
    def __init__(self, path_gps, path_sensor, folder, label = "", sublabel = "", subsublabel = "", valid = True):
        self.path_gps = path_gps
        self.path_sensor = path_sensor
        self.folder = folder
        self.label = label
        self.sublabel = sublabel
        self.subsublabel = subsublabel
        self.splitted_gps = []
        self.splitted_sensor = []
        self.valid = valid
        
    def __str__(self):
        string = "### Record Object ###\n" + \
                "GPS-Path: " + self.path_gps + "\n" + \
                "Label: " + self.label + "\n" + \
                "Sublabel: " + self.sublabel + "\n" + \
                "SubSubLabel: " + self.subsublabel  + "\n" + \
                "#####################"
        return string
 
class SensorDatapoint:
    def __init__(self, acc_path, lacc_path, gyro_path, 
                 maxFreqACC, maxFreqGYRO, maxSingleFreqACC, maxSingleFreqGYRO, 
                 stdAcc, varAcc, stdGyro, varGyro,
                 label, sublabel, subsublabel):
        self.acc_path = acc_path
        self.lacc_path = lacc_path
        self.gyro_path = gyro_path
        self.maxFreqACC = maxFreqACC,
        self.maxFreqGYRO = maxFreqGYRO,
        self.maxSingleFreqACC = maxSingleFreqACC,
        self.maxSingleFreqGYRO = maxSingleFreqGYRO,
        self.stdAcc = stdAcc,
        self.varAcc = varAcc,
        self.stdGyro = stdGyro,
        self.varGyro = varGyro,
        self.label = label
        self.sublabel = sublabel
        self.subsublabel = subsublabel
        
class GpsDatapoint:
    def __init__(self, avgSpeed, maxSpeed, minAcc, 
                 maxAcc, tow, towAvgSpeed, stdSpeed, varSpeed, 
                 stdAcc, varAcc, label, sublabel, subsublabel):
        self.avgSpeed = avgSpeed
        self.maxSpeed = maxSpeed
        self.minAcc = minAcc
        self.maxAcc = maxAcc
        self.tow = tow
        self.towAvgSpeed = towAvgSpeed
        self.stdSpeed = stdSpeed
        self.varSpeed = varSpeed
        self.stdAcc = stdAcc
        self.varAcc = varAcc
        self.label = label
        self.sublabel = sublabel
        self.subsublabel = subsublabel
        
    def __str__(self):
        string = "Average Speed :" + str(self.avgSpped)
        return string

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
    
async def raw_gps_interpolation(path_gps, enableMedianFiltering=False):
    df = pd.read_csv(path_gps, sep = ",")
    df = df[1:-1]
    
    # Median filtering test
    if enableMedianFiltering is True:
        df['latmed'] = df['Latitude'].rolling(window = 10, center=True).median()
        df['Latitude'] = df['latmed'].fillna(method='bfill').fillna(method='ffill')
        df['lonmed'] = df['Longitude'].rolling(window = 10, center=True).median()
        df['Longitude'] = df['lonmed'].fillna(method='bfill').fillna(method='ffill')
    
    start_time = df['Time_in_s'].iloc[0]
    df['Time_in_s'] = df['Time_in_s'] - start_time    
        
    df_gpsData = df[['Latitude', 'Longitude', 'Altitude', 'Speed']].copy()
    df_gpsData.index = pd.to_datetime(df['Time_in_s'], unit = 's')

    import time        
    start = time.time()
    print("\tStart Interpolation")
    
    gps = asyncio.create_task(
        reindex_and_interpolate(
            df_gpsData, 
            C.GPS_INTERPOLATE_FREQUENCY
        )
    )
    df_res_gps = await gps
    
    end = time.time()
    print("\t--> Finished: ", end - start) 
    
    ptbc_s = C.SECONDS_CUT_START                # Points to be cut (start)
    ptbc_e = C.SECONDS_CUT_END                  # Points to be cut (end)
    #pt_seg = C.SECONDS_SENSOR_SEGMENT           # Points per segment                                                    # 1 Point per secon   
                              
    df_res_gps = df_res_gps[ptbc_s:len(df_res_gps)-ptbc_e] 
    df_res_gps['Time_in_s'] = df_res_gps.index.astype(np.int64) // 10**9
    
    return df_res_gps

async def preperate_gps(record):   
# =============================================================================
# Alles was mit GPS Dateien zu tun hat - schneiden der Dateien, Berechnen der
# Features etc
# =============================================================================
    # DataFrame erstellen
    if os.path.isfile(record.path_gps):
        df = pd.read_csv(record.path_gps, sep = ",")
        df = df[1:-1]
        
        start_time = df['Time_in_s'].iloc[0]
        df['Time_in_s'] = df['Time_in_s'] - start_time    
            
        df_gpsData = df[['Latitude', 'Longitude', 'Altitude', 'Speed']].copy()
        df_gpsData.index = pd.to_datetime(df['Time_in_s'], unit = 's')

        import time        
        start = time.time()
        print("\tStart Interpolation")
        
        gps = asyncio.create_task(
            reindex_and_interpolate(
                df_gpsData, 
                C.GPS_INTERPOLATE_FREQUENCY
            )
        )
        df_res_gps = await gps
        
        end = time.time()
        print("\t--> Finished: ", end - start)
        
        # print("\tSize: ", len(df_res_gps))
        # print("\tdf_res_gps:  ", df_res_gps.index[0])
        # print("\tdf_res_gps:  ", df_res_gps.index[-1])  
        
        ptbc_s = C.SECONDS_CUT_START                # Points to be cut (start)
        ptbc_e = C.SECONDS_CUT_END                  # Points to be cut (end)
        pt_seg = C.SECONDS_SENSOR_SEGMENT           # Points per segment                                                    # 1 Point per secon   
                                  
        df_res_gps = df_res_gps[ptbc_s:len(df_res_gps)-ptbc_e] 
        df_res_gps['Time_in_s'] = df_res_gps.index.astype(np.int64) // 10**9
        
        label = record.label
        sublabel = record.sublabel
        subsublabel = record.subsublabel            
        
        for i in range(0, len(df_res_gps)-pt_seg, int(pt_seg/2)):
            
            df_work_gps = pd.DataFrame()
            df_work_gps = df_res_gps[i:i+pt_seg]
            
            data = calculate.ml_csv(df_work_gps)

            obj = GpsDatapoint(
                data['Average speed'].iloc[0],
                data['Maximum speed'].iloc[0],
                data['Minimum acceleration'].iloc[0],
                data['Maximum acceleration'].iloc[0],
                data['Time of waiting'].iloc[0],
                data['Average speed without waiting'].iloc[0],
                data['STDSPEED'].iloc[0],
                data['VARSPEED'].iloc[0],
                data['STDACC'].iloc[0],
                data['VARACC'].iloc[0],
                label, sublabel, subsublabel
            )     
            record.splitted_gps.append(obj)        
    
# =========================================================================
# Resampling der Daten
# https://stackoverflow.com/questions/47148446/pandas-resample-interpolate-is-producing-nans?noredirect=1&lq=1
# =========================================================================
async def reindex_and_interpolate(df, frequency=C.INTERPOLATE_FREQUENCY):
    oidx = df.index
    nidx = pd.date_range(oidx.min(), oidx.max(), freq=frequency)
    df_res = df.reindex(oidx.union(nidx)).interpolate('index').reindex(nidx)
    #df_res = df.reindex(oidx.union(nidx)).interpolate(method='spline', order=5).reindex(nidx)
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
        
        # =====================================================================
        # Resampling der Daten
        # https://stackoverflow.com/questions/47148446/pandas-resample-interpolate-is-producing-nans?noredirect=1&lq=1
        # =====================================================================
        import time        
        
        start = time.time()
        print("\tStart Interpolation")
        
        acc = asyncio.create_task(reindex_and_interpolate(df_accData))
        lacc = asyncio.create_task(reindex_and_interpolate(df_laccData))
        gyro = asyncio.create_task(reindex_and_interpolate(df_gyroData))
        
        df_res_acc = await acc
        df_res_lacc = await lacc
        df_res_gyro = await gyro
        
        end = time.time()
        print("\t--> Finished: ", end - start)
        
        # print("\tSize: ", len(df_res_acc))
        # print("\tdf_accData:  ", df_accData.index[0])
        # print("\tdf_accData:  ", df_accData.index[-1])
        
        # print("\tdf_laccData: ", df_laccData.index[0])
        # print("\tdf_laccData: ", df_laccData.index[-1])
        
        # print("\tdf_gyroData: ", df_gyroData.index[0])
        # print("\tdf_gyroData: ", df_gyroData.index[-1])
        
        # =====================================================================
        # Abschneiden von Start und Ende der Daten      
        # =====================================================================
        ptps = C.SENSOR_INTERPOLATE_FREQUENCY_INT
        ptbc_s = C.SECONDS_CUT_START * ptps         # Points to be cut (start)
        ptbc_e = C.SECONDS_CUT_END * ptps           # Points to be cut (end)
        pt_seg = C.SECONDS_SENSOR_SEGMENT * ptps    # Points per segment
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
            
            df_toSave_lacc = pd.DataFrame()
            df_toSave_lacc = df_res_lacc[i:i+pt_seg]   
                    
            df_toSave_gyro = pd.DataFrame()
            df_toSave_gyro = df_res_gyro[i:i+pt_seg] 
            
            if(C.WRITE_SENSOR_DATA_TO_FILE):
                df_toSave_acc.to_pickle(path + "_acc.pkl", protocol = 2)
                df_toSave_lacc.to_pickle(path + "_lacc.pkl", protocol = 2)
                df_toSave_gyro.to_pickle(path + "_gyro.pkl", protocol = 2) 
                
            maxFreqACC = calcSensor.sensorEuclideanFFT(
                calcSensor.vectorLength(df_toSave_acc, "ACC"), 
                (label + "_" + sublabel)
            )
            maxFreqGYRO = calcSensor.sensorEuclideanFFT(
                calcSensor.vectorLength(df_toSave_gyro, "GYRO"), 
                (label + "_" + sublabel)
            )
            maxSingleFreqACC = calcSensor.sensorAxsFFT(
                df_toSave_acc['ACC_X'], 
                df_toSave_acc['ACC_Y'], 
                df_toSave_acc['ACC_Z'], 
                (label + "_" + sublabel)
            )
            maxSingleFreqGYRO = calcSensor.sensorAxsFFT(
                df_toSave_gyro['w_X'], 
                df_toSave_gyro['w_Y'], 
                df_toSave_gyro['w_Z'], 
                (label + "_" + sublabel)
            )
            stdAcc, varAcc = calcSensor.metrics(
                calcSensor.vectorLength(df_toSave_acc, "ACC")
            )
            stdGyro, varGyro = calcSensor.metrics(
                calcSensor.vectorLength(df_toSave_gyro, "GYRO")
            )
                     
            obj = SensorDatapoint(
                path + "_acc.pkl", 
                path + "_lacc.pkl", 
                path + "_gyro.pkl", 
                maxFreqACC.astype(float),
                maxFreqGYRO.astype(float),
                maxSingleFreqACC.astype(float),
                maxSingleFreqGYRO.astype(float),
                stdAcc.astype(float),
                varAcc.astype(float),
                stdGyro.astype(float),
                varGyro.astype(float),
                label, sublabel, subsublabel
            )
                     
            record.splitted_sensor.append(obj)
                    
async def totalSensorSegments(records):
    counter = 0
    for record in records:
        counter = counter + len(record.splitted_sensor)  
    return counter
  
async def validate_data(records):
  
    count = list(range(len(records)))

    print("Checking files for errors")
    for record, i in zip(records, count):
        
        if True:
     
            print("######################################")
            print("File ", i, " of ", len(records))   
            
            totalTimeGPS = 0
            totalTimeSensor = 0
         
            ### Prüfe ob GPS-Dateien genug Datenpunkte enthalten
            csv_raw = pd.read_csv(record.path_gps)
            csv = csv_raw.iloc[1:]
            csv.index = range(0, len(csv))  
    
            timeStartGPS = csv["Time_in_s"].loc[0] + C.SECONDS_CUT_START
            timeStopGPS = csv["Time_in_s"].loc[len(csv)-1] - C.SECONDS_CUT_END
            csvStart = 0
            csvStop = 0
            
            totalTimeGPS = csv["Time_in_s"].iloc[-1] - csv["Time_in_s"].iloc[0] 
    
            if timeStopGPS > timeStartGPS:
                for j in range(len(csv)):
                    if csv["Time_in_s"].loc[j] > timeStartGPS and csvStart == 0:
                        csvStart = j
                    if csv["Time_in_s"].loc[j] > timeStopGPS and csvStop == 0:
                        csvStop = j
    
                csv = csv.iloc[csvStart:csvStop]
                record.valid = True
            else:
                record.valid = False
                print("File invalid: ", record.path_gps)
                
            try:
                csv_raw = pd.read_csv(record.path_sensor)
                csv = csv_raw.iloc[1:]
                maxTimeSensor = csv["Time_in_ns"].max()
                minTimeSensor = csv["Time_in_ns"].min()
                
                totalTimeSensor = (csv["Time_in_ns"].iloc[-2] - csv["Time_in_ns"].iloc[0]) / (1000 * 1000 * 1000)
                
                if(maxTimeSensor - minTimeSensor < 4 * 60 * 60 * 1000 * 1000 * 1000):
                    record.valid = True
                else:
                    record.valid = False
                    print("File invalid: ", record.path_sensor)            
                
                if abs(totalTimeGPS - totalTimeSensor) > 60:
                    record.valid = False
                    print("GPS TIME: ", totalTimeGPS)
                    print("SENSOR TIME: ", totalTimeSensor)
                    print("Files do not fit ", record.path_sensor, record.path_gps)
                    if(totalTimeGPS < totalTimeSensor):
                        lb = get_sensor_seperation_index(csv)
                        #print("LB: ", lb)
                        csv = csv[lb:] 
                        try:
                            os.remove(record.path_sensor)
                        except:
                            pass
                        csv.to_csv(record.path_sensor)
                        totalTimeSensor = (csv["Time_in_ns"].iloc[-2] - csv["Time_in_ns"].iloc[0]) / (1000 * 1000 * 1000)
                        if abs(totalTimeGPS - totalTimeSensor) < 60:
                            print("Error fixed!")
                            record.valid = True    
       
            except:
                record.valid = False
                print("File not existing: ", record.path_sensor)
        
    await delete_invalid_Entries(records)       
    print("Done")

def get_sensor_seperation_index(df):
    df['diff'] = df["Time_in_ns"].diff()

    print("MEAN: ", df["diff"].mean())
    print("MIN: ", df["diff"].min())
    print("MAX: ", df["diff"].max())
    print(df["diff"].idxmax())
    
    return df["diff"].idxmax()

async def delete_invalid_Entries(records):
    for record in records:
        if record.valid is False:
            try: 
                os.remove(record.path_gps)
            except:
                pass
            try:
                os.remove(record.path_sensor)
            except:
                pass
            try:
                records.remove(record)
            except:
                pass
  
async def preperate_data(records):
        
    if(C.VALIDATE is True):
        await validate_data(records)
        
    count = list(range(len(records)))
    
    for record, i in zip(records, count):
        if(record.valid):
            
            print("######################################")
            print("File ", i, " of ", len(records))
            print("\tFile: ", record.path_gps)

            try:
                await preperate_gps(record)
            except:
                pass
    
            ## Sensor Preperation ###
            print("\tFile: ", record.path_sensor)
            
            try:
                size = os.path.getsize(record.path_sensor)
                print('\tFile size: ' + str(round(size / (1024 * 1024), 3)) + ' Megabytes')
            except:
                print("\tDatei nicht verfügbar!")
            
            try:
                await preperate_sensor(record)
            except:
                print("\tUnerwarteter Fehler: Preperate Sensor")
            
       
    ### Statistik: Anzahl der eingelesenen Segmente ###    
    segment_count = await totalSensorSegments(records)
    print("Total sensor segments: ", segment_count)

async def writeFusedSegmentCSV(records):
    
    counter = 0
    df = pd.DataFrame(columns=['accFile', 'laccFile', 'gyroFile', 'avgSpeed', 
                               'maxSpeed', 'minAcc', 'maxAcc', 'tow', 'towAvgSpeed',
                               'stdSpeed', 'varSpeed', 'stdAcc', 'varAcc',
                               'maxFreqACC', 'maxFreqGYRO', 'maxSingleFreqACC', 'maxSingleFreqGYRO',
                               'sensor_stdAcc', 'sensor_varAcc', 'sensor_stdGyro', 'sensor_varGyro',
                               'folder', 'Label', 'Sublabel', 'Subsublabel'])
    
    for record in records:
        for segment_gps, segment_sensor in zip(record.splitted_gps, record.splitted_sensor):
            df.loc[counter] = [
                segment_sensor.acc_path, 
                segment_sensor.lacc_path, 
                segment_sensor.gyro_path,             
                segment_gps.avgSpeed, 
                segment_gps.maxSpeed, 
                segment_gps.minAcc,
                segment_gps.maxAcc,
                segment_gps.tow,
                segment_gps.towAvgSpeed,
                segment_gps.stdSpeed,
                segment_gps.varSpeed,
                segment_gps.stdAcc,
                segment_gps.varAcc,
                segment_sensor.maxFreqACC[0],
                segment_sensor.maxFreqGYRO[0],
                segment_sensor.maxSingleFreqACC[0],
                segment_sensor.maxSingleFreqGYRO[0],
                segment_sensor.stdAcc[0],
                segment_sensor.varAcc[0],
                segment_sensor.stdGyro[0],
                segment_sensor.varGyro[0],
                record.folder,
                segment_gps.label, 
                segment_gps.sublabel, 
                segment_gps.subsublabel
            ]
            counter = counter + 1

    df.to_csv(C.FUSED_DATA_CSV)
    
async def writeGpsSegmentCSV(records):
    
    counter = 0
    df = pd.DataFrame(columns=['avgSpeed', 'maxSpeed', 'minAcc', 'maxAcc', 'tow', 'towAvgSpeed', 
                               'stdSpeed', 'varSpeed', 'stdAcc', 'varAcc',
                               'folder', 'Label', 'Sublabel', 'Subsublabel'])
    
    for record in records:
        for segment in record.splitted_gps:
            df.loc[counter] = [
                segment.avgSpeed, 
                segment.maxSpeed, 
                segment.minAcc,
                segment.maxAcc,
                segment.tow,
                segment.towAvgSpeed,
                segment.stdSpeed,
                segment.varSpeed,
                segment.stdAcc,
                segment.varAcc,
                record.folder,
                segment.label, 
                segment.sublabel, 
                segment.subsublabel
            ]
            counter = counter + 1
    
    df.to_csv(C.GPS_DATA_CSV)
    
async def writeSensorSegmentCSV(records):
    
    counter = 0
    df = pd.DataFrame(columns=['accFile', 'laccFile', 'gyroFile', 
                               'folder', 'Label', 'Sublabel', 'Subsublabel'])
    
    for record in records:
        for segment in record.splitted_sensor:
            df.loc[counter] = [
                segment.acc_path, 
                segment.lacc_path, 
                segment.gyro_path, 
                record.folder,
                segment.label, 
                segment.sublabel, 
                segment.subsublabel
            ]
            counter = counter + 1
    
    df.to_csv(C.SENSOR_DATA_CSV)
               
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
                        folder= folder,
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
    await writeSensorSegmentCSV(records)
    await writeGpsSegmentCSV(records)
    await writeFusedSegmentCSV(records)
    
    # ml_csv = data_import(path)
    # ml_csv.to_csv(save_path_gps)
    
path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/FirebaseStorageTripData/trips/"
#path = "C:/Users/Lukas/Desktop/SensorData/Testdaten/"
save_path_gps = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/06-Datenaufbereitung/processedData/ml_gps.csv"

if(__name__ == "__main__"):
    import nest_asyncio
    nest_asyncio.apply()  
    asyncio.run(main())
    
    
    