import matplotlib.pyplot as plt
import numpy as np

import sys, shutil, os
sys.path.insert(0,'..')
import triplog_constants as C

def dataDistribution(stringLabel, allLabels):
    counts = []
    for i in range(len(stringLabel)):
        counts.append(0)
        
    for i in allLabels:
        counts[i] = counts[i] + 1
    print(counts)
    
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


if(__name__ == "__main__"):
    pass