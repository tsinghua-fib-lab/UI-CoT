import json

def extract_dominant_race(conversations):
    """根据 conversations 提取主导种族"""
    # 提取选项并映射
    options_str = conversations[0]["value"]
    options_dict = {}
    options_lines = options_str.split("\n")
    
    for line in options_lines:
        if line.startswith("A.") or line.startswith("B.") or line.startswith("C.") or line.startswith("D."):
            # 分割选项
            option_letter = line[0]  # A, B, C, D
            race = line[3:].strip()  # 选项后的种族名称
            options_dict[option_letter] = race

    # 获取 GPT 的回答
    gpt_answer = conversations[1]["value"].strip()

    # 根据 GPT 的回答返回主导种族
    return options_dict.get(gpt_answer, None)

def process_json(input_file, output_file):
    """处理 JSON 文件，提取主导种族并输出为 JSONL 格式"""
    results = []
    
    with open(input_file, 'r') as infile:
        data = json.load(infile)
        
        for sample in data:
            sample_id = sample["sample_id"]  # 对应tract号
            conversations = sample["conversations"]
            
            dominant_race = extract_dominant_race(conversations)
            
            if dominant_race:  # 如果成功提取到主导种族
                result = {
                    "tract": sample_id,
                    "dominant_race": dominant_race
                }
                results.append(result)

    # 输出结果到 JSONL 文件
    with open(output_file, 'w') as outfile:
        for result in results:
            outfile.write(json.dumps(result) + '\n')

# 示例调用
input_file = "/data3/maruolong/Train_Data/Add_Path/NEW_Train/dr_5008_train.json"  # 输入文件路径
output_file = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/tract_dominant_race_train.jsonl"  # 输出文件路径
process_json(input_file, output_file)
