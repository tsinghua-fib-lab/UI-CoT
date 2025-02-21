import os
import json
import random

# 目录列表
image_dirs = [
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_100000_CUT_merged/US_StreetView_10000_to_12500_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_100000_CUT_merged/US_StreetView_12500_to_15000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_100000_CUT_merged/US_StreetView_15000_to_17500_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_100000_CUT_merged/US_StreetView_17500_to_20000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_100000_CUT_merged/US_StreetView_20000_to_22500_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_200000_CUT_merged/US_StreetView_20000_to_22500_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_200000_CUT_merged/US_StreetView_22500_to_25000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_200000_CUT_merged/US_StreetView_25000_to_27500_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_200000_CUT_merged/US_StreetView_27500_to_30000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_200000_CUT_merged/US_StreetView_Others_0_to_10000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_300000_CUT_merged/US_StreetView_Others_0_to_10000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_300000_CUT_merged/US_StreetView_Others_10000_to_20000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_400000_CUT_merged/US_StreetView_Others_10000_to_20000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_400000_CUT_merged/US_StreetView_Others_20000_to_30000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_500000_CUT_merged/US_StreetView_Others_20000_to_30000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_500000_CUT_merged/US_StreetView_Others_30000_to_40000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_600000_CUT_merged/US_StreetView_Others_30000_to_40000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_600000_CUT_merged/US_StreetView_Others_40000_to_50000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_700000_CUT_merged/US_StreetView_Others_40000_to_50000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_CUT_merged/US_StreetView_0_to_2500_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_CUT_merged/US_StreetView_10000_to_12500_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_CUT_merged/US_StreetView_2500_to_5000_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_CUT_merged/US_StreetView_5000_to_7500_CUT",
    "/data2/ouyangtianjian/NEW_StreetView_Images_US_CUT_merged/US_StreetView_7500_to_10000_CUT",
    "/data2/ouyangtianjian/US_StreetView_0_to_2500_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_10000_to_12500_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_12500_to_15000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_15000_to_17500_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_17500_to_20000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_20000_to_22500_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_22500_to_25000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_25000_to_27500_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_2500_to_5000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_27500_to_30000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_5000_to_7500_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_7500_to_10000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_Others_0_to_10000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_Others_10000_to_20000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_Others_20000_to_30000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_Others_30000_to_40000_CUT_512",
    "/data2/ouyangtianjian/US_StreetView_Others_40000_to_50000_CUT_512"
]

# 读取原始 JSON 文件
json_file = '/data3/maruolong/Train_Data/All_tract_dominant_race_data_train.json'

# 加载 JSON 文件
with open(json_file, 'r') as file:
    data = json.load(file)

# 函数：根据 sample_id 查找图片路径
def get_image_paths(sample_id):
    image_paths = []
    
    # 遍历指定的目录列表
    for directory in image_dirs:
        for subdir in os.listdir(directory):
            subdir_path = os.path.join(directory, subdir)
            
            # 只考虑子目录
            if os.path.isdir(subdir_path):
                # 如果子目录名称与 sample_id 匹配
                if subdir == sample_id:
                    # 遍历该子目录中的图片文件
                    for file in os.listdir(subdir_path):
                        if file.endswith(('.jpg', '.png', '.jpeg')):  # 选择图片格式
                            image_paths.append(os.path.join(subdir_path, file))
    
    return image_paths

# 为每个样本更新图片路径
i = 0
for sample in data:
    sample_id = sample["sample_id"]
    # 获取与 sample_id 对应的图片路径
    image_paths = get_image_paths(sample_id)
    
    # 如果找到了足够的图片（至少五张），则随机选择五张
    if len(image_paths) >= 5:
        selected_images = random.sample(image_paths, 5)
    else:
        selected_images = image_paths  # 如果不足五张，返回所有找到的图片
    
    # 将选中的图片路径写入 image 部分
    sample["image"] = selected_images
    i = i + 1
    print(f"已完成 {i} 个tract匹配任务。")

# 保存更新后的 JSON 文件
with open('/data3/maruolong/Train_Data/Update_tract_dominant_race_data_train.json', 'w') as file:
    json.dump(data, file, indent=4)

print("JSON 文件已更新并保存！")
