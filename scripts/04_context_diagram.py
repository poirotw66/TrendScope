import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 載入 .env 文件中的環境變數
load_dotenv()


csv_path = os.getenv("INPUT_CSV_PATH", "gtc_session.csv") # 這個變數現在可能不再使用，取決於您是否完全替換了輸入源
output_path = os.getenv("CONTEXT_DIAGRAM_OUTPUT_PATH", "2025_aicon.md")
# model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")
# model_name = "gemini-2.5-flash-preview-05-20"
model_name = "gemini-2.5-pro-preview-05-06"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "yur_api_key")

# 指定存放 txt 檔案的目錄
txt_dir = '/Users/cfh00896102/Github/TrendScope/data/202505_aicon/md'

def get_all_chunk():
    """
    讀取指定目錄下所有 .txt 檔案的內容並合併。

    Returns:
        str: 合併後的檔案內容，以換行符分隔。
    """
    all_content = []
    if not os.path.isdir(txt_dir):
        print(f"錯誤：找不到目錄 '{txt_dir}'")
        return ""

    for filename in os.listdir(txt_dir):
        if filename.endswith(".txt") or filename.endswith(".md"):
            filepath = os.path.join(txt_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_content.append(f"--- 檔案: {filename} ---\n{content}") # 可以在每個檔案內容前加上標示
            except Exception as e:
                print(f"讀取檔案 '{filepath}' 時發生錯誤：{e}")

    return "\n\n".join(all_content)

def get_all_key(csv_path):
   # 讀取 CSV 檔案
    df = pd.read_csv(csv_path)

    # 取得所有 Key 欄位非空的摘要
    session_keys = df["Key"].dropna().tolist()

    # 將所有 session 摘要合併為一個脈絡描述
    context_text = "\n\n".join([f"Session {i + 1}: {key}" for i, key in enumerate(session_keys)])
    return context_text
# --- 主要邏輯 ---
try:
    
    # 呼叫 get_all_chunk 函式來取得所有 txt 檔案的內容
    context_text = get_all_chunk()

    if not context_text:
        print("沒有讀取到任何有效的檔案內容，無法生成脈絡圖。")
        sys.exit(1) # 退出腳本

    # Gemini prompt (保持不變)
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

2. **技術趨勢分類圖**
   - 樹狀圖
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
    # 設定 Gemini API
    genai.configure(api_key=GEMINI_API_KEY)

    # 呼叫 Gemini API
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    # 將結果寫入 markdown 檔案
    with open(output_path, "w", encoding="utf-8") as f:
        # 檢查 response 是否有 text 屬性，並處理可能的錯誤
        if hasattr(response, 'text'):
            f.write(response.text)
            print(f"脈絡圖已產生並儲存於 {output_path}")
        elif hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
            print(f"內容生成被阻止：{response.prompt_feedback.block_reason}")
            print(f"詳細資訊：{response.prompt_feedback.block_reason_message}")
        else:
            print("錯誤：無法從 Gemini API 獲取有效的回應內容。")
            print("API 回應:", response)


except FileNotFoundError:
    # 這個錯誤處理現在主要針對輸出路徑，因為輸入來源改為 txt 檔案
    print(f"錯誤：無法寫入輸出檔案 '{output_path}'。請檢查路徑或權限。")
except Exception as e:
    print(f"執行過程中發生錯誤：{e}")

