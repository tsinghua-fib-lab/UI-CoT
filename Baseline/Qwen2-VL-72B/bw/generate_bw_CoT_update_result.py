import json
import re

# 定义提取Income Ratio的函数
def extract_income_ratio(text):
    # 使用正则表达式匹配 'Income Ratio: ' 后面的数字
    match = re.search(r'Income Ratio:\s*([\d\.]+)', text)
    if match:
        return float(match.group(1))  # 提取并返回为浮动数值
    else:
        return None  # 如果未找到，返回null

# 读取原始jsonl文件
input_file_path = '/data3/maruolong/Train_Data/change_path_number/bw/result/5_images_bw_CoT_result.jsonl'
output_file_path = '/data3/maruolong/Train_Data/change_path_number/bw/result/5_images_bw_CoT_result_update.jsonl'

with open(input_file_path, 'r', encoding='utf-8') as infile, open(output_file_path, 'w', encoding='utf-8') as outfile:
    for line in infile:
        sample = json.loads(line)  # 解析原始的jsonl文件
        
        # 提取label中的Income Ratio
        label_income_ratio = extract_income_ratio(sample.get('label', ''))
        
        # 提取predict中的Income Ratio
        predict_income_ratio = extract_income_ratio(sample.get('predict', ''))
        
        # 构建新的样本数据
        new_sample = {
            'tract': sample.get('tract', ''),
            'label': label_income_ratio,
            'predict': predict_income_ratio
        }
        
        # 写入到新的jsonl文件
        json.dump(new_sample, outfile, ensure_ascii=False)
        outfile.write('\n')  # 每个sample写入后换行
