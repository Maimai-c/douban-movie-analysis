import pandas as pd
import ast
from collections import Counter

# 1. 读取数据
df = pd.read_csv('data.csv')
print(f"数据总行数: {len(df)}")

# 2. 清洗导演数据
# 移除“未知”导演，并按分隔符（如“/”、“、”）分割多个导演
def split_directors(director_str):
    if pd.isna(director_str) or director_str == "未知":
        return []
    # 常见的导演分隔符：/ 、 、
    for sep in ['/', '、', ',', '，', '&', '&amp;', ' ']:
        if sep in str(director_str):
            return [d.strip() for d in str(director_str).split(sep) if d.strip()]
    return [str(director_str).strip()]

# 应用分割函数
all_directors = []
for directors in df['director'].apply(split_directors):
    all_directors.extend(directors)

# 3. 统计导演作品数量
director_count = Counter(all_directors)
print(f"统计到 {len(director_count)} 位不同的导演（包括联合导演）")

# 4. 按作品数量降序排列，并取前20名
top_n = 20
top_directors = director_count.most_common(top_n)

print(f"\n作品最多的前{top_n}位导演:")
for i, (director, count) in enumerate(top_directors, 1):
    print(f"{i:2d}. {director:20} - {count} 部")

# 5. 保存统计结果为CSV，供图表脚本使用
top_df = pd.DataFrame(top_directors, columns=['director', 'count'])
top_df.to_csv('director_stats.csv', index=False, encoding='utf-8-sig')
print(f"\n导演统计数据已保存至: director_stats.csv")
