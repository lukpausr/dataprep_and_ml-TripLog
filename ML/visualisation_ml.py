import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics

import sys, shutil, os
sys.path.insert(0,'..')
import triplog_constants as C

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
    print("Accuracy:", metrics.accuracy_score(Y_test, Y_prediction))
    print('------------------------------------------------')
    
    # metrics.plot_confusion_matrix(clf, X_test, Y_test)  
    # plt.show()  
    
    titles_options = [("Confusion matrix, without normalization", None),
                  ("Normalized confusion matrix", 'true')]
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