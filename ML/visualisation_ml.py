import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import metrics
import asyncio

import tikzplotlib
import folium

import sys, shutil, os
sys.path.insert(0,'..')

import triplog_constants as C
import data_import as DI
import calculate as cal


async def showPredictionOnMap(gps_offline_test_path):
    
    df = await DI.raw_gps_interpolation(gps_offline_test_path)
    features = cal.ml_csv(df, printReq=True)
    
    print(df.head(20))
    
    m = folium.Map(location=[45.5236, -122.6750])
    m.fit_bounds(
        [
            [df['Latitude'].min(), df['Longitude'].min()],
            [df['Latitude'].max(), df['Longitude'].max()],
        ]
    )
    
    locations = df[['Latitude', 'Longitude']]
    locationlist = locations.values.tolist()
    
    print(locations)
    
    folium.PolyLine(locationlist, weight=5, color='blue').add_to(m)
    
    m.save("map.html")

    
    return




def beautifyStringLabels(stringLabels):
    labels = []
    for i in range(0, len(stringLabels)):
        for j in range(0, len(C.CLEAN_LABELS)):
            if(C.CLEAN_LABELS[j][0] in stringLabels[i]):
                labels.append(stringLabels[i].replace(C.CLEAN_LABELS[j][0], C.CLEAN_LABELS[j][1]))
    print(labels)        
    return labels

def beautifyBoxplotTitles(feature):
    for j in range(0, len(C.CLEAN_UNITS)):
        if feature in C.CLEAN_UNITS[j][0]:
            label = C.CLEAN_UNITS[j][0] + " in " + C.CLEAN_UNITS[j][1]
    print(label)        
    return label

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


      
    # df0 = df.loc[df["numeric"] == 0]
    # data_1 = df0[features[0]]
    # data_2 = np.random.normal(90, 20, 200) 
    # data_3 = np.random.normal(80, 30, 200) 
    # data_4 = np.random.normal(70, 40, 200) 
    # data = [data_1, data_2, data_3, data_4] 
      
    # fig = plt.figure(figsize =(10, 7)) 
      
    # # Creating axes instance 
    # ax = fig.add_axes([0, 0, 1, 1]) 
      
    # # Creating plot 
    # bp = ax.boxplot(data) 
      
    # # show plot 
    # plt.show() 



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
    plt.ylabel("Anzahl Datensätze", fontdict= {"fontsize": "x-large"})
    xlocs, xlabels = plt.xticks()

    newXticks = list(range(len(stringLabel)))
    newXlabels = stringLabel
    plt.xticks(newXticks, newXlabels)
    
    #plt.savefig(C.SENSOR_DATA_SEGMENT_FOLDER + "fig.png")
    plt.show()

def confusionMatrix(clf, X_test, Y_test, stringLabels):
    # plt.figure(figsize=(50,10))  # set plot size (denoted in inches)
    # tree.plot_tree(clf, fontsize=10)
    # plt.savefig("C:/Users/Lukas/Desktop/dt.png", dpi=400)
    
    Y_prediction = clf.predict(X_test)
    
    print("Classifier: ",type(clf))
    print("Accuracy on Test-Dataset:", metrics.accuracy_score(Y_test, Y_prediction))
    print('------------------------------------------------')
    
    # metrics.plot_confusion_matrix(clf, X_test, Y_test)  
    # plt.show()  
    
    titles_options = [("Confusion matrix, without normalization: " + str(type(clf)), None),
                  ("Normalized confusion matrix: " + str(type(clf)), 'true')]
    for title, normalize in titles_options:
            fig, ax = plt.subplots(figsize=(60, 15))
            disp = metrics.plot_confusion_matrix(clf, X_test, Y_test,
                                         display_labels=stringLabels,
                                         cmap=plt.cm.Blues,
                                         normalize=normalize, ax=ax)
            disp.ax_.set_title(title)
            plt.show()

if(__name__ == "__main__"):
    pass