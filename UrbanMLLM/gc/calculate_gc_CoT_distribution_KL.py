import json
import numpy as np
from scipy.special import kl_div  # 计算KL散度

epsilon = 1e-10

def calculate_kl_divergence(predict, label):
    """计算两个分布之间的 KL 散度"""
    predict = np.array(predict)+epsilon
    label = np.array(label)+epsilon
    # 避免除零错误，添加一个极小值（例如1e-10）
    kl = np.sum(kl_div(label, predict))
    return kl

# 读取 JSONL 文件并计算平均 KL 散度
def calculate_average_kl(jsonl_file):
    kl_divergences = []
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            try:
                predict = [data["predict"][f"LEVEL{i}"] for i in range(1, 11)]
                label = [data["label"][f"LEVEL{i}"] for i in range(1, 11)]
            except:
                continue
            print(predict)
            print(label)
            # 计算当前 tract 的 KL 散度
            kl = calculate_kl_divergence(predict, label)
            if kl > -2 and kl < 2:
                kl_divergences.append(kl)
            # kl_divergences.append(kl)
    # 返回所有 tract 的平均 KL 散度
    return np.mean(kl_divergences)

# 示例：计算输入文件的平均 KL 散度
jsonl_file = "/data3/maruolong/Train_Data/Add_Path/Train_result/extract_from_5_CoT_pretrained_data2.jsonl"  # 替换为你的 JSONL 文件路径
average_kl = calculate_average_kl(jsonl_file)
print(f"Average KL Divergence: {average_kl:.4f}")
