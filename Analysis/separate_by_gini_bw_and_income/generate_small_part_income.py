import json
import pandas as pd

# 输入的文件路径
input_json_path = "/data3/maruolong/Train_Data/Add_Path/NEW_Test/gc_2000_test_calcultate_gini_value.json"  # JSON 文件路径
input_xlsx_path = "/data3/maruolong/Train_Data/Add_Path/Median_Income.xlsx"  # XLSX 文件路径

# 输出的 JSONL 文件路径
output_jsonl_small_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_and_income/small_income_part_tract.jsonl"  # 小的一半
output_jsonl_large_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_and_income/large_income_part_tract.jsonl"  # 大的一半

# 读取 XLSX 文件，假设它包含 'tract' 和 'Income' 两列
income_data = pd.read_excel(input_xlsx_path)

# 将 'tract' 列转换为字符串类型，确保匹配无误
income_data["tract"] = income_data["tract"].astype(str)

# 读取整个 JSON 文件
with open(input_json_path, "r") as infile:
    data = json.load(infile)  # 解析整个 JSON 文件为 Python 数据结构（列表）

# 存储包含 tract 和 Income 的样本数据
samples = []

# 遍历 JSON 文件中的样本
for sample in data:
    sample_id = sample["sample_id"]
    # 找到该 sample 对应的 Income
    income = income_data.loc[income_data["tract"] == sample_id, "Income"].values
    if len(income) > 0:  # 确保有匹配到的收入
        income_value = income[0]
        samples.append({"tract": sample_id, "Income": income_value})

# 按照 Income 排序（从小到大）
samples.sort(key=lambda x: x["Income"])

# 计算分割点（总样本数的一半）
half_size = len(samples) // 2

# 取出前一半较小的样本
small_half_samples = samples[:half_size]
# 取出后一半较大的样本
large_half_samples = samples[half_size:]

# 将前一半较小的样本写入新的 JSONL 文件
with open(output_jsonl_small_path, "w") as outfile:
    for sample in small_half_samples:
        json.dump(sample, outfile)
        outfile.write("\n")

# 将后一半较大的样本写入新的 JSONL 文件
with open(output_jsonl_large_path, "w") as outfile:
    for sample in large_half_samples:
        json.dump(sample, outfile)
        outfile.write("\n")

print(f"前一半较小的样本已保存到 {output_jsonl_small_path}")
print(f"后一半较大的样本已保存到 {output_jsonl_large_path}")
