import pandas as pd
from google import genai
from config.config import GEMINI_API_KEY

# 讀取 CSV 檔案
csv_path = "google_next_sessions.csv"
df = pd.read_csv(csv_path)

# 取得所有 Key 欄位非空的摘要
session_keys = df["Key"].dropna().tolist()

# 將所有 session 摘要合併為一個脈絡描述
context_text = "\n\n".join([f"Session {i+1}: {key}" for i, key in enumerate(session_keys)])

# Gemini prompt
prompt = f"""請根據以下研討會內容，輸出一份**技術趨勢脈絡圖**，格式為 Markdown 階層式結構。目的是整理研討會中提及的重要技術趨勢、其子分類與應用脈絡。請用清晰的層級（# / ## / ###）呈現。

內容應包含：
- 主題技術趨勢（如 AI、邊緣運算、Web3 等）
- 每項趨勢的子技術 / 子領域
- 每項趨勢的應用場景（如醫療、金融、教育等）
- 潛在影響或關鍵挑戰
- 若有提及，補充代表性技術、工具、平台

請用下列格式：

# 技術趨勢總覽
## 趨勢一：主技術趨勢名稱（如 AI、Web3、量子運算）
### 子趨勢：具體技術名稱（如 LLM、聯邦學習、NFT 等）
- 子趨勢總覽與建議：
- 應用場景：
  - 具體產業或情境（如醫療診斷、智慧製造）
- 潛在影響：
  - 對產業、社會或商業模式的影響（如自動化、就業轉型）
- 關鍵挑戰：
  - 技術或實務層面待解決的問題（如資料隱私、法規限制）
- 相關工具／平台：
  - 有代表性的開源技術、商業平台或框架

...


所有內容請以繁體中文撰寫。

==== session 摘要 ====
{context_text}
"""

client = genai.Client(api_key=GEMINI_API_KEY)
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-04-17",
    contents=[prompt]
)

# 將結果寫入 markdown 檔案
output_path = "context_diagram.md"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"脈絡圖已產生並儲存於 {output_path}")