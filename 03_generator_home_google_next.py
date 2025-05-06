import pandas as pd
import random
import markdown
import os
import re
from datetime import datetime

def load_meetings(file_path):
    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")

def select_random_meetings(df, categories):
    selected_meetings = {}
    for category in categories:
        filtered = df[df["Topic"] == category]
        if not filtered.empty:
            selected_meetings[category] = filtered.sample(n=1).iloc[0].to_dict()
    return selected_meetings

def generate_markdown(selected_meetings):
    import pandas as pd
    # 將 selected_meetings 轉回 DataFrame 以便處理
    df = pd.DataFrame(selected_meetings.values())
    md_content = """# Google Cloud Next 2025
2025年 4 月 9 ─ 4 月 11 日  
Next 是我們的全球性展覽，展現靈感、創新和教育。決策者、開發者以及任何熱衷於普及、可擴展、具社會責任感的雲端人士，都將齊聚一堂，分享挑戰、解決方案、突破性的構想（10 倍速的創意）和改變遊戲規則的技術。

"""
    for _, row in df.iterrows():
        topic = row.get('Topic', 'N/A')
        meeting = row.get('Meeting', 'N/A')
        key = row.get('Key', 'N/A')
        md_content += f"# {topic}\n"
        md_content += f"## {meeting}\n"
        md_content += f"### {key}\n"
    return md_content

