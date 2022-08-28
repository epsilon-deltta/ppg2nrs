import torch
def train(dl,model,lossf,opt,device='cuda'):

    model.train()
    for x,y in dl:
        x,y = x.to(device),y.to(device)
        pre = model(x)
        loss = lossf(pre,y)

        opt.zero_grad()
        loss.backward()
        opt.step()

def test(dl,model,lossf,epoch=None,exist_acc=True,device='cuda'):
    model.eval()
    size, acc , losses = len(dl.dataset) ,0,0
    with torch.no_grad():
        for x,y in dl:
            x,y = x.to(device),y.to(device)
            pre = model(x)
            loss = lossf(pre,y)
            
            if exist_acc: 
                acc += (pre.argmax(1)==y).type(torch.float).sum().item()
            losses += loss.item()
    if exist_acc:
        accuracy = round(acc/size,4)
    else:
        accuracy = None
    val_loss = round(losses/size,6)
    print(f'[{epoch}] acc/loss: {accuracy}/{val_loss}')
    return accuracy,val_loss

import copy
def trainval(trdl, valdl, model, loss, opt, scheduler=None, epoch=100,patience = 5, exist_acc=True, device='cuda'): # ,  class_weight=False
    val_losses = {0:1}
    model = model.to(device)
            
    for i in range(epoch):
        train(trdl,model,loss,opt,device=device)
        acc,val_loss = test(valdl,model,loss,epoch=i,exist_acc=exist_acc,device=device)
        
        if scheduler:
            scheduler.step()

        if min(val_losses.values() ) > val_loss:
            val_losses[i] = val_loss
            best_model = copy.deepcopy(model)
        if i == min(val_losses,key=val_losses.get)+patience:
            break
    return best_model, val_losses

import numpy as np
def get_classweight_dl(trdl):
    
    labels = []
    for i in range(len(trdl.dataset)):
        _,y = trdl.dataset[i]
        labels.append(y)
    labels = np.array(labels)
    
    from sklearn.utils import class_weight
    class_weights=class_weight.compute_class_weight('balanced',classes=np.unique(labels),y=labels)
    class_weights=torch.tensor(class_weights,dtype=torch.float)
    return class_weights

def get_classweight(trdt):
    
    labels = []
    for i in range(len(trdt)):
        _,y = trdt[i]
        labels.append(y)
    labels = np.array(labels)
    
    from sklearn.utils import class_weight
    class_weights=class_weight.compute_class_weight('balanced',classes=np.unique(labels),y=labels)
    class_weights=torch.tensor(class_weights,dtype=torch.float)
    return class_weights

def get_classweight_all(trdt,class_weight):
    
    from torch.utils.data import WeightedRandomSampler
    tr_y = []
    for i in range(len(trdt)):
        tr_y.append(trdt[i][1])
    class_weight_all = class_weight[tr_y]
    return class_weight_all