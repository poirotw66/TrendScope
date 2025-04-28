import pandas as pd
import os
import random
import markdown

def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df

def select_meetings_by_topic(df, sample_size=15):
    grouped = df.groupby("Topic")
    selected_data = {}
    
    for topic, group in grouped:
        sampled = group.sample(n=min(sample_size, len(group)), random_state=42)  # 確保可重現性
        selected_data[topic] = sampled[['Meeting', 'Key']].values.tolist()
    
    return selected_data

def generate_markdown(topic, meetings):
    md_content = f"# {topic}\n\n"
    
    for meeting, key in meetings:
        # 使用純 Markdown 格式，避免混合 HTML 標籤
        md_content += f"## {meeting}\n\n"
        md_content += "### Key Takeaways\n\n"
        md_content += f"{key}\n\n"
        md_content += "---\n\n"  # 使用 Markdown 分隔線區分不同會議
    
    return md_content

def markdown_to_email_html(md_content):
    # 轉換 Markdown 為 HTML
    html_content = markdown.markdown(md_content)
    
    # 處理 HTML 內容，為每個會議添加適當的樣式
    # 找到所有 <h2> 標籤（會議標題）並為其添加樣式
    import re
    
    # 為會議標題和內容添加樣式，同時添加超連結
    html_content = re.sub(
        r'<h2>(.*?)</h2>',
        lambda m: f'<div class="meeting-item"><h2><a href="./session/{m.group(1)}_summary.html" style="text-decoration: none; color: inherit;">{m.group(1)}</a></h2>',
        html_content
    )
    
    # 為Key Takeaways添加樣式
    html_content = re.sub(
        r'<h3>Key Takeaways</h3>',
        r'<h3>Key Takeaways</h3><div class="key-content">',
        html_content
    )
    
    # 為分隔線添加結束標籤
    html_content = re.sub(
        r'<hr />',
        r'</div></div><hr />',
        html_content
    )
    
    # 移除最後一個分隔線
    html_content = html_content.replace('<hr />', '')
    
    # 確保所有會議項目都有正確的結束標籤
    if not html_content.endswith('</div>'):
        html_content += '</div></div>'
    
    # 當前日期
    from datetime import datetime
    current_date = datetime.now().strftime("%Y年%m月%d日")
    
    # 提取標題
    title_match = re.search(r'<h1>(.*?)</h1>', html_content)
    title = "研討會會議清單"
    if title_match:
        title = title_match.group(1)
    
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
                background-color: #f8f9fa;
                color: #333;
                margin: 0;
                padding: 0;
                line-height: 1.6;
            }}
            header {{
                text-align: center;
                padding: 30px 20px;
                background: linear-gradient(135deg, #4b6cb7, #182848);
                color: #fff;
                position: relative;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                border-radius: 10px 10px 0 0;
            }}
            header h1 {{
                font-size: 2.2rem;
                margin: 0 0 10px 0;
                letter-spacing: 0.5px;
            }}
            header p {{
                font-size: 1.1rem;
                margin: 0;
                opacity: 0.9;
            }}
            header img {{
                max-width: 35%;
                height: auto;
                margin-bottom: 15px;
            }}
            main {{
                max-width: 900px;
                margin: 30px auto;
                padding: 0 20px;
            }}
            .content-container {{
                background-color: #fff;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
                padding: 30px;
                margin-bottom: 30px;
            }}
            .section-block {{
                background-color: #fff;
                padding: 25px;
                border-radius: 8px;
                margin-bottom: 25px;
                border-left: 5px solid #4b6cb7;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            .section-block:hover {{
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: 	#FFFFFF;
                font-size: 2rem;
                margin-top: 0;
                margin-bottom: 30px;
                padding-bottom: 10px;
                border-bottom: 2px solid #4b6cb7;
            }}
            h2 {{
                color: #3498db;
                font-size: 1.5rem;
                margin-top: 25px;
                margin-bottom: 15px;
                padding-bottom: 8px;
                border-bottom: 1px solid #e0e0e0;
            }}
            h3 {{
                color: #2ecc71;
                font-size: 1.2rem;
                margin-top: 20px;
                margin-bottom: 10px;
            }}
            p {{
                margin-bottom: 15px;
                line-height: 1.7;
            }}
            ul {{
                padding-left: 20px;
            }}
            li {{
                margin-bottom: 10px;
                position: relative;
                list-style-type: none;
                padding-left: 25px;
            }}
            li::before {{
                content: "•";
                position: absolute;
                left: 0;
                color: #4b6cb7;
                font-size: 1.2rem;
                font-weight: bold;
            }}
            footer {{
                text-align: center;
                padding: 25px 20px;
                background-color: #f0f2f5;
                color: #666;
                border-radius: 0 0 10px 10px;
                border-top: 1px solid #e0e0e0;
            }}
            footer img {{
                max-width: 35%;
                height: auto;
                margin-bottom: 15px;
            }}
            footer p {{
                margin: 5px 0;
                font-size: 0.95rem;
            }}
            .meeting-item {{
                margin-bottom: 40px;
                padding: 20px;
                background-color: #f7fbff;
                border-radius: 8px;
                border-left: 5px solid #3498db;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }}
            .meeting-item:hover {{
                transform: translateY(-3px);
                box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
            }}
            .key-content {{
                background-color: #f5fffc;
                padding: 15px;
                border-radius: 5px;
                border-left: 3px solid #1abc9c;
                margin-top: 10px;
                margin-bottom: 15px;
            }}
            /* 確保列表項目在 key-content 中正確顯示 */
            .key-content ul {{
                padding-left: 15px;
            }}
            .key-content li {{
                margin-bottom: 8px;
            }}
            .key-content li::before {{
                color: #1abc9c;
            }}
        </style>
    </head>
    <body>
        <header>
            <img src="https://i.imgur.com/0LXUWvj.png" alt="會議摘要圖示">
            <h1>{title}</h1>
            <p>類別清單</p>
        </header>
        <main>
            <div class="content-container">
                {html_content}
            </div>
        </main>
        <footer>
            <img src="https://i.imgur.com/0LXUWvj.png" alt="會議摘要圖示">
            <p>此摘要由 AI 輔助生成</p>
            <p>如有任何問題或需要更多詳細資訊，請聯繫 ITR 小組</p>
        </footer>
    </body>
    </html>
    """
    return email_html

def ensure_directories(output_dir):
    """確保輸出目錄存在"""
    os.makedirs(f"{output_dir}/md", exist_ok=True)
    os.makedirs(f"{output_dir}/session", exist_ok=True)

def main(file_path, output_dir="../report"):
    """
    主函數 - 處理Excel文件並生成報告
    
    Args:
        file_path (str): Excel文件路徑
        output_dir (str): 輸出目錄路徑
    """
    df = read_excel(file_path)
    selected_data = select_meetings_by_topic(df)
    
    ensure_directories(output_dir)
    
    for topic, meetings in selected_data.items():
        md_content = generate_markdown(topic, meetings)
        html_content = markdown_to_email_html(md_content)
        
        # 處理特殊字符，避免文件名問題
        safe_topic = topic
        if topic == "Business / Executive":
            safe_topic = "Business_Executive"
        elif "/" in topic:
            safe_topic = topic.replace("/", "_")
        
        md_filename = f"{output_dir}/md/{safe_topic}.md"
        html_filename = f"{output_dir}/{safe_topic}.html"
        
        with open(md_filename, "w", encoding="utf-8") as md_file:
            md_file.write(md_content)
        
        with open(html_filename, "w", encoding="utf-8") as html_file:
            html_file.write(html_content)
    
    print(f"Markdown 和 HTML 文件已成功生成於 {output_dir} 目錄。")

if __name__ == "__main__":
    import argparse
    
    # 創建命令行參數解析器
    parser = argparse.ArgumentParser(description="生成會議報告的 Markdown 和 HTML 文件")
    parser.add_argument("-i", "--input", required=True, help="輸入的 Excel 文件路徑")
    parser.add_argument("-o", "--output", default="./report/topic", help="輸出目錄路徑 (預設: ./report)")
    
    # 解析命令行參數
    args = parser.parse_args()
    
    # 執行主函數
    main(args.input, args.output)