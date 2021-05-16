import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
import asyncio

import tikzplotlib
import folium
from branca.element import Template, MacroElement
import sklearn.metrics as Metrics

import sys, shutil, os
sys.path.insert(0,'..')

import triplog_constants as C
import data_import as DI
import calculate as cal

# =============================================================================
# getColors
# Determine fft_frequency feature for euclidian data
#
# Parameter:
#   stringLabel - Label in form of Strings (not numerical labels)
#
# Returns:
#   color - color relating to the given label
# =============================================================================
def getColors(stringLabel):
    if(C.COMPRESS_LABELS == False):
        for j in range(0, len(C.CLEAN_COLORS)):
            if(C.CLEAN_COLORS[j][0] in stringLabel):
                return C.CLEAN_COLORS[j][1]
    else:
        for j in range(0, len(C.CLEAN_SHORT_COLORS)):
            if(C.CLEAN_SHORT_COLORS[j][0] in stringLabel):
                return C.CLEAN_SHORT_COLORS[j][1]
   
# =============================================================================
# getFoliumLegend
# Create draggable legend for means of transportation and corresponding colors
# See: https://nbviewer.jupyter.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd
#
# Parameter:
#   -
#
# Returns:
#   macro - being used by folium to be added as legend to the map
# =============================================================================
def getFoliumLegend():
    template = ""
    if(C.COMPRESS_LABELS == False):
        template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:28px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legende: Fortbewegungsmittel</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>Auto</li>
    <li><span style='background:lightred;opacity:0.7;'></span>Hybridauto</li>
    <li><span style='background:pink;opacity:0.7;'></span>Elektroauto</li>
    <li><span style='background:yellow;opacity:0.7;'></span>Gehen</li>
    <li><span style='background:blue;opacity:0.7;'></span>S-Bahn</li>
    <li><span style='background:lightblue;opacity:0.7;'></span>U-Bahn</li>
    <li><span style='background:green;opacity:0.7;'></span>Fahrrad</li>
    <li><span style='background:lightgreen;opacity:0.7;'></span>e-Bike</li>
    <li><span style='background:orange;opacity:0.7;'></span>Bus</li>
  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 36px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 32px;
    width: 60px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""
    else:
        template = """
{% macro html(this, kwargs) %}

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>jQuery UI Draggable - Default functionality</title>
  <link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css">

  <script src="https://code.jquery.com/jquery-1.12.4.js"></script>
  <script src="https://code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
  
  <script>
  $( function() {
    $( "#maplegend" ).draggable({
                    start: function (event, ui) {
                        $(this).css({
                            right: "auto",
                            top: "auto",
                            bottom: "auto"
                        });
                    }
                });
});

  </script>
</head>
<body>

 
<div id='maplegend' class='maplegend' 
    style='position: absolute; z-index:9999; border:2px solid grey; background-color:rgba(255, 255, 255, 0.8);
     border-radius:6px; padding: 10px; font-size:28px; right: 20px; bottom: 20px;'>
     
<div class='legend-title'>Legende: Fortbewegungsmittel</div>
<div class='legend-scale'>
  <ul class='legend-labels'>
    <li><span style='background:red;opacity:0.7;'></span>Auto</li>
    <li><span style='background:yellow;opacity:0.7;'></span>Fuß</li>
    <li><span style='background:blue;opacity:0.7;'></span>Zug</li>
    <li><span style='background:green;opacity:0.7;'></span>Fahrrad</li>
    <li><span style='background:orange;opacity:0.7;'></span>Bus</li>
  </ul>
</div>
</div>
 
</body>
</html>

<style type='text/css'>
  .maplegend .legend-title {
    text-align: left;
    margin-bottom: 5px;
    font-weight: bold;
    font-size: 90%;
    }
  .maplegend .legend-scale ul {
    margin: 0;
    margin-bottom: 5px;
    padding: 0;
    float: left;
    list-style: none;
    }
  .maplegend .legend-scale ul li {
    font-size: 80%;
    list-style: none;
    margin-left: 0;
    line-height: 36px;
    margin-bottom: 2px;
    }
  .maplegend ul.legend-labels li span {
    display: block;
    float: left;
    height: 32px;
    width: 60px;
    margin-right: 5px;
    margin-left: 0;
    border: 1px solid #999;
    }
  .maplegend .legend-source {
    font-size: 80%;
    color: #777;
    clear: both;
    }
  .maplegend a {
    color: #777;
    }
</style>
{% endmacro %}"""
    macro = MacroElement()
    macro._template = Template(template)
    return macro

