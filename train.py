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
def run(trdl, valdl, model, loss, opt, epoch=100,patience = 5, exist_acc=True, device='cuda'):
    val_losses = {0:1}
    model = model.to(device)
    for i in range(epoch):
        train(trdl,model,loss,opt,device=device)
        acc,val_loss = test(valdl,model,loss,epoch=i,exist_acc=exist_acc,device=device)


        if min(val_losses.values() ) > val_loss:
            val_losses[i] = val_loss
            best_model = copy.deepcopy(model)
        if i == min(val_losses,key=val_losses.get)+patience:
            break
    return best_model, val_losses