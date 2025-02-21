import json
import numpy as np
from sklearn.metrics import confusion_matrix

# 预定义的种族列表，只有这些种族是有效的
valid_races = [
    "White alone, not Hispanic or Latino",
    "Black or African American",
    "Asian",
    "Hispanic or Latino"
]

def load_jsonl(file_path):
    """加载jsonl文件，返回每条记录为字典的列表"""
    with open(file_path, 'r') as file:
        return [json.loads(line.strip()) for line in file]

def preprocess_data(jsonl_data):
    """预处理数据，移除无效的tract和dominant_race"""
    cleaned_data = []
    for entry in jsonl_data:
        tract = entry.get("tract")
        dominant_race = entry.get("dominant_race")
        
        # 检查 tract 和 dominant_race 是否有效，且 tract 必须是字符串
        if tract and isinstance(tract, str) and dominant_race in valid_races:
            cleaned_data.append(entry)

    return cleaned_data

def get_dominant_race_dict(jsonl_data):
    """将jsonl数据转换为字典形式，key为tract，value为dominant_race"""
    return {entry['tract']: entry['dominant_race'] for entry in jsonl_data}

def print_confusion_details(predictions, ground_truth, labels):
    """输出真实值为某种族时，预测成各种族的样例数目"""
    # 仅选择在 predictions 和 ground_truth 中都存在的 tract
    common_tracts = set(predictions.keys()) & set(ground_truth.keys())
    
    # 获取实际和预测值
    y_true = [ground_truth[tract] for tract in common_tracts]
    y_pred = [predictions[tract] for tract in common_tracts]
    
    # 生成混淆矩阵
    conf_matrix = confusion_matrix(y_true, y_pred, labels=labels)

    # 输出每个种族的预测情况
    for i, true_race in enumerate(labels):
        print(f"\nActual: {true_race}")
        for j, predicted_race in enumerate(labels):
            print(f"  Predicted {predicted_race}: {conf_matrix[i][j]}")

def main():
    # 加载jsonl文件
    jsonl1_file = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/tract_dominant_race_images_match_method1.jsonl"  # 预测结果文件路径
    jsonl2_file = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/tract_dominant_race_train.jsonl"  # 实际结果文件路径
    
    jsonl1_data = load_jsonl(jsonl1_file)
    jsonl2_data = load_jsonl(jsonl2_file)
    
    # 预处理数据，移除无效的记录
    jsonl1_data = preprocess_data(jsonl1_data)
    jsonl2_data = preprocess_data(jsonl2_data)
    
    # 转换为字典形式
    predictions = get_dominant_race_dict(jsonl1_data)
    ground_truth = get_dominant_race_dict(jsonl2_data)
    
    # 定义种族标签
    labels = [
        "White alone, not Hispanic or Latino",
        "Black or African American",
        "Asian",
        "Hispanic or Latino"
    ]
    
    # 输出混淆矩阵详细情况
    print_confusion_details(predictions, ground_truth, labels)

# 调用主函数
main()
