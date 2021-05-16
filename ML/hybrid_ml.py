#print(__name__)
#__file__ = r"C:\Studium\5.Semester\Studienarbeit\dataprep_TripLog\ML\hybrid_ml.py"
import sys, shutil, os
sys.path.insert(0,'..')

# print(os.path.abspath("."))
#import dataprep_triplog.triplog_constants as C
import triplog_constants as C

import asyncio
import nest_asyncio

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import visualisation_ml as vis
import calculate as cal

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from mlxtend.feature_selection import SequentialFeatureSelector as SFS


# =============================================================================
# getAvailableLabels
# Get all available labels
#
# Parameter:
#   hydrid_segments - segments of hybrid data
#
# Returns:
#   labels - list of all available lists 
# =============================================================================
def getAvailableLabels(hydrid_segments): 
    labels = set()
    if(C.COMPRESS_LABELS):
        labels.update(hydrid_segments['Label'])
    else:
        labels.update(hydrid_segments['Label'] + "_" + hydrid_segments['Sublabel'])  
    return list(labels)

# =============================================================================
# convertLabeltoInt
# Converts labels to numerical label representation
#
# Parameter:
#   labelList - list of all labels
#   stringLabels - labels in string representation (set()-like)
#
# Returns:
#   labellist - list of numerical labels
# =============================================================================
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

# =============================================================================
# countLabels
# Count the amount of each Label
#
# Parameter:
#   labelList - list of all labels
#   stringLabels - labels in string representation (set()-like)
#
# Returns:
#   number_of_elements - amount of labels
# =============================================================================
def countLabels(labelList, stringLabels):
    number_of_elements = []
    for i in range(len(stringLabels)):
        number_of_elements.append(0)
    for i in labelList:
        number_of_elements[i] = number_of_elements[i] + 1
    return number_of_elements;

# =============================================================================
# removeUntilEqual
# Remove rows until all amount of labels are equal
#
# Parameter:
#   df - DataFrame of all data
#   hybrid_segment_labels_numeric - numerical label representation
#
# Returns:
#   df - DataFrame of all data
# =============================================================================
def removeUntilEqual(df, hybrid_segment_labels_numeric):
    df['numeric'] = hybrid_segment_labels_numeric
    count = df['numeric'].value_counts()
    min_number_of_elements = count.min()         
    df = df.groupby('numeric').apply(lambda s: s.sample(min_number_of_elements))
    return df

# =============================================================================
# copyUntilEqual
# Copy rows until all amount of labels are equal
#
# Parameter:
#   df - DataFrame of all data
#   hybrid_segment_labels_numeric - numerical label representation
#
# Returns:
#   frame_new - DataFrame of all data
# =============================================================================
def copyUntilEqual(df, hybrid_segment_labels_numeric):
    df['numeric'] = hybrid_segment_labels_numeric
    count = df['numeric'].value_counts()
    max_number_of_elements = count.max()
    
    lst = [df]
    for class_index, group in df.groupby('numeric'):
        lst.append(group.sample(max_number_of_elements-len(group), replace=True))
    frame_new = pd.concat(lst)

    return frame_new

# =============================================================================
# custom_train_test_split
# Manually split data into train- and testdata
#
# Parameter:
#   df - DataFrame of all data
#   hybrid_segment_labels_numeric - numerical label representation
#
# Returns:
#   train, test - data split into train- and testdata
# =============================================================================
def custom_train_test_split(df, hybrid_segment_labels_numeric):
    occurances = df['Sublabel'].value_counts()
    
    df['numeric'] = hybrid_segment_labels_numeric
    
    train = df
    test = pd.DataFrame()
    
    test_occurances = int(0.5 * min(occurances))  
    test = df.groupby('numeric').apply(lambda s: s.sample(test_occurances))
    train[~train.index.isin(test.index)]
    
    return train, test

# =============================================================================
# cleanData
# Drop rows where feature tow is indicating waiting times over 50% of the
# whole segments time
#
# Parameter:
#   df - DataFrame of all data
#
# Returns:
#   df - DataFrame without rows where waiting time is over 50%
# =============================================================================
def cleanData(df):
    print("Anzahl der Segmente vor Data-Cleaning:", len(df))
    df.drop(
        df[df['tow'] > 0.5 * C.SECONDS_SENSOR_SEGMENT].index,
        inplace=True
    )
    print("Anzahl der Segmente nach Data-Cleaning:", len(df))
    print('------------------------------------------------')
    return df

