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

def get_ppg(path,type_='or',sample_rate=sample_rate, duration=min5):
    
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
                