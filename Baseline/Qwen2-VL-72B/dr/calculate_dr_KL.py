import json
import pandas as pd
import numpy as np

# 计算绝对误差和（sum_i |p_i,true - p_i,pred|）
def calculate_absolute_error(predict, label):
    """计算两个分布之间的绝对误差和"""
    # 计算绝对误差
    error = np.sum(np.abs(np.array(label) - np.array(predict)))
    return error

# 从 Excel 读取标准数据并处理
def read_and_process_standard_data(excel_file):
    # 读取 Excel 文件
    df = pd.read_excel(excel_file)
    
    # 提取相关列并除以 100 归一化
    df = df[['TRACT_ID', 'WHITE ALONE', 'BLACK', 'ASIAN', 'HISPANIC']]
    df['TRACT_ID'] = df['TRACT_ID'].astype(str)
    df = df.set_index('TRACT_ID')  # 将 tract_id 设置为索引
    
    # 将百分比除以100，确保所有种族的总和为1
    df = df / 100.0
    df['TOTAL'] = df.sum(axis=1)
    
    # 归一化，使总和为 1
    df = df.div(df['TOTAL'], axis=0)
    return df.drop(columns=['TOTAL'])  # 删除不再需要的 'TOTAL' 列

# 计算所有样本的平均绝对误差
def calculate_average_absolute_error(jsonl_file, standard_data):
    absolute_errors = []
    
    with open(jsonl_file, 'r') as file:
        for line in file:
            data = json.loads(line)
            tract_id = data['question_id']
            predict = [data['text'].get(race, 0) for race in ['White alone, not Hispanic or Latino', 'Black or African American', 'Asian', 'Hispanic or Latino']]

            # 获取预测值
            if None in predict:
                continue
            predict = [
                data['text'].get('White alone, not Hispanic or Latino', 0) / 100.0,
                data['text'].get('Black or African American', 0) / 100.0,
                data['text'].get('Asian', 0) / 100.0,
                data['text'].get('Hispanic or Latino', 0) / 100.0
            ]
            # predict = [
            #     data['predict'].get('White alone, not Hispanic or Latino', 0) / 100.0,
            #     data['predict'].get('Black or African American', 0) / 100.0,
            #     data['predict'].get('Asian', 0) / 100.0,
            #     data['predict'].get('Hispanic or Latino', 0) / 100.0
            # ]
            # 从标准数据中获取正确的种族比例
            if tract_id in standard_data.index:
                label = standard_data.loc[tract_id].values
                # 计算绝对误差和
                abs_error = calculate_absolute_error(predict, label)
                # if abs_error > 2:
                #     continue  # 如果误差过大则忽略该样本
                absolute_errors.append(abs_error)
    
    # 返回平均绝对误差
    return np.mean(absolute_errors)

# 示例：计算输入文件的平均绝对误差
excel_file = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/race_ratio.xlsx"  # 替换为标准数据的文件路径
jsonl_file = "/data3/maruolong/Train_Data/Add_Path/bw_ratio/UrbanMLLM_train/dr_pretrained_5_CoT_result.jsonl"  # 替换为 JSONL 文件路径

# 读取并处理标准数据
standard_data = read_and_process_standard_data(excel_file)

# 计算平均绝对误差
average_abs_error = calculate_average_absolute_error(jsonl_file, standard_data)
print(f"Average Absolute Error: {average_abs_error:.6f}")
