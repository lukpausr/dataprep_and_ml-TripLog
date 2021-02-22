import matplotlib.pyplot as plt

def dataDistribution(stringLabel, allLabels):
    x_pos = [i for i, _ in enumerate(stringLabel)]
    
    y_pos = []
    for i in len(stringLabel):
        y_pos[i] = allLabels.count(stringLabel[i])
    
    plt.bar(x_pos, y_pos, color='green')
    plt.xlabel("Verkehrsmittel")
    plt.ylabel("Absolute Häufigkeit")
    plt.title("Absolute Häufigkeit von Verkehrsmitteln im Datensatz")
    plt.xticks(x_pos, stringLabel)
    plt.show()

if(__name__ == "__main__"):
    pass