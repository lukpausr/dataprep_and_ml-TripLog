# =============================================================================
# db_network_extractor
# Find all GPS Points in XML Data from Deutsche Bahn AG
#
# Result: Excel file with all GPS Points of DB Infrastructure 
# (around 1.000.000 GPS points)
# =============================================================================

import xml.etree.ElementTree as ET
import pandas as pd

###############################################################################
### Load XML-Tree with ElementTree library
### efficiant data handling only possible with python, file is too big
### to open in notepad editor
###############################################################################
parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse(
    #"Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/06-Datenaufbereitung/DB-Netz_INSPIRE_20200217.xml",
    "B:\Downloads\DB_Inspire_XML_2019\DB-Netz_INSPIRE_20200217.xml",
    parser=parser)

root = tree.getroot()

###############################################################################
### Element list for visualisation of different xml layers
###############################################################################
elements_j = []
elements_k = []
elements_l = []
elements_m = []

###############################################################################
### Position list for saving position elements of xml file
###############################################################################
posList = []
pos = []

###############################################################################
### Iterate through all elements in xml file and collect text of elements with
### posList or pos in tag
###############################################################################
for elem in root:
    print(elem.attrib)
    for subelem in elem:
        for i in subelem:
            for j in i:
                elements_j.append(j.tag)
                for k in j:
                    elements_k.append(k.tag)
                    for l in k:
                        elements_l.append(l.tag)
                        for m in l:
                            elements_m.append(m.tag)
                            if("posList" in m.tag):
                                posList.append(m.text)
                            if("pos" in m.tag):
                                pos.append(m.text)

###############################################################################
### Extract positions of position lists and append them to gps location lists
### This is required because element text gps points are given in weird shapes
###############################################################################                        
gpsLocations = []
gpsLocLists = []

for p in pos:
    split = p.split()
    if(len(split) == 2):
        gpsLocations.append(split)
    else:
        gpsLocLists.append(split)
       
for p in posList:
    split = p.split()
    gpsLocLists.append(split)

for p in gpsLocLists:
    for i in range(0, len(p), 2):
        pos=[p[i], p[i+1]]
        gpsLocations.append(pos)
 
###############################################################################
### Write each gps point to a row in a pandas DataFrame and save to excel
### for later use. This script needs to be executed just once
###############################################################################
df = pd.DataFrame(gpsLocations, columns=['Latitude', 'Longitude'])
df.to_excel('DB_Infrastructure.xlsx', index=False)