import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics

import tikzplotlib

import sys, shutil, os
sys.path.insert(0,'..')
import triplog_constants as C

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
        
        stringLabelsWithoutSpaces = []
        for i in range(0, len(stringLabels)):
            stringLabelsWithoutSpaces.append(stringLabels[i].replace("_", " "))
            
        
        plt.xticks(range(1, len(stringLabels)+1), stringLabelsWithoutSpaces)
        plt.xticks(rotation=90)
        plt.title(feature)
        tikzplotlib.save("C:/Users/Lukas/Desktop/Studienarbeit/T3200/images/boxplots/" + feature + ".tex")
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