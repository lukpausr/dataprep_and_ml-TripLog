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

from sklearn.model_selection import train_test_split

print('TensorFlow version: {}'.format(tf.__version__))
print('------------------------------------------------')



def getAvailableFeatures(sensor_segments):
    
    features = []
    labels = set()
    labels.update(sensor_segments['Label'] + "_" + sensor_segments['Sublabel'])
    print(list(labels))
    
    return list(labels)

def loadTrainingData(df, sensorType):
    result_data = []
    result_labels = []
    
    for index, row in df.iterrows():
        result_data.append(pd.read_pickle(row[sensorType]).to_numpy())
        result_labels.append(row['Label'] + "_" + row['Sublabel'])
        
    return np.array(result_data), np.array(result_labels)

def convertLabeltoInt(labelList, stringLabels):
    # https://stackoverflow.com/questions/176918/finding-the-index-of-an-item-in-a-list
    for i in range(len(labelList)):
        index = stringLabels.index(labelList[i])
        labelList[i] = int(index)
    numericLabels = labelList.astype(np.int32)
    return numericLabels

def sensorML(training_data, training_labels, test_data, test_labels, output_layer):
    
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(C.SECONDS_SENSOR_SEGMENT*50, 3)),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(output_layer)
    ])
    
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )
    
    model.fit(training_data, training_labels, epochs=50)
    
    test_loss, test_acc = model.evaluate(test_data,  test_labels, verbose=2)
    print('\nTest accuracy:', test_acc)

def sensorLSTM(training_data, training_labels, test_data, test_labels, output_layer):
    
    model = keras.Sequential()
    model.add(keras.layers.LSTM(units=256, input_shape=(C.SECONDS_SENSOR_SEGMENT*50, 3)))
    model.add(keras.layers.Dropout(rate=0.5))
    model.add(keras.layers.Dense(units=128, activation='relu'))
    model.add(keras.layers.Dense(output_layer, activation='softmax'))
    
    model.compile(
      loss='sparse_categorical_crossentropy',
      optimizer='adam',
      metrics=['accuracy']
    )

    model.fit(training_data, training_labels, epochs=50)

    test_loss, test_acc = model.evaluate(test_data,  test_labels, verbose=2)
    print('\nTest accuracy:', test_acc)

    
if(__name__ == "__main__"):
    
    # Load CSV
    sensor_segments = pd.read_csv(C.SENSOR_DATA_CSV)
    
    # Shuffle CSV
    sensor_segments = sensor_segments.sample(frac=1).reset_index(drop=True)
    
    # Split file into Train- and Test-Data
    train, test = train_test_split(sensor_segments, test_size=0.2)
    print(len(train), len(test))
    print('------------------------------------------------')
    
    # Loading Pickle Files Training Data
    training_data, training_labels = loadTrainingData(train, "accFile")
    print(training_data[0], training_labels[0])
    print('------------------------------------------------')
    
    # Loading Pickle Files Test Data
    test_data, test_labels = loadTrainingData(test, "accFile")
    print(test_data[0], test_labels[0])
    print('------------------------------------------------')
    
    
    # Return Labels
    stringLabels = getAvailableFeatures(sensor_segments)
    
    # Get amount of individual labels
    output_layer = len(stringLabels)
    
    
    # Convert Training Labels to numeric representation
    training_labels_numeric = convertLabeltoInt(training_labels, stringLabels)
    print(training_labels[:10])
    print(training_labels_numeric[:10])
    print('------------------------------------------------')
    
    # Convert Test Labels to numeric representation
    test_labels_numeric = convertLabeltoInt(test_labels, stringLabels)
    print(test_labels[:10])
    print(test_labels_numeric[:10])
    print('------------------------------------------------')
    
    print(training_data.shape)
    print(training_labels_numeric.shape)
    
    # Train ML Modell
    # sensorML(training_data, training_labels_numeric, test_data, test_labels_numeric, output_layer)
    
    
    # Reshape Input to 3D
    train_X = training_data.reshape((training_data.shape[0], training_data.shape[1], 3))
    test_X = test_data.reshape((test_data.shape[0], test_data.shape[1], 3))
    print(train_X.shape, training_labels_numeric.shape, test_X.shape, test_labels_numeric.shape)
    
    sensorLSTM(train_X, training_labels_numeric, test_X, test_labels_numeric, output_layer)