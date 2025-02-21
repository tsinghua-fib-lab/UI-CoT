import json
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.special import kl_div
from matplotlib.colors import LinearSegmentedColormap

correct_count = 0

def parse_percentage(value):
    """将百分比值转换为小数，如果不含百分号直接返回浮点数"""
    try:
        if "%" in value:
            return float(value.strip("%")) / 100
        return float(value)
    except ValueError:
        raise ValueError(f"Invalid percentage value: {value}")

def extract_data_from_jsonl(jsonl_path):
    true_ginis = []
    pred_ginis = []
    true_levels = []
    pred_levels = []

    with open(jsonl_path, 'r') as f:
        for line in f:
            sample = json.loads(line.strip())
            label = sample['label']
            predict = sample['predict']

            # 提取基尼系数
            try:
                true_gini_str = label.split("Gini coefficient: ")
                true_gini = float(true_gini_str[1].strip()) if len(true_gini_str) > 1 else None
                if true_gini is None or true_gini <= 0 or not isinstance(true_gini, (float, int)):
                    raise ValueError("Invalid true Gini coefficient")
            except Exception as e:
                print(f"Error extracting true Gini coefficient for sample {sample.get('tract')}: {e}")
                continue

            try:
                pred_gini_str = predict.split("Gini coefficient: ")
                pred_gini = float(pred_gini_str[1].strip().split("\n")[0]) if len(pred_gini_str) > 1 else None
                if pred_gini is None or pred_gini <= 0 or pred_gini >= 1.0:
                    raise ValueError("Invalid predicted Gini coefficient")
            except Exception as e:
                print(f"Error extracting predicted Gini coefficient for sample {sample.get('tract')}: {e}")
                continue

            true_ginis.append(true_gini)
            pred_ginis.append(pred_gini)
            if abs(true_gini - pred_gini) <= 0.05:
                global correct_count
                correct_count += 1

            # 提取收入层级的比例，确保LEVEL1到LEVEL10都有值，若没有则赋值为0
            true_level = [0] * 10
            pred_level = [0] * 10

            for line in label.split("\n")[1:-1]:
                if "LEVEL" in line:
                    try:
                        level_num = int(line.split(":")[0].strip().replace("LEVEL", "")) - 1
                        level_value = parse_percentage(line.split(":")[1].strip().split(",")[0])
                        true_level[level_num] = level_value
                    except Exception as e:
                        print(f"Skipping invalid LEVEL line in label: {line} - {e}")

            for line in predict.split("\n")[1:-1]:
                if "LEVEL" in line:
                    try:
                        level_num = int(line.split(":")[0].strip().replace("LEVEL", "")) - 1
                        level_value = parse_percentage(line.split(":")[1].strip().split(",")[0])
                        pred_level[level_num] = level_value
                    except Exception as e:
                        print(f"Skipping invalid LEVEL line in predict: {line} - {e}")

            true_levels.append(true_level)
            pred_levels.append(pred_level)

    return np.array(true_ginis), np.array(pred_ginis), np.array(true_levels), np.array(pred_levels)

# 使用示例
jsonl_path = '/data3/maruolong/Train_Data/change_path_number/gc/result/10_images_gc_CoT_result.jsonl'
true_ginis, pred_ginis, true_levels, pred_levels = extract_data_from_jsonl(jsonl_path)

# 计算 MSE、MAE 和 R²
mse = mean_squared_error(true_ginis, pred_ginis)
mae = mean_absolute_error(true_ginis, pred_ginis)
r2 = r2_score(true_ginis, pred_ginis)
accuracy = correct_count / len(true_ginis) if len(true_ginis) > 0 else 0

print(f'MSE: {mse}')
print(f'MAE: {mae}')
print(f'R²: {r2}')
print(f'准确率: {accuracy:.4f}')

# 使用 Gaussian KDE 计算点的密度
xy = np.vstack([true_ginis, pred_ginis])  # 将 x 和 y 数据堆叠成一个 2D 数组
kde = gaussian_kde(xy)  # 创建高斯核密度估计对象
densities = kde(xy)  # 计算每个点的密度

# 绘制基尼系数对比的散点图
plt.figure(figsize=(6, 6))
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["axes.titlesize"] = 18  # 设置轴标题的字体大小
matplotlib.rcParams["axes.labelsize"] = 16  # 设置轴标签的字体大小
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
colors = [(0, "lightblue"), (0.5, "royalblue"), (1, "black")]  # 从浅到深的蓝色
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)
scatter = plt.scatter(true_ginis, pred_ginis, c=densities, alpha=0.7, cmap=cmap)
plt.plot([min(true_ginis), max(true_ginis)], [min(true_ginis), max(true_ginis)], color='red', linestyle='--')
plt.xlabel('True Gini Coefficient')
plt.ylabel('Predicted Gini Coefficient')
# plt.title('True vs Predicted Gini Coefficient (CoT & Qwen2-VL-72B & 10)')
cbar = plt.colorbar(scatter, label='Density') 
cbar.ax.tick_params(labelsize=14)  # 设置颜色条刻度字体大小
plt.grid(alpha=0.4)
plt.tight_layout()
#plt.savefig('/data3/maruolong/Train_Data/Add_Path/baseline/Qwen2-VL-72B/gc_test/gc_72B_CoT_scatter_plot.pdf')
plt.show()

# 计算所有真值收入层级比例和预测收入层级比例的KL散度
epsilon = 1e-10
kl_divergences = []

for true, pred in zip(true_levels, pred_levels):
    # 添加微小值来避免零
    true = np.array(true) + epsilon
    pred = np.array(pred) + epsilon

    kl_divergence = np.sum(kl_div(true, pred))
    if kl_divergence > -2 and kl_divergence < 2:
        kl_divergences.append(kl_divergence)

    #kl_divergences.append(kl_divergence)

# 计算所有样本的平均KL散度
print(len(kl_divergences))
average_kl_divergence = np.mean(kl_divergences)
print(f'Average KL Divergence: {average_kl_divergence}')
