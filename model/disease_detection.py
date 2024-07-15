import torch

import cv2
import numpy as np
import pandas as pd
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt

from model.sam_model import Sam_model
from model.cnn_model import Cnn_model
from model.grad_cam import Grad_cam

import asyncio

class AI_model:
    def __init__(self, paths_to_model: dict):
        """
        Args:
            paths_to_model : dict = {'model_name', 'path/to/model'}
        """
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        print(f"Device: {self.device}")
        self.sam_model = Sam_model(device= self.device)

        self.cnn_models = {}
        self.grad_cam_models = {}
        
        for model_name, path_to_model in paths_to_model.items():
            try:
                cnn_model = Cnn_model(path_to_model=path_to_model, device= self.device)
                
                self.cnn_models[model_name] = cnn_model
                self.grad_cam_models[model_name] = Grad_cam(model=cnn_model.get_model(), model_name= cnn_model.model_name)
            except FileNotFoundError:
                print(f'[ERROR] Model not found in {path_to_model}')
        try:
            self.best_threshold_df = pd.read_excel(path_to_model + '/best_threshold.xlsx', index_col=0)
        except:
            self.best_threshold_df = None
            
    def class_name_to_idx(self, class_name: str, model_name: str | None = None, verbose: bool = False):
        if model_name is not None:
            print(f"[WARNING] '{model_name}' is not defined!")
        cnn_model = self.cnn_models.get(model_name, list(self.cnn_models.values())[0])
        return cnn_model.class_name_to_idx[class_name]
        
    def _predict(self, img: Image, model_name: str | None = None, verbose: bool = False):
        pointed_img = self.sam_model.plot_points(img)
        removed_bg_img = self.sam_model.remove_bg(img)

        if verbose and (model_name not in self.cnn_models.keys()):
            if model_name is not None:
                print(f"[WARNING] '{model_name}' is not defined!")
            print(f"[WARNING] Using '{list(self.cnn_models.keys())[0]}' model!")
            
        cnn_model = self.cnn_models.get(model_name, list(self.cnn_models.values())[0])
        grad_cam = self.grad_cam_models.get(model_name, list(self.grad_cam_models.values())[0])
            
        predict_logit, predicted_class, score = cnn_model._predict(removed_bg_img)

        grayscale_cam, visualization = grad_cam.visualize(removed_bg_img, predict_logit, threshold= 0.5)
        
        results = {
            "image" : img,
            "pointed_img" : pointed_img,
            "removed_bg_img": removed_bg_img,
            "predicted_image" : visualization,
            'heatmap': grayscale_cam,
            "class_name" : predicted_class,
            "score" : score
        }
        return results
        
    async def predict(self, img: Image, model_name: str | None = None, verbose: bool = False):
        """
        Args:
            img: PIL.Image()
            model_name : str
        Returns:
            dict: {
                "image" : PIL.Image(),
                "pointed_img" PIL.Image(): 
                "removed_bg_img": PIL.Image(),
                "predicted_image" : PIL.Image(),
                'heatmap': array,
                "class_name" : int,
                "score" : float,
                "threshold" : float,                
            }
        """
        results = self._predict(img, model_name, verbose)
        
        if self.best_threshold_df is not None:           
            cnn_model = self.cnn_models.get(model_name, list(self.cnn_models.values())[0])
                
            class_idx = cnn_model.class_name_to_idx[results["class_name"]]
            results['threshold'] = self.best_threshold_df.loc['threshold', class_idx]
        
        return results
