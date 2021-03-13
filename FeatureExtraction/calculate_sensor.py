import sys, shutil, os
sys.path.insert(0,'..')

import triplog_constants as C

from scipy.fft import fft, ifft
from scipy.fftpack import fftfreq
from scipy import signal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def sensorEuclideanFFT(df, label):
    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.fft.fft.html
    # https://docs.scipy.org/doc/scipy/reference/tutorial/fft.html
    
    mean = df.mean()
    df = df - mean
    
    N = C.SAMPLE_POINTS
    T = 1.0 / C.DATA_FREQUENCY_HZ
    x = np.linspace(0.0, N*T, N)
    y = df.to_numpy()
    
    yf = fft(y, len(y), norm="ortho")
    xf = fftfreq(len(y), T)
    
    for freq, i in zip(xf, list(range(len(xf)))):
        if np.abs(freq) < 0.5:
            yf[i] = 0.0

    max_idx = np.argmax(yf)
    max_freq = np.abs(xf[max_idx])
    max_amp = np.abs(yf[max_idx])
    
    if(C.SHOW_FFT_PLOTS):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(30, 10))
        #plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')
        ax1.plot(np.abs(xf), np.abs(yf))
        #n, bins, patches = ax.hist(yf[50:], 64, density=True)
        #ax.set_ylim(0, 50)
        ax1.set_title(label + ", Max Amplitude at " + str(max_freq) + " Hz (Corrected " + str(max_freq/2) + " Hz)")
        ax1.set_xlabel("Frequency [HZ]")
        ax1.set_ylabel("Amplitude")
        
        # Sensor data
        ax2.plot(df)    
        ax2.set_ylim(-10, 10)
        ax2.set_title(label)
        ax2.set_xlabel("Zeit [s]")
        ax2.set_ylabel("Beschleunigung [m/s^2]")
        
        plt.show()
    
    # Teilen durch Faktor 2, da Berechnung der Vektorlänge 
    # Ausschläge nach oben spiegelt
    # Risiko von Verfälschung!
    return max_freq / 2

def singleFFT(df):
    mean = df.mean()
    df = df - mean 
    
    N = C.SAMPLE_POINTS
    T = 1.0 / C.DATA_FREQUENCY_HZ
    
    y = df.to_numpy() 
    yf = fft(y, len(y), norm="ortho")
    xf = fftfreq(len(y), T)  
    
    for freq, i in zip(xf, list(range(len(xf)))):
        if np.abs(freq) < 0.5:
            yf[i] = 0.0
     
    max_idx = np.argmax(yf)
    max_freq = np.abs(xf[max_idx])
    max_amp = np.abs(yf[max_idx])
   
    return max_freq, max_amp

def sensorAxsFFT(dfx, dfy, dfz, label):
    max_freq = []
    max_amp = []
    
    f, a = singleFFT(dfx)
    max_freq.append(f)
    max_amp.append(a)
    
    f, a = singleFFT(dfy)
    max_freq.append(f)
    max_amp.append(a)
    
    f, a = singleFFT(dfz)
    max_freq.append(f)
    max_amp.append(a)
                
    max_idx = np.argmax(np.array(max_amp))
    # print("MaxAMP: ", max_amp)
    # print("MaxFreq: ", max_freq)
    # print("RESULT_FREQ: ", max_freq[max_idx])
    
    return max_freq[max_idx]
    
def vectorLength(df, sensorType):
    if sensorType == "LINEAR_ACC":
        df['SUM'] = np.sqrt((df['LINEAR_ACC_X'])**2 + (df['LINEAR_ACC_Y'])**2 + (df['LINEAR_ACC_Z'])**2)
    if sensorType == "ACC":
        df['SUM'] = np.sqrt((df['ACC_X'])**2 + (df['ACC_Y'])**2 + (df['ACC_Z'])**2)
    if sensorType == "GYRO":
        df['SUM'] = np.sqrt((df['w_X'])**2 + (df['w_Y'])**2 + (df['w_Z'])**2)
    return df['SUM']

def metrics(df):
    npArray = df.to_numpy()
    std = np.std(npArray, dtype = np.float64)
    var = np.var(npArray, dtype = np.float64)   
    return std, var
    







