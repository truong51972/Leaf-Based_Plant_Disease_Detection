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
    def __init__(self, path_to_model: str):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.sam_model = Sam_model()
        
        self.cnn_model = Cnn_model(path_to_model=path_to_model)

        model = self.cnn_model.get_model()
        self.grad_cam = Grad_cam(model=model)

        try:
            self.best_threshold_df = pd.read_excel(path_to_model + '/best_threshold.xlsx', index_col=0)
        except:
            self.best_threshold_df = None
            
    def _predict(self, img: Image):
        pointed_img = self.sam_model.plot_points(img)
        removed_bg_img = self.sam_model.remove_bg(img)
        
        predict, predicted_class, probability = self.cnn_model.predict(removed_bg_img)

        grayscale_cam, visualization = self.grad_cam.visualize(removed_bg_img, predict, threshold= 0.5)
        
        results = {
            "image" : img,
            "pointed_img" : pointed_img,
            "removed_bg_img": removed_bg_img,
            "predicted_image" : visualization,
            'heatmap': grayscale_cam,
            "class_name" : predicted_class,
            "score" : probability
        }
        return results
        
    async def predict(self, img: Image):
        results = self._predict(img)
        
        if self.best_threshold_df is not None:
            class_idx = self.cnn_model.class_name_to_idx[results["class_name"]]
            results['threshold'] = self.best_threshold_df.loc['threshold', class_idx]
        
        return results
