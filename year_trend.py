from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig, ThemeType
import analysis
import pandas as pd

CurrentConfig.ONLINE_HOST = "https://cdn.staticfile.org/echarts/5.4.2/"

def draw_year_trend():
    """生成电影年度数量趋势折线图"""
    # 从analysis模块获取年份数据
    # 如果analysis中没有，直接从CSV读取
    try:
        df = pd.read_csv('data.csv')
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        year_data = df['year'].dropna().astype(int).value_counts().sort_index()
    except:
        print("无法获取年份数据，使用示例数据")
        year_data = pd.Series({
            1994: 5, 1995: 4, 1997: 6, 1999: 5, 2000: 8,
            2001: 7, 2002: 6, 2003: 5, 2004: 8, 2005: 7,
            2006: 6, 2007: 5, 2008: 4, 2009: 7, 2010: 9,
            2011: 8, 2012: 7, 2013: 6, 2014: 5, 2015: 4,
            2016: 5, 2017: 6, 2018: 7, 2019: 8, 2020: 6
        })
    
    # 准备数据
    years = [str(int(year)) for year in year_data.index]
    counts = [int(count) for count in year_data.values]
    
    # 创建折线图
    line = (
        Line(init_opts=opts.InitOpts(
            theme=ThemeType.LIGHT, 
            width="1000px", 
            height="600px",
            bg_color="white"
        ))
        .add_xaxis(years)
        .add_yaxis(
            series_name="电影数量",
            y_axis=counts,
            is_smooth=True,  # 平滑曲线
            symbol="circle",  # 数据点形状
            symbol_size=8,
            linestyle_opts=opts.LineStyleOpts(width=3),
            itemstyle_opts=opts.ItemStyleOpts(
                border_width=2, 
                border_color="#fff"
            ),
            label_opts=opts.LabelOpts(is_show=False),  # 不显示数据标签
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="豆瓣TOP250电影年度分布趋势",
                subtitle="数据来源: 豆瓣电影TOP250榜单",
                title_textstyle_opts=opts.TextStyleOpts(font_size=20, font_weight="bold"),
                subtitle_textstyle_opts=opts.TextStyleOpts(font_size=12, color="#666"),
                pos_left="center"
            ),
            # 修复：移除不支持的axispointer_opts参数
            tooltip_opts=opts.TooltipOpts(
                trigger="axis",
                formatter="{a}<br/>{b}年: {c}部"
            ),
            xaxis_opts=opts.AxisOpts(
                name="上映年份",
                name_location="middle",
                name_gap=30,
                type_="category",  # 分类轴
                axislabel_opts=opts.LabelOpts(rotate=45),  # 标签旋转45度
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                splitline_opts=opts.SplitLineOpts(is_show=False)
            ),
            yaxis_opts=opts.AxisOpts(
                name="电影数量",
                name_location="middle",
                name_gap=50,
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                min_interval=1
            ),
            datazoom_opts=[
                opts.DataZoomOpts(range_start=0, range_end=100),  # 底部滑动条
                opts.DataZoomOpts(type_="inside")  # 内置缩放
            ],
            legend_opts=opts.LegendOpts(is_show=False),  # 单线图可不显示图例
        )
        .set_series_opts(
            areastyle_opts=opts.AreaStyleOpts(
                opacity=0.1,  # 面积图透明度
                color="rgba(102, 126, 234, 0.5)"  # 渐变填充色
            )
        )
    )
    return line

if __name__ == "__main__":
    import os
    
    if not os.path.exists("templates"):
        os.makedirs("templates")
    
    chart = draw_year_trend()
    output_path = "templates/year_trend.html"
    chart.render(output_path)
    
    file_size_kb = os.path.getsize(output_path) / 1024
    print(f"✅ 年度趋势折线图已生成: {output_path}")
    print(f"   文件大小: {file_size_kb:.2f} KB")
    print(f"\n请执行以下命令查看：")
    print(f"   1. 启动HTTP服务器: python -m http.server")
    print(f"   2. 在浏览器访问: http://localhost:8000/{output_path}")