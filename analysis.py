import pandas as pd

df = pd.read_csv('data.csv')

# 1. 清洗：去掉无评分的数据
df = df[df['score'] != '暂无']
df['score'] = df['score'].astype(float)

# 2. 核心统计（为画图做准备）
score_distribution = df['score'].value_counts().sort_index()
genre_count = {} # 这里简单演示，实际需拆分类型字符串
print("统计完成，等待画图...")