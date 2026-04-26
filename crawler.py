import requests
from bs4 import BeautifulSoup
import time
import random
import csv
import re  # 新增导入正则库

# 🔐 保命设置：伪装浏览器 + 延时
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
base_url = "https://movie.douban.com/top250" # 只爬TOP250，可控

def get_page(url):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        if r.status_code != 200:
            print(f"警告：页面状态码为 {r.status_code}")
            return None
        return r.text
    except Exception as e:
        print(f"请求出错：{e}")
        return None

def parse_data(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('div', class_='item')
    data_list = []

    for item in items:
        # 1. 片名
        title_elem = item.find('span', class_='title')
        title = title_elem.text.strip() if title_elem else "未知"

        # 2. 评分
        rating_elem = item.find('span', class_='rating_num')
        rating = rating_elem.text.strip() if rating_elem else "暂无"

        # 3. 导演（保持你原来的稳定版）
        director = "未知"
        bd_elem = item.find('div', class_='bd')
        if bd_elem:
            full_text = bd_elem.get_text(separator='\n')
            lines = full_text.split('\n')
            for line in lines:
                line = line.strip()
                if '导演:' in line:
                    parts = line.split('导演:')[-1].split('主演:')
                    if parts and parts[0].strip():
                        raw = parts[0].strip()
                        # 取第一个导演（按/或空格切）
                        if '/' in raw:
                            director = raw.split('/')[0].strip()
                        else:
                            director = raw.split()[0] if raw.split() else raw
                    break

        # ============== 重写：类型/年份/人数（统一从文本硬提）==============
        if not bd_elem:
            # 兜底
            genre, year, votes = "未知", "未知", "0"
        else:
            text_block = bd_elem.get_text(separator='|')  # 用|合并所有文本

            # 4. 类型：找“xx / xx”模式（至少两个中文词用/隔开）
            genre_match = re.search(r'([\u4e00-\u9fa5]+)\s*/\s*([\u4e00-\u9fa5]+)', text_block)
            genre = f"{genre_match.group(1)} / {genre_match.group(2)}" if genre_match else "未知"

            # 5. 年份：找4位数字（1900-202x）
            year_match = re.search(r'\b(19\d{2}|20[0-2]\d)\b', text_block)
            year = year_match.group(0) if year_match else "未知"

            # 6. 评价人数：找“123人评价”模式
            vote_match = re.search(r'(\d+)\s*人评价', text_block)
            votes = vote_match.group(1) if vote_match else "0"

        data_list.append({
            'name': title,
            'director': director,
            'score': rating,
            'genre': genre,
            'year': year,
            'votes': votes
        })

    return data_list

if __name__ == '__main__':
    all_data = []
    total_pages = 10
    page_size = 25
    
    for page in range(total_pages):
        start = page * page_size
        url = f"{base_url}?start={start}"
        print(f"[进度] 正在爬取第 {page+1}/{total_pages} 页: {url}")
        
        html = get_page(url)
        if not html:
            print(f"第 {page+1} 页获取失败，跳过")
            continue
            
        page_data = parse_data(html)
        print(f"本页解析到 {len(page_data)} 部电影")
        all_data.extend(page_data)
        
        delay = random.uniform(3, 8)
        time.sleep(delay)
            
    # ✅ 更新CSV列名
    filename = 'data.csv'
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        fieldnames = ['name', 'director', 'score', 'genre', 'year', 'votes']  # 扩充列
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_data)
    print(f"完成！共爬取 {len(all_data)} 条记录，已保存至 {filename}")