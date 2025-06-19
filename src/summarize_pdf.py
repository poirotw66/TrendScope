from google import genai
from google.genai import types
import pathlib
import httpx
from config.config import GEMINI_API_KEY, MAX_TRANSCRIPT_LENGTH
import time
import csv

client = genai.Client(api_key=GEMINI_API_KEY)

def get_url_from_csv(csv_path, topic_name):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('Topic', '').strip() == topic_name.strip():
                return row.get('url', '').strip()
    return "TEST.com"

def get_category_from_csv(csv_path, topic_name):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get('Topic', '').strip() == topic_name.strip():
                return row.get('Type', '').strip()
    return "主題演講"

def summarize_pdf(pdf_path, csv_path, output_dir="output/md"):
    file_path = pathlib.Path(pdf_path)
    file_name = file_path.stem
    url = get_url_from_csv(csv_path, file_name)
    category = get_category_from_csv(csv_path, file_name)
    sample_file = client.files.upload(
        file=file_path,
    )

    prompt = f"""
    ## 處理指示

    請依照以下步驟處理我提供的「簡報內容」，並遵循所有格式要求：

    ### 1. 內部校對（不輸出）
    - 仔細閱讀提供的「簡報內容」。
    - 將簡報內容中的簡體中文翻譯成繁體中文。
    - 僅作為後續撰寫會議總結的依據，不需要輸出校對結果或任何校對過程。

    ### 2. 撰寫會議總結（僅輸出此部分）
    根據內部校對後的簡報內容，撰寫一份有完整脈絡的簡報內容。具體要求如下：

    - 總結標題：
      - 第一行輸出提供的 {file_name} 原文。
      - 第二行輸出{category}
      - 第三行輸出格式： `[會議影片連結]({url})`
      - 第四行中文翻譯：{file_name} 
      - 範例：  
        ```
        # OpenAI Developer Day 2024  
        主題演講
        [會議影片連結](https://example.com)
        OpenAI 開發者日 2024
        ```

    - 內容結構（需依下列順序分段撰寫、並且儘量詳細）：
      - **1. 核心觀點**
      - **2. 詳細內容**
      - **3. 重要結論**

    - 各段落之間需有明確分隔（如空行）。

    ### 3. 輸出要求
    - 請僅輸出步驟2的「會議總結」。
    - 嚴禁輸出校對內容、校對過程、任何額外說明或多餘文字。
    - 使用 Markdown 格式。
    - 全文必須使用繁體中文。

    ---
    輸出範例：

    # "谈故障色变”到有章可循：美图 SRE 故障应急与复盘实践
    主題演講  
    [會議影片連結](TEST.com)
    "談故障色變"到有章可循：美圖SRE故障排除與複盤實踐

    ---

    ## 1. 核心觀點

    本次演講主要圍繞美圖公司在 SRE（Site Reliability Engineering，網站可靠性工程）方面，如何從被動處理故障轉變為有系統、有規律的應對，以及如何透過故障應急和復盤實踐來提升系統穩定性。核心觀點包括：

    - **建立正確的故障認知：**  
      將故障視為常態，並理解干預手段的代價。

    - **體系化建設以主動出擊：**  
      包括可觀測性、高可用性、應急體系等。

    - **強化流程與指揮機制：**  
      確保故障應急過程順暢高效。

    - **故障復盤作為持續改進關鍵：**  
      不是單純事後檢討，而是正向推動進步。

    - **明確 SRE 核心職責與企業價值關聯：**  
      穩定是安全生產的基礎，效率與成本控制帶來競爭優勢。

    - **建立故障管理框架：**  
      以度量指標（如 MTTR）推動穩定性改善。

    - **引入可用性體系（SLI/SLO/SLA）：**  
      並與業務價值緊密聯動。

    ---

    ## 2. 詳細內容

    ### **洞若觀火**
    - 深刻洞察故障本質，理解其規律。
    - 建立可靠性工程框架，推動 SRE 核心職責與企業發展對齊。
    - 強調穩定性為基礎，效率與成本為優勢。

    ### **未雨綢繆**
    從被動應對轉為主動建設，體系化推進：

    - **穩定性運營體系：**  
      - OnCall 輪值  
      - 常規巡檢  
      - 重點保障

    - **可觀測性體系：**  
      - 告警覆蓋  
      - 監控報表  
      - Metrics、Traces、Logs 故障排查

    - **高可用體系：**  
      - 災備建設  
      - 容量規劃  
      - 柔性架構設計

    - **應急體系：**  
      - 應急預案制定  
      - 預案演練  
      - 一鍵應急操作

    - **SRE 工具箱建設：**  
      - 涵蓋事前、事中、事後全流程工具  
      - 包括事件管理、故障管理、值班管理等模組

    ### **指揮若定**
    - 建立「消防隊」式故障應急團隊。
    - 明確優先級：恢復優先，問題定界優於根因定位。
    - 穩定現場指揮心態。
    - 建立標準流程與機制：
      - 故障升級流程
      - War Room 機制
      - 信息通報規範

    ### **復盤改進**
    - **黃金三問：**
      1. 如何更快恢復業務？
      2. 如何避免類似問題再發生？
      3. 有哪些經驗可總結、提煉並固化？
      4. One more thing：還能做些什麼？

    - 進行故障定級、定性、定責，並納入運作機制（如高壓線原則、健壯性原則）。
    - 週期性回顧數據，洞察故障趨勢。

    ### **補充總結與未來展望**
    - 強調故障管理框架建設：
      - 可用性體系
      - 錯誤預算、故障分管理
      - 組織結構支撐

    - 分享未來趨勢觀察：
      - 雲原生
      - 可觀測性深化
      - LLM Ops
      - AI Agent
    - 鼓勵大家：
      - 看清本質
      - 擁抱變化
      - 順勢而為
      - 精確定位、保有價值、泰然自若

    ---

    ## 3. 重要結論

    美圖公司透過 SRE 團隊的努力，建立了完善的故障應急與復盤機制，實現從被動應對到主動預防的轉變，大幅提升系統穩定性與可靠性。本次演講提供了寶貴的實戰經驗，對其他希望提升 SRE 能力的企業具有高度參考價值。

    """

    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=[sample_file, prompt])

    markdown_content = response.text

    output_dir = pathlib.Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filename = file_path.stem + ".md"
    output_path = output_dir / output_filename

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    print(f"已將摘要儲存至 {output_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="摘要單一PDF")
    parser.add_argument("--pdf", required=True, help="PDF檔案路徑")
    parser.add_argument("--csv", required=True, help="CSV檔案路徑")
    parser.add_argument("--output_dir", default="output/md", help="輸出目錄")
    args = parser.parse_args()
    summarize_pdf(args.pdf, args.csv, args.output_dir)