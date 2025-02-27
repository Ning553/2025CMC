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
additional_info = df.groupby('Name').first()[['Sex', 'Team', 'Year', 'Sport', 'Event']]

# 将奖牌统计与其他信息合并，并显式添加 'Name' 列
result_df = pd.merge(additional_info, medal_counts, on='Name', how='left')

# 对没有获得奖牌的运动员，填充金、银、铜牌数以及总奖牌数为零
result_df['Gold'] = result_df['Gold'].fillna(0)
result_df['Silver'] = result_df['Silver'].fillna(0)
result_df['Bronze'] = result_df['Bronze'].fillna(0)
result_df['Total_Medals'] = result_df[['Gold', 'Silver', 'Bronze']].sum(axis=1)

# 保存结果为新的CSV文件
output_file_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\运动员获奖情况_处理后6.csv'
result_df.to_csv(output_file_path, index=False)

print(f"结果已保存为: {output_file_path}")
