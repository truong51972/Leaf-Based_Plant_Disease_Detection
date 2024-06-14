import torch

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt

from segment_anything import sam_model_registry, SamPredictor

class Sam_model:
    def __init__(self, model_type = "vit_l", sam_checkpoint = "./sam/sam_vit_l_0b3195.pth"):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        sam = sam_model_registry[model_type](checkpoint=sam_checkpoint)
        sam.to(device=self.device)
        
        self.predictor = SamPredictor(sam)

        mp_point = 40
        input_point_focus = np.array([[128, 128], [128-mp_point, 128], [128+mp_point, 128], [128, 128-mp_point], [128, 128+mp_point]])
        input_label_focus = np.array([1, 1, 1, 1, 1])

        mp_point = 20
        input_point_ignore = np.array([[mp_point, mp_point], [mp_point, 256-mp_point], [256-mp_point, mp_point], [256-mp_point, 256-mp_point]])
        input_label_ignore = np.array([0, 0, 0, 0])

        self.input_point = np.concatenate([input_point_focus, input_point_ignore], axis= 0)
        self.input_label = np.concatenate([input_label_focus, input_label_ignore], axis= 0)
        
    def remove_noise(self, mask, kernel= (5, 5), iters= [1, 1]):
        mask = mask.transpose(1, 2, 0).astype(np.uint8)
        kernel = np.ones(kernel, np.uint8)
    
        iter = iters[0]
        dilated_mask = cv2.dilate(mask, kernel, iterations=iter)
        eroded_mask = cv2.erode(dilated_mask, kernel, iterations=iter)
        
        iter = iters[1]
        eroded_mask = cv2.erode(eroded_mask, kernel, iterations=iter)
        dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=iter)
    
        return dilated_mask

    def plot_points(self, image, radius=3):
        image = np.array(image)
        for i in range(len(self.input_label)):
            x = self.input_point[i, 0]
            y = self.input_point[i, 1]

            color = (0, 255, 0) if self.input_label[i] == 1 else (255, 0, 0)
            
            image = cv2.circle(image, (x, y), radius=radius, color=color, thickness=-1)
            
        image = Image.fromarray(image)
        return image

    # @time_decorator
    def remove_bg(self, image):
        image = np.array(image)
        self.predictor.set_image(image)
        
        mask, score, logit = self.predictor.predict(
            point_coords=self.input_point,
            point_labels=self.input_label,
            multimask_output=False,
        )

        mask = self.remove_noise(mask)
        removed_bg_img = cv2.bitwise_and(image, image, mask= mask)
        
        removed_bg_img = Image.fromarray(removed_bg_img)

        return removed_bg_img
