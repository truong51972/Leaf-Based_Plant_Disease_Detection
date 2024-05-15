import torch
from torch import nn
from torchvision import transforms

from pathlib import Path
from torchmetrics import Accuracy

from model.data_setup import create_dataloader
from model.engine import train
from model.utils import save_model
from model.model_builder import resnet50_model

def run(dataset_path: str= 'path_to_dataset', epoch:int= 25, learning_rate: float= 0.001, batch_size: int= 32, pretrain_model: None|str= None):
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    dataset_path = Path(dataset_path)
    
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

    train_dataloader, val_dataloader, class_names = create_dataloader(dataset_path=dataset_path,
                                                              batch_size=batch_size,
                                                              train_transform=train_transforms_data,
                                                              val_transform=val_transforms_data)


    model = resnet50_model(class_names= class_names, pretrain_model= pretrain_model, device= device)
    
    loss_func = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(params= model.parameters(), lr= learning_rate)
    
    mectric_func = Accuracy(task='multiclass', num_classes= len(class_names)).to(device)
    
    results = train(
            model= model,
            train_dataloader= train_dataloader,
            val_dataloader= val_dataloader,
            loss_func= loss_func,
            optimizer= optimizer,
            mectric_func= mectric_func,
            epochs= epoch,
            device= device
    )

    save_model(model= model, results= results)
