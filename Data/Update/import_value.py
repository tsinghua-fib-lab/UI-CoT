import json

# 更新后的 JSON 文件路径
json_file = '/data3/maruolong/Train_Data/Update_tract_white_black_income_ratio_data.json'

# 加载 JSON 文件
with open(json_file, 'r') as file:
    data = json.load(file)

# 遍历每个 sample，更新 human 的 value 字段
for sample in data:
    # 获取当前 image 字段的路径数量，并额外增加一个计数
    num_images = len(sample["image"]) + 1
    
    # 生成 `<image>` 标签字符串
    image_tag_str = "<image>" * num_images
    
    # 更新 human 的 value 字段
    human_value = sample["conversations"][0]["value"]
    sample["conversations"][0]["value"] = f"{image_tag_str}{human_value}"

print("所有 sample 的 <image> 标签已更新。")

# 保存更新后的 JSON 文件
output_json_file = '/data3/maruolong/Train_Data/Updated_white_black_income_ratio_data.json'
with open(output_json_file, 'w') as file:
    json.dump(data, file, indent=4)

print("JSON 文件已更新并保存！")
