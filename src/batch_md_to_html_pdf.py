import os
import markdown
import re

def wrap_sections_to_columns(html):
    # 取得所有 <h2> 章節與內容
    parts = re.split(r'(<h2>.*?</h2>)', html)
    sections = []
    current = ""
    for part in parts:
        if part.startswith("<h2>"):
            if current:
                sections.append(current)
            current = part
        else:
            current += part
    if current:
        sections.append(current)
        # 只取前3個章節，剩下的合併為第4欄
    columns = ["", "", "", ""]
    for i, section in enumerate(sections):
        if i < 3:
            columns[i] = f'<div class="section-card">{section}</div>'
        else:
            columns[3] += f'<div class="section-card">{section}</div>'
        # 組成四欄
    html_grid = ""
    for col in columns:
        html_grid += f'<div class="column">{col}</div>'
    return html_grid

def wrap_sections_to_meeting_items(html):
    # 取得所有 <h2> 章節與內容
    parts = re.split(r'(<h2>.*?</h2>)', html)
    sections = []
    current = ""
    for part in parts:
        if part.startswith("<h2>"):
            if current:
                sections.append(current)
            current = part
        else:
            current += part
    if current:
        sections.append(current)
    # 每個章節包成 meeting-item
    html_meetings = ""
    for section in sections:
        html_meetings += f'<div class="meeting-item">{section}</div>'
    return html_meetings

def markdown_to_email_html(md_content, index=0):
    html_content = markdown.markdown(md_content)
    title_match = re.search(r'<h1>(.*?)</h1>', html_content)
    title = "研討會會議摘要"
    if title_match:
        title = title_match.group(1)
    lines = md_content.strip().splitlines()
    content_after_4th = "\n".join(lines[index:]) if len(lines) > index else ""
    if index == 3:
        content_after_4th = "## " + content_after_4th
    html_content = markdown.markdown(content_after_4th)
    # 將每個 h2 章節包成 meeting-item
    html_content = wrap_sections_to_meeting_items(html_content)
    html_content = re.sub(
        r'<h3>Key Takeaways</h3>',
        r'<h3>Key Takeaways</h3><div class="key-content">',
        html_content
    )
    html_content = re.sub(
        r'<hr />',
        r'</div></div><hr />',
        html_content
    )
    html_content = html_content.replace('<hr />', '')
    if not html_content.endswith('</div>'):
        html_content += '</div></div>'
    lines = md_content.strip().splitlines()
    category = lines[1].strip() if len(lines) > 1 else "演講類別"
    url_match = re.search(r'\[.*?\]\((https?://[^\)]+)\)', md_content)
    url = url_match.group(1) if url_match else ""
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
            .video-link {{
                    display: inline-block;
                    margin: 10px 0;
                    padding: 8px 15px;
                    background-color: rgba(255, 255, 255, 0.2);
                    color: #fff;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: 500;
                    transition: all 0.3s ease;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }}
                .video-link:hover {{
                    background-color: rgba(255, 255, 255, 0.3);
                    transform: translateY(-2px);
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }}
                .video-link i {{
                    margin-right: 5px;
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
                background: #fff;
                border-radius: 16px;
                box-shadow: 0 4px 24px rgba(75,108,183,0.10), 0 1.5px 4px rgba(75,108,183,0.07);
                padding: 40px 32px;
                margin-bottom: 32px;
                border: 1.5px solid #e3e8f0;
                transition: box-shadow 0.2s;
                max-width: 900px;
                margin-left: auto;
                margin-right: auto;
            }}
            .content-container:hover {{
                box-shadow: 0 8px 32px rgba(75,108,183,0.15), 0 2px 8px rgba(75,108,183,0.12);
            }}
            h1 {{
                color: #2176ff;
                font-size: 2.3rem;
                margin-top: 0;
                margin-bottom: 30px;
                padding-bottom: 10px;
                border-bottom: 2px solid #4b6cb7;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            h2 {{
                color: #1b5cb7;
                font-size: 1.7rem;
                margin-top: 32px;
                margin-bottom: 18px;
                padding-bottom: 8px;
                border-bottom: 1.5px solid #e0e0e0;
                font-weight: 600;
            }}
            h3 {{
                color: #2ecc71;
                font-size: 1.25rem;
                margin-top: 24px;
                margin-bottom: 12px;
                font-weight: 600;
            }}
            strong, b {{
                color: #2176ff;
                font-weight: 700;
            }}
            ul, ol {{
                padding-left: 28px;
                margin-bottom: 18px;
            }}
            li {{
                margin-bottom: 10px;
                line-height: 1.7;
            }}
            p {{
                margin-bottom: 18px;
                line-height: 1.8;
                font-size: 1.08rem;
            }}
            @media (max-width: 600px) {{
                .content-container {{
                    padding: 18px 6px;
                }}
                h1 {{
                    font-size: 1.3rem;
                }}
                h2 {{
                    font-size: 1.1rem;
                }}
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
            {f'<img src="https://i.imgur.com/0LXUWvj.png" alt="{title} 圖示">' if title else ''}
            <h1>{title}</h1>
            <p>{category}</p>
            {f'<a href="{url}" class="video-link" target="_blank"><i>▶</i> 會議影片超連結</a>' if url else ''}
        </header>
        <main>
            <div class="content-container">
                <div class="main-sections">
                    {html_content}
                </div>
            </div>
        </main>
        <footer>
            {f'<img src="https://i.imgur.com/0LXUWvj.png" alt="{title} 圖示">' if title else ''}
            <p>此摘要由 AI 輔助生成</p>
            <p>如有任何問題或需要更多詳細資訊，請聯繫 ITR 小組</p>
        </footer>
    </body>
    </html>
    """
    return email_html

def batch_md_to_html(md_dir, html_dir, index3=False):
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    for filename in os.listdir(md_dir):
        if filename.endswith('.md'):
            md_path = os.path.join(md_dir, filename)
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            html_content = markdown_to_email_html(md_content, index3)
            html_filename = os.path.splitext(filename)[0] + '.html'
            html_path = os.path.join(html_dir, html_filename)
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"已轉換: {md_path} -> {html_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="批次將 Markdown 轉換為 HTML")
    parser.add_argument("-i", "--input", default="../output/md", help="Markdown 檔案資料夾")
    parser.add_argument("-o", "--output", default="../output/html", help="輸出 HTML 資料夾")
    args = parser.parse_args()
    batch_md_to_html(args.input, args.output)