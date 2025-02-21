import pandas as pd
import json

# 读取黑白人收入数据和黑白收入比数据
income_data = pd.read_excel('/data3/maruolong/Train_Data/Add_Path/bw_ratio/bw_race_income.xlsx')  # 包含tract, Black, White收入
income_ratio_data = pd.read_excel('/data3/maruolong/Train_Data/Add_Path/bw_ratio/data.xlsx')  # 包含tract_id, Income_Ratio2

# 读取 JSON 文件
with open('/data3/maruolong/Train_Data/Add_Path/bw_ratio/NEW_test/bw_CoT_test_change_prompt.json', 'r') as f:
    data = json.load(f)

# 定义根据收入判断 LEVEL
def get_income_level(income):
    if income < 10000:
        return 1
    elif income < 15000:
        return 2
    elif income < 25000:
        return 3
    elif income < 35000:
        return 4
    elif income < 50000:
        return 5
    elif income < 75000:
        return 6
    elif income < 100000:
        return 7
    elif income < 150000:
        return 8
    elif income < 200000:
        return 9
    else:
        return 10

# 用于存储不一致的tract_id
inconsistent_tracts = []

# 遍历每个 sample
for sample in data:
    tract_id = int(sample['sample_id'])  # 假设 sample_id 对应 tract_id
    
    # 查找对应 tract 的黑白人收入
    tract_income = income_data[income_data['tract'] == tract_id]
    if tract_income.empty:
        continue  # 如果没有找到相关数据，则跳过

    black_income = int(tract_income['Black or African American'].values[0])
    white_income = int(tract_income['White alone, not Hispanic or Latino'].values[0])

    # 查找对应 tract 的收入比
    tract_income_ratio = income_ratio_data[income_ratio_data['TRACT_ID'] == tract_id]
    if tract_income_ratio.empty:
        continue  # 如果没有找到相关数据，则跳过

    income_ratio = tract_income_ratio['Income_Ratio2'].values[0]
    
    # 计算收入区间
    black_level = get_income_level(black_income)
    white_level = get_income_level(white_income)
    
    # 计算收入比，并判断是否大于2
    income_ratio_pre = round(1 / income_ratio, 2) if income_ratio != 0 else 2  # 计算黑白收入比，避免除以0
    income_ratio = income_ratio_pre
    
    if income_ratio > 2:
        income_ratio = 2
        ratio_statement = f"Since the ratio {income_ratio_pre} is greater than 2, so the result is capped at 2."
    else:
        ratio_statement = f"Since the ratio {income_ratio} is less than 2, so the result remains unchanged."
    
    # 获取原始 JSON 的 second value (模型预测的收入比)
    predicted_ratio = float(sample['conversations'][1]['value'])
    
    # 如果计算的 ratio 与原始预测不一致，记录 tract_id
    if income_ratio != predicted_ratio:
        inconsistent_tracts.append(tract_id)
    
    # 创建 CoT 内容
    cot_summary = f"""
- Black Median Income: {black_income}
- White Median Income: {white_income}
- Income Ratio: {income_ratio}
"""
    
    # 替换 sample 的第二个 value
    sample['conversations'][1]['value'] = cot_summary

# 输出所有不一致的tract_id
if inconsistent_tracts:
    print("Inconsistent Tracts:", inconsistent_tracts)

# 保存新的 JSON 文件
with open('/data3/maruolong/Train_Data/Add_Path/bw_ratio/NEW_test/bw_CoT_test_change_prompt.json', 'w') as f:
    json.dump(data, f, indent=4)
