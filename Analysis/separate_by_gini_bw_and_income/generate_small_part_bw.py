import json

input_json_path = "/data3/maruolong/Train_Data/Add_Path/NEW_Test/bw_2000_test_new_value.json"  # 输入的 JSONL 文件路径
output_jsonl_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/small_bw_part_tract.jsonl"  # 输出的 JSONL 文件路径
output_jsonl_large_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/large_bw_part_tract.jsonl"  # 存储后一半较大的样本的 JSONL 文件路径

# 存储所有样本和对应的数值
samples = []

# 读取 JSONL 文件
# 读取整个 JSON 文件
with open(input_json_path, "r") as infile:
    data = json.load(infile)  # 解析整个 JSON 文件为 Python 数据结构（列表）
    
    for sample in data:
        sample_id = sample["sample_id"]
        # 提取第二个 value（GPT 的回答）
        value = float(sample["conversations"][1]["value"])  # 转为 float
        samples.append({"tract": sample_id, "value": value})

# 按 value 数值进行排序（从小到大）
samples.sort(key=lambda x: x["value"])

# 取出前一半较小的样本
half_samples = samples[:len(samples) // 2]
# 取出后一半较大的样本
large_half_samples = samples[len(samples) //2:]

# 将结果写入新的 JSONL 文件
with open(output_jsonl_path, "w") as outfile:
    for sample in half_samples:
        json.dump(sample, outfile)
        outfile.write("\n")

# 将后一半较大的样本写入新的 JSONL 文件
with open(output_jsonl_large_path, "w") as outfile:
    for sample in large_half_samples:
        json.dump(sample, outfile)
        outfile.write("\n")

print(f"已提取并保存前一半较小的样本到 {output_jsonl_path}")
