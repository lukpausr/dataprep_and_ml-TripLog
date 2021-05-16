import sys, shutil, os
sys.path.insert(0,'..')

import triplog_constants as C

from scipy.fft import fft, ifft
from scipy.fftpack import fftfreq
from scipy import signal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# =============================================================================
# sensorEuclideanFFT
# Determine fft_frequency feature for euclidian data
#
# Parameter:
#   df - DataFrame with Euclidian Sensor-Data (1-dimensional)
#   label - Label fitting to the given Data, used for printing fft plots
#
# Returns:
#   max_freq - frequency at maximum calculated amplitude, devided by 2 to
#              compensate rectificatiom
# =============================================================================
def sensorEuclideanFFT(df, label):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fft.html
    
    ###########################################################################          
    ### Remove dc-part of the signal (mean value)
    ###########################################################################    
    mean = df.mean()
    df = df - mean
    
    ###########################################################################          
    ### FFT using scipys fft method
    ###########################################################################    
    N = C.SAMPLE_POINTS
    T = 1.0 / C.DATA_FREQUENCY_HZ
    x = np.linspace(0.0, N*T, N)
    y = df.to_numpy()
    
    yf = fft(y, len(y), norm="ortho")
    xf = fftfreq(len(y), T)

    ###########################################################################          
    ### Set amplitudes to zero below given treshold to eliminate very low
    ### frequencies which can influence model quality
    ###########################################################################     
    for freq, i in zip(xf, list(range(len(xf)))):
        if np.abs(freq) < 0.5:
            yf[i] = 0.0

    ###########################################################################          
    ### Find maximum ampltiudes index to find frequency where the amplitude
    ### is at the maximum in fft result list
    ###########################################################################
    max_idx = np.argmax(yf)
    max_freq = np.abs(xf[max_idx])
    max_amp = np.abs(yf[max_idx])
    
    ###########################################################################          
    ### plot fft results for visualisation, only being used when
    ### constant SHOW_FFT_PLOTS is set to True in triplog_constants.py
    ###########################################################################     
    if(C.SHOW_FFT_PLOTS):
        plt.rcParams.update({'font.size': 16})   
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 10))
        #plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')
        ax1.plot(np.abs(xf), np.abs(yf))
        #n, bins, patches = ax.hist(yf[50:], 64, density=True)
        #ax.set_ylim(0, 50)
        ax1.set_title(label + ", max. Amplitude at " + str(max_freq) + " Hz (Corrected " + str(max_freq/2) + " Hz)")
        ax1.set_xlabel("Frequency [HZ]")
        ax1.set_ylabel("Amplitude")
        
        # Sensor data
        ax2.plot(df)    
        ax2.set_ylim(-10, 10)
        ax2.set_title(label)
        ax2.set_xlabel("Zeit [s]")
        ax2.set_ylabel("Beschleunigung [m/s^2]")
        
        plt.show()
    
    ###########################################################################          
    ### frequency at maximum calculated amplitude, devided by 2 to
    ### compensate rectificatiom
    ########################################################################### 
    max_freq = max_freq / 2
    return max_freq

# =============================================================================
# singleFFT
# Determine the FFT feature of a single axis
#
# Parameter:
#   df - DataFrame of the axis
#
# Returns:
#   max_freq, max_amp - frequency and amplitude where amplitude is maximum
#                       in fft results                     
# =============================================================================  
def singleFFT(df):
    ###########################################################################          
    ### Remove dc-part of the signal (mean value)
    ########################################################################### 
    mean = df.mean()
    df = df - mean 
    
    ###########################################################################          
    ### FFT using scipys fft method
    ########################################################################### 
    N = C.SAMPLE_POINTS
    T = 1.0 / C.DATA_FREQUENCY_HZ
    
    y = df.to_numpy() 
    yf = fft(y, len(y), norm="ortho")
    xf = fftfreq(len(y), T)  
    
    ###########################################################################          
    ### Set amplitudes to zero below given treshold to eliminate very low
    ### frequencies which can influence model quality
    ########################################################################### 
    for freq, i in zip(xf, list(range(len(xf)))):
        if np.abs(freq) < 0.5:
            yf[i] = 0.0
     
    ###########################################################################          
    ### Find maximum ampltiudes index to find frequency where the amplitude
    ### is at the maximum in fft result list
    ########################################################################### 
    max_idx = np.argmax(yf)
    max_freq = np.abs(xf[max_idx])
    max_amp = np.abs(yf[max_idx])
   
    return max_freq, max_amp

# =============================================================================
# sensorAxsFFT
# Determine frequency at maximum amplitude of the max axis
#
# Parameter:
#   dfx - DataFrame with x values
#   dfy - DataFrame with y values
#   dfz - DataFrame with z values
#
# Returns:
#   max_freq[max_idx] - frequency at maximum amplitude of axis with maximum
#                       ampltiude at frequency
# =============================================================================  
def sensorAxsFFT(dfx, dfy, dfz):
    max_freq = []
    max_amp = []

    ###########################################################################          
    ### Calculate fft features for each axis and append result to lists
    ###########################################################################    
    f, a = singleFFT(dfx)
    max_freq.append(f)
    max_amp.append(a)
    
    f, a = singleFFT(dfy)
    max_freq.append(f)
    max_amp.append(a)
    
    f, a = singleFFT(dfz)
    max_freq.append(f)
    max_amp.append(a)
      
    ###########################################################################          
    ### Calculate index of maximum ampltiude value to find out which frequency
    ### is the most important
    ###########################################################################
    max_idx = np.argmax(np.array(max_amp))
    
    return max_freq[max_idx]

# =============================================================================
# vectorLength
# Calculates euclidian distance of given, 3-dimensional, sensor data
# 
# Parameter:
#   df - DataFrame from which this feature should be determined
#   sensorType - Select sensorType (possible: "LINEAR_ACC", "ACC", "GYRO")
#
# Returns:
#   df['SUM'] - DataFrame with euclidean distance (per row)
# =============================================================================      
def vectorLength(df, sensorType):
    if sensorType == "LINEAR_ACC":
        df['SUM'] = np.sqrt((df['LINEAR_ACC_X'])**2 + (df['LINEAR_ACC_Y'])**2 + (df['LINEAR_ACC_Z'])**2)
    if sensorType == "ACC":
        df['SUM'] = np.sqrt((df['ACC_X'])**2 + (df['ACC_Y'])**2 + (df['ACC_Z'])**2)
    if sensorType == "GYRO":
        df['SUM'] = np.sqrt((df['w_X'])**2 + (df['w_Y'])**2 + (df['w_Z'])**2)
    return df['SUM']

# =============================================================================
# metrics
# Determine the standard deviation and variance of a dataFrame
#
# Parameter:
#   df - DataFrame from which the features are to be determined
#
# Returns:
#   std, var - standard deviation and variance
# =============================================================================  
def metrics(df):
    npArray = df.to_numpy()
    std = np.std(npArray, dtype = np.float64)
    var = np.var(npArray, dtype = np.float64)   
    return std, var
