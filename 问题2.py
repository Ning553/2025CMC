import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

# 读取CSV文件
file_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\Q2_国力提现.csv'
data = pd.read_csv(file_path)

# 提取 NOC 和 Medal score 两列
noc_medal_data = data[['NOC', 'Medal score']]

# 按 Medal score 排序，便于可视化
noc_medal_data_sorted = noc_medal_data.sort_values('Medal score', ascending=True)

# 定义颜色
colors = []

# 给不同的排名分配颜色
for i in range(len(noc_medal_data_sorted)):
    if i < 5:
        colors.append((241/255, 196/255, 205/255))  # RGB(116, 27, 41)
    elif i < 10:
        colors.append((231/255, 124/255, 142/255))  # RGB(238, 63, 77)
    elif i < 15:
        colors.append((238/255, 63/255, 77/255))  # RGB(231, 124, 142)
    else:
        colors.append((116/255, 27/255, 41/255))  # RGB(241, 196, 205)

# 创建环状柱状图
angles = np.linspace(0, 2 * np.pi, len(noc_medal_data_sorted), endpoint=False).tolist()
radii = noc_medal_data_sorted['Medal score'].tolist()

# 创建极坐标图
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 6))

# 绘制环状柱状图
bars = ax.bar(angles, radii, color=colors, width=0.3, bottom=0.1)

# 设置标题
ax.set_title('Medal score by NOC', fontsize=16)

# 去掉极坐标图的刻度
ax.set_yticklabels([])

# 设置NOC标签
ax.set_xticks(angles)
ax.set_xticklabels(noc_medal_data_sorted['NOC'], fontsize=12, rotation=90)

# 显示图表
plt.tight_layout()
plt.show()
