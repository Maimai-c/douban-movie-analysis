from pyecharts.charts import Pie
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig, ThemeType
import analysis  # 导入我们之前的数据分析模块

# 使用与第一个图表相同的CDN配置，确保资源加载一致
CurrentConfig.ONLINE_HOST = "https://cdn.staticfile.org/echarts/5.4.2/"

def draw_genre_pie():
    # 1. 准备数据：从analysis模块获取类型统计结果
    # 添加调试信息
    print(f"genre_count 类型: {type(analysis.genre_count)}")
    print(f"genre_count 内容: {analysis.genre_count}")
    
    # 确保genre_count是Counter对象并且不为空
    if not analysis.genre_count or len(analysis.genre_count) == 0:
        print("警告：类型统计数据为空，使用示例数据")
        # 使用示例数据以便调试
        from collections import Counter
        genre_data = Counter({
            '剧情': 85, '犯罪': 50, '爱情': 40, '喜剧': 35, 
            '动画': 30, '奇幻': 25, '冒险': 20, '悬疑': 18,
            '科幻': 15, '动作': 12, '其他': 20
        })
    else:
        genre_data = analysis.genre_count
    
    # 确保数据格式正确
    if not isinstance(genre_data, dict) and not hasattr(genre_data, 'items'):
        print(f"错误：genre_count 类型为 {type(genre_data)}，预期是字典或Counter")
        return None
    
    # 转换为PyECharts需要的格式：[('类型名', 数量), ...]，并取数量最多的前10项
    try:
        data_pairs = list(genre_data.items())
        print(f"数据对数量: {len(data_pairs)}")
        
        if len(data_pairs) == 0:
            print("警告：没有可用的类型数据")
            return None
            
        # 排序
        data_pairs.sort(key=lambda x: x[1], reverse=True)  # 按数量降序排序
        top_n = 10  # 展示前10种类型，其余归为"其他"
        
        if len(data_pairs) > top_n:
            # 取前N项
            main_data = data_pairs[:top_n]
            # 计算剩余类型的总数
            other_count = sum(count for _, count in data_pairs[top_n:])
            main_data.append(("其他", other_count))
        else:
            main_data = data_pairs
        
        print(f"最终使用的数据对: {main_data}")
        
    except Exception as e:
        print(f"数据处理错误: {e}")
        return None
    
    # 2. 创建饼图
    try:
        pie = (
            Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT, width="1000px", height="600px"))
            .add(
                series_name="电影类型",
                data_pair=main_data,
                radius=["30%", "60%"],  # 内半径30%，外半径60%，形成环形
                label_opts=opts.LabelOpts(
                    formatter="{b}: {c}部 ({d}%)",  # 标签格式：类型名: 数量 (百分比)
                    position="outside",  # 标签在外部，避免重叠
                ),
            )
            .set_global_opts(
                title_opts=opts.TitleOpts(
                    title="豆瓣TOP250电影类型分布",
                    subtitle="数据来源: 豆瓣电影TOP250榜单",
                    title_textstyle_opts=opts.TextStyleOpts(font_size=20)
                ),
                legend_opts=opts.LegendOpts(
                    type_="scroll",  # 图例可滚动，防止类型过多显示不全
                    orient="vertical",
                    pos_right="5%",
                    pos_top="15%",
                ),
                tooltip_opts=opts.TooltipOpts(
                    trigger="item",  # 触发类型为数据项
                    formatter="{a}<br/>{b}: {c}部 ({d}%)"  # 悬浮提示框格式
                ),
            )
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(trigger="item"),
            )
        )
        return pie
    except Exception as e:
        print(f"创建饼图错误: {e}")
        return None

if __name__ == "__main__":
    # 确保 templates 目录存在
    import os
    if not os.path.exists("templates"):
        os.makedirs("templates")
    
    # 生成图表
    chart = draw_genre_pie()
    if chart is None:
        print("❌ 饼图生成失败，请检查以上错误信息")
    else:
        output_path = "templates/genre_pie.html"
        chart.render(output_path)
        
        # 检查文件
        file_size_kb = os.path.getsize(output_path) / 1024
        print(f"✅ 类型分布饼图已生成: {output_path}")
        print(f"   文件大小: {file_size_kb:.2f} KB")
        print(f"\n请执行以下命令查看：")
        print(f"   1. 启动HTTP服务器: python -m http.server")
        print(f"   2. 在浏览器访问: http://localhost:8000/{output_path}")