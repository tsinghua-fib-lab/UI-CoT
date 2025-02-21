import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from scipy.stats import gaussian_kde
from matplotlib.colors import LinearSegmentedColormap

def calculate_metrics_and_plot(input_jsonl_path):
    """
    计算MSE、MAE、R²并绘制散点图。
    """
    # 用于存储真实值和预测值
    true_ginis = []
    predicted_ginis = []
    correct_count = 0
    # 读取JSONL文件并提取数据
    with open(input_jsonl_path, "r") as infile:
        for line in infile:
            sample = json.loads(line)
            true_ginis.append(sample["label"].get("GINI", 0))  # 真实值
            predicted_ginis.append(sample["predict"].get("Calculate GINI", 0))  # 预测值
            #predicted_ginis.append(sample["predict"].get("GINI", 0))  # 预测值
            if abs(sample["label"].get("GINI", 0) - sample["predict"].get("Calculate GINI", 0)) <= 0.05:
            # if abs(sample["label"].get("GINI", 0) - sample["predict"].get("GINI", 0)) <= 0.05:
                 correct_count += 1
    
    # 计算 MSE、MAE 和 R²
    mse = mean_squared_error(true_ginis, predicted_ginis)
    mae = mean_absolute_error(true_ginis, predicted_ginis)
    r2 = r2_score(true_ginis, predicted_ginis)
    accuracy = correct_count / len(true_ginis) if len(true_ginis) > 0 else 0
    
    print(f'有效样本数量: {len(true_ginis)}')
    print(f'MSE: {mse}')
    print(f'MAE: {mae}')
    print(f'R²: {r2}')
    print(f'准确率: {accuracy:.4f}')
    
    # 使用 Gaussian KDE 计算点的密度
    xy = np.vstack([true_ginis, predicted_ginis])  # 将真实值和预测值堆叠成一个 2D 数组
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
    scatter = plt.scatter(true_ginis, predicted_ginis, c=densities, alpha=0.7, cmap='Blues')  # 使用 'viridis' colormap 上色
    plt.plot([min(true_ginis), max(true_ginis)], [min(true_ginis), max(true_ginis)], color='red', linestyle='--')
    plt.xlabel('True Gini Coefficient')
    plt.ylabel('Predicted Gini Coefficient')
    plt.ylim(0.25, 0.7)
    plt.xlim(0.25, 0.7)
    # plt.ylim(0, 1)
    # plt.title('True vs Predicted Gini Coefficient (UrbanMLLM & CoT & Calculate)')
    cbar = plt.colorbar(scatter, label='Density', shrink = 0.7)  # 显示颜色条，表示密度
    cbar.ax.tick_params(labelsize=16)  # 设置颜色条刻度字体大小
    cbar.set_label('Density', fontsize=16)  # 设置颜色条标签的字体大小
    plt.grid(alpha=0.4)
    plt.tight_layout()

    # 保存散点图
    #plt.savefig('/data3/maruolong/Train_Data/Add_Path/Train_result/gc_UrbanMLLM_pretrained_CoT_scatter_plot.pdf', transparent = True)
    # plt.savefig('/data3/maruolong/Train_Data/change_path_number/gc/result/gc_5_CoT_test_scatter_plot.png')

    # 显示图表
    plt.show()

# 输入文件路径
input_jsonl_path = "/data3/maruolong/Train_Data/Add_Path/Train_result/extract_from_5_CoT_pretrained_data2.jsonl"


# 调用函数
calculate_metrics_and_plot(input_jsonl_path)
