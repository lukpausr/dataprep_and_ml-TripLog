import os
import pandas as pd 
import calculate
import numpy as np 

path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/FirebaseStorageTripData/trips/"

def gpx_to_csv():
    a = 1

def gpx_import(path):
    a = 1
    #if (path[:-3]+"csv") in os.listdir(path):
    #    csv_import(path[:-3]+"csv")
    #else:
        #Converter(input_file=path, output_file= (path[:-3] + "csv"))
    #    gpx_to_csv(path[:-3] + "csv")

def csv_import(path):        
    csv = pd.read_csv(path, sep = ",")    
    ml_csv = calculate.ml_csv(csv)    
    return(ml_csv)
    

def data_import():

    for files in os.listdir(path):
        for data in os.listdir(path + files + "/"):
            #Labels extrahieren
            split = data.split(".")
            split = split[0].split("_")
            split = split[1:]

            if data[-3:] == "csv":
                #DataFrame einstellen
                try:
                    dataFrame = csv_import(path+files+"/"+data)
                except: 
                    print("INVALID DATA: " +path+files+"/"+data)
                    dataFrame = pd.DataFrame(columns=["Average speed", "Maximum speed", "Average speed without waiting","Minimum acceleration", "Maximum acceleration", "Duration", "Distance"])

                #Labels einfügen
                dataFrame["label"] = None
                dataFrame["sublabel"] = None
                dataFrame["subsublabel"] = None
                try: 
                    dataFrame["label"] = split[0]
                    dataFrame["sublabel"] = split[1]
                    dataFrame["subsublabel"] = split[2]
                except:
                    None

                #ML-CSV erstellen
                try:               
                    ml_csv = pd.concat([ml_csv, dataFrame])
                except:
                    ml_csv = dataFrame
    

            elif data[-3:] == "gpx":
                a = 1
                #dataFrame = gpx_import(path[:-1]+data)
        
            else:
                a = 1
                print("Invalid data format:" + data[-3:])

        #return(dataFrame)
    print(ml_csv) 
    #ml_csv.to_csv(path + "ml_csv.csv")


data_import()