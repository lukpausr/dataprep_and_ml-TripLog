import os
import gpxpy


def find_path(name):
    
    path = os.path.abspath("..")

    for file in os.listdir(path):
        if "Mess" in file:
            path = path + "\\" + file

                
    path = path + "\\" + name
    return(path)

def import_data(path):

    gpx_file = open(path, 'r')
    gpx = gpxpy.parse(gpx_file)
    print(gpx.name)
    return(gpx)




path = r"Z:\2020-JG18-T31Bewegungsanalyse-Pelz-Kroener\05-Messfahrten_Daten\Messfahrt2.gpx"
gpx = import_data(path)




