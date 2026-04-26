# diagnose_director.py
import pandas as pd
from collections import Counter
import os

print("=== 开始诊断导演数据 ===")

try:
    # 1. 检查文件是否存在
    csv_path = 'data.csv'
    if not os.path.exists(csv_path):
        print(f"❌ 错误：找不到数据文件 {csv_path}")
    else:
        print(f"✅ 找到数据文件: {csv_path}")

        # 2. 尝试读取数据
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
        print(f"   成功读取，数据总行数: {len(df)}")

        # 3. 查看导演列格式
        print(f"\n   'director' 列前3行内容:")
        print(f"   {df['director'].head(3).tolist()}")

        # 4. 统计导演
        all_directors = []
        for director in df['director']:
            if pd.isna(director):
                continue
            s = str(director).strip()
            if s in ['', '未知']:
                continue
            # 简单分割
            for sep in ['/', '、']:
                if sep in s:
                    all_directors.extend([p.strip() for p in s.split(sep) if p.strip()])
                    break
            else:
                all_directors.append(s)

        # 5. 输出统计结果
        counter = Counter(all_directors)
        top_10 = counter.most_common(10)

        print(f"\n✅ 导演统计完成，共 {len(counter)} 位不同的导演。")
        print(f"\n📊 作品最多的前10名导演:")
        for i, (name, count) in enumerate(top_10, 1):
            print(f"   {i:2d}. {name:<20} - {count} 部")

except Exception as e:
    print(f"\n❌ 诊断过程中发生错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n=== 诊断结束 ===")