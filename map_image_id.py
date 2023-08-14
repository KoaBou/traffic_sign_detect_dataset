import json
import os

# Đọc dữ liệu từ tập tin JSON

train_json_path = 'dataset_13k_folder/dataset_13k_filtered/annotations/val.json'

with open(train_json_path, 'r') as json_file:
    data = json.load(json_file)

new_id = 0
id_mapping = {}

# Duyệt qua mảng images để cập nhật lại trường id và tạo ánh xạ id cũ sang id mới
for image in data["images"]:
    old_id = image["id"]
    if old_id not in id_mapping:
        print(f"Add new id {old_id} to {new_id}")
        id_mapping[old_id] = new_id
        image["id"] = new_id
        new_id += 1

# Cập nhật các trường image_id trong mảng annotations
for annotation in data["annotations"]:
    old_image_id = annotation["image_id"]
    new_image_id = id_mapping[old_image_id]
    annotation["image_id"] = new_image_id

# Lưu dữ liệu đã được cập nhật vào tập tin mới
output_json_file = 'dataset_13k_folder/dataset_13k_filtered/annotations/val.json'
with open(output_json_file, "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Updated JSON file saved.")
