import os
from pathlib import Path
import matplotlib.pyplot as plt
import torch

def plot_loss_curves(results: dict[str, list[float]]):
    
    # Get the loss values of the results dictionary (training and val)
    train_loss = results['train_loss']
    val_loss = results['train_loss']
    # Get the accuracy values of the results dictionary (training and val)
    train_accuracy = results['train_acc']
    val_accuracy = results['val_acc']

    # Figure out how many epochs there were
    epochs = range(len(results['train_loss']))

    # Setup a plot 
    plt.figure(figsize=(15, 7))

    # Plot loss
    plt.subplot(1, 2, 1)
    plt.plot(epochs, train_loss, label='train_loss')
    plt.plot(epochs, val_loss, label='val_loss')
    plt.title('Loss')
    plt.xlabel('Epochs')
    plt.legend()

    # Plot accuracy
    plt.subplot(1, 2, 2)
    plt.plot(epochs, train_accuracy, label='train_accuracy')
    plt.plot(epochs, val_accuracy, label='val_accuracy')
    plt.title('Accuracy')
    plt.xlabel('Epochs')
    plt.legend()
    return plt

def save_model(model: torch.nn.Module,
               results: dict[str, list[float]]):
    
    graph = plot_loss_curves(results)
    
    target_dir = Path('runs/classify/')
    model_name = 'model.pth'
    graph_name = 'loss.jpg'
    
    train_paths = os.listdir(target_dir)
    print(train_paths)
    
    i = 0
    
    while True:
        train_path = f'train{i}'
        if train_path not in train_paths:
            break
        else:
            i += 1

    target_dir = target_dir / train_path
    
    target_dir_path = Path(target_dir)
    target_dir_path.mkdir(parents=True,
                        exist_ok=True)
    
    model_save_path = target_dir_path / model_name
    graph_save_path = target_dir_path / graph_name
    
    print(f"[INFO] Saving model to: {target_dir}")
    graph.savefig('graph_save_path')
    torch.save(obj=model.state_dict(),
             f=model_save_path)