# =============================================================================
# removeBySublabel
# Drop rows of given type of label
#
# Parameter:
#   df - DataFrame of all data
#   labeltype - sublabel which should be removed from dataframe
#
# Returns:
#   df - DataFrame without rows of given labeltype
# =============================================================================
def removeBySublabel(df, labeltype):
    df.drop(
        df[df['Sublabel'] == labeltype].index,
        inplace=True
    )
    return df

# =============================================================================
# standardize
# Standardize data with given mean and std values
#
# Parameter:
#   df - DataFrame of all data
#   mean - mean value for calculation, if not given = None
#   std - std value for calculation, if not given = None
#
# Returns:
#   df - DataFrame with standardized features
# =============================================================================
def standardize(df, mean=None, std=None):
    if mean is None or std is None:
        mean = df[C.HYBRID_SELECTED_FEATURES].mean()
        std = df[C.HYBRID_SELECTED_FEATURES].std()
        
    df[C.HYBRID_SELECTED_FEATURES] = (
        (df[C.HYBRID_SELECTED_FEATURES] - mean) / std
    )
    return df

# =============================================================================
# getStandardizationAndNormalizationValues
# Calculates min, max, mean and std values of data
#
# Parameter:
#   df - DataFrame of all data
#
# Returns:
#   min, max, mean, std - values calculated from given DataFrame
# =============================================================================
def getStandardizationAndNormalizationValues(df):  
    return (
        df[C.HYBRID_SELECTED_FEATURES].min(), 
        df[C.HYBRID_SELECTED_FEATURES].max(), 
        df[C.HYBRID_SELECTED_FEATURES].mean(),
        df[C.HYBRID_SELECTED_FEATURES].std()
    )

# =============================================================================
# normalize
# Normalize data with given minima and maxima values
#
# Parameter:
#   df - DataFrame of all data
#   minima - minima value for calculation, if not given = None
#   maxima - maxima value for calculation, if not given = None
#
# Returns:
#   df - DataFrame with normalized features
# =============================================================================
def normalize(df, minima=None, maxima=None):
    if minima is None or maxima is None:
        minima=df[C.HYBRID_SELECTED_FEATURES].min()
        maxima=df[C.HYBRID_SELECTED_FEATURES].max()
    
    df[C.HYBRID_SELECTED_FEATURES] = (
        (df[C.HYBRID_SELECTED_FEATURES] - minima) / (maxima - minima)
    )
    return df

# =============================================================================
# dt, rf, svc, knn, nn
# sckit-learn Algorithms (Machine Learning Models with Parameters)
#
# Parameter:
#   X_train - dataframe with features for training
#   Y_train - dataframe with actual (numerical) labels
#   X_test - dataframe with features for testing
#   Y_test - dataframe with actual (numerical) labels
#   classWeight - sklearn weight setting for classifiers which can use weighted
#                 features (i.e.: "balanced")
#   stringLabels - labels in string representation (set()-like) for confusion
#                  matrix
#
# Returns:
#   clf - trained classifier
# =============================================================================
def dt(X_train, Y_train, X_test, Y_test, classWeight, stringLabels):
    clf = DecisionTreeClassifier(
        random_state = 42,
        class_weight = classWeight
    )
    clf = clf.fit(X_train, Y_train)    
    vis.confusionMatrix(clf, X_test, Y_test, stringLabels)    
    return clf
    
def rf(X_train, Y_train, X_test, Y_test, classWeight, stringLabels):
    clf = RandomForestClassifier(
        n_estimators = 200, 
        criterion = 'entropy',
        n_jobs = -1,
        random_state = 42,
        class_weight = classWeight
    )
    clf = clf.fit(X_train, Y_train)    
    vis.confusionMatrix(clf, X_test, Y_test, stringLabels)    
    return clf

def svc(X_train, Y_train, X_test, Y_test, classWeight, stringLabels):
    clf = SVC(
        degree = 5,
        kernel = 'sigmoid',
        random_state = 42,
        class_weight = classWeight
    )
    clf = clf.fit(X_train, Y_train)    
    vis.confusionMatrix(clf, X_test, Y_test, classWeight, stringLabels)    
    return clf
    
def knn(X_train, Y_train, X_test, Y_test, classWeight, stringLabels):
    clf = KNeighborsClassifier(len(stringLabels))
    clf = clf.fit(X_train, Y_train)    
    vis.confusionMatrix(clf, X_test, Y_test, stringLabels)    
    return clf

