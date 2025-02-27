import pandas as pd

# 读取CSV文件时指定编码格式
file_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_athletes.csv'

# 尝试使用不同的编码格式读取文件
try:
    df = pd.read_csv(file_path, encoding='utf-8-sig')  # 尝试使用 utf-8-sig 编码
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_path, encoding='gbk')  # 如果 utf-8-sig 失败，尝试 gbk 编码
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')  # 如果 gbk 也失败，尝试 latin1 编码

# 根据年份筛选数据（只选择2024和2020）
df_2_years = df[df['Year'].isin([2024, 2020])]

# 找到所有金牌的行
gold_medals = df_2_years[df_2_years['Medal'] == 'Gold']

# 获取每个 Event 和 Team 的组合
event_gold_teams = gold_medals.groupby(['Event', 'Team']).size().reset_index(name='count')

# 获取所有 Event 中每个 Team 都获得金牌的 Team
# 这里我们需要确认每个 Event 都有金牌并且每个 Team 都参与了
gold_teams_all_events = event_gold_teams.groupby('Team').filter(lambda x: len(x) == len(gold_medals['Event'].unique()))

# 提取满足条件的 Team
result_teams = gold_teams_all_events['Team'].unique()

# 创建一个 DataFrame 保存结果
result_df = pd.DataFrame(result_teams, columns=['Team'])

# 保存结果到新的 CSV 文件
output_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\金牌.csv'
result_df.to_csv(output_path, index=False, encoding='utf-8-sig')

print("金牌国家（Team）已保存至文件：金牌.csv")
