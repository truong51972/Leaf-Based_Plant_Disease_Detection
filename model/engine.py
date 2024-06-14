import torch
from torchmetrics import Accuracy
from tqdm.auto import tqdm
from model.utils import save_checkpoint

def __train(model: torch.nn.Module,
            dataloader: torch.utils.data.DataLoader,
            loss_func: torch.nn.Module,
            optimizer: torch.optim.Optimizer,
            mectric_func: Accuracy,
            verbose: bool,
            device: str):
    
    train_loss = 0
    train_acc = 0
    
    model.train()

    for _, (X, y) in enumerate(tqdm(dataloader, desc= '-----Train', disable= (not verbose))):
        X, y = X.to(device), y.to(device)

        y_pred = model(X)
        loss = loss_func(y_pred, y)

        train_loss += loss.item()

        optimizer.zero_grad()
        loss.backward()

        optimizer.step()
        y_pred_class = torch.argmax(torch.softmax(y_pred, dim= 1), dim= 1)
        train_acc += mectric_func(y_pred, y).item()

    train_loss /= len(dataloader)
    train_acc /= len(dataloader)
    
    return train_loss, train_acc

def __val(model: torch.nn.Module,
           dataloader: torch.utils.data.DataLoader,
           loss_func: torch.nn.Module,
           mectric_func: Accuracy,
           verbose: bool,
           device: str):

    val_loss = 0
    val_acc = 0
    
    model.eval()
    
    with torch.inference_mode():
        for _, (X, y) in enumerate(tqdm(dataloader, desc= '-------Val', disable= (not verbose))):
            X, y = X.to(device), y.to(device)
            
            y_pred = model(X)
            loss = loss_func(y_pred, y)
            
            val_loss += loss.item()
            
            y_pred_class = torch.argmax(torch.softmax(y_pred, dim= 1), dim= 1)
            val_acc += mectric_func(y_pred, y).item()

        val_loss /= len(dataloader)
        val_acc /= len(dataloader)
        
    return val_loss, val_acc

def __test(model: torch.nn.Module,
           dataloader: torch.utils.data.DataLoader,
           verbose: bool,
           device: str):
    
    model.eval()
    target = torch.tensor([]).to(device)
    preds = torch.tensor([]).to(device)
    score = torch.tensor([]).to(device)
    
    with torch.inference_mode():
        for _, (X, y) in enumerate(tqdm(dataloader, desc= '------Test', disable= (not verbose))):
            X, y = X.to(device), y.to(device)

            
            y_pred = model(X)

            y_probs = torch.softmax(y_pred, dim= 1)
            y_pred_class = torch.argmax(torch.softmax(y_pred, dim= 1), dim= 1)

            y_pred_scores = torch.max(y_probs, dim= 1)[0]

            target = torch.cat((target, y), dim= 0)
            preds = torch.cat((preds, y_pred_class), dim= 0)
            score = torch.cat((score, y_pred_scores), dim= 0)

    test_results = {
        'preds' : preds.tolist(),
        'targets' : target.tolist(),
        'scores' : score.tolist()
    }

    return test_results

def train(model: torch.nn.Module,
          train_dataloader: torch.utils.data.DataLoader,
          val_dataloader: torch.utils.data.DataLoader,
          loss_func: torch.nn.Module,
          optimizer: torch.optim.Optimizer,
          lr_scheduler: torch.optim.lr_scheduler.LRScheduler,
          mectric_funcs: Accuracy,
          epochs: int,
          info_data: list,
          save_checkpoint_freq: int,
          verbose: bool,
          device: str):
    
    temp_model_state_dict = model.state_dict()
    
    if info_data is None:
        results = {
            'train_loss': [],
            'train_acc': [],
            'val_loss': [],
            'val_acc': [],
            'test_results' : {}
        }
    else:
        results = info_data['results']
    
    if epochs <= 0: return results
        
    try:
        torch.manual_seed(42) 
        torch.cuda.manual_seed(42)
        for epoch in tqdm(range(epochs), desc= 'Training', disable=(not verbose)):
            if (verbose):
                print(f"\n\nEpoch: {epoch+1:2} ------------")
            train_loss, train_acc = __train(model=model,
                                            dataloader=train_dataloader,
                                            loss_func=loss_func,
                                            optimizer=optimizer,
                                            mectric_func=mectric_funcs,
                                            verbose= verbose,
                                            device= device)
            lr_scheduler.step()
            val_loss, val_acc = __val(model=model,
                                    dataloader=val_dataloader,
                                    loss_func=loss_func,
                                    mectric_func=mectric_funcs,
                                    verbose= verbose,
                                    device= device)
            
            print(f"Epoch: {epoch+1:2} | Train Loss: {train_loss:.5f} | Train Acc: {train_acc*100:.4f} | Val Loss: {val_loss:.5f} | Val Acc: {val_acc*100:.4f}")
            results["train_loss"].append(train_loss)
            results["train_acc"].append(train_acc)
            results["val_loss"].append(val_loss)
            results["val_acc"].append(val_acc)
    
            if (save_checkpoint_freq != 0) and ((epoch+1) % save_checkpoint_freq == 0):
                save_checkpoint(model= model, num= int((epoch+1) / save_checkpoint_freq))
                
            temp_model_state_dict = model.state_dict()
    except KeyboardInterrupt:
        print('\nStop trainning')
        model.load_state_dict(temp_model_state_dict)
   
    print('\n\n')
    
    return results
    
def test(model: torch.nn.Module,
          test_dataloader: torch.utils.data.DataLoader,
          results: dict,
          verbose: bool,
          device: str):
    
    results["test_results"] = __test(model=model,
                                     dataloader=test_dataloader,
                                     verbose= verbose,
                                     device= device)
    return results
