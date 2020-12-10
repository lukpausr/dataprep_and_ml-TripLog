import os
import gpxpy
from gpx_csv_converter import Converter
import calculate
import pandas as pd

path = r"Z:\2020-JG18-T31Bewegungsanalyse-Pelz-Kroener\05-Messfahrten_Daten\Messfahrt2.gpx"
path = r"C:\Studium\5.Semester\Studienarbeit\1608195983032_Car_Electric.csv"

def gpx_import(path):
    if (path[:-3]+"csv") in ordner:
        csv_import(path[:-3]+"csv")
    else:
        Converter(input_file=path, output_file= (path[:-3] + "csv"))
        gpx_to_csv(path[:-3] + "csv")

def csv_import(path):
    csv = pd.read_csv(path, sep = ",")
    ml_csv = calculate.ml_csv(csv)
    return(ml_csv)


