import json

# 加载 JSON 文件
with open("/data3/maruolong/Train_Data/Add_Path/NEW_Test/bw_2000_test_new_value.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 遍历每个 sample
for sample in data:
    # 获取当前 image 数组和 conversations 中的第一个 value
    image_paths = sample.get("image", [])
    human_conversation = sample["conversations"][0]["value"]
    
    # 计算 <image> 标签的数量
    num_images = len(image_paths)
    num_placeholders = human_conversation.count("<image>")
    
    # 替换为正确数量的 <image> 标签
    if num_images != num_placeholders:
        updated_placeholders = "<image>" * num_images
        human_conversation_updated = human_conversation.replace(
            "<image>" * num_placeholders, updated_placeholders, 1
        )
        sample["conversations"][0]["value"] = human_conversation_updated

# 保存修改后的 JSON 文件
with open("/data3/maruolong/Train_Data/Add_Path/NEW_Test/bw_2000_test_new_value.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("调整完成，已生成 data_updated.json 文件。")
