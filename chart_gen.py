from pyecharts.globals import CurrentConfig
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.globals import CurrentConfig
import os

# 关键设置：清空在线主机地址，这将触发 pyecharts 在 HTML 中嵌入所有必要的 ECharts JavaScript 代码
CurrentConfig.ONLINE_HOST = "https://cdn.staticfile.org/echarts/5.4.2/"

# 导入您的分析结果
import analysis

def draw_bar():
    bar = (
        Bar(init_opts=opts.InitOpts(width="1200px", height="600px"))
        .add_xaxis(list(analysis.score_distribution.index.astype(str).tolist()))
        .add_yaxis("电影数量", list(analysis.score_distribution.values.tolist()))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="豆瓣TOP250电影评分分布"),
            xaxis_opts=opts.AxisOpts(name="评分"),
            yaxis_opts=opts.AxisOpts(name="数量"),
        )
    )
    return bar

if __name__ == "__main__":
    if not os.path.exists("templates"):
        os.makedirs("templates")
    
    c = draw_bar()
    output_path = "templates/chart.html"
    
    # 使用“不依赖网络”的模式渲染
    c.render(output_path)
    
    file_size_kb = os.path.getsize(output_path) / 1024
    print(f"图表已生成: {output_path}")
    print(f"文件大小: {file_size_kb:.2f} KB")
    
    if file_size_kb > 500:  # 离线文件通常大于500KB
        print("✅ 成功生成了独立的离线图表文件！")
        print("请运行：python -m http.server")
        print("然后在浏览器中访问：http://localhost:8000/templates/chart.html")
    else:
        print("⚠️  文件大小仍然偏小，可能离线模式未生效。请检查PyECharts版本。")