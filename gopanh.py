#C:/Users/ASUS/Downloads/v1 + v2/annotations/train.json
#C:/Users/ASUS/Downloads/trafficsign.v1i.coco (v1)/annotations/train.json
#C:/Users/ASUS/Downloads/trafficsign.v1i.coco (v1)/annotations/train.json
#C:/Users/ASUS/Downloads/trafficsign.v1i.coco (v1)/train/
#C:/Users/ASUS/Downloads/trafficsign.v1i.coco (v2)/train/
#image_folder1 = "C:/Users/ASUS/Downloads/trafficsign.v1i.coco (v1)/train/"
#file1_path = "C:/Users/ASUS/Downloads/trafficsign.v1i.coco (v1)/annotations/train.json"
#image_folder2 = "C:/Users/ASUS/Downloads/trafficsign.v1i.coco (v2)/train/"
#file2_path = "C:/Users/ASUS/Downloads/trafficsign.v1i.coco (v2)/annotations/train.json"
#output_file_path = "C:/Users/ASUS/Downloads/v1 + v2/annotations/train.json"


import os
import json
import shutil

def rename_images_with_duplicates(image_folder, data, file_name_counts):
    for item in data["images"]:
        image_id = item["id"]
        old_file_name = item["file_name"]
        file_name_without_ext = file_name_without_ext = old_file_name.split(".")[0]

        if file_name_without_ext in file_name_counts:
            file_name_counts[file_name_without_ext] += 1
        else:
            file_name_counts[file_name_without_ext] = 1

        sequence_number = file_name_counts[file_name_without_ext]
        sequence_number_str = f"{sequence_number:02d}"

        new_file_name = f"{file_name_without_ext}{sequence_number_str}.jpg"
        item["file_name"] = new_file_name

        old_file_path = os.path.join(image_folder, old_file_name)
        new_file_path = os.path.join(image_folder, new_file_name)

        try:
            os.rename(old_file_path, new_file_path)
            print(f"Đã đổi tên ảnh {old_file_name} thành {new_file_name} và cập nhật trong dữ liệu JSON.")
        except Exception as e:
            print(f"Lỗi khi đổi tên ảnh {old_file_name}: {e}")

def merge_json_files(image_folder1, file1_path, image_folder2, file2_path, output_file_path):
    # Đọc dữ liệu từ hai tệp JSON
    with open(file1_path, "r") as f1, open(file2_path, "r") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    # Khởi tạo biến file_name_counts và đổi tên ảnh trong thư mục chứa ảnh nếu cần thiết
    file_name_counts = {}
    rename_images_with_duplicates(image_folder1, data1, file_name_counts)
    rename_images_with_duplicates(image_folder2, data2, file_name_counts)

    # Tính toán id mới cho tệp JSON thứ hai và cập nhật id cho images và old_annotations
    max_image_id = max(item["id"] for item in data1["images"])
    max_annotation_id = max(item["id"] for item in data1["annotations"])
    max_image_id1 = max(item["id"] for item in data1["images"]) +1
    max_annotation_id1 = max(item["id"] for item in data1["annotations"]) +1
    for item in data2["images"]:
        max_image_id += 1
        item["id"] = max_image_id
        # Đổi tên ảnh trong thư mục chứa ảnh của tệp JSON thứ hai và cập nhật ngay lúc đó
        old_file_name = item["file_name"]
        file_name_without_ext = old_file_name.split(".")[0]
        if file_name_without_ext in file_name_counts:
            file_name_counts[file_name_without_ext] += 1
        else:
            file_name_counts[file_name_without_ext] = 1
        sequence_number = file_name_counts[file_name_without_ext]
        sequence_number_str = f"{sequence_number:02d}"
        new_file_name = f"{file_name_without_ext}{sequence_number_str}.jpg"
        item["file_name"] = new_file_name

        old_file_path = os.path.join(image_folder2, old_file_name)
        new_file_path = os.path.join(image_folder2, new_file_name)

        try:
            os.rename(old_file_path, new_file_path)
            print(f"Đã đổi tên ảnh {old_file_name} thành {new_file_name} và cập nhật trong dữ liệu JSON.")
        except Exception as e:
            print(f"Lỗi khi đổi tên ảnh {old_file_name}: {e}")

    for annotation in data2["annotations"]:
        annotation["id"] = max_annotation_id1 + annotation["id"]
        annotation["image_id"] = max_image_id1 +  annotation["image_id"]

    # Gộp các thông tin trong hai tệp JSON lại thành một
    data1["images"].extend(data2["images"])
    data1["annotations"].extend(data2["annotations"])

    # Ghi dữ liệu mới vào tệp JSON kết quả
    with open(output_file_path, "w") as output_file:
        json.dump(data1, output_file, indent=4)

    print("Đã gộp, cập nhật thông tin ảnh và tạo tệp JSON kết quả thành công!")

# Thay đường dẫn tệp JSON, thư mục chứa ảnh 1, tệp JSON 2 và thư mục chứa ảnh 2 cho phù hợp
# # #### Train
# image_folder1 = "dataset_13k_folder/dataset_13k/train"
# file1_path = "dataset_13k_folder/dataset_13k/annotations/train.json"
# image_folder2 = "dataset_13k_folder/dataset_13k_augmented/train"
# file2_path = "dataset_13k_folder/dataset_13k_augmented/annotations/train.json"
# output_file_path = "dataset_13k_folder/dataset_13k_mergered_v5/annotations/train.json"
# # #### Val
image_folder1 = "dataset_13k_folder/dataset_13k_augmentx3/train"
file1_path = "dataset_13k_folder/dataset_13k_augmentx3/annotations/train.json"
image_folder2 = "dataset_13k_folder/dataset_13k_filtered/train"
file2_path = "dataset_13k_folder/dataset_13k_filtered/annotations/train.json"
output_file_path = "dataset_13k_folder/dataset_13k_augmentx3/annotations/train.json"

merge_json_files(image_folder1, file1_path, image_folder2, file2_path, output_file_path)

