import os
import random
import shutil
import pandas as pd
import cv2
import numpy as np

def split_train_test(root_dir, train_dir, test_dir, test_ratio=0.2):
    """
    Chuyển một tỷ lệ xác định các tệp từ thư mục `train_dir` sang thư mục `test_dir`.
    
    :param root_dir: Thư mục gốc chứa thư mục train và test.
    :param train_dir: Tên thư mục chứa dữ liệu train.
    :param test_dir: Tên thư mục chứa dữ liệu test.
    :param test_ratio: Tỷ lệ phần trăm dữ liệu được chuyển từ train sang test.
    """
    train_path = os.path.join(root_dir, train_dir)
    test_path = os.path.join(root_dir, test_dir)
    
    if not os.path.exists(test_path):
        os.makedirs(test_path)
    
    # Duyệt qua các lớp trong thư mục train
    for class_name in os.listdir(train_path):
        class_train_path = os.path.join(train_path, class_name)
        class_test_path = os.path.join(test_path, class_name)
        
        if not os.path.exists(class_test_path):
            os.makedirs(class_test_path)
        
        # Danh sách các tệp trong lớp hiện tại
        files = os.listdir(class_train_path)
        random.shuffle(files)
        
        # Số lượng tệp cần chuyển
        num_files_to_move = int(len(files) * test_ratio)
        
        # Chuyển các tệp
        for file_name in files[:num_files_to_move]:
            shutil.move(os.path.join(class_train_path, file_name), os.path.join(class_test_path, file_name))
            
    print("Đã chuyển dữ liệu thành công.")

    
def count_files(file_path):
    file_counts = {}

    for category in os.listdir(file_path):
        category_path = os.path.join(file_path, category)
        if os.path.isdir(category_path):
            num_files = len(os.listdir(category_path))
            file_counts[category] = num_files
    file_counts_df = pd.DataFrame(list(file_counts.items()), columns=['Category', 'File Count'])
    print(file_counts_df)

def read_image(file_path):
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if image is not None:
        return cv2.resize(image, (100, 100)).flatten()  # Resize the image to a smaller size for faster comparison
    else:
        print(f"Error reading image: {file_path}")
        return None

def images_are_identical(img1, img2):
    return np.array_equal(img1, img2)

def remove_same_image_folder(image_folder):
    images = []
    file_names = []

    for file_name in os.listdir(image_folder):
        if file_name.endswith(('.png', '.jpg', '.jpeg', '.JPG')):
            file_path = os.path.join(image_folder, file_name)
            image = read_image(file_path)
            if image is not None:
                images.append(image)
                file_names.append(file_path)

    print(file_names)
    duplicate_files = set()

    for i in range(len(images)):
        if i in duplicate_files:
            continue
        for j in range(i + 1, len(images)):
            if j in duplicate_files:
                continue
            if images_are_identical(images[i], images[j]):
                duplicate_files.add(j)
                print(f"Duplicate found: {file_names[j]}")

    # Remove duplicate images
    for index in duplicate_files:
        print(f"Removing: {file_names[index]}")
        os.remove(file_names[index])

    print(f"Removed {len(duplicate_files)} duplicate images.")