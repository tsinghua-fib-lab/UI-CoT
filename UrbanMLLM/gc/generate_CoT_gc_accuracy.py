import json
import math
import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# 文件路径
jsonl_file_path = '/data3/zhangxin/wuwen/vila-1.5/gini_results_attn/gini_cot/vila_train_all_sisv_pretrain_att_186w_clean_8B_cot.jsonl'  # 替换为你的 JSONL 文件路径

# 初始化统计变量
valid_samples = []
total_samples = 0

# 从文本中提取 Gini coefficient
def extract_gini_coefficient(text):
    match = re.search(r'Gini coefficient:\s*([\d.]+)', text)
    if match:
        return float(match.group(1))
    return None  # 如果没有找到，返回 None

# 读取 JSONL 文件
with open(jsonl_file_path, 'r') as f:
    for line in f:
        total_samples += 1

        # 跳过空行
        if not line.strip():
            continue
        
        try:
            # 尝试解析每一行 JSON 数据
            sample = json.loads(line.strip())
            
            # 提取实际的 Gini coefficient（从 ground_truth）
            ground_truth = extract_gini_coefficient(sample['ground_truth'])
            # 提取模型预测的 Gini coefficient（从 text）
            predicted = extract_gini_coefficient(sample['text'])

            # 如果都能提取到 Gini coefficient，就添加到有效样本
            if ground_truth is not None and predicted is not None and predicted > 0 and predicted < 0.99:
                valid_samples.append((ground_truth, predicted))
        
        except json.JSONDecodeError:
            print(f"Skipping invalid JSON line: {line.strip()}")
        except KeyError as e:
            print(f"Missing expected key in sample {sample.get('question_id', 'Unknown')}: {e}")
        except Exception as e:
            print(f"Error processing sample {sample.get('question_id', 'Unknown')}: {e}")

# 如果没有有效样例，直接退出
if not valid_samples:
    print("没有有效样例。")
    exit()

# 统计正确样例数
correct_count = sum(1 for label, predict in valid_samples if abs(label - predict) <= 2.0)

# 提取有效样例的真值和预测值
labels = [label for label, predict in valid_samples]
predictions = [predict for label, predict in valid_samples]

# 计算 MSE、MAE 和 R²
mse = mean_squared_error(labels, predictions)
mae = mean_absolute_error(labels, predictions)
r2 = r2_score(labels, predictions)

print(f'有效样本数量: {len(labels)}')
print(total_samples)
print(f'MSE: {mse}')
print(f'MAE: {mae}')
print(f'R²: {r2}')

# 使用 Gaussian KDE 计算点的密度
xy = np.vstack([labels, predictions])  # 将 x 和 y 数据堆叠成一个 2D 数组
kde = gaussian_kde(xy)  # 创建高斯核密度估计对象
densities = kde(xy)  # 计算每个点的密度

# 创建散点图
plt.figure(figsize=(6, 6))
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["axes.titlesize"] = 18  # 设置轴标题的字体大小
matplotlib.rcParams["axes.labelsize"] = 16  # 设置轴标签的字体大小
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
scatter = plt.scatter(labels, predictions, c=densities, alpha=0.7, cmap='viridis')  # 使用 'viridis' colormap 上色
plt.plot([min(labels), max(labels)], [min(labels), max(labels)], color='red', linestyle='--')
plt.xlabel('True Gini Coefficient')
plt.ylabel('Predicted Gini Coefficient')
plt.ylim(0.25, 0.7)  # 设置Y轴的范围
# plt.title('True vs Predicted Gini Coefficient (UrbanMLLM & CoT)')
cbar = plt.colorbar(scatter, label='Density')  # 显示颜色条，表示密度
cbar.ax.tick_params(labelsize=14)  # 设置颜色条刻度字体大小
plt.grid(alpha=0.4)
plt.tight_layout()

# 保存散点图
plt.savefig('/data3/maruolong/Train_Data/Add_Path/Train_result/gc_UrbanMLLM_pretrained_scatter_plot.png')

# 显示图表
plt.show()
