import os
from pathlib import Path
import torch
import json
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score

def plot_loss_curves(results: dict[str, list[float]]):
    train_loss = results['train_loss']
    val_loss = results['val_loss']
    train_accuracy = results['train_acc']
    val_accuracy = results['val_acc']

    epochs = range(len(results['train_loss']))

    plt.figure(figsize=(14, 5))

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

def plot_confmat(class_names, y_true, y_pred):
    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')
    f1 = f1_score(y_true, y_pred, average='macro')
    
    table = confusion_matrix(y_true=y_true, y_pred=y_pred)
    plt.figure(figsize=(7.5, 5))
    sns.heatmap(table, annot=True, fmt='.0f', cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    plt.text(x=12.5, y=0.5, s= f'Metric:')
    plt.text(x=12.5, y=1, s= f' - Precision: {round(precision, 3)}')
    plt.text(x=12.5, y=1.5, s= f' - Recall: {round(recall, 3)}')
    plt.text(x=12.5, y=2, s= f' - F1 score: {round(f1, 3)}')

    plt.text(x=12.5, y=3, s= f'Class names:')
    for i, class_name in enumerate(class_names):
        plt.text(x=12.5, y=3.5+(i/2), s= f' {i}. {class_name[:15]}{"..." if len(class_name) > 15 else ""}')

    plt.tight_layout()
    return plt

def save_model(model: torch.nn.Module,
               results: dict[str, list[float]],
               class_names: list,
               device: str,
               **kwargs):
    
    preds = results['test_results']['preds']
    targets = results['test_results']['targets']    
    
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

    graph_confmat = plot_confmat(class_names=class_names, y_true= targets, y_pred=preds)
    graph_confmat.savefig(graph_confmat_save_path)
    
    torch.save(obj=model.state_dict(), f=model_save_path)

def save_checkpoint(model: torch.nn.Module, num: int):
    target_path = Path('runs/classify/')
    target_path.mkdir(parents=True, exist_ok=True)

    checkpoint_dir = target_path / 'checkpoints'
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    checkpoint_names = os.listdir(checkpoint_dir)
    
    checkpoint_name = f'.checkpoint_{num}.pth'

    checkpoint_path = checkpoint_dir / checkpoint_name
    torch.save(obj=model.state_dict(), f=checkpoint_path)

    print(f'Save checkpoint to {checkpoint_path}')
