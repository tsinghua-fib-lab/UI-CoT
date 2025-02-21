import json
import re
import numpy as np

def extract_income_data(text):
    """从文本中提取黑人和白人收入数据"""
    black_income = None
    white_income = None
    
    # 匹配黑人收入
    black_match = re.search(r"- Black Median Income:\s*(\d+)", text)
    if black_match:
        black_income = float(black_match.group(1))
    
    # 匹配白人收入
    white_match = re.search(r"- White Median Income:\s*(\d+)", text)
    if white_match:
        white_income = float(white_match.group(1))
    
    return black_income, white_income

def calculate_income_divergence(predicted_black, predicted_white, actual_black, actual_white):
    """计算收入散度"""
    if None in [predicted_black, predicted_white, actual_black, actual_white]:
        return None  # 如果有任何收入是无效的，则跳过
    
    divergence = (abs(predicted_white - actual_white) / actual_white + 
                  abs(predicted_black - actual_black) / actual_black) / 2
    return divergence

def calculate_average_income_divergence(jsonl_file):
    divergences = []
    
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            
            # 提取 text 和 ground_truth
            text = data.get('text', '')
            ground_truth = data.get('ground_truth', '')
            
            # 提取收入数据
            predicted_black, predicted_white = extract_income_data(text)
            actual_black, actual_white = extract_income_data(ground_truth)
            
            # 如果成功提取到收入数据，计算收入散度
            divergence = calculate_income_divergence(predicted_black, predicted_white, actual_black, actual_white)
            if divergence is not None:
                divergences.append(divergence)
    
    # 计算并返回平均收入散度
    if divergences:
        return np.mean(divergences)
    else:
        return None

# 示例：计算输入文件的平均收入散度
jsonl_file = "/data3/zhangxin/wuwen/vila-1.5/gini_results_attn/bw_cot_5/vila_train_all_sisv_pretrain_attn_186w_clean_8B_cot5_7.jsonl"  # 替换为实际的 JSONL 文件路径
average_divergence = calculate_average_income_divergence(jsonl_file)

if average_divergence is not None:
    print(f"Average Income Divergence: {average_divergence:.6f}")
else:
    print("No valid data found.")
