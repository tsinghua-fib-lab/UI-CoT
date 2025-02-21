import json
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from scipy.stats import gaussian_kde
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from matplotlib.colors import LinearSegmentedColormap

# 文件路径
jsonl_file_path = '/data3/maruolong/Train_Data/Add_Path/bw_ratio/UrbanMLLM_train/bw_5_CoT_pretrained_result.jsonl'   # 替换为你的 JSONL 文件路

# 初始化统计变量
valid_samples = []
total_samples = 0

# 读取 JSONL 文件
with open(jsonl_file_path, 'r') as f:
    for line in f:
        total_samples += 1
        sample = json.loads(line.strip())
        # label = sample['ground_truth'].strip()
        # predict = sample['text'].strip()
        label = sample['label']
        predict = sample['predict']

        try:
            # 转换为浮点数，验证是否为数字
            label = float(label)
            predict = float(predict)
            if predict < 0 or predict > 2:
                continue
            valid_samples.append((label, predict))
        except:
            # 如果转换失败，跳过该样例
            continue

# 如果没有有效样例，直接退出
if not valid_samples:
    print("没有有效样例。")
    exit()


# 提取有效样例的真值和预测值
labels = [label for label, predict in valid_samples]
predictions = [predict for label, predict in valid_samples]
correct_count = sum(1 for label, predict in valid_samples if abs(label - predict) <= 0.2)
accuracy = correct_count / len(labels) if len(labels) > 0 else 0
# 计算 MSE、MAE 和 R²
mse = mean_squared_error(labels, predictions)
mae = mean_absolute_error(labels, predictions)
r2 = r2_score(labels, predictions)

print(f'有效样本数量: {len(labels)}')
print(f'MSE: {mse}')
print(f'MAE: {mae}')
print(f'R²: {r2}')
print(f'准确率: {accuracy:.4f}')

# 提取有效样例的真值和预测值
labels = [label for label, predict in valid_samples]
predictions = [predict for label, predict in valid_samples]

# 使用 Gaussian KDE 计算点的密度
xy = np.vstack([labels, predictions])  # 将 x 和 y 数据堆叠成一个 2D 数组
kde = gaussian_kde(xy)  # 创建高斯核密度估计对象
densities = kde(xy)  # 计算每个点的密度

# 创建散点图
plt.figure(figsize=(6, 6))
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["axes.titlesize"] = 22  # 设置轴标题的字体大小
matplotlib.rcParams["axes.labelsize"] = 22  # 设置轴标签的字体大小
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.gca().set_aspect('equal', adjustable='box')
colors = [(0, "lightblue"), (0.5, "royalblue"), (1, "black")]  # 从浅到深的蓝色
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)
scatter = plt.scatter(labels, predictions, c=densities, alpha=0.7, cmap='Blues')  # 使用 'viridis' colormap 上色
plt.plot([min(labels), max(labels)], [min(labels), max(labels)], color='red', linestyle='--')
plt.xlabel('True Racial Income Ratio')
plt.ylabel('Predicted Racial Income Ratio')
plt.ylim(0, 2)
# plt.title('True vs Predicted B-W Income Ratio (UrbanMLLM & CoT)')
cbar = plt.colorbar(scatter, label='Density', shrink = 0.7)  # 显示颜色条，表示密度
cbar.ax.tick_params(labelsize=16)  # 设置颜色条刻度字体大小
cbar.set_label('Density', fontsize=16)  # 设置颜色条标签的字体大小
plt.grid(alpha=0.4)
plt.tight_layout()

# 保存散点图
#plt.savefig('/data3/maruolong/Train_Data/Add_Path/bw_ratio/UrbanMLLM_train/bw_UrbanMLLM_CoT_pretrained_scatter_plot.pdf', transparent = True)
# 显示图表
plt.show()