import os
import json

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

# 函数：根据 sample_id 查找图片路径数目
def count_image_paths(sample_id):
    count = 0
    # 遍历指定的目录列表
    for directory in image_dirs:
        for subdir in os.listdir(directory):
            subdir_path = os.path.join(directory, subdir)
            # 如果子目录名称与 sample_id 匹配
            if os.path.isdir(subdir_path) and subdir == sample_id:
                # 统计该子目录中的图片文件数目
                count += sum(1 for file in os.listdir(subdir_path) if file.endswith(('.jpg', '.png', '.jpeg')))
    return count

# 输出 JSONL 文件路径
output_file = '/data3/maruolong/Train_Data/Tract_Image_Count.jsonl'

# 打开文件进行实时写入
with open(output_file, 'w') as file:
    i = 0
    for sample in data:
        sample_id = sample["sample_id"]
        # 获取与 sample_id 对应的图片路径数目
        image_count = count_image_paths(sample_id)
        # 构建单个结果
        result = {"tract": sample_id, "number": image_count}
        # 写入 JSONL 文件
        file.write(json.dumps(result) + '\n')
        i += 1
        print(f"已统计 {i} 个 tract 的图像路径数目，并写入文件。")

print("实时写入的图像路径统计已完成！")