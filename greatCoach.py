import pandas as pd

# 读取CSV文件时指定编码格式
file_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\运动员获奖情况_处理后6(没获奖的为0).csv'

# 尝试使用不同的编码格式读取文件
try:
    df = pd.read_csv(file_path, encoding='utf-8-sig')  # 尝试使用 utf-8-sig 编码
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_path, encoding='gbk')  # 如果 utf-8-sig 失败，尝试 gbk 编码
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')  # 如果 gbk 也失败，尝试 latin1 编码

# 根据年份筛选数据（只选择近六届：2024, 2020, 2016, 2012, 2008, 2004）
df_6_years = df[df['Year'].isin([2024, 2020, 2016, 2012, 2008, 2004])]

# 筛选出每个Event获得金牌的团队
def get_gold_streak_for_events(df, years):
    streak_teams = []
    for team in df['Team'].unique():
        team_data = df[df['Team'] == team].sort_values(by='Year')
        # 过滤出这些年中的金牌信息（即Gold > 0的情况）
        gold_events = team_data[team_data['Gold'] > 0 & team_data['Year'].isin(years)]
        # 如果在这几年内每个Event都获得了金牌，则视为符合条件
        if len(gold_events) == len(years):
            streak_teams.append(team)
    return df[df['Team'].isin(streak_teams)]

# 获取近三届（2024、2020、2016）在每个Event中获得金牌的团队
gold_streak_teams = get_gold_streak_for_events(df_6_years, [2024, 2020, 2016])

# 筛选连续三届金牌，但后续届未获得金牌的团队
def get_gold_streak_but_no_gold_next_for_events(df, streak_years):
    streak_teams = []
    for team in df['Team'].unique():
        team_data = df[df['Team'] == team].sort_values(by='Year')
        # 过滤出这些年中的金牌信息（即Gold > 0的情况）
        gold_events = team_data[team_data['Gold'] > 0 & team_data['Year'].isin(streak_years)]
        if len(gold_events) == len(streak_years):
            # 查找未来届是否没有金牌
            future_years = team_data[team_data['Year'].isin([2024, 2020, 2016, 2012, 2008, 2004]) & (team_data['Gold'] > 0)]
            if future_years.empty:  # 如果没有未来年份获得金牌，满足条件
                streak_teams.append(team)
    return df[df['Team'].isin(streak_teams)]

# 获取连续三届金牌，但之后届没获得金牌的团队（如2012、2016、2020 或 2008、2012、2016）
gold_streak_but_no_gold_next_teams = get_gold_streak_but_no_gold_next_for_events(df_6_years, [2012, 2016, 2020])

# 保存为新的CSV文件
output_path_1 = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\可能有金牌教练2.csv'
output_path_2 = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\可能要金牌教练2.csv'

gold_streak_teams.to_csv(output_path_1, index=False)
gold_streak_but_no_gold_next_teams.to_csv(output_path_2, index=False)

print("数据已成功保存到新的CSV文件！")
