# 豆瓣电影TOP250数据分析系统

这是我的毕业设计项目。该系统能自动分析豆瓣TOP250电影数据，并通过网页图表展示分析结果。

## 主要功能
- **数据爬取**：从豆瓣抓取TOP250电影信息。
- **多维分析**：从评分、类型、年份、导演四个角度分析数据。
- **可视化图表**：生成柱状图、饼图、折线图、条形图。
- **网页仪表盘**：通过Flask框架将四个图表整合在一个网页中展示。

## 如何运行
1.  **安装依赖**：`pip install -r requirements.txt`
2.  **启动应用**：`python app.py`
3.  **访问应用**：在浏览器打开 `http://localhost:5000`

## 系统截图
![豆瓣电影数据分析系统仪表盘截图](screenshots/dashboard.png)

## 项目结构
核心文件包括：
- `app.py` - 主程序
- `crawler.py` - 爬虫
- `data.csv` - 数据
- `templates/index.html` - 网页界面
- 以及 `chart_gen.py`, `genre_pie.py`, `year_trend.py`, `director_bar.py` 四个图表生成脚本。

> 数据来源：豆瓣电影TOP250，仅用于学习研究。