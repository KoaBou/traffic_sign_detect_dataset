import albumentations as A
import cv2
import json
import os

# Định nghĩa đường dẫn
classes = {1: 'stop', 2: 'left', 3: 'right', 4: 'straight', 5: 'no_left', 6: 'no_right'}



# #### Val
# image_folder = 'dataset_13k/val'
# train_json_path = 'dataset_13k/old_annotations/val.json'
# output_folder = 'dataset_13k_augmented/val'
# output_train_json_path = 'dataset_13k_augmented/old_annotations/val.json'

# Load file annoutation
def take_class():
    with open(train_json_path, 'r') as json_file:
        data = json.load(json_file)
# Lặp qua từng annotation trong train.json

    for annotation in data['annotations']:
        catergory = annotation['category_id']
        if catergory == category_id:
            image_id = annotation['image_id']
            image_filename = data['images'][image_id]['file_name']
            image_path = f"{image_folder}/{image_filename}"
            image = cv2.imread(image_path)


            bbox = annotation['bbox']  # [x, y, width, height]
            x, y, width, height = map(int, bbox)
            cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)  # Màu xanh lá cây, độ dày viền 2

            output_path = os.path.join(output_folder, f"{image_filename}")
            cv2.imwrite(output_path, image)
            print(f"Taken image {image_id} from class {classes[category_id]}")



#### Train
for category_id in range(1,7):
    image_folder = 'dataset_14k_folder/dataset_14k_mergered/train'
    train_json_path = 'dataset_14k_folder/dataset_14k_mergered/annotations/train.json'
    output_folder = f'Classes_14k/train/{classes[category_id]}'
    take_class()

#### Val
    image_folder = 'dataset_14k_folder/dataset_14k_mergered/val'
    train_json_path = 'dataset_14k_folder/dataset_14k_mergered/annotations/val.json'
    output_folder = f'Classes_14k/val/{classes[category_id]}'
    take_class()

