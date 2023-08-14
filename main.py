import cv2
import albumentations as A
import numpy as np
from utils import plot_examples
from PIL import Image
import os
import json

image = cv2.imread("dataset_13k/train/00001_jpg0001_jpg00010101.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


# transform = A.Compose(
#     [
#     A.ShiftScaleRotate(shift_limit=0, scale_limit=-0.3, rotate_limit=0, p=1),
#     A.Resize(width=416, height=416),
# ], bbox_params=A.BboxParams(format="pascal_voc", min_area=2048,min_visibility=0.3, label_fields=[]))

# image_list = [image]
# saved_bboxes = [bboxes[0]]
#
# for i in range(4):
#     augmentations = transform(image=image, bboxes=bboxes)
#     augmented_img = augmentations["image"]
#
#     if len(augmentations["bboxes"]) == 0:
#         continue
#
#     image_list.append(augmented_img)
#     saved_bboxes.append(augmentations["bboxes"][0])
# plot_examples(image_list, saved_bboxes)

# AUGMENTATION WITHOUT BBOX
transform = A.Compose(
[
    # A.RandomRain(blur_value=3,p=1),
    # A.Blur(blur_limit=(3, 5), p=1),
    # A.RandomGamma(p = 1),
    # A.ChannelShuffle(p=1),
    # A.RGBShift(p=0.5),
    A.Spatter(p=0.5),
    # A.ToSepia(p=0.5),
    # A.UnsharpMask(p=0.5),
    # A.PixelDropout(p=0.5),
    A.Superpixels(p=1),
    # A.CropAndPad(px= 50),
    # A.Resize(width=640, height=640)
])

image_list = [image]


# Định nghĩa đường dẫn
image_folder = 'dataset_9k1/val'
train_json_path = 'dataset_9k1/annotations/val.json'
output_folder = 'dataset_9k1_augmented/val'
output_train_json_path = 'dataset_9k1_augmented/annotations/val.json'


# Load file annoutation
with open(train_json_path, 'r') as json_file:
    data = json.load(json_file)


annotations_data = []
# Lặp qua từng annotation trong train.json
for annotation in data['annotations']:
    image_id = annotation['image_id']
    image_filename = data['images'][image_id]['file_name']
    image_path = os.path.join(image_folder, image_filename)
    image = cv2.imread(image_path)

    transformed = transform(image=image)

    output_path = os.path.join(output_folder, f"{image_filename}")
    cv2.imwrite(output_path, transformed['image'])

    # data['images'][image_id]['file_name'] = f"{image_filename}"
    data['images'][image_id]['height'] = transformed['image'].shape[0]
    data['images'][image_id]['width'] = transformed['image'].shape[1]

    print(f"Added file {image_filename}")


print("Transformation complete.")


with open(output_train_json_path, 'w') as json_file:
    json.dump(data, json_file)

#
# for i in range(16):
#     augmentations = transform(image=image)
#     augmented_img = augmentations["image"]
#     image_list.append(augmented_img)
#
# plot_examples(image_list)