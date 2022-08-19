import vitaldb
import pandas as pd

def get_vital(path,type_='or',sample_rate=300, duration=300*6*5):
    
    vf = vitaldb.VitalFile(path,track_names=['Intellivue/PLETH','Intellivue/NIBP_SYS','Intellivue/ECG_II'])
    ppg = vf.to_numpy('Intellivue/PLETH',1/sample_rate)
    ecg = vf.to_numpy('Intellivue/ECG_II',1/sample_rate)
    first_idx = 0 
    
    if type_ == 'or': # starts from nibp
        nibp_or = vf.to_numpy('Intellivue/NIBP_SYS',1/sample_rate)
        for i, value in enumerate(nibp_or):
            if pd.isna(value):
                continue
            else:
                first_idx = i
                break
                
    elif type_ == 'rec': # starts from non-nan
        for i, value in enumerate(ppg):
            if pd.isna(value):
                continue
            else:
                first_idx = i
                break
    
    ecg = ecg[first_idx:first_idx+duration]            
    ppg = ppg[first_idx:first_idx+duration]            
    return ppg, ecg

def get_ppg(path,type_='or',sample_rate=300, duration=300*60*5):
    
    vf = vitaldb.VitalFile(path,track_names=['Intellivue/PLETH','Intellivue/NIBP_SYS'])
    ppg = vf.to_numpy('Intellivue/PLETH',1/sample_rate)
    first_idx = 0 
    
    if type_ == 'or':
        nibp_or = vf.to_numpy('Intellivue/NIBP_SYS',1/sample_rate)
        for i, value in enumerate(nibp_or):
            if pd.isna(value):
                continue
            else:
                first_idx = i
                break
                
    elif type_ == 'rec':
        for i, value in enumerate(ppg):
            if pd.isna(value):
                continue
            else:
                first_idx = i
                break
                
    ppg = ppg[first_idx:first_idx+duration]            
    return ppg
                
    

import os
import pandas as pd
import json 
import numpy as np 

import vitaldb
import torch
from torch.nn import functional as F

from preprocess import list2specgram
# from dataset import get_vital 

class VitalDataset(torch.utils.data.Dataset):
    def __init__(self,root_dir='../data/pd_gy',ann_path='../data/pd_gy/train.json',sample_rate=300,duration=300*60*5):
        
        with open(ann_path,'r') as f:
            jf = json.load(f)
        
        self.jf = jf
        self.root_dir = root_dir
        self.sample_rate = sample_rate
        self.duration = duration
        
    def __getitem__(self,idx):
        
        item = self.jf[idx]
        orp, recp = self.get_path(item) 

        ppg_or, ecg_or   = get_vital(orp,  type_='or' ,sample_rate=self.sample_rate,duration=self.duration)
        ppg_rec, ecg_rec = get_vital(recp, type_='rec',sample_rate=self.sample_rate,duration=self.duration)
        
        ppgecg = list2specgram([ppg_or, ppg_rec, ecg_or, ecg_rec],type_=['ppg','ppg','ecg','ecg'], sample_rate=self.sample_rate)
        ppg_or, ppg_rec, ecg_or, ecg_rec = ppgecg
        
        vital = np.array([ppg_or,ecg_or,ppg_rec,ecg_rec])
        vital = torch.tensor(vital)
        
        
        y = item['nrs_2']
        y = torch.tensor(y)
        y = F.one_hot(y,num_classes=2)
        
        return vital, y
    
    def __len__(self):
        return len(self.jf)
    
    def get_path(self, item):
        
        orp = item['or_path'][0].replace('\\','/')
        orp = os.path.join(self.root_dir, orp)
        recp = item['rec_path'][0].replace('\\','/')
        recp = os.path.join(self.root_dir,recp)
        return orp, recp
