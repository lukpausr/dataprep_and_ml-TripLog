import os
import gpxpy
from gpx_csv_converter import Converter
import calculate
import pandas as pd

path = r"Z:\2020-JG18-T31Bewegungsanalyse-Pelz-Kroener\05-Messfahrten_Daten\FirebaseStorageTripData\trips\\"


def gpx_import(path):
    if (path[:-3]+"csv") in os.listdir(path):
        csv_import(path[:-3]+"csv")
    else:
        Converter(input_file=path, output_file= (path[:-3] + "csv"))
        gpx_to_csv(path[:-3] + "csv")

def csv_import(path):
    csv = pd.read_csv(path, sep = ",")
    ml_csv = calculate.ml_csv(csv)
    return(ml_csv)

def data_import():
    
    for data in os.listdir(path):

        if data[-3:] == "csv":
           dataFrame = csv_import((path[:-1]+data))

           try:
               ml_csv = pd.concat([ml_csv, dataFrame])
           except:
               ml_csv = dataFrame
    
        elif data[-3:] == "gpx":
           print("gpx")
           #dataFrame = gpx_import(path[:-1]+data)
        
        else:
            a = 1
           #print("Invalid data format.")

        #return(dataFrame)
    print(ml_csv) 




data_import()