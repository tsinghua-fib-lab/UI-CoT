import json
import random


def shuffle_json_samples(json_file):
    # 读取原始的 JSON 数据
    with open(json_file, "r") as f_in:
        data = json.load(f_in)

    # 使用 random.shuffle() 打乱样本顺序
    random.shuffle(data)

    # 将打乱后的数据保存回原 JSON 文件
    with open(json_file, "w") as f_out:
        json.dump(data, f_out, indent=4)

    print(f"Shuffled {len(data)} samples and updated the original file {json_file}")


# 示例使用
shuffle_json_samples("/data3/maruolong/Train_Data/Add_Path/Filtered_Update_dominant_race_data.json")
shuffle_json_samples("/data3/maruolong/Train_Data/Add_Path/Filtered_Update_dominant_race_data.json")