def nn(X_train, Y_train, X_test, Y_test, stringLabels):
    clf = MLPClassifier(
        solver='lbfgs', 
        alpha=1e-5, 
        learning_rate = 'adaptive',
        hidden_layer_sizes=(40, 20), 
        #random_state=1, 
        max_iter=50000,
        validation_fraction = 0.3,
        random_state = 42,
    )
    clf = clf.fit(X_train, Y_train)   
    vis.confusionMatrix(clf, X_test, Y_test, stringLabels)
    return clf

# =============================================================================
# generateDatasets
# Generates test- and train datasets and saves those to a *.csv file for later
# use
# This function is overcomplicated and could be simplified in a next version
# of this script
#
# Parameter:
#   -
#
# Returns:
#   -
# =============================================================================
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
        
        #hybrid_segments = copyUntilEqual(hybrid_segments, hybrid_segment_labels_numeric)
        hybrid_segments = hybrid_segments.sample(frac=1).reset_index(drop=True)
        
        # Normalize or Standardize
        if(C.NORMALIZE_ELSE_STANDARDIZE):
            hybrid_segments = normalize(hybrid_segments)
        else:
            hybrid_segments = standardize(hybrid_segments)
            
        
        
        
        original = hybrid_segments    
            
        # number_of_elements = countLabels(hybrid_segment_labels_numeric, stringLabels)
        # hybrid_segments = removeUntilEqual(hybrid_segments, hybrid_segments['numeric'])        
        # hybrid_segments = hybrid_segments.sample(frac=1).reset_index(drop=True)
                            
        # vis.dataDistribution(stringLabels, hybrid_segments['numeric'])
        
        
        hybrid_segment_labels_numeric = convertLabeltoInt(
            hybrid_segments[C.HYBRID_SELECTED_LABELS], 
            stringLabels
        )
        
        # Split file into Train- and Test-Data
        
        # train, test = custom_train_test_split(hybrid_segments, hybrid_segment_labels_numeric)      
        train, test = train_test_split(hybrid_segments, test_size=0.2)
        test = test[~test.isin(train)].dropna()
        original = original[~original.isin(test)].dropna()
        print("Trainings- und Testdatenset:", len(original), len(test))
        print('------------------------------------------------')
   
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
               
        # test = removeUntilEqual(test, test_numeric)
        # original = copyUntilEqual(original, train_numeric)
                
        # train_numeric = convertLabeltoInt(
        #     original[C.HYBRID_SELECTED_LABELS], 
        #     stringLabels
        # )
        # test_numeric = convertLabeltoInt(
        #     test[C.HYBRID_SELECTED_LABELS], 
        #     stringLabels
        # )
        # vis.dataDistribution(stringLabels, train_numeric)
        # vis.dataDistribution(stringLabels, test_numeric)
    
        original.to_csv(C.DATASET_FOLDER + "train_" + str(i) + ".csv")
        test.to_csv(C.DATASET_FOLDER + "test_" + str(i) + ".csv")

# =============================================================================
# initTestDataset
# Calculates normalized/standardized information of test dataset depending on
# previously calculated minima, maxima, mean and std from training data
# Is used for preperation of external 
#
# Parameter:
#   minima - precalculated minima by train dataset
#   maxima - precalculated maxima by train dataset
#   mean - precalculated mean value by train dataset
#   std - precalculated std value by train dataset
#   path - path of to be used fusedSegments.csv file
#
# Returns:
#   - test_segments with normalized/standardized values
# =============================================================================
def initTestDataset(minima, maxima, mean, std, path=C.OFFLINE_TEST_SEGMENTS):
    test_segments = pd.read_csv(path) 
    if(C.NORMALIZE_ELSE_STANDARDIZE):
        test_segments = normalize(test_segments, minima, maxima)
    else:
        test_segments = standardize(test_segments, mean, std)
    return test_segments
  
# =============================================================================
# loadDataset
# Loads presaved train- and test dataset from storage *.csv file
#
# Parameter:
#   i - number of train -and test file, if multiple exist
#
# Returns:
#   train, test - precreated and saved datasets
# =============================================================================      
def loadDataset(i):
    train = pd.read_csv(C.DATASET_FOLDER + "train_" + str(i) + ".csv")
    test = pd.read_csv(C.DATASET_FOLDER + "test_" + str(i) + ".csv")    
    return train, test

