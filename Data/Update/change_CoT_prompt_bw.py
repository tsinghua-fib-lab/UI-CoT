import json

# 加载原始JSON数据
with open('/data3/maruolong/Train_Data/Add_Path/bw_ratio/NEW_train/bw_CoT_train.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 你的新prompt
new_prompt = """
You are a geography inequality expert. Here are some satellite and street images from a U.S. census tract. Based on these, please estimate the income ratio between Black and White households, which is the median income of Black households divided by the median income of White households. This value ranges from 0 to 2. A value of 1 represents parity, lower values mean higher White incomes, and higher values mean higher Black incomes.

Follow the steps below to estimate the Black households’ median income, White households’ median income, and the Black-to-White income ratio for this area.

STEP 1: Based on all the images, analyze and estimate which income range the median income for Black and White households falls into:

- LEVEL1: Less than $10,000
- LEVEL2: $10,000 to $14,999
- LEVEL3: $15,000 to $24,999
- LEVEL4: $25,000 to $34,999
- LEVEL5: $35,000 to $49,999
- LEVEL6: $50,000 to $74,999
- LEVEL7: $75,000 to $99,999
- LEVEL8: $100,000 to $149,999
- LEVEL9: $150,000 to $199,999
- LEVEL10: $200,000 or more

STEP 2: Based on your predicted income ranges, estimate the specific income values within those ranges for both Black and White households.

STEP 3: Using the income data obtained in the previous step, calculate the income ratio between Black and White households. (This ratio should not exceed 2.)

Output format:
- Black Median Income: XXXXX
- White Median Income: XXXXX
- Income Ratio: X.XX
"""

# 遍历每个sample，替换value部分
for sample in data:
    # 获取第一个value中的 <image>\n 位置
    human_value = sample['conversations'][0]['value']
    image_pos = human_value.find('<image>\n')

    # 如果找到了 <image>\n, 替换后续部分
    if image_pos != -1:
        # 保留 <image>\n 之前的内容，并替换后面的部分
        new_value = human_value[:image_pos + len('<image>\n')] + new_prompt
        sample['conversations'][0]['value'] = new_value

# 将更新后的数据保存到新的文件
with open('/data3/maruolong/Train_Data/Add_Path/bw_ratio/NEW_train/bw_CoT_train_change_prompt.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
