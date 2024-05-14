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
    """Creates training and testing DataLoaders.
    
    Takes in a dataset directory path and turns
    them into PyTorch Datasets and then into PyTorch DataLoaders.
    
    Args:
        dataset_path: Path to dataset directory.
        batch_size: Number of samples per batch in each of the DataLoaders.
        train_transform: torchvision transforms to perform on training data.
        train_transform: torchvision transforms to perform on validation data.
    
    Returns:
        A tuple of (train_dataloader, test_dataloader, class_names).
        Where class_names is a list of the target classes.
    Example usage:
      train_dataloader, test_dataloader, class_names = \
        = create_dataloaders(train_dir=path/to/train_dir,
                             test_dir=path/to/test_dir,
                             transform=some_transform,
                             batch_size=32,
                             num_workers=4)
    """
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