def markdown_to_email_html(md_content):
    # 轉換 Markdown 為 HTML
    html_content = markdown.markdown(md_content)
    
    # 提取標題和介紹文字，以便後續單獨處理
    title_match = re.search(r'<h1>(.*?)</h1>', html_content)
    title = "Google Cloud Next 2025"
    if title_match:
        title = title_match.group(1)
    
    # 移除標題和介紹文字，只保留會議內容部分
    # 使用更精確的正則表達式來匹配介紹文字
    intro_pattern = r'<h1>Google Cloud Next 2025</h1>.*?<p>2025年 4 月 9 ─ 4 月 11 日</p>.*?<p>Next 是我們的全球性展覽.*?</p>.*?<p>解決方案、突破性的構想（10 倍速的創意）*?和改變遊戲規則的技術。</p>'
    html_content = re.sub(intro_pattern, '', html_content, flags=re.DOTALL)
    
    # 預處理：將連續的 h3 標題分開處理
    html_content = re.sub(
        r'(</h3>)(\s*<h3>)',
        r'\1</div><div class="key-content">\2',
        html_content
    )
    
    # 創建類別到超連結的映射
    category_links = {
        "Google Cloud Next 2025": "https://cloud.withgoogle.com/next/25",
        "Data_Analytics": "./topic/Data_Analytics.html",
        "Applied_AI": "./topic/Applied_AI.html",
        "AI": "./topic/AI.html",
        "Databases": "./topic/Databases.html",
        "Security": "./topic/Security.html",
        "Migration": "./topic/Migration.html",
        "Vertex_AI": "./topic/Vertex_AI.html",
        "Gemini": "./topic/Gemini.html",
        "Workspace": "./topic/Workspace.html",
        "App_Dev": "./topic/App_Dev.html",
        "Compute": "./topic/Compute.html",
        "Serverless": "./topic/Serverless.html",

    }
    # 依照 category_links 自動產生分類連結 HTML
    category_links_html = ""
    for cat, link in category_links.items():
        category_links_html += f'<a href="{link}" class="category-link">{cat}</a>\n'
    
    # 處理 h1 標題（類別標題）- 添加超連結
    def add_category_link(match):
        category = match.group(1)
        
        link = category_links.get(category, f"./topic/{category}.html")
        link = link.replace(" ", "_")
        return f'<div class="category-section"><h1><a href="{link}" class="category-title-link">{category}</a></h1>'
    
    html_content = re.sub(
        r'<h1>(.*?)</h1>',
        add_category_link,
        html_content
    )
    
    # 處理 h2 標題（會議標題）- 添加超連結
    def add_meeting_link(match):
        meeting_title = match.group(1)
        # 創建會議標題的超連結，使用會議名稱作為文件名
        # safe_filename = re.sub(r'[^\w\s-]', '', meeting_title)
        meeting_title_link = re.sub(r'[\\/:*?"<>|]', '', meeting_title)
        meeting_title_link = meeting_title_link.strip()
        link = f"./topic/session/{meeting_title_link}_summary.html"
        return f'<div class="meeting-item"><h2><a href="{link}" class="meeting-title-link">{meeting_title}</a></h2>'
    
    html_content = re.sub(
        r'<h2>(.*?)</h2>',
        add_meeting_link,
        html_content
    )
    
    # 處理 h3 標題（會議內容）- 第一個 h3 是描述
    html_content = re.sub(
        r'<h3>(.*?)</h3>',
        r'<h3>\1</h3><div class="key-content">',
        html_content
    )
    
    # 處理列表項目，確保它們在正確的容器內
    html_content = re.sub(
        r'(<ul>.*?</ul>)',
        r'\1</div><div class="key-content">',
        html_content,
        flags=re.DOTALL
    )
    
    # 移除多餘的空 key-content div
    html_content = re.sub(
        r'<div class="key-content"></div>',
        r'',
        html_content
    )
    
    # 清理：移除連續的 div 開始和結束標籤
    html_content = re.sub(
        r'</div>\s*<div class="key-content">',
        r'',
        html_content
    )
    
    # 為每個會議項目添加結束標籤
    # 先找出所有會議項目
    meeting_items = re.findall(r'<div class="meeting-item">.*?(?=<div class="meeting-item">|<div class="category-section">|$)', html_content, re.DOTALL)
    
    # 為每個會議項目添加適當的結束標籤
    for item in meeting_items:
        # 計算 key-content div 的數量
        key_content_count = item.count('<div class="key-content">')
        # 計算已有的結束標籤數量
        end_div_count = item.count('</div>')
        # 需要添加的結束標籤數量
        needed_end_divs = key_content_count + 1 - end_div_count  # +1 是為了 meeting-item div
        
        if needed_end_divs > 0:
            # 創建替換字符串，添加缺少的結束標籤
            replacement = item
            for _ in range(needed_end_divs):
                replacement += '</div>'
            
            # 替換原始字符串
            html_content = html_content.replace(item, replacement)
    
    # 為每個類別添加結束標籤
    category_sections = re.findall(r'<div class="category-section">.*?(?=<div class="category-section">|$)', html_content, re.DOTALL)
    for section in category_sections:
        # 計算開始和結束標籤的數量
        start_tags = section.count('<div')
        end_tags = section.count('</div>')
        
        # 如果結束標籤不足，添加缺少的標籤
        if start_tags > end_tags:
            needed_tags = start_tags - end_tags
            replacement = section
            for _ in range(needed_tags):
                replacement += '</div>'
            
            html_content = html_content.replace(section, replacement)
    
    # 確保所有標籤都正確關閉
    if not html_content.endswith('</div>'):
        html_content += '</div>'
    
    # 當前日期
    current_date = datetime.now().strftime("%Y年%m月%d日")
    
    email_html = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{
                font-family: 'Roboto', 'Microsoft JhengHei', sans-serif;
                background-color: #f0f2f5;
                color: #333;
                margin: 0;
                padding: 0;
                line-height: 1.6;
            }}
            header {{
                text-align: center;
                padding: 40px 20px;
                background: linear-gradient(135deg, #4b6cb7, #182848);
                color: #fff;
                position: relative;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
                border-radius: 0;
            }}
            header h1 {{
                font-size: 2.4rem;
                margin: 0 0 15px 0;
                letter-spacing: 0.5px;
                text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
            }}
            header p {{
                font-size: 1.2rem;
                margin: 0;
                opacity: 0.9;
            }}
            header img {{
                max-width: 35%;
                height: auto;
                margin-bottom: 20px;
                filter: drop-shadow(0px 4px 6px rgba(0, 0, 0, 0.2));
            }}
            header .date-info {{
                font-size: 1.1rem;
                margin-top: 10px;
                background-color: rgba(255, 255, 255, 0.15);
                display: inline-block;
                padding: 5px 15px;
                border-radius: 20px;
            }}
            main {{
                max-width: 1000px;
                margin: 40px auto;
                padding: 0 20px;
            }}
            .content-container {{
                background-color: #fff;
                border-radius: 12px;
                box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
                padding: 40px;
                margin-bottom: 40px;
            }}
            .section-block {{
                background-color: #fff;
                padding: 25px;
                border-radius: 10px;
                margin-bottom: 30px;
                border-left: 5px solid #4b6cb7;
                box-shadow: 0 3px 12px rgba(0, 0, 0, 0.07);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}
            .section-block:hover {{
                transform: translateY(-5px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
            }}
            h1 {{
                color: #2c3e50;
                font-size: 2.1rem;
                margin-top: 0;
                margin-bottom: 30px;
                padding-bottom: 12px;
                border-bottom: 2px solid #4b6cb7;
            }}
            h2 {{
                color: #2980b9;
                font-size: 1.6rem;
                margin-top: 30px;
                margin-bottom: 18px;
                padding-bottom: 10px;
                border-bottom: 1px solid #e0e0e0;
            }}
            h3 {{
                color: #27ae60;
                font-size: 1.3rem;
                margin-top: 25px;
                margin-bottom: 15px;
                font-weight: 600;
            }}
            p {{
                margin-bottom: 18px;
                line-height: 1.8;
                font-size: 1.05rem;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 12px;
                position: relative;
                list-style-type: none;
                padding-left: 28px;
                line-height: 1.7;
            }}
            li::before {{
                content: "•";
                position: absolute;
                left: 0;
                color: #4b6cb7;
                font-size: 1.4rem;
                font-weight: bold;
            }}
            footer {{
                text-align: center;
                padding: 35px 20px;
                background-color: #f8f9fa;
                color: #666;
                border-top: 1px solid #e0e0e0;
            }}
            footer img {{
                max-width: 35%;
                height: auto;
                margin-bottom: 20px;
                opacity: 0.9;
            }}
            footer p {{
                margin: 8px 0;
                font-size: 1rem;
            }}
            .category-section {{
                margin-bottom: 60px;
                padding: 30px 30px 10px 30px;
                background-color: #f9f9f9;
                border-radius: 16px;
                border-left: 7px solid #8e44ad;
                box-shadow: 0 5px 18px rgba(0, 0, 0, 0.08);
                transition: transform 0.3s ease;
                position: relative;
            }}
            .category-section:not(:last-child)::after {{
                content: "";
                display: block;
                height: 2px;
                background: linear-gradient(90deg, #8e44ad 0%, #fff 100%);
                margin: 40px 0 0 0;
                border-radius: 1px;
            }}
            .meeting-item {{
                margin-bottom: 35px;
                padding: 25px 25px 15px 25px;
                background-color: #f7fbff;
                border-radius: 12px;
                border-left: 5px solid #3498db;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
            }}
            .meeting-item:hover {{
                transform: translateY(-5px) scale(1.02);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.13);
            }}
            .key-content {{
                background-color: #f5fffc;
                padding: 18px 20px;
                border-radius: 8px;
                border-left: 4px solid #1abc9c;
                margin-top: 10px;
                margin-bottom: 10px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
                font-size: 1.08rem;
            }}
            .category-title-link:hover {{
                color: #6c3483;
                text-decoration: underline wavy #8e44ad;
                background: #f3e6fa;
                border-radius: 6px;
                padding: 2px 8px;
            }}
            .meeting-title-link:hover {{
                color: #21618c;
                text-decoration: underline wavy #3498db;
                background: #eaf6fb;
                border-radius: 6px;
                padding: 2px 8px;
            }}
            /* 確保列表項目在 key-content 中正確顯示 */
            .key-content ul {{
                padding-left: 15px;
            }}
            .key-content li {{
                margin-bottom: 10px;
            }}
            .key-content li::before {{
                color: #1abc9c;
            }}
            .intro-text {{
                font-size: 1.15rem;
                line-height: 1.9;
                margin-bottom: 35px;
                padding: 25px;
                background-color: #f0f7ff;
                border-radius: 10px;
                border-left: 5px solid #3498db;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
            }}
            .intro-text p {{
                margin-bottom: 15px;
            }}
            .intro-text p:last-child {{
                margin-bottom: 0;
            }}
            .category-links {{
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
                margin: 30px 0;
                justify-content: center;
            }}
            .category-link {{
                display: inline-block;
                padding: 10px 18px;
                background-color: #3498db;
                color: white;
                border-radius: 25px;
                text-decoration: none;
                font-weight: bold;
                transition: all 0.3s ease;
                box-shadow: 0 3px 8px rgba(52, 152, 219, 0.3);
            }}
            .category-link:hover {{
                background-color: #2980b9;
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(52, 152, 219, 0.4);
            }}
            header h1 {{
                color: #FFFFFF;
            }}
            /* 添加響應式設計 */
            @media (max-width: 768px) {{
                header h1 {{
                    font-size: 2rem;
                }}
                .content-container {{
                    padding: 25px;
                }}
                .category-section, .meeting-item {{
                    padding: 20px;
                }}
                .category-links {{
                    gap: 8px;
                }}
                .category-link {{
                    padding: 8px 15px;
                    font-size: 0.9rem;
                }}
            }}
            /* 添加標題超連結樣式 */
            .category-title-link {{
                color: #8e44ad;
                text-decoration: none;
                transition: all 0.3s ease;
            }}
            .category-title-link:hover {{
                color: #9b59b6;
                text-decoration: underline;
            }}
            .meeting-title-link {{
                color: #3498db;
                text-decoration: none;
                transition: all 0.3s ease;
            }}
            .meeting-title-link:hover {{
                color: #2980b9;
                text-decoration: underline;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="https://i.imgur.com/0LXUWvj.png" alt="GTC 2025 圖示">
            <h1>{title}</h1>
        </header>
        <main>
            <div class="content-container">
                <div class="category-links">
                    {category_links_html}
                </div>
                {html_content}
            </div>
        </main>
        <footer>
            <img src="https://i.imgur.com/0LXUWvj.png" alt="GTC 2025 圖示">
            <p>此摘要由 AI 輔助生成</p>
            <p>如有任何問題或需要更多詳細資訊，請聯繫 ITR 小組</p>
        </footer>
    </body>
    </html>
    """
    return email_html

def ensure_directories(output_dir):
    """確保輸出目錄存在"""
    os.makedirs(f"{output_dir}/topic/md", exist_ok=True)
    os.makedirs(f"{output_dir}/topic", exist_ok=True)

def main(file_path, output_dir="../report"):
    """
    主函數 - 處理Excel文件並生成首頁報告
    
    Args:
        file_path (str): Excel文件路徑
        output_dir (str): 輸出目錄路徑
    """
    # 讀取 Excel，取得所有不重複的 Type 欄位值
    df = pd.read_csv(file_path)
    categories = df["Topic"].dropna().unique().tolist()
    print(f"所有不重複的 Type 欄位值: {categories}")
    ensure_directories(output_dir)
    
    # meetings = load_meetings(file_path)
    # selected_meetings = select_random_meetings(meetings, categories)
    selected_meetings = select_random_meetings(df, categories)
    print(f"已選取的會議數量: {len(selected_meetings)}")
    markdown_output = generate_markdown(selected_meetings)
    html_output = markdown_to_email_html(markdown_output)
    
    # 保存 Markdown 文件
    md_path = f"{output_dir}/topic/md/homepage.md"
    with open(md_path, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_output)
    
    # 保存 HTML 文件
    html_path = f"{output_dir}/homepage.html"
    with open(html_path, "w", encoding="utf-8") as html_file:
        html_file.write(html_output)
    
    print(f"首頁 Markdown 文件已保存至: {md_path}")
    print(f"首頁 HTML 文件已保存至: {html_path}")

if __name__ == "__main__":
    import argparse
    
    # 創建命令行參數解析器
    parser = argparse.ArgumentParser(description="生成首頁報告")
    parser.add_argument("-i", "--input", required=True, help="輸入的 Excel 文件路徑")
    parser.add_argument("-o", "--output", default="./report", help="輸出目錄路徑 (預設: ./report)")
    
    # 解析命令行參數
    args = parser.parse_args()
    
    # 執行主函數
    main(args.input, args.output)
