import albumentations as A
import cv2
import json
import os

# Các phương pháp biến đổi
transform = A.Compose([
    A.RandomCrop(height=280, width=280, p=0.5),
    A.ShiftScaleRotate(rotate_limit=70, border_mode=1, p=0.5),
    A.Resize(416, 416),
], bbox_params=A.BboxParams(format='coco', label_fields=['category_id'], min_area= 512, min_visibility=0.3))
# Định nghĩa đường dẫn
image_folder = 'dataset_9k1/val'
train_json_path = 'dataset_9k1/annotations/val.json'
output_folder = 'dataset_9k1_spatial/val'
output_train_json_path = 'dataset_9k1_spatial/annotations/val.json'


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

    bboxes = annotation['bbox']
    category_id = annotation['category_id']
    try:
        transformed = transform(image=image, bboxes=[bboxes], category_id=[category_id])
    except:
        continue

    if 'bboxes' in transformed and len(transformed['bboxes']) > 0:
        output_path = os.path.join(output_folder, f"{image_filename}")
        cv2.imwrite(output_path, transformed['image'])

        # data['images'][image_id]['file_name'] = f"{image_filename}"
        data['images'][image_id]['height'] = transformed['image'].shape[0]
        data['images'][image_id]['width'] = transformed['image'].shape[1]

        annotation['bbox'] = transformed['bboxes'][0]
        annotations_data.append(annotation)
        print(f"Added file {image_filename}")
    else:
        print(f"Dropped file {image_filename}")



print("Transformation complete.")

new_data = {
    "images": data['images'],
    "categories": data['categories'],
    "annotations": annotations_data,
}

with open(output_train_json_path, 'w') as json_file:
    json.dump(new_data, json_file)
