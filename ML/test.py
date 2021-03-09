stringLabel = ["Haus", "Auto", "Hund", "Geld", "Baum"]
allStrings = [4,2,3,1,0,0,2,1,0,4,2,2,3,4,0,1]

counts = []
for i in range(len(stringLabel)):
    counts.append(0)

for i in allStrings:
    counts[i] = counts[i] + 1
print(counts)

import matplotlib.pyplot as plt
import numpy as np

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

print(ylabels)

# plt.yticks(ylocs, list(range(max(counts)+1)))
# print(list(range(max(counts)+1)))



plt.savefig(r"C:\Users\johan\Desktop\fig.png")

