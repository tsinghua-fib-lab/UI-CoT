import json
import re

def extract_predict_details(predict_text):
    """
    从predict文本中提取Choice和各族群的预测占比。
    :param predict_text: 字符串，包含Choice和族群比例的文本
    :return: 一个字典，包含Choice和各族群的比例
    """
    result = {}

    # 提取Choice
    choice_match = re.search(r"Choice:\s*([A-D])", predict_text)
    result["Choice"] = choice_match.group(1) if choice_match else None

    # 提取各族群的预测占比，如果没有找到则赋值为空
    result["White alone, not Hispanic or Latino"] = extract_percentage(predict_text, r"- White alone, not Hispanic or Latino:\s*([0-9.]+)%")
    result["Black or African American"] = extract_percentage(predict_text, r"- Black or African American:\s*([0-9.]+)%")
    result["Asian"] = extract_percentage(predict_text, r"- Asian:\s*([0-9.]+)%")
    result["Hispanic or Latino"] = extract_percentage(predict_text, r"- Hispanic or Latino:\s*([0-9.]+)%")

    return result

def extract_percentage(text, pattern):
    """
    从文本中提取百分比，如果没有找到，返回None。
    :param text: 输入文本
    :param pattern: 匹配的正则表达式
    :return: 提取的百分比或None
    """
    match = re.search(pattern, text)
    if match:
        return float(match.group(1))
    return None

def process_jsonl(input_jsonl, output_jsonl):
    """
    处理JSONL文件，提取predict中的详细信息，构建新的结构并保存到新的JSONL文件。
    :param input_jsonl: 输入的JSONL文件路径
    :param output_jsonl: 输出的新的JSONL文件路径
    """
    updated_data = []

    with open(input_jsonl, "r") as infile:
        for line in infile:
            sample = json.loads(line)

            # 提取predict中的详细信息
            predict_details = extract_predict_details(sample["text"])

            # 将提取的内容加入到predict字段下
            sample["text"] = predict_details

            updated_data.append(sample)

    # 将更新后的数据写入新的JSONL文件
    with open(output_jsonl, "w") as outfile:
        for sample in updated_data:
            outfile.write(json.dumps(sample) + "\n")

# 输入和输出文件路径
input_jsonl_path = "/data3/zhangxin/wuwen/vila-1.5/gini_results_attn/dr_cot_5/vila_train_all_sisv_pretrain_attn_186w_clean_8B_cot5_7.jsonl"
output_jsonl_path = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/UrbanMLLM_train/dr_pretrained_5_CoT_result7.jsonl"

# 调用函数处理文件
process_jsonl(input_jsonl_path, output_jsonl_path)
