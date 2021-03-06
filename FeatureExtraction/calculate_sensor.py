import sys, shutil, os
sys.path.insert(0,'..')

import triplog_constants as C

from scipy.fft import fft, ifft
from scipy.fftpack import fftfreq
from scipy import signal
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def sensorFFT(df, label):
    
    mean = df.mean()
    df = df - mean
    
    N = C.SAMPLE_POINTS
    T = 1.0 / C.DATA_FREQUENCY_HZ
    x = np.linspace(0.0, N*T, N)
    y = df.to_numpy()
    
    yf = np.abs(fft(y, N, norm="ortho"))
    xf = fftfreq(N,T)
    
    fig, ax = plt.subplots(1, 1, figsize=(20, 10))
    #plt.semilogy(xf[1:N//2], 2.0/N * np.abs(yf[1:N//2]), '-b')
    ax.plot(np.abs(xf), np.abs(yf))
    ax.set_ylim(0, 50)
    ax.set_title(label)
    ax.set_xlabel("Frequency [HZ]")
    ax.set_ylabel("Amplitude")
    plt.show()
    
def vectorLength(df, sensorType):
    if sensorType is "LINEAR_ACC":
        df['SUM'] = np.sqrt((df['LINEAR_ACC_X'])**2 + (df['LINEAR_ACC_Y'])**2 + (df['LINEAR_ACC_Z'])**2)
    if sensorType is "ACC":
        df['SUM'] = np.sqrt((df['ACC_X'])**2 + (df['ACC_Y'])**2 + (df['ACC_Z'])**2)
    return df['SUM']
