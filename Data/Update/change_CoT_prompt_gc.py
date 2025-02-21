import json

# 加载原始 JSON 文件
with open('/data3/maruolong/Train_Data/Add_Path/NEW_Test/gc_2000_test_calcultate_gini_value.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 新的提示信息（prompt）
new_prompt = """
You are a geography inequality expert. I will provide you with several images representing street view and satellite images of a U.S. census tract. Follow the steps below to estimate the Gini coefficient for this area. The Gini coefficient is a measure of income inequality, ranging from 0 (perfect equality) to 1 (maximum inequality).

STEP 1: Based on all the images, analyze and estimate the income distribution across ten levels, considering spatial heterogeneity, land use patterns, green space distribution, street cleanliness, housing quality, infrastructure, and access to local amenities.
LEVEL1: Less than $10,000
LEVEL2: $10,000 to $14,999
LEVEL3: $15,000 to $24,999
LEVEL4: $25,000 to $34,999
LEVEL5: $35,000 to $49,999
LEVEL6: $50,000 to $74,999
LEVEL7: $75,000 to $99,999
LEVEL8: $100,000 to $149,999
LEVEL9: $150,000 to $199,999
LEVEL10: $200,000 or more
Provide your estimated proportions for each level, ensuring the sum equals 1.

STEP 2: Using the proportions from STEP 1, calculate the Gini coefficient. Follow these steps:
1. Construct the Representative Income and Distribution
2. Calculate cumulative population and cumulative income ratios.
3. **Use the formula below to calculate the Gini coefficient:**

G = 1 - Σ p_i * (y_i + y_(i-1))

Where:
p_i is the population proportion sorted by income,
y_i is the cumulative income proportion.

**Important: Do not include explanations, calculations, or analysis in your response. Only provide the income distribution and Gini coefficient in the format specified below.**

Output format:
Income distribution:
LEVEL1: 0.XX, LEVEL2: 0.XX, LEVEL3: 0.XX, LEVEL4: 0.XX, LEVEL5: 0.XX, LEVEL6: 0.XX, LEVEL7: 0.XX, LEVEL8: 0.XX, LEVEL9: 0.XX, LEVEL10: 0.XX

Gini coefficient: 0.XX


Below is a detailed example of how to calculate the Gini coefficient. Please follow this process to estimate the Gini coefficient for your area:

Step 2.1: Construct the Representative Income and Distribution
Define the following representative incomes for each income level:
LEVEL1: $5,000, LEVEL2: $12,500, LEVEL3: $20,000, LEVEL4: $30,000, LEVEL5: $42,500, LEVEL6: $62,500, LEVEL7: $87,500, LEVEL8: $125,000, LEVEL9: $175,000, LEVEL10: $300,000.

Example income distribution (Income, Proportion):
(5,000, 0.05), (12,500, 0.10), (20,000, 0.12), (30,000, 0.15), (42,500, 0.10),
(62,500, 0.14), (87,500, 0.13), (125,000, 0.08), (175,000, 0.07), (350,000, 0.06).

Step 2.2: Calculate cumulative population and income
We first calculate the population proportion and income proportion for each income level, then compute their cumulative values.

Representative Income * population percentage:
5,000 * 0.05 = 250, 12,500 * 0.10 = 1,250, 20,000 * 0.12 = 2,400, 30,000 * 0.15 = 4,500, 42,500 * 0.10 = 4,250, 62,500 * 0.14 = 8,750, 87,500 * 0.13 = 11,375, 125,000 * 0.08 = 10,000, 175,000 * 0.07 = 12,250, 350,000 * 0.06 = 21,000

Cumulative income:
250, 250 + 1,250 = 1,500, 1,500 + 2,400 = 3,900, 3,900 + 4,500 = 8,400, 8,400 + 4,250 = 12,650, 12,650 + 8,750 = 21,400, 21,400 + 11,375 = 32,775, 32,775 + 10,000 = 42,775, 42,775 + 12,250 = 55,025, 55,025 + 21,000 = 76,075

Cumulative Income Percent:
250 / 76,075 = 0.0033, 1,500 / 76,075 = 0.0197, 3,900 / 76,075 = 0.0513, 8,400 / 76,075 = 0.1104, 12,650 / 76,075 = 0.1663, 21,400 / 76,075 = 0.2813, 32,775 / 76,075 = 0.4308, 42,775 / 76,075 = 0.5623, 55,025 / 76,075 = 0.7233, 76,075 / 76,075 = 1.0

Step 2.3: Calculate the Gini coefficient:
G = 1 - [ 0.10 * (0.0033 + 0.0197) + 0.12 * (0.0197 + 0.0513) + 0.15 * (0.0513 + 0.1104) + 0.10 * (0.1104 + 0.1663) + 0.14 * (0.1663 + 0.2813) + 0.13 * (0.2813 + 0.4308) + 0.08 * (0.4308 + 0.5623) + 0.07 * (0.5623 + 0.7233) + 0.06 * (0.7233 + 1.0)] = 0.51

The Gini coefficient calculated is 0.51


Please provide the estimated income distribution for the U.S. census tract images you are analyzing and use this data to calculate the Gini coefficient, following the same steps outlined above. Only provide the income distribution and Gini coefficient in the format specified below.

"""


# 遍历每个 sample，修改第一个 value
for sample in data:
    if sample.get("conversations"):
        first_conversation = sample["conversations"][0]
        # 提取<image>部分并替换后面的内容
        image_part = first_conversation["value"].split("\n")[0]  # 获取<image>部分
        first_conversation["value"] = image_part + "\n" + new_prompt

# 保存修改后的 JSON 文件
with open('/data3/maruolong/Train_Data/Add_Path/NEW_Test/gc_2000_test_calcultate_gini_value_with_example.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("JSON文件已成功修改并保存。")
