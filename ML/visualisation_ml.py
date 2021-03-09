import matplotlib.pyplot as plt
import numpy as np

def dataDistribution(stringLabel, allLabels):
    counts = []
    for i in range(len(stringLabel)):
        counts.append(0)
    
    plt.bar(list(range(len(stringLabel))), counts)
    plt.title("Verkehrsmittelverteilung", fontdict= {"fontsize": 20, "fontweight": "bold"})
    plt.axis()
    plt.xlabel("Verkehrsmittel", fontdict= {"fontsize": "x-large"})
    plt.ylabel("Anzahl Datensätze", fontdict= {"fontsize": "x-large"})
    xlocs, xlabels = plt.xticks()

    newXticks = list(range(len(stringLabel)))
    newXlabels = stringLabel
    plt.xticks(newXticks, newXlabels)

    ylocs, ylabels = plt.yticks()
    newYticks = list(range(max(counts)+1))
    newYlabels = list(range(max(counts)+1))
    plt.yticks(newYticks, newYlabels)

    plt.savefig(r"C:\Users\johan\Desktop\fig.png")

for i in allStrings:
    counts[i] = counts[i] + 1
print(counts)

if(__name__ == "__main__"):
    pass