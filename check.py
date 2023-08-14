import albumentations as A
import cv2
import json
import os



# Định nghĩa đường dẫn
#### Train
image_folder = 'dataset_13k_filtered/train'
train_json_path = 'dataset_13k_filtered/annotations/train.json'
# output_folder = 'dataset_13k_augmented/train'
# output_train_json_path = 'dataset_13k_augmented/old_annotations/train.json'
# #### Val
# image_folder = 'dataset_13k/val'
# train_json_path = 'dataset_13k/old_annotations/val.json'
# output_folder = 'dataset_13k_augmented/val'
# output_train_json_path = 'dataset_13k_augmented/old_annotations/val.json'

# Load file annoutation
with open(train_json_path, 'r') as json_file:
    data = json.load(json_file)
# Lặp qua từng annotation trong train.json
i = 0
for annotation in data['annotations']:
    image_id = annotation['image_id']
    print(image_id)
    image_filename = data['images'][image_id]['file_name']
    image_path = os.path.join(image_folder, image_filename)
    image = cv2.imread(image_path)
    # if image_id == i:
    #     i += 1
    #     continue
    # else:
    #     print(f"Thieu {image_id}")
    #     break

    # bboxes = annotation['bbox']
    # category_id = annotation['category_id']

    # transformed = transform(image=image)

    # output_path = os.path.join(output_folder, f"{image_filename}")
    # cv2.imwrite(output_path, transformed['image'])



