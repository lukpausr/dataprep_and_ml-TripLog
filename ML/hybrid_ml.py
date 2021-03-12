# =============================================================================
# CONDA ENVIRONMENT
# 
# =============================================================================
#print(__name__)
#__file__ = r"C:\Studium\5.Semester\Studienarbeit\dataprep_TripLog\ML\hybrid_ml.py"
import sys, shutil, os
sys.path.insert(0,'..')

# print(os.path.abspath("."))
#import dataprep_triplog.triplog_constants as C
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
    if(C.COMPRESS_LABELS):
        labels.update(hydrid_segments['Label'])
    else:
        labels.update(hydrid_segments['Label'] + "_" + hydrid_segments['Sublabel'])  
    return list(labels)

def convertLabeltoInt(labelList, stringLabels):
    # https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
    if(C.COMPRESS_LABELS):
        labelList = list(labelList['Label'])
    else:
        labelList = list(labelList['Label'] + "_" + labelList['Sublabel'])
        
    for i in range(len(labelList)):
        index = stringLabels.index(labelList[i])
        labelList[i] = int(index)
    return np.array(labelList)

def countLabels(labelList, stringLabels):
    number_of_elements = []
    for i in range(len(stringLabels)):
        number_of_elements.append(0)
    for i in labelList:
        number_of_elements[i] = number_of_elements[i] + 1
    return number_of_elements;

def removeUntilEqual(df, hybrid_segment_labels_numeric):
    df['numeric'] = hybrid_segment_labels_numeric
    count = df['numeric'].value_counts()
    min_number_of_elements = count.min()    
    # print("Number of Elements\n",count, "\nMin. Number: ",min_number_of_elements)        
    df = df.groupby('numeric').apply(lambda s: s.sample(min_number_of_elements))
    return df

def cleanData(df):
    print("Anzahl der Daten vor Data-Cleaning:", len(df))
    df.drop(
        df[df['tow'] > 0.5 * C.SECONDS_SENSOR_SEGMENT].index,
        inplace=True
    )
    print("Anzahl der Daten nach Data-Cleaning:", len(df))
    print('------------------------------------------------')
    return df

def standardize(df):
    df[C.HYBRID_SELECTED_FEATURES] = (
        (df[C.HYBRID_SELECTED_FEATURES] - 
         df[C.HYBRID_SELECTED_FEATURES].mean()) /
         df[C.HYBRID_SELECTED_FEATURES].std()
    )
    return df
    
def normalize(df):
    df[C.HYBRID_SELECTED_FEATURES] = (
        (df[C.HYBRID_SELECTED_FEATURES] -
         df[C.HYBRID_SELECTED_FEATURES].min()) /
        (df[C.HYBRID_SELECTED_FEATURES].max() -
         df[C.HYBRID_SELECTED_FEATURES].min())
    )
    return df


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
    hybrid_segments = pd.read_csv(C.FUSED_DATA_CSV)
    
    # Remove unusable Data
    hybrid_segments = cleanData(hybrid_segments)
    
    # Shuffle CSV
    hybrid_segments = hybrid_segments.sample(frac=1).reset_index(drop=True)
    
    # Calculate numeric labels
    stringLabels = getAvailableLabels(hybrid_segments)
    print("Available Labels:\n" + str(stringLabels))
    print('------------------------------------------------')
    
    # Remove Segments until each Label-Type has the same number of elements
    # Shuffle again because we just sorted the dataframe ._.
    # Shuffleing beforehand is needed because we don't want the first e.g. 300
    # Segments of the same trip
    hybrid_segment_labels_numeric = convertLabeltoInt(
        hybrid_segments[C.HYBRID_SELECTED_LABELS], 
        stringLabels
    )
    number_of_elements = countLabels(hybrid_segment_labels_numeric, stringLabels)
    hybrid_segments = removeUntilEqual(hybrid_segments, hybrid_segment_labels_numeric)
    hybrid_segments = hybrid_segments.sample(frac=1).reset_index(drop=True)
    
    if(C.NORMALIZE_ELSE_STANDARDIZE):
        hybrid_segments = normalize(hybrid_segments)
    else:
        hybrid_segments = standardize(hybrid_segments)
    
    
    # Split file into Train- and Test-Data
    train, test = train_test_split(hybrid_segments, test_size=0.2)
    print("Trainings- und Testdatenset:", len(train), len(test))
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
    


    
    vis.dataDistribution(stringLabels, Y_train)
    
    # Machine Learning
    dt(X_train, Y_train, X_test, Y_test, stringLabels)
    
    
    
    
    
    
    
    
    
    