import json
import random

# 输入和输出文件路径
input_file = "/data3/maruolong/Train_Data/Add_Path/baseline/train_tract_CoT.jsonl"  # 输入文件路径
output_file = "/data3/maruolong/Train_Data/Add_Path/baseline/train_tract_CoT_prompt.jsonl"  # 输出文件路径

# 定义 10 个不同的 prompt 开头
prompt_options = [
    "You are an expert in geographical inequality. I will give you several images depicting street view and satellite visuals of a U.S. census tract. The Gini coefficient measures income inequality, ranging from 0 (perfect equality) to 1 (maximum inequality). Follow the steps below to determine the income distribution and Gini coefficient.",
    "As a specialist in income inequality and geography, you will analyze several images of a U.S. census tract from both street view and satellite perspectives. The Gini coefficient, which ranges from 0 (perfect equality) to 1 (maximum inequality), will be used to quantify inequality. Follow the steps below to complete the task.",
    "You are an authority on economic inequality in geographical areas. I will provide images from street view and satellite perspectives of a U.S. census tract. Your task is to calculate the income distribution and the Gini coefficient (0 = perfect equality, 1 = maximum inequality). Follow the outlined steps below.",
    "As a geography expert, you will analyze the income inequality of a U.S. census tract using provided street view and satellite images. The Gini coefficient, which measures inequality on a scale from 0 (perfect equality) to 1 (maximum inequality), will guide your analysis. Follow the steps outlined below.",
    "You are a geographical economist focusing on inequality. You will be given images representing both street view and satellite perspectives of a U.S. census tract. Using the Gini coefficient (ranging from 0 for equality to 1 for inequality), follow the steps below to estimate the income distribution.",
    "You specialize in analyzing geographic inequality. I will provide street view and satellite images of a U.S. census tract. Your objective is to calculate the Gini coefficient (0 = perfect equality, 1 = maximum inequality) by following the steps outlined below.",
    "As an expert in geographic inequality, you will assess the provided images from a U.S. census tract, including street view and satellite visuals. The Gini coefficient measures income inequality, where 0 represents perfect equality and 1 maximum inequality. Follow the steps below.",
    "You are an economic inequality analyst specializing in geographic data. I will share images from street view and satellite sources of a U.S. census tract. Use the Gini coefficient, which ranges from 0 (perfect equality) to 1 (maximum inequality), and follow the instructions below.",
    "As a researcher in geographic inequality, you are tasked with examining street view and satellite images of a U.S. census tract. The Gini coefficient (0 for perfect equality, 1 for maximum inequality) will help quantify income disparity. Follow the steps below.",
    "You are a geographer with expertise in inequality analysis. I will provide you with several images of a U.S. census tract from street view and satellite perspectives. The Gini coefficient (0 = perfect equality, 1 = maximum inequality) will quantify inequality. Follow the steps below."
]

# 固定的 prompt 剩余部分
prompt_suffix = """
STEP 1: Based on all the images, analyze and estimate the income distribution across ten levels:
LEVEL1: Less than $10000
LEVEL2: $10000 to $14999
LEVEL3: $15000 to $24999
LEVEL4: $25000 to $34999
LEVEL5: $35000 to $49999
LEVEL6: $50000 to $74999
LEVEL7: $75000 to $99999
LEVEL8: $100000 to $149999
LEVEL9: $150000 to $199999
LEVEL10: $200000 or more
Provide your estimated proportions for each level, ensuring the sum equals 1.

STEP 2: Using the proportions from STEP 1, calculate the Gini coefficient. To aid this, you can use the following representative income values for each level:
LEVEL1: $5000 
LEVEL2: $12500 
LEVEL3: $20000 
LEVEL4: $30000 
LEVEL5: $42500 
LEVEL6: $62500 
LEVEL7: $87500 
LEVEL8: $125000 
LEVEL9: $175000 
LEVEL10: $350000

Output format:
Income distribution:
LEVEL1: 0.XX, LEVEL2: 0.XX, LEVEL3: 0.XX, LEVEL4: 0.XX, LEVEL5: 0.XX, LEVEL6: 0.XX, LEVEL7: 0.XX, LEVEL8: 0.XX, LEVEL9: 0.XX, LEVEL10: 0.XX

Gini coefficient: 0.XX
""".strip()

# 添加随机 prompt
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        sample = json.loads(line.strip())
        random_prompt = random.choice(prompt_options) + "\n\n" + prompt_suffix
        sample["prompt"] = random_prompt  # 添加 prompt
        outfile.write(json.dumps(sample) + "\n")  # 写入输出文件

print(f"文件已生成：{output_file}")
