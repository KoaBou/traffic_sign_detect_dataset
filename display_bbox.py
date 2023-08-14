import cv2
import json

# Đọc dữ liệu từ file JSON (thay đổi thành dữ liệu JSON của bạn)
with open('dataset_9k_folder/dataset_9k/annotations/train.json', 'r') as json_file:
    data = json.load(json_file)

# Đường dẫn thư mục chứa ảnh và nơi để lưu ảnh với bounding box
image_folder = 'dataset_9k_folder/dataset_9k/train'
output_folder = 'dataset_9k_folder/dataset_9k_with_bbox/train'

# Lặp qua mỗi annotation trong danh sách
# for annotation in data['old_annotations']:
#     image_id = annotation['image_id']
#     bbox = annotation['bbox']  # [x, y, width, height]
#
#     # Đọc ảnh tương ứng
#     image_filename = data['images'][image_id]['file_name']
#     image_path = f"{image_folder}/{image_filename}"
#     image = cv2.imread(image_path)
#
#     # Vẽ bounding box lên ảnh
#     x, y, width, height = map(int, bbox)
#     cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)  # Màu xanh lá cây, độ dày viền 2
#
#     # Lưu ảnh với bounding box vào thư mục đầu ra
#     output_path = f"{output_folder}/{image_filename}"
#     cv2.imwrite(output_path, image)
for item in data['images']:
    image_id = item['id']
    # Đọc ảnh
    image_filename = data['images'][image_id]['file_name']
    image_path = f"{image_folder}/{image_filename}"
    image = cv2.imread(image_path)

    for annotation in data['annotations']:
        if annotation['image_id'] != image_id:
            continue
        bbox = annotation['bbox']  # [x, y, width, height]

        # Đọc ảnh tương ứng


        # Vẽ bounding box lên ảnh
        x, y, width, height = map(int, bbox)
        cv2.rectangle(image, (x, y), (x + width, y + height), (0, 255, 0), 2)  # Màu xanh lá cây, độ dày viền 2

        # Lưu ảnh với bounding box vào thư mục đầu ra
    output_path = f"{output_folder}/{image_filename}"
    cv2.imwrite(output_path, image)
    print(f"Displayed image {image_id}")
print("Images with bounding boxes saved.")
