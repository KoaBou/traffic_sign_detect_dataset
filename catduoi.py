import os
import json
import shutil

# Hàm kiểm tra trùng lặp tên file ảnh
def is_duplicate_name(new_name, existing_names):
    return new_name in existing_names

# Đường dẫn đến thư mục chứa ảnh (thay đổi đường dẫn này theo đúng vị trí của thư mục chứa ảnh của bạn)
# #### Train_augmented
# image_folder = "dataset_9k_folder/dataset_9k_augmented/train"
# input_json = "dataset_9k_folder/dataset_9k_augmented/annotations/train.json"
# output_json = "dataset_9k_folder/dataset_9k_augmented/annotations/train.json"
# # # # #### Train
# image_folder = "dataset_9k_folder/dataset_9k/train"
# input_json = "dataset_9k_folder/dataset_9k/annotations/train.json"
# output_json = "dataset_9k_folder/dataset_9k/annotations/train.json"
# # # #### Val_augmented
image_folder = "train_13k/train"
input_json = "train_13k/annotations/train.json"
output_json = "train_13k/annotations/train.json"
# # # #### Val
# image_folder = "dataset_14k_folder/dataset_14k/val"
# input_json = "dataset_14k_folder/dataset_14k/annotations/val.json"
# output_json = "dataset_14k_folder/dataset_14k/annotations/val.json"

# Đọc dữ liệu từ tệp JSON
with open(input_json, "r") as f:
    data = json.load(f)

# Xóa trường "info" và "licenses"
data.pop("info", None)
data.pop("licenses", None)

# Tạo một danh sách chứa tất cả các tên file ảnh hiện có trong thư mục chứa ảnh
existing_names = os.listdir(image_folder)

# Tạo một từ điển để theo dõi số lần xuất hiện của từng tên file
file_name_counts = {}

# Duyệt qua danh sách thông tin ảnh và đổi tên các file_name
for item in data["images"]:
    old_file_name = item["file_name"]
    file_name_without_ext = old_file_name.split(".")[0]

    # Lấy phần trước dấu chấm của tên file để tạo thành phần đầu của tên mới
    file_name_prefix = file_name_without_ext.split('.')[0]

    # Kiểm tra xem tên file đã xuất hiện trước đó bao nhiêu lần
    if file_name_without_ext in file_name_counts:
        file_name_counts[file_name_without_ext] += 1
    else:
        file_name_counts[file_name_without_ext] = 1

    # Lấy số thứ tự bản sao và định dạng thành 4 chữ số (vd: 0001, 0002, ...)
    sequence_number = file_name_counts[file_name_without_ext]
    sequence_number_str = f"{sequence_number:04d}"

    # Xây dựng tên file mới bằng cách kết hợp phần đầu và số thứ tự, thêm phần mở rộng .jpg
    new_file_name = f"{file_name_prefix}{sequence_number_str}.jpg"

    # Kiểm tra trùng lặp tên file ảnh
    while is_duplicate_name(new_file_name, existing_names):
        sequence_number += 1
        sequence_number_str = f"{sequence_number:04d}"
        new_file_name = f"{file_name_prefix}{sequence_number_str}.jpg"

    # Đổi tên trong dữ liệu JSON
    item["file_name"] = new_file_name

    # Đổi tên tệp trong thư mục chứa ảnh
    old_file_path = os.path.join(image_folder, old_file_name)
    new_file_path = os.path.join(image_folder, new_file_name)

    try:
        # Đổi tên ảnh trong thư mục chứa ảnh
        os.rename(old_file_path, new_file_path)
        print(f"Đã đổi tên ảnh {old_file_name} thành {new_file_name} và cập nhật trong dữ liệu JSON.")
    except Exception as e:
        print(f"Lỗi khi đổi tên ảnh {old_file_name}: {e}")

    # Xóa thuộc tính "license" và "date_captured" khỏi phần tử trong danh sách "images"
    item.pop("license", None)
    item.pop("date_captured", None)

# Trích xuất dữ liệu từ các khóa "categories"
categories_data = [
    {"supercategory": "trafficsign", "id": 1, "name": "stop"},
    {"supercategory": "trafficsign", "id": 2, "name": "left"},
    {"supercategory": "trafficsign", "id": 3, "name": "right"},
    {"supercategory": "trafficsign", "id": 4, "name": "straight"},
    {"supercategory": "trafficsign", "id": 5, "name": "no_left"},
    {"supercategory": "trafficsign", "id": 6, "name": "no_right"},
]

# Gán lại các dữ liệu vào các khóa mới theo cấu trúc mới "images" -> "categories" -> "annotations"
annotations_data = data.pop("annotations", [])

new_data = {
    "images": data["images"],
    "categories": categories_data,
    "annotations": annotations_data,
}

# Cập nhật category_id trong danh sách annotations_data
category_id_mapping = {1: 2, 2: 5, 3: 6, 4: 3, 5: 1, 6: 4}
for ann in new_data["annotations"]:
    ann["category_id"] = category_id_mapping[ann["category_id"]]

# Ghi dữ liệu mới vào tệp JSON
with open(output_json, "w") as f:
    json.dump(new_data, f, indent=4)

print("Đã đổi cấu trúc file JSON, đổi tên file, và cập nhật category_id thành công!")
