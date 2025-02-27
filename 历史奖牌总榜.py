import pandas as pd

# 读取CSV文件
file_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\summerOly_medal_counts - 副本.csv'
# 尝试使用不同的编码格式读取文件
try:
    df = pd.read_csv(file_path, encoding='utf-8-sig')  # 尝试使用 utf-8-sig 编码
except UnicodeDecodeError:
    try:
        df = pd.read_csv(file_path, encoding='gbk')  # 如果 utf-8-sig 失败，尝试 gbk 编码
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')  # 如果 gbk 也失败，尝试 latin1 编码

# 按国家汇总奖牌数
country_medals = df.groupby('NOC')[['Bronze', 'Gold', 'Silver', 'Total']].sum()

# 将汇总后的结果保存到新CSV文件
output_path = r'C:\Users\lenovo\Desktop\2025MCM\2025_MCM-ICM_Problems\2025_Problem_C_Data\草稿3.csv'
country_medals.to_csv(output_path)

print(f"汇总结果已保存至: {output_path}")
