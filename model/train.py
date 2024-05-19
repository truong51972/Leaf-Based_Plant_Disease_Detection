import torch
from torch import nn
from torchvision import transforms

from pathlib import Path
from torchmetrics import Accuracy, ConfusionMatrix

from model.data_setup import create_dataloader
from model.engine import train
from model.utils import save_model
from model.model_builder import resnet50_model

def run(**kwargs):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: '{device}'")
    
    train_transforms_data = transforms.Compose([
        transforms.RandomResizedCrop(size=(224, 224), antialias=True),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomVerticalFlip(p=0.5),
        transforms.ToTensor()
    ])
    
    val_transforms_data = transforms.Compose([
        transforms.Resize(size= 224),
        transforms.ToTensor()
    ])

    test_transforms_data = transforms.Compose([
        transforms.Resize(size= 224),
        transforms.ToTensor()
    ])
    
    train_dataloader, val_dataloader, test_dataloader, class_names = create_dataloader(**kwargs,
                                                                          train_transform=train_transforms_data,
                                                                          val_transform=val_transforms_data,
                                                                          test_transform=test_transforms_data)


    model, info_data = resnet50_model(class_names= class_names, pretrain_model_path= kwargs['train_para']['pretrain_model_path'], device= device)
    
    loss_func = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(params= model.parameters(), lr= kwargs['train_para']['learning_rate'])
    
    accur = Accuracy(task='multiclass', num_classes= len(class_names)).to(device)
    
    results = train(
            model= model,
            train_dataloader= train_dataloader,
            val_dataloader= val_dataloader,
            test_dataloader= test_dataloader,
            loss_func= loss_func,
            optimizer= optimizer,
            mectric_funcs= accur,
            epochs= kwargs['train_para']['epoch'],
            info_data = info_data,
            device= device
    )
    
    save_model(model= model, results= results, class_names= class_names, device= device)
