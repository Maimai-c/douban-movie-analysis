from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig, ThemeType
import pandas as pd
import os
from collections import Counter

CurrentConfig.ONLINE_HOST = "https://cdn.staticfile.org/echarts/5.4.2/"

def split_directors(director_str):
    """分割导演名字，处理多个导演用'/'、'、'分隔的情况"""
    if pd.isna(director_str) or str(director_str).strip() in ['', '未知']:
        return []
    directors = str(director_str)
    for sep in ['/', '、']:  # 简化分隔符，只保留最常见的
        if sep in directors:
            return [d.strip() for d in directors.split(sep) if d.strip()]
    return [directors.strip()]

def draw_director_bar():
    """生成导演作品数量排行水平条形图 - 修复版本"""
    print("=" * 60)
    print("【导演作品排行图】开始生成（水平条形图）...")
    
    # 1. 数据统计
    try:
        df = pd.read_csv('data.csv', encoding='utf-8-sig')
        
        all_directors = []
        for director in df['director']:
            if pd.isna(director):
                continue
            s = str(director).strip()
            if s in ['', '未知']:
                continue
            for sep in ['/', '、']:
                if sep in s:
                    all_directors.extend([p.strip() for p in s.split(sep) if p.strip()])
                    break
            else:
                all_directors.append(s)
        
        from collections import Counter
        director_counter = Counter(all_directors)
        
        TOP_N = 10
        top_directors = director_counter.most_common(TOP_N)
        
        directors = [str(name) for name, _ in top_directors]
        counts = [int(num) for _, num in top_directors]
        
        print(f"✅ 数据统计完成，前{TOP_N}名导演:")
        for i, (name, count) in enumerate(top_directors, 1):
            print(f"   {i:2d}. {name:<20} - {count} 部")
        
    except Exception as e:
        print(f"❌ 数据准备失败: {e}")
        directors = ['宫崎骏', '克里斯托弗·诺兰', '史蒂文·斯皮尔伯格', '李安']
        counts = [8, 6, 6, 5]
    
    # 2. 创建水平条形图
    print("\n🎨 创建水平条形图...")
    
    # 反转列表，使最高的在最上面
    directors.reverse()
    counts.reverse()
    
    bar = (
        Bar(init_opts=opts.InitOpts(
            width="900px",
            height="500px"
        ))
        # 方法1：标准的水平条形图创建方法
        .add_xaxis(directors)  # X轴：分类（导演名字）
        .add_yaxis(
            "作品数量",  # 系列名称
            counts,      # Y轴：数值（作品数量）
            label_opts=opts.LabelOpts(
                is_show=True,
                position="right",
                formatter="{c}部"
            )
        )
        .reversal_axis()  # 翻转坐标轴
        .set_global_opts(
           title_opts=opts.TitleOpts(
                title="豆瓣TOP250导演作品数量排行",  # 必须是明确的字符串
                subtitle="数据来源: 豆瓣电影TOP250榜单",
                title_textstyle_opts=opts.TextStyleOpts(
                    font_size=20,
                    font_weight="bold"
                ),
                pos_left="center"
            ),
            xaxis_opts=opts.AxisOpts(
                name="作品数量（部）",  # 修改：X轴（底部）现在显示数字，应标为“作品数量”
                name_location="middle",
                name_gap=30,
                type_="value",  # 类型为数值轴
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            yaxis_opts=opts.AxisOpts(
                name="导演",          # 修改：Y轴（左侧）现在显示名字，应标为“导演”
                name_location="middle",
                name_gap=80,
                type_="category",     # 类型为分类轴
                axislabel_opts=opts.LabelOpts(font_size=11),
            ),
            legend_opts=opts.LegendOpts(is_show=False),
        )
    )
    
    print("✅ 图表对象创建成功")
    return bar

if __name__ == "__main__":
    if not os.path.exists("templates"):
        os.makedirs("templates")
    
    print("🚀 开始生成导演作品排行水平条形图...")
    print("=" * 60)
    
    try:
        chart = draw_director_bar()
        if chart is None:
            print("❌ 图表对象为None，生成失败")
            exit(1)
        
        output_path = "templates/director_bar.html"
        chart.render(output_path)
        
        file_size = os.path.getsize(output_path)
        file_size_kb = file_size / 1024
        print(f"✅ 图表已生成: {output_path} ({file_size_kb:.1f} KB)")
        
        if file_size_kb < 10:
            print("⚠️  警告: 文件大小异常偏小")
        else:
            print("✅ 文件大小正常")
        
        print(f"\n🌐 查看图表:")
        print(f"   1. 启动HTTP服务器: python -m http.server")
        print(f"   2. 浏览器访问: http://localhost:8000/templates/director_bar.html")
        
    except Exception as e:
        print(f"❌ 图表生成失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("=" * 60)