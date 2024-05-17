import torch
from torchvision import transforms

import numpy as np
from PIL import Image
from pathlib import Path

from model.model_builder import resnet50_model

from pytorch_grad_cam import GradCAM, HiResCAM, ScoreCAM, GradCAMPlusPlus, AblationCAM, XGradCAM, EigenCAM, FullGrad
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import asyncio

class AI_model:
    def __init__(self, path_to_model: str):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        self.model, info_data = resnet50_model(pretrain_model_path= path_to_model)
        self.class_names = info_data['class_names']

        self.img_transform = transforms.Compose([
            transforms.Resize(size= 224),
            transforms.ToTensor()
        ])

        target_layers = [self.model.layer4[-1]]
        self.cam = GradCAM(model=self.model, target_layers=target_layers)
        # self.cam = ScoreCAM(model=self.model, target_layers=target_layers)
        
    async def predict(self, img: Image):   
        img_tensor = self.img_transform(img)
        img_tensor_in_batch = img_tensor.unsqueeze(dim= 0)
        
        rgb_img = img_tensor.permute(1, 2, 0).numpy()
        
        
        
        self.model.eval()
        with torch.inference_mode():
            
            
            predict = self.model(img_tensor_in_batch)
            soft_max_persent = torch.softmax(predict, dim= 1)
            predicted_class = self.class_names[torch.argmax(predict, dim= 1)]

            
            
            probability = (soft_max_persent[0, torch.argmax(predict, dim= 1)].item())
            # print(predicted_class)
            
        targets = [ClassifierOutputTarget(torch.argmax(predict, dim= 1).item())]
        grayscale_cam = self.cam(input_tensor=img_tensor_in_batch, targets= targets)
        visualization = show_cam_on_image(rgb_img, grayscale_cam[0], use_rgb=True)

        results = {
            "image" : img,
            "predicted_image" : Image.fromarray(visualization),
            "class_name" : predicted_class,
            "class_prob" : probability
        }
        return results
        
