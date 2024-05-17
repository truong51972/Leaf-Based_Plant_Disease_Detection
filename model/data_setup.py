import torch
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from pathlib import Path
"""
Contain for setting updata with full func to create dataloader
"""

def create_dataloader(
                    dataset_path: Path,
                    batch_size: int,
                    train_transform: transforms.Compose,
                    val_transform: transforms.Compose,
                ):
    train_path = dataset_path / 'train'
    val_path = dataset_path / 'val'
    
    train_data = ImageFolder(
        root= train_path,
        transform= train_transform
    )
    
    val_data = ImageFolder(
        root= val_path,
        transform= val_transform
    )
    
    train_dataloader = DataLoader(
        dataset= train_data,
        batch_size= batch_size,
        shuffle= True
    )
    
    val_dataloader = DataLoader(
        dataset= val_data,
        batch_size= batch_size,
        shuffle= False
    )
    
    class_names = train_data.classes
    return train_dataloader, val_dataloader, class_names
