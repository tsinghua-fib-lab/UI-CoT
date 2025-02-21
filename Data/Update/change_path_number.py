import json
import random

# 加载原始JSON数据
with open('/data3/maruolong/Train_Data/Add_Path/NEW_Train/gc_CoT_train.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 遍历每个sample进行处理
for sample in data:
    # 保留第一条路径
    image_paths = sample['image']
    first_image_path = image_paths[0]

    # 从剩余路径中随机抽取最多10条路径
    remaining_image_paths = image_paths[1:]
    if len(remaining_image_paths) > 5:
        selected_paths = random.sample(remaining_image_paths, 5)
    else:
        selected_paths = remaining_image_paths

    # 新的image列表，包含第一条路径和随机抽取的其他路径
    new_image_paths = [first_image_path] + selected_paths
    sample['image'] = new_image_paths

    # 更新第一个value中的<image>标签数量
    human_value = sample['conversations'][0]['value']
    # 计算<image>标签的数量
    new_image_count = len(new_image_paths)

    # 生成连续的<image>标签，最后才加上换行符
    new_value = "<image>" * new_image_count + "\n" + human_value.split("\n", 1)[-1]
    sample['conversations'][0]['value'] = new_value

# 将更新后的数据保存到新的文件
with open('/data3/maruolong/Train_Data/change_path_number/gc/5_images_gc_CoT_train.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
