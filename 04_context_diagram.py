import pandas as pd
from google import genai
from config.config import GEMINI_API_KEY

# 讀取 CSV 檔案
csv_path = "gtc_session.csv"
df = pd.read_csv(csv_path)

# 取得所有 Key 欄位非空的摘要
session_keys = df["Key"].dropna().tolist()

# 將所有 session 摘要合併為一個脈絡描述
context_text = "\n\n".join([f"Session {i+1}: {key}" for i, key in enumerate(session_keys)])

# Gemini prompt
prompt = f"""請根據以下研討會內容，輸出一份**技術趨勢脈絡圖**，以**Markdown 階層式結構（# / ## / ###）**撰寫，並以**繁體中文**呈現。

這份脈絡圖將用於製作**視覺化資訊圖表（如技術地圖、簡報架構圖、詞雲、趨勢對應圖）**，請確保資訊邏輯清楚、層級分明，僅呈現研討會中提及的**技術趨勢與應用脈絡**，不需額外延伸說明或資料來源。

---

## 📌 Markdown 輸出格式範例：

# 技術趨勢總覽

## 趨勢一：主技術趨勢名稱（如：人工智慧 AI、Web3、邊緣運算）

### 子趨勢：具體技術名稱（如：大型語言模型、AI Agents、自主資料市場）
- 總覽與建議：
  - 濃縮的趨勢描述與發展建議
- 應用場景：
  - 具體產業或情境（如金融風控、智慧製造、醫療診斷）
- 潛在影響：
  - 對社會或產業的轉型影響（如自動化、效率提升）
- 關鍵挑戰：
  - 技術落地障礙（如成本、資安、合規）
- 相關工具／平台：
  - 提及的具體平台或工具（如 Hugging Face、LangChain、MetaMask）

## 趨勢二：...
（依此類推）

---

## 📊 請另外輸出下列圖像化資料：

1. **技術趨勢詞雲圖**
   - 根據研討會中頻繁出現的重要關鍵字（如 AI、LLM、自動化、隱私）生成詞雲
   - 詞頻大小代表熱度

2. **技術趨勢分類圖（樹狀圖或旭日圖）**
   - 主趨勢 → 子趨勢 → 應用領域
   - 可視化顯示趨勢間的層級與分佈

3. **應用領域對應表**
   - 列出每個技術趨勢對應到的產業（例如 AI → 醫療 / 金融 / 教育）

---

## ✨ 撰寫與輸出原則：

- 僅整理研討會實際提及的內容（不加入推測或外部分析）
- 條列式清晰排版，方便轉製為視覺資訊圖
- 所有內容請以**繁體中文**輸出


==== 研討會內容 ====
{context_text}
"""
# gemini-2.5-flash-preview-04-17
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