import os
import json
import base64
from PIL import Image, UnidentifiedImageError

def remove_empty_base64_samples(json_path, output_path):
    # 加载 JSON 数据
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    valid_samples = []
    removed_samples = []

    # 遍历每个样本
    for sample in data:
        sample_id = sample.get('sample_id')
        image_paths = sample.get('image')  # 假设路径字段为 'image' 且是列表
        has_invalid_path = False  # 标志是否有无效路径

        for image_path in image_paths:
            try:
                # 检查文件路径是否存在
                if not os.path.exists(image_path):
                    print(f"Image file not found: {image_path}. Removing sample_id: {sample_id}.")
                    has_invalid_path = True
                    break
                
                # 使用 Pillow 检查文件是否为有效图像
                with Image.open(image_path) as img:
                    img.verify()  # 验证图像文件是否完整

                # 打开文件并编码为 Base64
                with open(image_path, "rb") as image_file:
                    base64_content = base64.b64encode(image_file.read()).decode('utf-8')

                # 检查 Base64 内容是否为空
                if not base64_content.strip():
                    print(f"Empty base64 content for image: {image_path}. Removing sample_id: {sample_id}.")
                    has_invalid_path = True
                    break
            except (UnidentifiedImageError, IOError) as e:
                print(f"Invalid image file: {image_path}. Error: {e}. Removing sample_id: {sample_id}.")
                has_invalid_path = True
                break
            except Exception as e:
                print(f"Unexpected error processing image: {image_path}. Error: {e}. Removing sample_id: {sample_id}.")
                has_invalid_path = True
                break

        # 如果任意路径无效，将样本移除
        if has_invalid_path:
            removed_samples.append(sample_id)
        else:
            valid_samples.append(sample)

    # 保存更新后的 JSON 数据
    with open(output_path, 'w') as f:
        json.dump(valid_samples, f, indent=4)

    # 输出统计结果
    print(f"Total samples processed: {len(data)}")
    print(f"Valid samples kept: {len(valid_samples)}")
    print(f"Removed samples: {len(removed_samples)}")
    print(f"Removed sample IDs: {removed_samples}")
# 调用函数
json_file_path = "/data3/maruolong/Train_Data/Add_Path/NEW_Test/bw_2000_test_new_value.json"
output_file_path = "/data3/maruolong/Train_Data/Add_Path/NEW_Test/bw_2000_test_new_value.json"
remove_empty_base64_samples(json_file_path, output_file_path)
