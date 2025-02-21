import json

# 输入的 JSONL 文件路径
jsonl1_path = "/data3/maruolong/Train_Data/Add_Path/Train_result/extract_from_CoT_pretrained_data2.jsonl"  # 包含需要筛选的样本
jsonl2_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/low_gini_low_income.jsonl"  # 包含 tract 号的样本

# 输出的 JSONL 文件路径
output_jsonl_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/result_gc/low_gini_low_income_gc_pretrained_CoT.jsonl"

# 读取 JSONL 文件并返回每一行的样本列表
def read_jsonl(file_path):
    with open(file_path, "r") as infile:
        return [json.loads(line) for line in infile]

# 从 jsonl2 中提取 tract 号
def extract_tracts(jsonl2_samples):
    return set(sample["tract"] for sample in jsonl2_samples)

# 筛选 jsonl1 中与 jsonl2 中相同 tract 号的样本
def filter_samples(jsonl1_samples, tract_set):
    return [sample for sample in jsonl1_samples if sample["tract"] in tract_set]

# 读取两个 jsonl 文件
jsonl1_samples = read_jsonl(jsonl1_path)
jsonl2_samples = read_jsonl(jsonl2_path)

# 提取 jsonl2 中的 tract 号
tract_set = extract_tracts(jsonl2_samples)

# 筛选 jsonl1 中符合条件的样本
filtered_samples = filter_samples(jsonl1_samples, tract_set)

# 将筛选后的样本写入新的 JSONL 文件
with open(output_jsonl_path, "w") as outfile:
    for sample in filtered_samples:
        json.dump(sample, outfile)
        outfile.write("\n")

print(f"筛选后的样本已写入 {output_jsonl_path}")
