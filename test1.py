import pandas as pd 
import os

path = r"Z:\2020-JG18-T31Bewegungsanalyse-Pelz-Kroener\05-Messfahrten_Daten\Python Tests\temp_sensor.csv"
path1= r"Z:\2020-JG18-T31Bewegungsanalyse-Pelz-Kroener\05-Messfahrten_Daten\Python Tests\1609251975022_Car_Conventional_SENSOR.csv"

path = r"Z:\2020-JG18-T31Bewegungsanalyse-Pelz-Kroener\05-Messfahrten_Daten\Sensor Datenrate"

for folder in os.listdir(path):
    csvpath = path + "/" + folder
    for csvdata in os.listdir(csvpath):
        if "GPS" in csvdata:
            None
        else:
            csv = pd.read_csv(csvpath, sep = ",")
            


csv = pd.read_csv(path1, sep= ",")
lists = []
for i in range(1,len(csv)):
    a = (csv["Time_in_ns"][i] - csv["Time_in_ns"][i-1])
    lists.append(a/1000000)

print(sum(lists)/len(lists))


