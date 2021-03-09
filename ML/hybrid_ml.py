# =============================================================================
# CONDA ENVIRONMENT
# 
# =============================================================================

import sys, shutil, os
sys.path.insert(0,'..')
import triplog_constants as C

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import tensorflow as tf
import keras

import visualisation_ml as vis

from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn import metrics

print('TensorFlow version: {}'.format(tf.__version__))
print('------------------------------------------------')

def getAvailableLabels(hydrid_segments): 
    labels = set()
    labels.update(hydrid_segments['Label'] + "_" + hydrid_segments['Sublabel'])   
    return list(labels)

def convertLabeltoInt(labelList, stringLabels):
    # https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
    labelList = list(labelList['Label'] + "_" + labelList['Sublabel'])
    for i in range(len(labelList)):
        index = stringLabels.index(labelList[i])
        labelList[i] = int(index)
    return np.array(labelList)

def dt(X_train, Y_train, X_test, Y_test, stringLabels):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X_train, Y_train)

    # plt.figure(figsize=(50,10))  # set plot size (denoted in inches)
    # tree.plot_tree(clf, fontsize=10)
    # plt.savefig("C:/Users/Lukas/Desktop/dt.png", dpi=400)
    
    Y_prediction = clf.predict(X_test)
    
    print("Accuracy:", metrics.accuracy_score(Y_test, Y_prediction))
    
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
    
    # Load CSV
    hydrid_segments = pd.read_csv(C.FUSED_DATA_CSV)
    
    # Shuffle CSV
    hydrid_segments = hydrid_segments.sample(frac=1).reset_index(drop=True)
    
    # Split file into Train- and Test-Data
    train, test = train_test_split(hydrid_segments, test_size=0.2)
    print("Trainings- und Testdatenset:", len(train), len(test))
    print('------------------------------------------------')
    
    # Calculate numeric labels
    stringLabels = getAvailableLabels(hydrid_segments)
    print("Available Labels:\n" + str(stringLabels))
    print('------------------------------------------------')
    
    # Load Training Data
    X_train = np.array(train[C.HYBRID_SELECTED_FEATURES])
    Y_train = convertLabeltoInt(train[C.HYBRID_SELECTED_LABELS], stringLabels)
    print("Training Dataset X:\n", X_train.shape)
    print("Training Dataset Y:\n", Y_train.shape)
    print('------------------------------------------------')
    
    # Load Test Data
    X_test = np.array(test[C.HYBRID_SELECTED_FEATURES])
    Y_test = convertLabeltoInt(test[C.HYBRID_SELECTED_LABELS], stringLabels)
    print("Test Dataset X:\n", X_test.shape)
    print("Test Dataset Y:\n", Y_test.shape)
    print('------------------------------------------------')
    
    # Überprüfen der Daten
    # print(np.where(np.isnan(X_train)))
    # print(np.where(np.isnan(Y_train)))
    # print(np.where(np.isnan(X_test)))
    # print(np.where(np.isnan(Y_test)))
    
    # Casten to Float
    # np.nan_to_num(X_train)
    # np.nan_to_num(Y_train)
    # np.nan_to_num(X_test)
    # np.nan_to_num(Y_test)
    
    vis.dataDistribution(stringLabels, Y_train)
    
    # Machine Learning
    #dt(X_train, Y_train, X_test, Y_test, stringLabels)
    
    
    
    
    
    
    
    
    
    