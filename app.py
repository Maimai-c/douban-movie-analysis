from flask import Flask, render_template
from chart_gen import draw_bar
from genre_pie import draw_genre_pie
from year_trend import draw_year_trend
from director_bar import draw_director_bar  # 新增：导入导演排行图
import os
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """
    主页路由，显示所有四个图表
    """
    try:
        # 1. 生成评分分布柱状图
        bar_chart = draw_bar()
        bar_html = bar_chart.render_embed() if bar_chart else "<p>评分分布图生成失败</p>"
        
        # 2. 生成类型分布饼图
        pie_chart = draw_genre_pie()
        pie_html = pie_chart.render_embed() if pie_chart else "<p>类型分布图生成失败</p>"
        
        # 3. 生成年度趋势折线图
        line_chart = draw_year_trend()
        line_html = line_chart.render_embed() if line_chart else "<p>年度趋势图生成失败</p>"
        
        # 4. 生成导演作品排行水平条形图
        director_chart = draw_director_bar()  # 新增
        director_html = director_chart.render_embed() if director_chart else "<p>导演排行图生成失败</p>"
        
        return render_template('index.html', 
                             bar_chart=bar_html, 
                             pie_chart=pie_html,
                             line_chart=line_html,
                             director_chart=director_html,  # 新增参数
                             title="豆瓣电影数据分析仪表盘",
                             now=datetime.now())
    except Exception as e:
        return f"图表生成错误: {str(e)}"

@app.route('/score_distribution')
def score_distribution():
    """单独显示评分分布图"""
    try:
        chart = draw_bar()
        if chart:
            return chart.render_embed()
        return "<p>图表生成失败</p>"
    except Exception as e:
        return f"错误: {str(e)}"

@app.route('/genre_distribution')
def genre_distribution():
    """单独显示类型分布图"""
    try:
        chart = draw_genre_pie()
        if chart:
            return chart.render_embed()
        return "<p>图表生成失败</p>"
    except Exception as e:
        return f"错误: {str(e)}"

@app.route('/year_trend')
def year_trend():
    """单独显示年度趋势图"""
    try:
        chart = draw_year_trend()
        if chart:
            return chart.render_embed()
        return "<p>图表生成失败</p>"
    except Exception as e:
        return f"错误: {str(e)}"

@app.route('/director_ranking')
def director_ranking():
    """单独显示导演作品排行图 (新增路由)"""
    try:
        chart = draw_director_bar()
        if chart:
            return chart.render_embed()
        return "<p>图表生成失败</p>"
    except Exception as e:
        return f"错误: {str(e)}"

if __name__ == '__main__':
    # 确保模板目录存在
    if not os.path.exists("templates"):
        os.makedirs("templates")
    
    print("=" * 50)
    print("豆瓣电影数据分析系统启动中...")
    print("访问地址: http://localhost:5000")
    print("=" * 50)
    
    app.run(debug=True, port=5000)