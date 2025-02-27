import pandas as pd

# 读取CSV文件
file_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_athletes_processed.csv'
df = pd.read_csv(file_path)

# 筛选出有奖牌的记录
medal_df = df[df['Medal'] != 'No medal']

# 统计每个运动员获得的金、银、铜牌数以及总的奖牌数
medal_counts = medal_df.groupby('Name')['Medal'].value_counts().unstack(fill_value=0)

# 计算每个运动员的总奖牌数
medal_counts['Total_Medals'] = medal_counts.sum(axis=1)

# 获取每个运动员的其他信息（Sex, Team, Year, Sport, Event）并合并
# 这里通过 'first' 方法选择每个运动员在这些列中的第一个值
additional_info = df.groupby('Name').first()[['Sex', 'Team', 'Year', 'Sport', 'Event']]

# 将奖牌统计与其他信息合并
result_df = pd.merge(additional_info, medal_counts, on='Name')

# 保存结果为新的CSV文件
output_file_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\运动员获奖情况.csv'
result_df.to_csv(output_file_path, index=False)

print(f"结果已保存为: {output_file_path}")