# =============================================================================
# showReferenceMap
# Show reference trip on a map, labels are being set manually, although a
# little bit of trial and error makes sense to get everything on the right
# place
#
# Parameter:
#   gps_offline_test_path - Path of GPS-Data which will be printed on the map
#   filename - default: "reference", determines the final name of the *.html
#              file which is being created
#
# Returns:
#   - (a *.html file with a map will be saved in the same folder)
# =============================================================================
async def showReferenceMap(gps_offline_test_path, filename="reference"):
    df = await DI.raw_gps_interpolation(gps_offline_test_path)
    tooltipList = [None] * len(df['Latitude'])
    colorList = [None] * len(df['Latitude'])
    
    
    ###############################################################################
    ### Set labels to reference trip
    ###############################################################################
    
    referenceLabels = [0] * 6769
    referenceLabels[0:195] = ['Auto'] * (195+1)
    referenceLabels[196:367] = ['Fuß'] * (367-195)
    referenceLabels[368:1832] = ['Zug'] * (1832-367)
    referenceLabels[1833:2108] = ['Fuß'] * (2108-1832)
    referenceLabels[2109:2360] = ['Zug'] * (2360-2108)
    referenceLabels[2361:4118] = ['Fuß'] * (4118-2360)
    referenceLabels[4119:4635] = ['Bus'] * (4635-4118)
    referenceLabels[4636:5022] = ['Fuß'] * (5022-4635)
    referenceLabels[5023:6500] = ['Bus'] * (6500-5022)
    referenceLabels[6501:6777] = ['Fuß'] * (6777-6500)
    
    for i in range(0, len(df['Latitude'])):
        tooltipList[i] = str(i)
        colorList[i] = getColors(referenceLabels[i])
       
        
    ###############################################################################
    ### Create a folium map and add gps points
    ###############################################################################        
       
    m = folium.Map()
    m.fit_bounds(
        [
            [df['Latitude'].min(), df['Longitude'].min()],
            [df['Latitude'].max(), df['Longitude'].max()],
        ]
    )
    
    locations = df[['Latitude', 'Longitude']]
    locationlist = locations.values.tolist()
    

    for i in range(0, len(locationlist)):
        folium.CircleMarker(
            location=locationlist[i], 
            tooltip=referenceLabels[i], 
            radius=2,
            weight=3, 
            color=colorList[i] # getColors(referenceLabels[i]),
        ).add_to(m)
    m.get_root().add_child(getFoliumLegend())   
    m.save(filename + ".html")  

# =============================================================================
# showPredictionOnMap
# Show predicted trip on a map, code similar to showReferenceMap
#
# Parameter:
#   gps_offline_test_path - Path of GPS-Data which will be printed on the map
#   predictions - predicted means of transportation by selected ML model
#   stringLabels - labels in string representation (set()-like)
#
# Returns:
#   - (a *.html file with a map will be saved in the same folder)
# =============================================================================    
async def showPredictionOnMap(gps_offline_test_path, predictions, stringLabels, filename="map"):
    
    df = await DI.raw_gps_interpolation(gps_offline_test_path)
    
    stringLabels = beautifyStringLabels(stringLabels)
    
    tooltipList = [None] * len(df['Latitude'])
    colorList = [None] * len(df['Latitude'])
    
    ###########################################################################
    ### find corresponding string labels and colors to predictions
    ###########################################################################                        
    for i in range(0, predictions.size):
        n = predictions[i]
        for j in range(i*30, i*30+59):
            tooltipList[j] = stringLabels[n]
            colorList[j] = getColors(stringLabels[n])
    
    m = folium.Map()
    m.fit_bounds(
        [
            [df['Latitude'].min(), df['Longitude'].min()],
            [df['Latitude'].max(), df['Longitude'].max()],
        ]
    )
    
    locations = df[['Latitude', 'Longitude']]
    locationlist = locations.values.tolist()
    
    for i in range(0, len(locationlist)):
        folium.CircleMarker(
            location=locationlist[i], 
            tooltip=tooltipList[i], 
            radius=2,
            weight=3, 
            color=colorList[i],
        ).add_to(m)
    
    m.get_root().add_child(getFoliumLegend())    
    m.save(filename + ".html")   
    
    getDifferenceMap(tooltipList, locationlist, df, filename)

