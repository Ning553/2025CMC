import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
#from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split

# 数据预处理

# 加载数据
file_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\运动员获奖情况（没获奖的删除）。csv'

data = pd.read_csv(file_path)

# 查看数据
data.head()

# 确保数据中没有缺失值（尤其是获奖信息）
data = data.dropna(subset=['Bronze', 'Gold', 'Silver', 'Total_Medal'])

# 将年份数据转为整数
data['Year'] = data['Year'].astype(int)

# 按国家和年份进行排序
data = data.sort_values(by=['Team', 'Year'])

# 选择需要的列进行预测
data = data[['Team', 'Year', 'Bronze', 'Gold', 'Silver', 'Total_Medal']]

# 查看数据的描述性统计
data.describe()

# 数据格式化

# 先获取所有国家的列表
countries = data['Team'].unique()

# 构建训练数据
X = []
y = []

# 假设用过去5年的数据来预测未来一年的奖牌数
time_steps = 5

for country in countries:
    country_data = data[data['Team'] == country]

    # 按年份排序
    country_data = country_data.sort_values(by='Year')

    # 滚动窗口，创建时间序列
    for i in range(time_steps, len(country_data)):
        X.append(country_data[['Bronze', 'Gold', 'Silver', 'Total_Medal']].iloc[i - time_steps:i].values)
        y.append(country_data[['Bronze', 'Gold', 'Silver', 'Total_Medal']].iloc[i].values)

# 转换为 NumPy 数组
X = np.array(X)
y = np.array(y)

# 检查数据的形状
print(X.shape, y.shape)

# 数据标准化
# 对X进行标准化
scaler = StandardScaler()

# 遍历每个国家进行标准化
X_reshaped = X.reshape((-1, X.shape[2]))  # 将X变成二维（样本数 * 特征数）的形状
X_scaled = scaler.fit_transform(X_reshaped)

# 恢复回原来的三维形状
X_scaled = X_scaled.reshape((X.shape[0], X.shape[1], X.shape[2]))

# 检查标准化后的数据形状
print(X_scaled.shape)

# 构建 seq2seq2模型

# 构建 Seq2Seq 模型
model = Sequential()

# 编码器部分
model.add(LSTM(units=64, return_sequences=True, input_shape=(X_scaled.shape[1], X_scaled.shape[2])))
model.add(Dropout(0.2))

# 解码器部分
model.add(LSTM(units=64, return_sequences=False))
model.add(Dropout(0.2))

# 输出层
model.add(Dense(units=4))  # 4个输出：Bronze, Gold, Silver, Total_Medal

# 编译模型
model.compile(optimizer='adam', loss='mean_squared_error')

# 查看模型结构
model.summary()


# 拆分训练集和测试集

# 拆分数据集（80%训练，20%测试）
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, shuffle=False)

# 训练模型
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

# 评估模型
# 评估模型
test_loss = model.evaluate(X_test, y_test)
print(f'Test Loss: {test_loss}')

#预测

# 获取最新的数据进行预测（假设输入的是2016到2024年的数据）
country = '中国'  # 假设预测中国的奖牌
latest_data = data[(data['Team'] == country) & (data['Year'] >= 2016)]

# 选择过去5年的数据（如果年份大于2023年，则可能需要预测）
X_predict = latest_data[['Bronze', 'Gold', 'Silver', 'Total_Medal']].values[-time_steps:]

# 标准化数据
X_predict_scaled = scaler.transform(X_predict.reshape(-1, 4)).reshape(1, time_steps, 4)

# 预测2028年奖牌
predicted_medals = model.predict(X_predict_scaled)

# 输出预测结果
predicted_medals = predicted_medals.flatten()
print(f"Predicted Medals for {country} in 2028:")
print(f"Bronze: {predicted_medals[0]}")
print(f"Gold: {predicted_medals[1]}")
print(f"Silver: {predicted_medals[2]}")
print(f"Total Medals: {predicted_medals[3]}")
# 预测结果可视化
# 可视化预测和实际数据的对比
plt.figure(figsize=(10, 6))
plt.plot([2024, 2028], [latest_data['Gold'].iloc[-1], predicted_medals[1]], label='Gold')
plt.plot([2024, 2028], [latest_data['Silver'].iloc[-1], predicted_medals[2]], label='Silver')
plt.plot([2024, 2028], [latest_data['Bronze'].iloc[-1], predicted_medals[0]], label='Bronze')
plt.xlabel('Year')
plt.ylabel('Medal Count')
plt.title(f'Predicted Medal Count for {country} in 2028')
plt.legend()
plt.show()
