import json

# 输入的 JSONL 文件路径
high_gini_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/large_bw_part_tract.jsonl"
low_gini_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/small_bw_part_tract.jsonl"
high_income_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/large_income_part_tract.jsonl"
low_income_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/small_income_part_tract.jsonl"

# 输出的 JSONL 文件路径
high_gini_high_income_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/high_bw_high_income.jsonl"
high_gini_low_income_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/high_bw_low_income.jsonl"
low_gini_high_income_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/low_bw_high_income.jsonl"
low_gini_low_income_path = "/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/low_bw_low_income.jsonl"

# 读取 JSONL 文件并将其转为字典列表
def read_jsonl(file_path):
    with open(file_path, "r") as infile:
        return [json.loads(line) for line in infile]

high_gini_samples = read_jsonl(high_gini_path)
low_gini_samples = read_jsonl(low_gini_path)
high_income_samples = read_jsonl(high_income_path)
low_income_samples = read_jsonl(low_income_path)

# 创建一个字典来根据 tract 快速查找
high_gini_dict = {sample["tract"]: sample["value"] for sample in high_gini_samples}
low_gini_dict = {sample["tract"]: sample["value"] for sample in low_gini_samples}
high_income_dict = {sample["tract"]: sample["Income"] for sample in high_income_samples}
low_income_dict = {sample["tract"]: sample["Income"] for sample in low_income_samples}

# 函数：交叉匹配并生成结果
def generate_combined_jsonl(gini_dict, income_dict, output_path):
    combined_samples = []
    for tract in gini_dict:
        if tract in income_dict:
            combined_samples.append({
                "tract": tract,
                "value": gini_dict[tract],
                "Income": income_dict[tract]
            })
    
    # 将结果写入新的 JSONL 文件
    with open(output_path, "w") as outfile:
        for sample in combined_samples:
            json.dump(sample, outfile)
            outfile.write("\n")

# 生成四个 JSONL 文件
generate_combined_jsonl(high_gini_dict, high_income_dict, high_gini_high_income_path)
generate_combined_jsonl(high_gini_dict, low_income_dict, high_gini_low_income_path)
generate_combined_jsonl(low_gini_dict, high_income_dict, low_gini_high_income_path)
generate_combined_jsonl(low_gini_dict, low_income_dict, low_gini_low_income_path)

print("四个 JSONL 文件已成功生成！")
