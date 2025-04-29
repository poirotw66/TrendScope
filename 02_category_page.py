import pandas as pd
import os
import re
from src.batch_md_to_html import batch_md_to_html

output_md_dir = "./output/topic_md"
output_html_dir = "./report/topic"
session_html_dir = "./report/topic/session"
# 確保輸出資料夾存在
os.makedirs(output_md_dir, exist_ok=True)

def normalize_filename(title):
    # 移除不合法字元，只保留中英文、數字、空格、底線、點
    title = re.sub(r'[\\/:*?"<>|]', '', title)
    title = title.strip()
    return title

def find_same_name_html(meeting, session_html_dir):
    # 遍歷所有 HTML 檔案
    for filename in os.listdir(session_html_dir):
        if filename.endswith(".html"):
            # 移除檔案的副檔名
            file_meeting = os.path.splitext(filename)[0]
            # 檢查是否有相同的名稱
            if normalize_filename(meeting) == normalize_filename(file_meeting[:-8]):
                return f"./session/{filename}"
    # 確保輸出資料夾存在

def export_topic_markdown(df, output_md_dir, top_n=3):
    topics = df['Topic'].dropna().unique()
    print(f"所有 Topic 下的前 {top_n} 項 Meeting：")
    for topic in topics:
        # 選出該 Topic 下的 Meeting、URL、Key 欄位，去除空值，取前 top_n 項
        topic_df = df[df['Topic'] == topic][['Meeting', 'URL', 'Key']].dropna().head(top_n)
        # 組成 markdown 內容
        md_content = f"# {topic}\n"
        for _, row in topic_df.iterrows():
            meeting = row['Meeting']
            html_path = find_same_name_html(meeting, session_html_dir)
            url = row['URL']
            keytakeway = row['Key']
            md_content += f"## {meeting}\n"
            if html_path:
                md_content += f"### <a href=\"{html_path}\" style=\"text-decoration: none; color: inherit;\">詳細摘要頁面</a>\n"
            md_content += f"- 連結: [{url}]({url})\n"
            md_content += f"- 摘要: {keytakeway}\n"
        # 儲存成 markdown 檔案
        safe_topic = "".join([c if c.isalnum() or c in "_-" else "_" for c in topic.strip()])
        md_path = os.path.join(output_md_dir, f"{safe_topic}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"已儲存 {md_path}")

# 讀取 CSV 檔案
df = pd.read_csv("google_next_sessions.csv")
export_topic_markdown(df, output_md_dir, top_n=20)
batch_md_to_html(output_md_dir, output_html_dir, 2)