# =============================================================================
# getDifferenceMap
# Compare reference map to predicted map and show differences
#
# Parameter:
#   tooltipList - list of predicted tooltips
#   locationlist - list of gps-locations
#   df - interpolated gps track
#   filename - name of the created *.html file
#
# Returns:
#   - (a *.html file with a map will be saved in the same folder)
# =============================================================================  
def getDifferenceMap(tooltipList, locationlist, df, filename):
    m = folium.Map()
    m.fit_bounds(
        [
            [df['Latitude'].min(), df['Longitude'].min()],
            [df['Latitude'].max(), df['Longitude'].max()],
        ]
    )
    
    locations = df[['Latitude', 'Longitude']]
    locationlist = locations.values.tolist()
    
    referenceLabels = [0] * 6769
    referenceLabels[0:195] = ['Auto'] * (195+1)
    referenceLabels[196:367] = ['Fuß'] * (367-195)
    referenceLabels[368:1832] = ['Zug'] * (1832-367)
    referenceLabels[1833:2108] = ['Fuß'] * (2108-1832)
    referenceLabels[2109:2360] = ['Zug'] * (2360-2108)
    referenceLabels[2361:4118] = ['Fuß'] * (4118-2360)
    referenceLabels[4119:4635] = ['Bus'] * (4635-4118)
    referenceLabels[4636:5022] = ['Fuß'] * (5022-4635)
    referenceLabels[5023:6500] = ['Bus'] * (6500-5022)
    referenceLabels[6501:6777] = ['Fuß'] * (6777-6500)
    tooltipList[-20:] = ['Fuß'] * 20    
        
    ###########################################################################
    ### compare reference labels to labels saved in predicted tooltipList
    ### red marker - not equal, green marker - equal
    ###########################################################################     
    for i in range(0, len(locationlist)):
        if(tooltipList[i] in referenceLabels[i]):
            folium.CircleMarker(
                location=locationlist[i], 
                tooltip=tooltipList[i], 
                radius=2,
                weight=3, 
                color='green',
            ).add_to(m)
        else:
            folium.CircleMarker(
                location=locationlist[i], 
                tooltip=tooltipList[i], 
                radius=2,
                weight=3, 
                color='red',
            ).add_to(m)
            
    m.get_root().add_child(getFoliumLegend())    
    m.save(filename + "Differences.html")   

# =============================================================================
# beautifyStringLabels
# Does exactly what the name says
#
# Parameter:
#   stringLabels - list of labels in string representation
#
# Returns:
#   labels - return beautified string labels (defined in triplog_constants.py)
# =============================================================================  
def beautifyStringLabels(stringLabels):
    labels = []
    for i in range(0, len(stringLabels)):
        if(C.COMPRESS_LABELS == False):
            for j in range(0, len(C.CLEAN_LABELS)):
                if(C.CLEAN_LABELS[j][0] in stringLabels[i]):
                    labels.append(stringLabels[i].replace(C.CLEAN_LABELS[j][0], C.CLEAN_LABELS[j][1]))
        else:
            for j in range(0, len(C.CLEAN_SHORT_LABELS)):
                if(C.CLEAN_SHORT_LABELS[j][0] in stringLabels[i]):
                    labels.append(stringLabels[i].replace(C.CLEAN_SHORT_LABELS[j][0], C.CLEAN_SHORT_LABELS[j][1]))
    return labels

# =============================================================================
# beautifyBoxplotTitles
# Does exactly what the name says
#
# Parameter:
#   feature - feature which is going to be used for the creation of a boxplot
#
# Returns:
#   label - boxplot title as string
# ============================================================================= 
def beautifyBoxplotTitles(feature):
    for j in range(0, len(C.CLEAN_UNITS)):
        if feature in C.CLEAN_UNITS[j][0]:
            label = C.CLEAN_UNITS[j][0] + " in " + C.CLEAN_UNITS[j][1]       
    return label

