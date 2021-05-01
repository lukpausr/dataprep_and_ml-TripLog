# -*- coding: utf-8 -*-
"""
Created on Fri Apr 30 17:27:17 2021

@author: Lukas
"""

import xml.etree.ElementTree as ET
parser = ET.XMLParser(encoding="utf-8")
tree = ET.parse(
    #"Z:/2020-JG18-T31Bewegungsanalyse-Pelz-Kroener/06-Datenaufbereitung/DB-Netz_INSPIRE_20200217.xml",
    "B:\Downloads\DB_Inspire_XML_2019\DB-Netz_INSPIRE_20200217.xml",
    parser=parser)

root = tree.getroot()

elements_j = []
elements_k = []
elements_l = []
elements_m = []

posList = []
pos = []

for elem in root:
    print(elem.attrib)
    for subelem in elem:
        # Feature Collection
        # print(subelem.attrib)
        # print(subelem.tag)
        for i in subelem:
            # Member
            #print(i.tag)
            if("boundedBy" in i.tag):
                # print("bounds")
                pass
            if("member" in i.tag):
                # print("member")
                pass
            for j in i:
                elements_j.append(j.tag)
                # if("MarkerPost" in j.tag):
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
                        

set_j = set(elements_j)
for i in set_j:
    print(i)
    
print("#############################")

set_k = set(elements_k)
for i in set_k:
    print(i)
    
print("#############################")

set_l = set(elements_l)
for i in set_l:
    print(i)
    
print("#############################")

set_m = set(elements_m)
for i in set_m:
    print(i)
    
print("#############################")
print("#############################")
print("#############################")

# print(posList)
# print(pos)

import folium
from folium.plugins import FastMarkerCluster
import pandas as pd

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
    
#print(gpsLocLists)

for p in gpsLocLists:
    for i in range(0, len(p), 2):
        pos=[p[i], p[i+1]]
        gpsLocations.append(pos)
    


df = pd.DataFrame(gpsLocations, columns=['Latitude', 'Longitude'])

m = folium.Map()
m.fit_bounds(
    [
        [df['Latitude'].min(), df['Longitude'].min()],
        [df['Latitude'].max(), df['Longitude'].max()],
    ]
)

locations = df[['Latitude', 'Longitude']]
locationlist = locations.values.tolist()

tooltipList = [None] * len(df['Latitude'])
colorList = [None] * len(df['Latitude'])
       
for i in range(0, len(df)):
    tooltipList[i] = "p"
    colorList[i] = "blue"
    
# m.add_child(FastMarkerCluster(df[['Latitude', 'Longitude']].values.tolist()))

for i in range(0, len(locationlist)):
    folium.CircleMarker(
        location=locationlist[i], 
        #tooltip=tooltipList[i], 
        radius=1,
        weight=2, 
        color=colorList[i],
    ).add_to(m)

m.save("db.html")
