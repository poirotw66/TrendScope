import pandas as pd
import os
import re
from dotenv import load_dotenv
from src.batch_md_to_html import batch_md_to_html

# 載入 .env 文件中的環境變數
load_dotenv()

# 從環境變數讀取設定，如果未設定則使用預設值
output_md_dir = os.getenv("OUTPUT_MD_DIR", "./GTC_summary/topic_md")
output_html_dir = os.getenv("OUTPUT_HTML_DIR", "./GTC_summary/topic")
session_html_dir = os.getenv("SESSION_HTML_DIR", "./GTC_summary/topic/session")
input_csv_path = os.getenv("INPUT_CSV_PATH", "./data/sheet/GTC25.csv")
top_n_meetings = int(os.getenv("TOP_N_MEETINGS", 5)) # 從環境變數讀取 top_n，預設為 3
batch_md_to_html_index = int(os.getenv("BATCH_MD_TO_HTML_INDEX", 1)) # 從環境變數讀取 index，預設為 1

# 確保輸出資料夾存在
os.makedirs(output_md_dir, exist_ok=True)
os.makedirs(output_html_dir, exist_ok=True) # 確保 HTML 輸出目錄也存在
os.makedirs(session_html_dir, exist_ok=True) # 確保 session HTML 目錄也存在

def normalize_filename(title):
    # 移除不合法字元，只保留中英文、數字、空格、底線、點
    title = re.sub(r'[\\/:*?"_<>|]', '', title)
    title = title.strip()
    return title

def find_same_name_html(meeting, session_dir):
    # 遍歷所有 HTML 檔案
    try:
        for filename in os.listdir(session_dir):
            if filename.endswith(".html"):
                # 移除檔案的副檔名
                file_meeting = os.path.splitext(filename)[0]
                normalized_file_meeting = normalize_filename(file_meeting[4:]) # 備用邏輯
                print(f"normalized_file_meeting: {normalized_file_meeting}")

                if normalize_filename(meeting) == normalized_file_meeting:
                    # 返回相對於 output_html_dir 的路徑
                    relative_session_dir = os.path.relpath(session_dir, output_html_dir)
                    return os.path.join(relative_session_dir, filename).replace("\\", "/") # 確保路徑分隔符為 /
    except FileNotFoundError:
        print(f"錯誤：找不到目錄 {session_dir}")
        return None
    return None # 找不到則返回 None

def export_topic_markdown(df, md_dir, session_dir, top_n=3):
    topics = df['Topic'].dropna().unique()
    print(f"所有 Topic 下的前 {top_n} 項 Meeting：")
    for topic in topics:
        # 選出該 Topic 下的 Meeting、URL、Key 欄位，去除空值，取前 top_n 項
        topic_df = df[df['Topic'] == topic][['Meeting', 'URL', 'Key']].dropna().head(top_n)
        # 組成 markdown 內容
        md_content = f"# {topic}\n"
        for _, row in topic_df.iterrows():
            meeting = row['Meeting']
            # 將 session_html_dir 傳遞給 find_same_name_html
            html_path = find_same_name_html(meeting, session_dir)
            url = row['URL']
            keytakeway = row['Key']
            md_content += f"## {meeting}\n"
            if html_path:
                # 使用相對路徑連結
                md_content += f"### <a href=\"{html_path}\" style=\"text-decoration: none; color: inherit;\">詳細摘要頁面</a>\n"
            md_content += f"- 連結: [{url}]({url})\n"
            md_content += f"- 摘要: {keytakeway}\n"
        # 儲存成 markdown 檔案
        safe_topic = "".join([c if c.isalnum() or c in "_-" else "_" for c in topic.strip()])
        md_path = os.path.join(md_dir, f"{safe_topic}.md")
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"已儲存 {md_path}")

# 讀取 CSV 檔案
try:
    df = pd.read_csv(input_csv_path)
    # 將 session_html_dir 傳遞給 export_topic_markdown
    export_topic_markdown(df, output_md_dir, session_html_dir, top_n=top_n_meetings)
    batch_md_to_html(output_md_dir, output_html_dir, batch_md_to_html_index)
except FileNotFoundError:
    print(f"錯誤：找不到 CSV 檔案 {input_csv_path}")
except Exception as e:
    print(f"處理過程中發生錯誤：{e}")

# 移除舊的註解
# google next 2
# gtc25 1
