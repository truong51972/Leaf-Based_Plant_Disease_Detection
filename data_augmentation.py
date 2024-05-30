import cv2
import os
import random
import numpy as np

def change_brightness(image, value=None):
    if value is None:
        value = random.randint(-30, 30)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, value)
    v = np.clip(v, 0, 255)
    final_hsv = cv2.merge((h, s, v))
    image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return image

def flip_image(image):
    flip_code = random.choice([-1, 0, 1])  # -1: both, 0: vertical, 1: horizontal
    return cv2.flip(image, flip_code)

def change_contrast(image, alpha=None, beta=0):
    if alpha is None:
        alpha = random.uniform(0.5, 1.5)
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return image

def augment_image(image, num_augmentations=5):
    augmented_images = []
    
    for _ in range(num_augmentations):
        aug_image = image.copy()
        
        # Apply random brightness change
        if random.choice([True, False]):
            aug_image = change_brightness(aug_image)
        
        # Apply random flip
        if random.choice([True, False]):
            aug_image = flip_image(aug_image)
        
        # Apply random contrast change
        if random.choice([True, False]):
            aug_image = change_contrast(aug_image)
        
        augmented_images.append(aug_image)
    
    return augmented_images

def save_augmented_images(folder_path, output_folder, num_augmentations=3):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for label in os.listdir(folder_path):
        label_folder = os.path.join(folder_path, label)
        if os.path.isdir(label_folder):
            label_output_folder = os.path.join(output_folder, label)
            if not os.path.exists(label_output_folder):
                os.makedirs(label_output_folder)
            for image_file in os.listdir(label_folder):
                if image_file.endswith(('.jpg', '.jpeg', '.png','.JPG')):
                    file_path = os.path.join(label_folder, image_file)
                    image = cv2.imread(file_path)
                    if image is not None:
                        # Original image
                        output_file_path = os.path.join(label_output_folder, os.path.splitext(image_file)[0] + '_original.jpg')
                        cv2.imwrite(output_file_path, image)
                        
                        # Augmented images
                        augmented_images = augment_image(image, num_augmentations)
                        for idx, aug_image in enumerate(augmented_images):
                            output_file_path = os.path.join(label_output_folder, os.path.splitext(image_file)[0] + f'_aug_{idx}.jpg')
                            cv2.imwrite(output_file_path, aug_image)

# Sử dụng hàm để lưu ảnh augment vào các thư mục
train_folder_path = "tomato/train"
output_folder_path = "tomato/train_aug"
save_augmented_images(train_folder_path, output_folder_path, num_augmentations=3)
