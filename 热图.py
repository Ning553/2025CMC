import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from matplotlib.colors import ListedColormap

# 载入数据
file_path = r'C:/Users/lenovo/Desktop/2025MCM/2025_MCM-ICM_Problems/2025_Problem_C_Data/correlation_matrix.csv'
data = pd.read_csv(file_path)

# 选择数值型列
data_numeric = data.select_dtypes(include=[np.number])

# 计算相关矩阵（皮尔逊相关系数）
correlation_matrix = data_numeric.corr(method='pearson')

# 计算p值矩阵
def compute_p_values(df):
    p_values = pd.DataFrame(np.ones_like(df.corr(), dtype=float), columns=df.columns, index=df.columns)
    for i in range(len(df.columns)):
        for j in range(i, len(df.columns)):
            _, p_value = pearsonr(df.iloc[:, i], df.iloc[:, j])
            p_values.iloc[i, j] = p_value
            p_values.iloc[j, i] = p_value
    return p_values

p_values = compute_p_values(data_numeric)


# 自定义调色板，使用你提供的RGB颜色
custom_colors = [
    #(0/255, 8/255, 51/255),  # RGB: 008 051 110
    (16/255, 92/255, 164/255), # RGB: 016 092 164
    (56/255, 136/255, 192/255), # RGB: 056 136 192
    (104/255, 172/255, 213/255), # RGB: 104 172 213
    (170/255, 207/255, 229/255), # RGB: 170 207 229
    (210/255, 227/255, 243/255), # RGB: 210 227 243
    # (244/255, 249/255, 254/255)  # RGB: 244 249 254
]


mask = p_values > 0.05
# 创建一个从高到低的调色板
cmap = ListedColormap(custom_colors[::-1])  # 使用[::-1]反转颜色顺序


# 绘制相关性热图
plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap=cmap, fmt='.2f', linewidths=0.5, mask = mask)

# 设置坐标轴标签字体大小
plt.xticks(fontsize=12, rotation=45)  # 横坐标字体倾斜45度
plt.yticks(fontsize=12)

# 设置标题居中并增加字体大小
plt.title('Correlation Matrix with Significance Mask', fontsize=18, loc='center')
# 显示图形
plt.show()
