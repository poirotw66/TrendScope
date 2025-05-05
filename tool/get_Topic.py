import pandas as pd
from config.config import GEMINI_API_KEY
from google import genai
import time

def classify_topic(value):
    client = genai.Client(api_key=GEMINI_API_KEY)
    prompt = f"""
    # 現在有一段摘要，請根據內容**從以下領域列表中，選出最符合的一個領域**。

    ## 領域列表
    - Al
    - APIs
    - App Dev
    - Applied AI
    - Architecture
    - Business Intelligence
    - Chrome
    - Compute
    - Cost Optimization
    - Data Analytics
    - Databases
    - Firebase
    - Gemini
    - Kaggle
    - Migration
    - Multicloud
    - Networking
    - Security
    - Serverless
    - Storage
    - Vertex AI
    - Workspace

    ## 指示
    - 請**只回覆對應的領域名稱**，不要附加解釋。
    - 如果摘要內容涉及多個領域，**選擇最主要或最關鍵的一個領域**。
    - 如果摘要內容完全無法歸類到上述任一領域，請回覆 `Unknown`。

    ## 摘要
    {value}
    """
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-lite",
                contents=[prompt]
            )
            return response.text
        except Exception as e:
            print(f"API錯誤，第{attempt+1}次重試: {e}")
            time.sleep(5)
        time.sleep(2)  # 每次請求間隔2秒
    return "Unknown"

excel_path = "google_next_sessions.xlsx"

# 讀取 Excel 檔案
df = pd.read_excel(excel_path)

# 確保有 Topic 欄位
if 'Topic' not in df.columns:
    df['Topic'] = ""

# 檢查是否有 'Key' 欄位
if 'Key' in df.columns:
    for idx, value in enumerate(df['Key']):
        if pd.notna(value):
            topic = classify_topic(value)
            print(f"第{idx+1}筆 Topic 欄位內容: {topic}")
            df.at[idx, 'Topic'] = topic
    # 儲存回 Excel
    df.to_excel(excel_path, index=False)
    print("已將 Topic 欄位寫回 Excel。")
else:
    print("找不到 'Key' 欄位")