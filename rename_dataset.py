import os
from pathlib import Path
import random

def rename_class(path):
    class_names = os.listdir(path)

    for class_name in class_names:
        new_name = class_name.split('___')[1].replace(' ', '_')
        os.rename(path / class_name, path / new_name)
        # print(path / new_name)

def rename_img(path):
    class_names = os.listdir(path)

    for class_name in class_names:
        img_names = os.listdir(path / class_name)
        for img_name in img_names:
            extension = img_name[-4:]
            img_path = path / class_name / img_name
            new_img_path = path / class_name / (str(random.random())[2:] + extension)

            os.rename(img_path, new_img_path)
            # break
if __name__ == '__main__':
    datasets_path = Path('./datasets/tomato')
    # rename_class(datasets_path / 'train')
    # rename_class(datasets_path / 'val')

    rename_img(datasets_path / 'train')
    rename_img(datasets_path / 'val')
