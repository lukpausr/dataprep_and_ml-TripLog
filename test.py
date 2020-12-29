import os
import pandas as pd
import numpy as np

path = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/Python Tests/1609198295601_Car_Conventional_SENSOR.csv"
savepath = "Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/05-Messfahrten_Daten/Python Tests/1609198295601_Car_Conventional_SENSORtest.csv"

csv = pd.read_csv(path, sep = ",")

times0 = list(csv["Time_in_ns"])
times1 = list(csv["Time_in_ns.1"])
times2 = list(csv["Time_in_ns.2"])

begin0 = times0[0]
begin1 = times1[0]
begin2 = times2[0]

for i in range(len(times0)):
    times0[i] = times0[i] - begin0
    times1[i] = times1[i] - begin1
    times2[i] = times2[i] - begin2

csv["Time_in_ns"] = times0
csv["Time_in_ns.1"] = times1
csv["Time_in_ns.2"] = times2


csv.to_csv(savepath, index = None, compression = "infer")
