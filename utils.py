import pandas as pd


def num2class(nrs,type_=2,no_mild=[0,1,2,3]):
    nrs = int(nrs)
    label = ''
    if type_ ==2:
        if nrs in no_mild:
            label = 0
        else:
            label = 1
    else:
        raise Exception(f'there is no type {type_}.')
    return label 

def get_ppg_sample(idx=0):
    path = f'./sample/ppg{idx}.csv'
    df   = pd.read_csv(path,index_col=0)
    return df.to_numpy()


import json
import os

def get_sample_config(idx=0,root_dir = '../data/pd_gy',path = '../data/pd_gy/train_2.json'):
    
    with open(path,'r') as f:
        tr_jf = json.load(f)

    sample_rate = 300
    min5 = sample_rate*60*5
    
    recp = tr_jf[idx]['rec_path'][0].replace('\\','/')
    recp = os.path.join(root_dir,recp)
    orp = tr_jf[idx]['or_path'][0].replace('\\','/')
    orp = os.path.join(root_dir, orp)

    age = tr_jf[idx]['age']
    gender = tr_jf[idx]['gender']
    nrs2 = tr_jf[idx]['nrs2']
    nrs = tr_jf[idx]['nrs']
    item = tr_jf[idx]
    return orp, recp, sample_rate, min5, item