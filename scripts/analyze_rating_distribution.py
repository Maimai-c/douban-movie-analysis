"""
计算豆瓣TOP250电影评分的核心统计量及区间占比。
用于生成论文第4.1.1节（评分分布分析）中的数据。

输入: 项目根目录下的 data.csv 文件
输出: 在终端打印平均值、中位数、区间占比等统计结果。
"""
# 计算评分统计量
import pandas as pd

# 1. 读取数据
df = pd.read_csv('data.csv', encoding='utf-8-sig')

# 2. 计算核心统计量
actual_rating_column = 'score'  # 关键修改：将'评分'改为'score'

rating_mean = df[actual_rating_column].mean()
rating_median = df[actual_rating_column].median()
print(f"评分平均值: {rating_mean:.2f}")
print(f"评分中位数: {rating_median:.2f}")

# 3. 计算评分区间占比
total_movies = len(df)
top_tier = df[df[actual_rating_column] >= 9.0]
high_core = df[(df[actual_rating_column] >= 8.5) & (df[actual_rating_column] < 9.0)]
gateway = df[df[actual_rating_column] < 8.5]

print(f"\n【评分区间占比】")
print(f"顶尖评分 (≥9.0): {len(top_tier)} 部，占比 {len(top_tier)/total_movies*100:.1f}%")
print(f"高分核心 (8.5-8.9): {len(high_core)} 部，占比 {len(high_core)/total_movies*100:.1f}%")
print(f"榜单入门 (<8.5): {len(gateway)} 部，占比 {len(gateway)/total_movies*100:.1f}%")

# 4. 查看整体统计
print(f"\n【描述性统计】")
print(df[actual_rating_column].describe())