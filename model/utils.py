import os
from pathlib import Path
import torch
import json
import matplotlib.pyplot as plt
import seaborn as sns

from torchmetrics import ConfusionMatrix

def plot_loss_curves(results: dict[str, list[float]]):
    train_loss = results['train_loss']
    val_loss = results['val_loss']
    train_accuracy = results['train_acc']
    val_accuracy = results['val_acc']

    epochs = range(len(results['train_loss']))

    plt.figure(figsize=(15, 7))

    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_loss, label='train_loss')
    plt.plot(epochs, val_loss, label='val_loss')
    plt.title('Loss')
    plt.xlabel('Epochs')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, train_accuracy, label='train_accuracy')
    plt.plot(epochs, val_accuracy, label='val_accuracy')
    plt.title('Accuracy')
    plt.xlabel('Epochs')
    plt.legend()
    return plt

def plot_confmat(table):
    plt.figure(figsize=(11, 8))
    sns.heatmap(table, annot=True, fmt='.0f')
    plt.title('Confusion Matrix')

    return plt

def save_model(model: torch.nn.Module,
               results: dict[str, list[float]],
               class_names: list,
               device: str,
               **kwargs):

    confmat = ConfusionMatrix(task="multiclass", num_classes= len(class_names)).to(device)
    
    preds = torch.tensor(results['test_results']['preds']).to(device)
    target = torch.tensor(results['test_results']['target']).to(device)
    table = confmat(preds, target).tolist()
    
    
    
    target_dir = Path('runs/classify/')
    target_dir.mkdir(parents=True, exist_ok=True)
    
    model_name = kwargs['save_para']['model_name']
    graph_loss_name = kwargs['save_para']['graph_loss_name']
    graph_confmat_name = kwargs['save_para']['graph_confmat_name']
    info_file_name = kwargs['save_para']['info_file_name']
    
    train_paths = os.listdir(target_dir)
    
    i = 0
    
    while True:
        train_path = f'train{i}'
        if train_path not in train_paths:
            break
        else:
            i += 1

    target_dir = target_dir / train_path
    
    target_dir_path = Path(target_dir)
    target_dir_path.mkdir(parents=True,exist_ok=True)
    
    model_save_path = target_dir_path / model_name
    graph_loss_save_path = target_dir_path / graph_loss_name
    graph_confmat_save_path = target_dir_path / graph_confmat_name
    info_save_path = target_dir_path / info_file_name
    
    print(f"[INFO] Saving model to: {target_dir}")
    
    info_data = {
        "class_names" : class_names,
        "results" : results
    }
    
    with open(info_save_path, 'w') as f:
        json.dump(info_data, f, indent=4)
        
    graph_loss = plot_loss_curves(results)
    graph_loss.savefig(graph_loss_save_path)

    graph_confmat = plot_confmat(table)
    graph_confmat.savefig(graph_confmat_save_path)
    
    torch.save(obj=model.state_dict(), f=model_save_path)
