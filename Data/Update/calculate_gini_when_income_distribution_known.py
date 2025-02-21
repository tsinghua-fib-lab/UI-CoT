import json
import numpy as np

def calculate_gini_with_ranges(income_ranges, population_percentages):
    """
    使用收入范围和人口百分比计算基尼系数。
    :param income_ranges: list of tuple, 收入范围 [(min_income, max_income), ...]
    :param population_percentages: list, 各收入范围对应的人口百分比
    :return: float, 基尼系数
    """
    # 估算每个收入区间的代表性收入
    income_values = [
        (min_income + max_income) / 2 if max_income else min_income * 1.75  # 对高收入无上限区间，用 min_income 的 2 倍
        for min_income, max_income in income_ranges
    ]
    
    # 构建收入分布 [(收入值, 人口数)]
    total_population = 100  # 假设总人口为100%
    income_distribution = [
        (income, population_percent / 100 * total_population)
        for income, population_percent in zip(income_values, population_percentages)
    ]
    
    # 排序收入分布
    income_distribution.sort(key=lambda x: x[0])  # 按收入升序排序

    # 计算累积比例
    cum_population = np.cumsum([item[1] for item in income_distribution])
    cum_income = np.cumsum([item[0] * item[1] for item in income_distribution])
    
    # 标准化为百分比
    cum_population /= cum_population[-1]
    cum_income /= cum_income[-1]
    
    # 基尼系数计算
    gini = 1 - np.sum((cum_population[1:] - cum_population[:-1]) * (cum_income[1:] + cum_income[:-1]))
    return gini

def update_jsonl_with_calculate_gini(input_jsonl_path, output_jsonl_path):
    """
    更新JSONL文件，计算并添加基尼系数。
    """
    # 定义收入范围
    income_ranges = [
        (0, 10000), (10000, 14999), (15000, 24999), (25000, 34999), (35000, 49999),
        (50000, 74999), (75000, 99999), (100000, 149999), (150000, 199999), (200000, None)
    ]

    # 逐行读取JSONL文件并更新
    updated_data = []
    with open(input_jsonl_path, "r") as infile:
        for line in infile:
            sample = json.loads(line)
            
            # 提取收入分布数据
            income_distribution = [
                sample["LEVEL1"],
                sample["LEVEL2"],
                sample["LEVEL3"],
                sample["LEVEL4"],
                sample["LEVEL5"],
                sample["LEVEL6"],
                sample["LEVEL7"],
                sample["LEVEL8"],
                sample["LEVEL9"],
                sample["LEVEL10"]
            ]
            
            # 平滑处理：避免极端数据对基尼系数的影响（可选）
            income_distribution = [max(x, 0.01) for x in income_distribution]
            
            # 计算基尼系数
            calculate_gini = calculate_gini_with_ranges(income_ranges, income_distribution)
            
            # 添加新的字段
            sample["Calculate GINI"] = round(calculate_gini, 2)
            
            # 保存更新后的样本
            updated_data.append(sample)
    
    # 写入新的JSONL文件
    with open(output_jsonl_path, "w") as outfile:
        for sample in updated_data:
            outfile.write(json.dumps(sample) + "\n")

# 输入和输出文件路径
input_jsonl_path = "/data3/maruolong/Train_Data/Add_Path/baseline/Qwen2-VL-7B/gc_150_original2.jsonl"
output_jsonl_path = "/data3/maruolong/Train_Data/Add_Path/baseline/Qwen2-VL-7B/gc_150_calculate_original2.jsonl"

# 调用函数
update_jsonl_with_calculate_gini(input_jsonl_path, output_jsonl_path)
