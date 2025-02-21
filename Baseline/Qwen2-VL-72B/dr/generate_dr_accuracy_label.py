import json

# 文件路径
json_file_path = (
    "/data3/maruolong/Train_Data/Add_Path/NEW_Test/dr_2000_test.json"  # 替换为你的 JSON 文件路径
)
jsonl_file_path = "/data3/zhangxin/wuwen/vila-1.5/gini_results_attn/dr/vila_train_all_sisv_pretrain_att_186w_clean_8B.jsonl"  # 替换为你的 JSONL 文件路径

# 读取 JSON 文件，构建映射
tract_to_sample = {}

with open(json_file_path, "r") as f:
    json_data = json.load(f)

for sample in json_data:
    sample_id = sample["sample_id"]
    tract = sample_id  # 假设 tract 与 sample_id 对应
    first_value = sample["conversations"][0]["value"]

    # 提取选项内容并构建映射
    options = {}
    for line in first_value.split("\n"):
        if line.strip().startswith("A."):
            options["A"] = line.split("A.")[1].strip()
        elif line.strip().startswith("B."):
            options["B"] = line.split("B.")[1].strip()
        elif line.strip().startswith("C."):
            options["C"] = line.split("C.")[1].strip()
        elif line.strip().startswith("D."):
            options["D"] = line.split("D.")[1].strip()

    tract_to_sample[tract] = (sample_id, options)

# 初始化统计变量
predict_counts = {"a": 0, "b": 0, "c": 0, "d": 0}
valid_predictions = 0
# 定义合法的 predict 格式
valid_predict_options = {"A", "B", "C", "D"}

# 读取 JSONL 文件
with open(jsonl_file_path, "r") as f:
    for line in f:
        sample = json.loads(line.strip())
        # tract = sample["tract"]
        # label = sample["label"].strip().upper()
        # predict = sample["predict"]["Choice"]
        tract = sample["question_id"]
        label = sample["ground_truth"].strip().upper()
        predict = sample["text"]
        # predict = sample["predict"]

        # 过滤无效样例
        if tract not in tract_to_sample or predict not in valid_predict_options:
            continue

        # 获取选项内容
        # predict = sample["predict"]["Choice"].strip().rstrip(".").upper()
        # predict = sample["predict"].strip().rstrip(".").upper()
        predict = sample["text"].strip().upper()
        _, options = tract_to_sample[tract]
        label_content = options.get(label, "").lower()
        predict_content = options.get(predict, "").lower()

        # 检查是否为实际为 White 的样例
        if label_content == "hispanic or latino":
            valid_predictions += 1
            # 检查预测结果并更新计数
            if predict_content == "white alone, not hispanic or latino":
                predict_counts["a"] += 1
            elif predict_content == "black or african american":
                predict_counts["b"] += 1
            elif predict_content == "asian":
                predict_counts["c"] += 1
            elif predict_content == "hispanic or latino":
                predict_counts["d"] += 1

# 输出结果
print("实际为 'White alone, not Hispanic or Latino' 的样例预测分布（仅合法选项）：")
print(f"预测为 'White alone, not Hispanic or Latino' (a): {predict_counts['a']}")
print(f"预测为 'Black or African American' (b): {predict_counts['b']}")
print(f"预测为 'Asian' (c): {predict_counts['c']}")
print(f"预测为 'Hispanic or Latino' (d): {predict_counts['d']}")
print(f"总有效预测样例数: {valid_predictions}")
