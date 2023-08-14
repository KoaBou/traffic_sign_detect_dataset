import albumentations as A
import cv2
import json
import os

# Các phương pháp biến đổi
transform = A.Compose([
    A.OneOf([
        A.Blur(blur_limit=(3, 4),p = 0.5),
        A.ISONoise(p = 0.5)
    ], p = 0.7),
    A.OneOf([
        A.RandomBrightnessContrast(p = 0.5),
        A.RandomRain(blur_value = 3, p = 0.4),
        A.RandomGamma(p = 0.5)
    ], p = 0.5),
    A.OneOf([
        A.ChannelShuffle(p = 0.5),
        A.RGBShift(p = 0.5),
        A.ToGray(p = 0.5)
    ], p = 0.5),
    # A.ShiftScaleRotate(shift_limit=0, scale_limit=(-0.3, 0.2), rotate_limit=0, p=0.7),
    # A.Resize(416, 416),
])

# # Định nghĩa đường dẫn
image_folder = 'dataset_14k_folder/dataset_14k/train'
train_json_path = 'dataset_14k_folder/dataset_14k/annotations/train.json'
output_folder = 'dataset_14k_folder/dataset_14k_augmented/train'
output_train_json_path = 'dataset_14k_folder/dataset_14k_augmented/annotations/train.json'
# #### Val
# image_folder = 'dataset_14k_folder/dataset_14k/val'
# train_json_path = 'dataset_14k_folder/dataset_14k/annotations/val.json'
# output_folder = 'dataset_14k_folder/dataset_14k_augmented/val'
# output_train_json_path = 'dataset_14k_folder/dataset_14k_augmented/annotations/val.json'

# Load file annoutation
with open(train_json_path, 'r') as json_file:
    data = json.load(json_file)
# Lặp qua từng annotation trong train.json

for item in data['images']:
    image_filename = item['file_name']
    image_path = os.path.join(image_folder, image_filename)
    image = cv2.imread(image_path)

    # bboxes = annotation['bbox']
    # category_id = annotation['category_id']

    transformed = transform(image=image)

    output_path = os.path.join(output_folder, f"{image_filename}")
    cv2.imwrite(output_path, transformed['image'])
    print(f"Augmented {item['id']}")

    # # data['images'][image_id]['file_name'] = f"{image_filename}"
    # data['images'][image_id]['height'] = transformed['image'].shape[0]
    # data['images'][image_id]['width'] = transformed['image'].shape[1]
    #
    # # if 'bboxes' in transformed and len(transformed['bboxes']) > 0:
    # #     annotation['bbox'] = transformed['bboxes'][0]
    # i = i + 1
    # print(i)


print("Transformation complete.")

with open(output_train_json_path, 'w') as json_file:
    json.dump(data, json_file)