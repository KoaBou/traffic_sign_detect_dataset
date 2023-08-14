import albumentations as A
import cv2
import json
import os

# Định nghĩa đường dẫn
#### Train
# image_folder = 'dataset_13k_folder/dataset_13k_mergered_v3/train'
train_json_path = 'dataset_13k_folder/dataset_13k/old_annotations/train.json'
# output_folder = 'dataset_13k_augmented/train'
output_train_json_path = 'dataset_13k_folder/dataset_13k/annotations/train.json'
# #### Val
# image_folder = 'dataset_13k/val'
# train_json_path = 'dataset_13k/old_annotations/val.json'
# output_folder = 'dataset_13k_augmented/val'
# output_train_json_path = 'dataset_13k_augmented/old_annotations/val.json'

# Load file annoutation
with open(train_json_path, 'r') as json_file:
    data = json.load(json_file)
# Lặp qua từng annotation trong train.json

for annotation in data['annotations']:
    catergory = annotation['category_id']
    if catergory==2:
        annotation['category_id'] = 5
    elif catergory==5:
        annotation['category_id'] = 1
    elif catergory==6:
        annotation['category_id'] = 4
    elif catergory==3:
        annotation['category_id'] = 6
    elif catergory==1:
        annotation['category_id'] = 2
    elif catergory==4:
        annotation['category_id'] = 3


    # output_path = os.path.join(output_folder, f"{image_filename}")
    # cv2.imwrite(output_path, transformed['image'])

with open(output_train_json_path, "w") as f:
        json.dump(data, f)


