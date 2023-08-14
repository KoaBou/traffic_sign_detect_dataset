import albumentations as A
import cv2
import json
import os

# Các phương pháp biến đổi
transform = A.Compose([
    A.OneOf([
        A.Blur(blur_limit=(3, 4),p=0.5),
        A.ISONoise(p=0.5),
        A.GaussNoise(p=0.5)
    ], p=0.4),
    A.OneOf([
        A.RandomBrightnessContrast(p=0.5),
        A.RandomGamma(p=0.5)
    ], p=0.2),
    A.OneOf([
        A.OneOf([
        A.RandomFog(p=0.5),
        A.RandomSnow(p=0.5),
        # A.RandomSunFlare(p=0.5),
        A.RandomShadow(p=0.5),
        A.RandomRain(p=0.5),
        ], p=0.9),
        A.OneOf([
        A.ChannelShuffle(p=0.5),
        A.RGBShift(p=0.5),
        A.HueSaturationValue(p=0.5)
        ], p=0.2),
    ]),
    # A.ShiftScaleRotate(shift_limit=0, scale_limit=(-0.3, 0.2), rotate_limit=0, p=0.7),
    A.Resize(416, 416),
])

# Định nghĩa đường dẫn
image_folder = 'dataset_9k1/val'
train_json_path = 'dataset_9k1/annotations/val.json'
output_folder = 'dataset_9k1_pixel/val'
output_train_json_path = 'dataset_9k1_pixel/annotations/val.json'


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
