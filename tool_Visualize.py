import os
import random
import shutil
import pandas as pd

def move_random(train_path, test_path):
    for category in os.listdir(train_path):
        category_path = os.path.join(train_path, category)
        if os.path.isdir(category_path):
            test_category_path = os.path.join(test_path, category)
            os.makedirs(test_category_path, exist_ok=True)

            # Get all files in the category
            files = os.listdir(category_path)
            
            # Randomly select a subset of files to move to test set
            num_files_to_move = int(len(files) * 0.2)  # Adjust the percentage as needed
            files_to_move = random.sample(files, num_files_to_move)
            
            for file_name in files_to_move:
                src_file = os.path.join(category_path, file_name)
                dst_file = os.path.join(test_category_path, file_name)
                
                # Move the file
                shutil.move(src_file, dst_file)

    print("Files have been moved to the test set.")
    
def count_files(file_path):
    file_counts = {}

    for category in os.listdir(file_path):
        category_path = os.path.join(file_path, category)
        if os.path.isdir(category_path):
            num_files = len(os.listdir(category_path))
            file_counts[category] = num_files
    file_counts_df = pd.DataFrame(list(file_counts.items()), columns=['Category', 'File Count'])
    print(file_counts_df)