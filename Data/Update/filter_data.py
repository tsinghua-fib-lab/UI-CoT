import json

# 输入数据集文件路径
input_json_file = '/data3/maruolong/Train_Data/Add_Path/Update_white_black_income_ratio_data.json'

# 输出更新后的数据集文件路径
output_json_file = '/data3/maruolong/Train_Data/Add_Path/Filtered_Update_white_black_income_ratio_data.json'

# 加载 JSON 数据
with open(input_json_file, 'r') as file:
    data = json.load(file)

# 过滤掉 image 中只有一条路径的样本
filtered_data = [sample for sample in data if len(sample.get("image", [])) > 1]

# 保存更新后的数据集
with open(output_json_file, 'w') as file:
    json.dump(filtered_data, file, indent=4)

print(f"Filtered dataset saved with {len(filtered_data)} samples: {output_json_file}")
