from model import train

if __name__ == '__main__':
    config = {
        'dataset' : {
            'dataset_path':'./datasets/tomato',
            'folder_train': 'train',
            'folder_val': 'val',    
            'folder_test': 'test',
            'batch_size': 32,
        },
        'train_para': {
            'pretrain_model_path': None,
            'epochs': 20,
            'optimize' : {
                'learning_rate': 0.001,
                'momentum': 0.9,
                'weight_decay': 0.0001,
            },
            'lr_scheduler' : {
                'step_size' : 5,
                'gamma' : 0.5,
            },
            'save_checkpoint_freq' : 2,
        },
        'save_para': {
            'model_name': 'model.pth',
            'graph_loss_name': 'loss_acc.jpg',
            'graph_confmat_name': 'confusion_matrix.jpg',
            'info_file_name': 'info.json'
        }
    }

    train.run(**config)