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
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from mlxtend.feature_selection import SequentialFeatureSelector as SFS

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

def custom_train_test_split(df, hybrid_segment_labels_numeric):
    occurances = df['Sublabel'].value_counts()
    
    df['numeric'] = hybrid_segment_labels_numeric
    
    train = df
    test = pd.DataFrame()
    
    test_occurances = int(0.5 * min(occurances))
    print(test_occurances)
    
    test = df.groupby('numeric').apply(lambda s: s.sample(test_occurances))
    train[~train.index.isin(test.index)]
    
    print(test['Sublabel'].value_counts())
    print(train['Sublabel'].value_counts())
    
    return train, test

def cleanData(df):
    print("Anzahl der Daten vor Data-Cleaning:", len(df))
    df.drop(
        df[df['tow'] > 0.5 * C.SECONDS_SENSOR_SEGMENT].index,
        inplace=True
    )
    print("Anzahl der Daten nach Data-Cleaning:", len(df))
    print('------------------------------------------------')
    return df

def removeBySublabel(df, labeltype):
    df.drop(
        df[df['Sublabel'] == labeltype].index,
        inplace=True
    )
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

# sckit-learn Algorithms
def dt(X_train, Y_train, X_test, Y_test, stringLabels):
    clf = DecisionTreeClassifier()
    clf = clf.fit(X_train, Y_train)
    
    vis.confusionMatrix(clf, X_test, Y_test, stringLabels)
    
def rf(X_train, Y_train, X_test, Y_test, stringLabels):
    clf = RandomForestClassifier()
    clf = clf.fit(X_train, Y_train)
    
    vis.confusionMatrix(clf, X_test, Y_test, stringLabels)

def svc(X_train, Y_train, X_test, Y_test, stringLabels):
    clf = SVC()
    clf = clf.fit(X_train, Y_train)
    
    vis.confusionMatrix(clf, X_test, Y_test, stringLabels)
    
def knn(X_train, Y_train, X_test, Y_test, stringLabels):
    clf = KNeighborsClassifier(len(stringLabels))
    clf = clf.fit(X_train, Y_train)
    
    vis.confusionMatrix(clf, X_test, Y_test, stringLabels)

def nn(X_train, Y_train, X_test, Y_test, stringLabels):
    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(30, 2), random_state=1, max_iter=10000)
    clf = clf.fit(X_train, Y_train)
    
    vis.confusionMatrix(clf, X_test, Y_test, stringLabels)

def generateDatasets():
    for i in range(0, 1):
    
        # Load CSV
        hybrid_segments = pd.read_csv(C.FUSED_DATA_CSV)
        
        # Remove unusable Data
        hybrid_segments = cleanData(hybrid_segments)
        hybrid_segments = removeBySublabel(hybrid_segments, "Running")
        
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
        
        
        # Normalize or Standardize
        if(C.NORMALIZE_ELSE_STANDARDIZE):
            hybrid_segments = normalize(hybrid_segments)
        else:
            hybrid_segments = standardize(hybrid_segments)
            
        original = hybrid_segments    
            
        # number_of_elements = countLabels(hybrid_segment_labels_numeric, stringLabels)
        hybrid_segments = removeUntilEqual(hybrid_segments, hybrid_segment_labels_numeric)
        
        hybrid_segments = hybrid_segments.sample(frac=1).reset_index(drop=True)
                    
        vis.dataDistribution(stringLabels, hybrid_segment_labels_numeric)
        
        
        hybrid_segment_labels_numeric = convertLabeltoInt(
            hybrid_segments[C.HYBRID_SELECTED_LABELS], 
            stringLabels
        )
        # Split file into Train- and Test-Data
        #train, test = custom_train_test_split(hybrid_segments, hybrid_segment_labels_numeric)
        
        train, test = train_test_split(hybrid_segments, test_size=0.5)
        original = original[~original.isin(test)].dropna()
        print("Trainings- und Testdatenset:", len(original), len(test))
        print('------------------------------------------------')
    
        original.to_csv(C.DATASET_FOLDER + "train_" + str(i) + ".csv")
        test.to_csv(C.DATASET_FOLDER + "test_" + str(i) + ".csv")
        
        
        train_numeric = convertLabeltoInt(
            original[C.HYBRID_SELECTED_LABELS], 
            stringLabels
        )
        test_numeric = convertLabeltoInt(
            test[C.HYBRID_SELECTED_LABELS], 
            stringLabels
        )
        vis.dataDistribution(stringLabels, train_numeric)
        vis.dataDistribution(stringLabels, test_numeric)
        
        

def loadDataset(i):
    train = pd.read_csv(C.DATASET_FOLDER + "train_" + str(i) + ".csv")
    test = pd.read_csv(C.DATASET_FOLDER + "test_" + str(i) + ".csv")    
    return train, test

if(__name__ == "__main__"):
    
    # Load CSV for String Labels
    hybrid_segments = pd.read_csv(C.FUSED_DATA_CSV) 
    # Remove unusable Data
    hybrid_segments = cleanData(hybrid_segments)   
    hybrid_segments = removeBySublabel(hybrid_segments, "Running")
    # Shuffle CSV
    hybrid_segments = hybrid_segments.sample(frac=1).reset_index(drop=True)    
    # Calculate numeric labels
    stringLabels = getAvailableLabels(hybrid_segments)
    hybrid_segment_labels_numeric = convertLabeltoInt(
        hybrid_segments[C.HYBRID_SELECTED_LABELS], 
        stringLabels
    )
    
    
    
    
    if(C.GENERATE_ELSE_LOAD_DATA):
        generateDatasets()
        
        
    else:
        # Load Data
        train, test = loadDataset(0)
        
        print(test['Sublabel'].value_counts(ascending=True))
        print(train['Sublabel'].value_counts(ascending=True))
        
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
        

        vis.dataDistribution(stringLabels, hybrid_segment_labels_numeric)
        vis.dataDistribution(stringLabels, Y_train)
        
        # Machine Learning
        dt(X_train, Y_train, X_test, Y_test, stringLabels)
        rf(X_train, Y_train, X_test, Y_test, stringLabels)
        svc(X_train, Y_train, X_test, Y_test, stringLabels)
        knn(X_train, Y_train, X_test, Y_test, stringLabels)
        nn(X_train, Y_train, X_test, Y_test, stringLabels)
        
        # clf = RandomForestClassifier()
        # sfs1 = SFS(     
        #     clf, 
        #     k_features=8, 
        #     forward=True, 
        #     floating=False, 
        #     verbose=2,
        #     scoring='accuracy',
        #     cv=5,
        #     n_jobs=-1
        # )
        # sfs1 = sfs1.fit(X_train, Y_train, custom_feature_names=C.HYBRID_SELECTED_FEATURES)
        # vis.confusionMatrix(sfs1, X_test, Y_test, stringLabels)   