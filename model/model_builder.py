import torch
from torch import nn
from torchvision.models import efficientnet_v2_s, EfficientNet_V2_S_Weights
from torchvision.models import resnet50, ResNet50_Weights

def efficientnet_v2_s_model(class_names: list, device: str):
    weights = EfficientNet_V2_S_Weights.DEFAULT
    model = efficientnet_v2_s(weights= weights)

    model.classifier = nn.Sequential(
        nn.Dropout(p=0.2, inplace=True),
        nn.Linear(in_features=1280, out_features=len(class_names), bias=True)
    )

    model = model.to(device)
    return model

def resnet50_model(class_names: list, device: str):
    weights = ResNet50_Weights.DEFAULT
    model = resnet50(weights= weights).to(device)

    model.fc = nn.Sequential(
        nn.Linear(in_features=2048, out_features=len(class_names), bias=True)
    )

    model = model.to(device)
    return model
