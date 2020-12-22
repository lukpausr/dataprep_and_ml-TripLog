import os
import pandas as pd
import numpy as np

path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/FirebaseStorageTripData/trips/"

dataFrame = pd.DataFrame([np.nan]) #, columns=["a", "b", "c"])
dataFrame = pd.DataFrame(columns=["a", "b", "c", "d", "e"])
print(dataFrame)

