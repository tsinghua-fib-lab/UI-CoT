import matplotlib.pyplot as plt
import numpy as np
import matplotlib

# 数据：RMSE 和 Accuracy
rmse_values = [0.4675, 0.5346, 0.2605, 0.2573]  # RMSE 值
acc_values = [0.3404, 0.3102, 0.5787, 0.5697]   # Accuracy 值

# 设定 2x2 网格的坐标
positions = [(0, 0), (0, 1), (1, 0), (1, 1)]  # 这对应高种族收入比高收入、高低、低高、低低的四个格子

# 计算圆的大小（可以放大一个常数因子来提高视觉效果）
accuracy_sizes = [acc * 70000 for acc in acc_values]

# 创建颜色的归一化对象
norm = plt.Normalize(0.1, 0.6)  # 将颜色映射范围设定为 RMSE 的最小和最大值
cmap = plt.cm.Blues # 使用 coolwarm 色谱

# 计算文本颜色（基于圆圈的颜色）
def get_text_color(value, cmap):
    """根据RMSE值的颜色，返回适合的文本颜色：浅色背景使用深色文本，深色背景使用浅色文本"""
    rgba = cmap(norm(value))  # 获取对应的RGBA颜色
    brightness = 0.2126 * rgba[0] + 0.7152 * rgba[1] + 0.0722 * rgba[2]  # 计算亮度
    return 'black' if brightness > 0.5 else 'white'  # 若亮度大于0.5，使用黑色文字；否则使用白色文字

# 绘图
plt.figure(figsize=(8, 8))
matplotlib.rcParams["font.family"] = "Times New Roman"
matplotlib.rcParams["axes.titlesize"] = 18  # 设置轴标题的字体大小
matplotlib.rcParams["axes.labelsize"] = 16  # 设置轴标签的字体大小
plt.xticks(fontsize=28)
plt.yticks(fontsize=28)
plt.gca().set_aspect('equal', adjustable='box')

# 绘制四个圆，分别对应四种情况
# 绘制四个圆，分别对应四种情况
for i, (rmse, acc, (x, y)) in enumerate(zip(rmse_values, acc_values, positions)):
    plt.scatter(x, y, s=accuracy_sizes[i], c=[rmse], cmap=cmap, edgecolors='black', alpha=0.8, norm=norm)
    # 获取合适的文本颜色
    text_color = get_text_color(rmse, cmap)
    plt.text(x, y, f'{acc:.4f}', ha='center', va='center', fontsize=30, color=text_color)

# 设置图像标签
plt.xlim(-0.5, 1.5)
plt.ylim(-0.5, 1.5)
plt.xticks([0, 1], ['High Racial\n Income Ratio', 'Low Racial\n Income Ratio'])
plt.yticks([0, 1], ['High\nIncome', 'Low\nIncome'])
#plt.title('RMSE and Accuracy for Different Scenarios')

# 展示图形
plt.tight_layout()
plt.savefig("/data3/maruolong/Train_Data/Add_Path/separate_by_gini_bw_and_income/result_bw/bw_income_accuracy_RMSE_plot.pdf")
plt.show()
