import pandas as pd

# 读取CSV文件
file_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_athletes_processed.csv'
df = pd.read_csv(file_path)

# 筛选出没有获得奖牌的记录
no_medal_df = df[df['Medal'] == 'No medal']

# 获取每个国家的所有年份
total_years = df['Year'].nunique()

# 找出所有年份内没有获得奖牌的国家（Team）
no_medal_teams = no_medal_df.groupby('Team')['Year'].nunique()

# 只保留那些在所有年份中都没有奖牌的国家
teams_without_medals = no_medal_teams[no_medal_teams == total_years].index.tolist()

# 输出没有获得奖牌的国家
print("没有获得奖牌的国家:", teams_without_medals)
