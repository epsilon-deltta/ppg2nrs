import numpy as np
import pandas as pd

def interpolate(x :np.ndarray,mode='nearest')-> np.ndarray:

    if mode == 'nearest':
        x = pd.DataFrame(x,columns=['x'])
        x = x.fillna(method='ffill').fillna(method='bfill')
        x = x['x'].to_numpy()
    return x

def moving_average(x, w=30): # window
    return np.convolve(x, np.ones(w), 'valid') / w

from scipy import signal
def bandpass(x, band=[0.5,10], sample_rate=3000, order=101):
    fw = signal.firwin(order,band,fs=sample_rate,pass_zero='bandpass')
    x = signal.lfilter(fw,[1.0],x)
    return x

def moving_average(x, w): # window
    return np.convolve(x, np.ones(w), 'valid') / w

def norm_z(x,mean=47,std=15):
    return (x-mean)/std


def get_spectrogram(x,fs):
    f, t, xspec = signal.spectrogram(x, fs=fs, nperseg=fs)
    return xspec


def get_scalogram(x):
    pass


# ==== end2end preprocessing ======

def ppg_pre(x,sample_rate=300,norm=False):
    x = interpolate(x)
    x = bandpass(x, band=[0.5,15],sample_rate=sample_rate)
    x = moving_average(x,w=30)
    x = signal.resample(x,sample_rate*60*5)
    if norm:
        x = norm_z(x)
    return x


import neurokit2 as nk
def ecg_pre(x,sample_rate=300):
    
    x = interpolate(x)
    x = nk.ecg_clean(x,sampling_rate=sample_rate)
    return x
    
    
# ==== end2end spectrogram ======

def ppg2specgram(x: np.array,sample_rate= 300):
    
    x = ppg_pre(x, sample_rate=sample_rate, norm=False)
    f, t, xspec = signal.spectrogram(x, fs=sample_rate, nperseg=sample_rate)
    return xspec


def ecg2specgram(x: np.array,sample_rate= 300):
    
    x = ecg_pre(x, sample_rate=sample_rate)
    f, t, xspec = signal.spectrogram(x, fs=sample_rate, nperseg=sample_rate)
    return xspec
########

def ppg2specgram_all(x: np.array,sample_rate= 300):
    
    x = ppg_pre(x, sample_rate=sample_rate, norm=False)
    f, t, xspec = signal.spectrogram(x, fs=sample_rate, nperseg=sample_rate)
    return f,t,xspec


def ecg2specgram_all(x: np.array,sample_rate= 300):
    
    x = ecg_pre(x, sample_rate=sample_rate)
    f, t, xspec = signal.spectrogram(x, fs=sample_rate, nperseg=sample_rate)
    return f,t,xspec

########    
    
def ecgs2specgram(x:list,sample_rate=300):
    specgrams = []
    for ppg in x:
        specgrams.append(ecg2specgram(ppg))
    return specgrams

def ppgs2specgram(x:list,sample_rate=300):
    specgrams = []
    for ppg in x:
        specgrams.append(ppg2specgram(ppg))
    return specgrams


def list2specgram(x:list, type_:list, sample_rate=300):
    specgrams = []
    for i,sig in enumerate(x):
        if type_[i] == 'ppg':
            specgrams.append(ppg2specgram(sig))
        elif type_[i] == 'ecg':
            specgrams.append(ecg2specgram(sig))
    return specgrams