import torch
from torch import nn
from torchvision.models import efficientnet_v2_s, EfficientNet_V2_S_Weights
from torchvision.models import resnet50, ResNet50_Weights

from pathlib import Path
import json

def efficientnet_v2_s_model(class_names: None|list = None, pretrain_model_path: None|str= None, device: str= 'cpu'):
    weights = EfficientNet_V2_S_Weights.DEFAULT
    model = efficientnet_v2_s(weights= weights).to(device)

    model.classifier = nn.Sequential(
        nn.Dropout(p=0.2, inplace=True),
        nn.Linear(in_features=1280, out_features=len(class_names), bias=True)
    )

    model = model.to(device)
    return model

def resnet50_model(class_names: None|list = None, pretrain_model_path: None|str= None, device: str= 'cpu'):
    info_data = None
    if pretrain_model_path is None:
        weights = ResNet50_Weights.DEFAULT
        model = resnet50(weights= weights).to(device)
        model.fc = nn.Sequential(
            nn.Linear(in_features=2048, out_features=len(class_names), bias=True)
        )
        model = model.to(device)
        
    else:
        pretrain_model_path = Path(pretrain_model_path)

        with open(pretrain_model_path / 'info.json', 'r') as f:
            info_data = json.load(f)
        
        model = resnet50().to(device)
        model.fc = nn.Sequential(
            nn.Linear(in_features=2048, out_features=len(info_data['class_names']), bias=True)
        )
        model.load_state_dict(torch.load(f=pretrain_model_path / 'model.pth'))
        model = model.to(device)
        
    return model, info_data
