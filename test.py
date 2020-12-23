import os
import pandas as pd
import numpy as np

path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/FirebaseStorageTripData/trips/"

for files in os.listdir(path):

    for data in os.listdir(path + files + "/"):
        print(path + files + "/" + data)
        csv = pd.read_csv(path + files + "/" + data, sep = ",")    
    print (csv)
           