# =============================================================================
# main
# Main function for machine learning stuff
#
# Parameter:
#   -
# Returns:
#   -
# =============================================================================
async def main():
    
    ###########################################################################          
    ### Pregenerate data for extraction of available labels, values which are
    ### being used for normalization/standardization
    ###########################################################################  
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
    hybrid_segments["numeric"] = hybrid_segment_labels_numeric
    copyUntilEqual(hybrid_segments, hybrid_segment_labels_numeric)
    minima, maxima, mean, std = getStandardizationAndNormalizationValues(hybrid_segments)
    
    ###########################################################################          
    ### Generate test and train datasets if option is set in 
    ### triplog_constants.py
    ###########################################################################  
    if(C.GENERATE_ELSE_LOAD_DATA):
        generateDatasets()
        
    ###########################################################################          
    ### Train and evaluate machine learning models if option is disabled in
    ### triplog_constants.py
    ###########################################################################         
    else:
        #######################################################################     
        ### Data preperation for machine learning process
        #######################################################################        
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
            
        # set classWeight for ML-Algorithms which can work with weighted inputs
        classWeight = "balanced"
        
        #######################################################################     
        ### Data visualisation (currently not being used)
        #######################################################################
        # Show data distribution
        # vis.dataDistribution(stringLabels, hybrid_segment_labels_numeric)
        # vis.dataDistribution(stringLabels, Y_train)
        
        # Print Boxplots as pgf/tikz to be used in a latex document
        # vis.boxplotByFeature(hybrid_segments, stringLabels)
        
        #######################################################################     
        ### Machine learning / Model training
        #######################################################################
        # Machine Learning / Comment out Models which should be trained
        dt_clf = dt(X_train, Y_train, X_test, Y_test, classWeight, stringLabels)
        rf_clf = rf(X_train, Y_train, X_test, Y_test, classWeight, stringLabels)
        nn_clf = nn(X_train, Y_train, X_test, Y_test, stringLabels)
     
        #######################################################################     
        ### Machine learning / Feature importance
        ### WORK IN PROGRESS - CURRENTLY NOT WORKING (DATA HAS TO BE CUT
        ### SO ONLY C.HYBRID_SELECTED_LABELS FEATURES ARE BEING USED)
        #######################################################################
        # importances = rf_clf.feature_importances_
        # sorted_indices = np.argsort(importances)[::-1]
        # import matplotlib.pyplot as plt
        # plt.title('Feature Importance')
        # plt.bar(range(X_train.shape[1]), importances[sorted_indices], align='center')
        # plt.xticks(range(X_train.shape[1]), X_train[0][sorted_indices+1], rotation=90)
        # plt.tight_layout()
        # plt.show()
        
        #######################################################################     
        ### Machine learning / Model evaluation on test trip
        #######################################################################
        # offlineTestDf = initTestDataset(minima, maxima, mean, std)
        # offlineTestDf = np.array(offlineTestDf[C.HYBRID_SELECTED_FEATURES])
        # await vis.showReferenceMap(C.OFFLINE_TEST_PATH_GPS)
        
        # predictions = dt_clf.predict(offlineTestDf)        
        # await vis.showPredictionOnMap(
        #     C.OFFLINE_TEST_PATH_GPS, 
        #     predictions, 
        #     stringLabels,
        #     filename="dtPrediction"
        # )
        
        # predictions = rf_clf.predict(offlineTestDf)        
        # await vis.showPredictionOnMap(
        #     C.OFFLINE_TEST_PATH_GPS, 
        #     predictions, 
        #     stringLabels,
        #     filename="rfPrediction"
        # )
        
        # predictions = nn_clf.predict(offlineTestDf)        
        # await vis.showPredictionOnMap(
        #     C.OFFLINE_TEST_PATH_GPS, 
        #     predictions, 
        #     stringLabels,
        #     filename="nnPrediction"
        # )
        
        #######################################################################     
        ### Machine learning / Sequential feature selection
        ### WORK IN PROGRESS - CURRENTLY NOT BEING USED, USABLE BUT
        ### NOT VERY EASY TO INTERPRET, COULD USE SOME WORK
        #######################################################################
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
        # print('Selected features:', sfs1.k_feature_idx_)

        # vis.confusionMatrix(sfs1, X_test, Y_test, stringLabels)   
        
if __name__ == "__main__":
    # import nest_asyncio
    nest_asyncio.apply()  
    asyncio.run(main())