# =============================================================================
# boxplotByFeature
# Creates a boxplot for each feature for every type of transportation and saves
# it as pgf/tikz in the defined folder
#
# Parameter:
#   df - DataFrame of features
#   stringLabels - Label for each type of transportation as string 
#   features - default: C.HYBRID_SELECTED_FEATURES - used features
#
# Returns:
#   -
# ============================================================================= 
def boxplotByFeature(df, stringLabels, features=C.HYBRID_SELECTED_FEATURES):
    for feature in features:
        df_label = []
        df_features = []
        for i in range(0, len(stringLabels)):
            df_label.append(df.loc[df["numeric"] == i])
            df_features.append(df_label[i][feature])
        
        fig = plt.figure(figsize =(20, 10)) 
  
        # Creating axes instance 
        ax = fig.add_axes([0, 0, 1, 1]) 
        # Creating plot 
        bp = ax.boxplot(df_features, showfliers=False)  
        # show plot 
        print(range(1, len(stringLabels)+1))
        
        beautifulLabels = beautifyStringLabels(stringLabels)
        beautifulTitles = beautifyBoxplotTitles(feature)
        
        plt.xticks(range(1, len(stringLabels)+1), beautifulLabels)
        plt.xticks(rotation=90)
        plt.title(beautifulTitles)
        tikzplotlib.save(
            "C:/Users/Lukas/Desktop/Studienarbeit/T3200/images/boxplots/" + feature + ".tex",
            axis_width = "12cm",
            axis_height = "8cm",
            textsize = 10.0,
            flavor = "latex"
        )
        plt.show() 

# =============================================================================
# dataDistribution
# Create a plot which shows the distribution of the data
#
# Parameter:
#   stringLabels - Label for each type of transportation as string 
#   allLabels - list of all Labels
#
# Returns:
#   -
# ============================================================================= 
def dataDistribution(stringLabel, allLabels):
    counts = []
    for i in range(len(stringLabel)):
        counts.append(0)
        
    for i in allLabels:
        counts[i] = counts[i] + 1
    
    plt.figure(figsize=(20,10))
    plt.bar(list(range(len(stringLabel))), counts)
    plt.title("Verkehrsmittelverteilung", fontdict= {"fontsize": 20, "fontweight": "bold"})
    plt.axis()
    plt.xlabel("Verkehrsmittel", fontdict= {"fontsize": "x-large"})
    plt.ylabel("Anzahl Datens{\"a}tze", fontdict= {"fontsize": "x-large"})
    xlocs, xlabels = plt.xticks()

    beautifulLabels = beautifyStringLabels(stringLabel)
    newXticks = list(range(len(beautifulLabels)))
    newXlabels = beautifulLabels
    plt.xticks(newXticks, newXlabels)
    plt.xticks(rotation=60)
    plt.ylim(0, 3600)

    plt.show()

# =============================================================================
# confusionMatrix
# Create a confusion Matrix of a given classifier (normalized and without 
# normalization)
#
# Parameter:
#   clf - ML prediction model
#   X_test - test data(features)
#   Y_test - test data(labels)
#   stringLabels - Label for each type of transportation as string 
#
# Returns:
#   -
# ============================================================================= 
def confusionMatrix(clf, X_test, Y_test, stringLabels):
    
    Y_prediction = clf.predict(X_test)
    
    print("Classifier: ",type(clf))
    print("Accuracy on Test-Dataset:", metrics.accuracy_score(Y_test, Y_prediction))
    print("Balanced Accuracy on Test-Dataset: ", Metrics.balanced_accuracy_score(Y_test, Y_prediction))
    print('------------------------------------------------')
    
    beautifulLabels = beautifyStringLabels(stringLabels)
    beautifulTitle = 0
    if("MLP" in str(type(clf))):
        beautifulTitle = "ANN"
    if("Random" in str(type(clf))):
        beautifulTitle = "RF"
    if("Decision" in str(type(clf))):
        beautifulTitle = "DT"
    
    titles_options = [("Confusion Matrix Without Normalisation", None),
                  ("Confusion Matrix, Normalisiert", 'true')]
    for title, normalize in titles_options:
            fig, ax = plt.subplots(figsize=(15, 15))
            plt.rcParams.update({'font.size':20})
            disp = metrics.plot_confusion_matrix(clf, X_test, Y_test,
                                         display_labels=beautifulLabels,
                                         cmap=plt.cm.Blues,
                                         normalize=normalize, 
                                         ax=ax,
                                         colorbar=False,
                                         xticks_rotation=45)
            disp.ax_.set_title(title)
            plt.show()
                        
if(__name__ == "__main__"):
    pass