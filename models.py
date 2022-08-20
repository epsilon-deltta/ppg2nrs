import torchvision
from torch import nn
import torch

class PrePostNet(nn.Module):

    def __init__(self):
        super(PrePostNet, self).__init__()
        
        self.two2three_pre  = nn.Conv2d(2,3,3)
        self.two2three_post = nn.Conv2d(2,3,3)
        
        self.pre_backbone = torchvision.models.resnet34(pretrained=True)
        self.post_backbone = torchvision.models.resnet34(pretrained=True)
        self.pre_backbone.fc = nn.Sequential(nn.Linear(512,256),nn.Linear(256,128))
        self.post_backbone.fc = nn.Sequential(nn.Linear(512,256),nn.Linear(256,128))
        
        self.fusion = nn.Sequential(nn.Linear(256,128),nn.BatchNorm1d(128),nn.ReLU(),
                       nn.Linear(128,64), nn.BatchNorm1d(64), nn.ReLU(),
                       nn.Linear(64,2)) 
        
    
    def forward(self, x):
        x_pre, x_post = x[:,:2], x[:,2:]
        
        x_pre  = self.two2three_pre(x_pre)
        x_post = self.two2three_post(x_post)
        
        x_pre  = self.pre_backbone(x_pre)
        x_post = self.post_backbone(x_post)
        
        x_fusion = torch.cat([x_pre,x_post],axis=1)
        x_fusion = self.fusion(x_fusion)
        
        return x_fusion