"""
會議逐字稿總結工具 - 使用Gemini 2.0 API
"""

import os
import sys
import json
import google.generativeai as genai
from pathlib import Path
import re

# 添加專案根目錄到系統路徑
sys.path.append(str(Path(__file__).parent.parent))

from config.config import GEMINI_API_KEY, MAX_TRANSCRIPT_LENGTH
from src.meeting_list_reader import meeting_list

class TranscriptSummarizer:
    """使用Gemini 2.0 API總結會議逐字稿的類"""
    
    def __init__(self):
        """初始化Gemini客戶端"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        # self.model = genai.GenerativeModel('gemini-2.0-flash-lite')
        # self.model = genai.GenerativeModel('gemini-2.5-pro-exp-03-25')
    
    def summarize(self, transcript_text, meeting_title):
        """
        總結會議逐字稿
        
        Args:
            transcript_text (str): 會議逐字稿文本
            
        Returns:
            dict: 包含總結內容的字典
        """
        if len(transcript_text) > MAX_TRANSCRIPT_LENGTH:
            print(f"警告: 文本長度超過{MAX_TRANSCRIPT_LENGTH}字符，可能需要分段處理")
        url = meeting_list.get_url(meeting_title)
        print(f"URL: {url}, ,Meeting: {meeting_title}")
        prompt = f"""
        請遵循以下步驟處理提供的會議逐字稿：

        1.  內部校對：
            *   仔細閱讀下方提供的「會議逐字稿」。
            *   在內部處理中，找出並修正逐字稿裡最明顯的錯字或口誤（例如：同音異字、打字錯誤、常見用詞錯誤）。
            *   使用建議的正確詞彙替換錯誤詞彙。
            *   將簡體中文翻譯成繁體中文。
            *   重要限制：校正時必須保持句子原有語氣，忠於原文意涵，僅修正明顯錯誤，避免過度詮釋或修改。
            *   此校對結果不需輸出。

        2.  撰寫會議總結（僅輸出此部分）：
            *   基於內部校對後的逐字稿內容，，撰寫一份有完整脈絡的會議總結。具體要求如下：
            - 總結標題：
                - 第一行輸出提供的 {meeting_title} 原文。
                - 第三行輸出格式： `[會議影片連結]({url})`
                - 第四行繁體中文翻譯的{meeting_title}
                - 範例：
                ```
                # OpenAI Developer Day 2024
                [會議影片連結](https://example.com)
                OpenAI 開發者日 2024
                ```

            - 內容結構（需依下列順序分段撰寫、並且儘量詳細）：
            - **1. 核心觀點**
            - **2. 詳細內容**
            - **3. 重要結論**

            - 各段落之間需有明確分隔（如空行）。

        3.  輸出要求：
            *   最終輸出內容僅包含步驟 2所述的會議總結。
            *   請勿輸出校對過程、校對後的逐字稿、或任何非總結內容的額外說明文字。
            *   請產生純文字形式的 markdown 內容，不要加上程式碼區塊（例如 markdown 或 ），只要直接輸出結果。
            *   輸出語言必須為繁體中文。
            *   總結的段落之間要有明確的分隔。
        會議逐字稿:
        {transcript_text}

        輸出範例：

        # "谈故障色变”到有章可循：美图 SRE 故障应急与复盘实践
        主題演講  
        [會議影片連結](TEST.com)
        "談故障色變"到有章可循：美圖SRE故障排除與複盤實踐

        ---

        ## 1. 核心觀點

        本次演講主要圍繞美圖公司在 SRE（Site Reliability Engineering，網站可靠性工程）方面，如何從被動處理故障轉變為有系統、有規律的應對，以及如何透過故障應急和復盤實踐來提升系統穩定性。核心觀點包括：

        - **建立正確的故障認知：**  
        將故障視為常態，並理解干預防手段的代價。

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
        
        try:
            generation_config = genai.GenerationConfig(temperature=0.1)
            # response = self.model.generate_content(contents=prompt)
            response = self.model.generate_content(contents=prompt, generation_config=generation_config)
            summary_text = response.text
            
            # 提取 Key Takeaways 部分
            key_takeaways = self._extract_key_takeaways(summary_text)
            
            # 將 Key Takeaways 存入 Excel 檔案
            self._save_key_takeaways_to_excel(meeting_title, key_takeaways)
            
            return {
                "summary": summary_text,
                "status": "success",
                "key_takeaways": key_takeaways
            }
        except Exception as e:
            return {
                "summary": "",
                "status": "error",
                "error_message": str(e)
            }
    
    def _extract_key_takeaways(self, summary_text):
        """
        從摘要文本中提取 Key Takeaways 部分
        
        Args:
            summary_text (str): 摘要文本
            
        Returns:
            str: Key Takeaways 內容
        """
        lines = summary_text.strip().split('\n')
        key_takeaways = ""
        in_key_takeaways = False
        
        for i, line in enumerate(lines):
            if line.startswith('## 1. 核心觀點'):
                in_key_takeaways = True
                continue
            
            if in_key_takeaways:
                # 如果遇到下一個段落標題，結束提取
                if line.startswith('## ') and not line.startswith('## 1. 核心觀點'):
                    break
                key_takeaways += line + '\n'
        
        return key_takeaways.strip()
    
    def _save_key_takeaways_to_excel(self, meeting_title, key_takeaways):
        """
        將 Key Takeaways 存入 Excel 檔案
        
        Args:
            meeting_title (str): 會議標題
            key_takeaways (str): Key Takeaways 內容
        """
        try:
            import pandas as pd
            from pathlib import Path
            
            # Excel 檔案路徑
            excel_path = Path.home() / "Github" / "google_next" / "google_next_sessions.xlsx"
            
            # 檢查檔案是否存在
            if not excel_path.exists():
                print(f"警告: 找不到 Excel 檔案 {excel_path}")
                return
            
            # 讀取 Excel 檔案
            df = pd.read_excel(excel_path)
            
            # 檢查是否有 'Meeting' 欄位
            if 'Meeting' not in df.columns:
                print("警告: Excel 檔案中沒有 'Meeting' 欄位")
                return
            
            # 檢查是否有 'Key' 欄位，如果沒有則新增
            if 'Key' not in df.columns:
                df['Key'] = ""
            
            # 尋找對應的會議標題並更新 Key 欄位
            def normalize_filename(title):
                # 移除不合法字元，只保留中英文、數字、空格、底線、點
                title = re.sub(r'[\\/:*?"<>|]', '', title)
                title = title.strip()
                return title
            found = False
            for i, row in df.iterrows():
                if normalize_filename(str(row['Meeting'])) == normalize_filename(meeting_title):
                    df.at[i, 'Key'] = key_takeaways
                    found = True
                    break
            
            if not found:
                print(f"警告: 在 Excel 檔案中找不到會議標題 '{meeting_title}'")
                return
            
            # 保存 Excel 檔案
            df.to_excel(excel_path, index=False)
            print(meeting_title)
            print(f"已將 Key Takeaways 存入 Excel 檔案: {excel_path}")
            
        except Exception as e:
            print(f"存入 Excel 檔案時發生錯誤: {e}")
    
    def save_summary(self, summary, output_path):
        """
        保存總結到文件
        
        Args:
            summary (dict): 總結內容
            output_path (str): 輸出文件路徑
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"總結已保存到: {output_path}")
    
    def generate_email_html(self, summary_text, meeting_title=None):
        url = ""
        if meeting_title:
            url = meeting_list.get_url(meeting_title)
        # 解析 markdown，提取標題、影片連結、中文標題與三大段落
        lines = summary_text.strip().split('\n')
        en_title = ""
        video_url = ""
        zh_title = ""
        core_content = ""
        detail_content = ""
        conclusion_content = ""
        section = None
        buffer = []
    
        for line in lines:
            if line.startswith("# "):
                en_title = line[2:].strip()
            elif line.startswith("[會議影片連結]"):
                if "(" in line and ")" in line:
                    video_url = line.split("(", 1)[1].split(")", 1)[0]
            elif not zh_title and line.strip() and not line.startswith("#") and not line.startswith("["):
                zh_title = line.strip()
            elif line.strip().startswith("## 1. 核心觀點"):
                if buffer and section:
                    if section == "core":
                        core_content = "\n".join(buffer).strip()
                    elif section == "detail":
                        detail_content = "\n".join(buffer).strip()
                    elif section == "conclusion":
                        conclusion_content = "\n".join(buffer).strip()
                buffer = []
                section = "core"
            elif line.strip().startswith("## 2. 詳細內容"):
                if buffer and section:
                    if section == "core":
                        core_content = "\n".join(buffer).strip()
                    elif section == "detail":
                        detail_content = "\n".join(buffer).strip()
                    elif section == "conclusion":
                        conclusion_content = "\n".join(buffer).strip()
                buffer = []
                section = "detail"
            elif line.strip().startswith("## 3. 重要結論"):
                if buffer and section:
                    if section == "core":
                        core_content = "\n".join(buffer).strip()
                    elif section == "detail":
                        detail_content = "\n".join(buffer).strip()
                    elif section == "conclusion":
                        conclusion_content = "\n".join(buffer).strip()
                buffer = []
                section = "conclusion"
            else:
                if section:
                    buffer.append(line)
        # 收尾
        if buffer and section:
            if section == "core":
                core_content = "\n".join(buffer).strip()
            elif section == "detail":
                detail_content = "\n".join(buffer).strip()
            elif section == "conclusion":
                conclusion_content = "\n".join(buffer).strip()
    
        # markdown 轉 html
        import markdown
        core_html = markdown.markdown(core_content)
        detail_html = markdown.markdown(detail_content)
        conclusion_html = markdown.markdown(conclusion_content)
    
        # HTML 模板
        html_template = f"""
        <!DOCTYPE html>
        <html lang="zh-TW">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{en_title or meeting_title}</title>
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
                /* 為不同段落設置不同的邊框顏色和背景 */
                .section-block.conclusion {{
                    border-left-color: #e74c3c;
                    background-color: #fff9f9;
                }}
                .section-block.meeting-topic {{
                    border-left-color: #3498db;
                    background-color: #f7fbff;
                }}
                .section-block.tech-points {{
                    border-left-color: #2ecc71;
                    background-color: #f7fff9;
                }}
                .section-block.decisions {{
                    border-left-color: #f39c12;
                    background-color: #fffaf5;
                }}
                .section-block.timeline {{
                    border-left-color: #9b59b6;
                    background-color: #faf5ff;
                }}
                .section-block.challenges {{
                    border-left-color: #e67e22;
                    background-color: #fff8f2;
                }}
                .section-block.action-plan {{
                    border-left-color: #1abc9c;
                    background-color: #f5fffc;
                }}
                .section-title {{
                    font-size: 1.5rem;
                    margin-top: 0;
                    margin-bottom: 20px;
                    padding-bottom: 10px;
                    border-bottom: 2px solid #4b6cb7;
                    display: inline-block;
                }}
                /* 為不同段落標題設置對應的顏色 */
                .section-block.conclusion .section-title {{
                    color: #e74c3c;
                    border-bottom-color: #e74c3c;
                }}
                .section-block.meeting-topic .section-title {{
                    color: #3498db;
                    border-bottom-color: #3498db;
                }}
                .section-block.tech-points .section-title {{
                    color: #2ecc71;
                    border-bottom-color: #2ecc71;
                }}
                .section-block.decisions .section-title {{
                    color: #f39c12;
                    border-bottom-color: #f39c12;
                }}
                .section-block.timeline .section-title {{
                    color: #9b59b6;
                    border-bottom-color: #9b59b6;
                }}
                .section-block.challenges .section-title {{
                    color: #e67e22;
                    border-bottom-color: #e67e22;
                }}
                .section-block.action-plan .section-title {{
                    color: #1abc9c;
                    border-bottom-color: #1abc9c;
                }}
                .content-container ul {{
                    padding-left: 20px;
                }}
                .content-container li {{
                    margin-bottom: 10px;
                    position: relative;
                    list-style-type: none;
                    padding-left: 25px;
                }}
                .content-container li::before {{
                    content: "•";
                    position: absolute;
                    left: 0;
                    color: #4b6cb7;
                    font-size: 1.2rem;
                    font-weight: bold;
                }}
                .section-block.conclusion li::before {{ color: #e74c3c; }}
                .section-block.meeting-topic li::before {{ color: #3498db; }}
                .section-block.tech-points li::before {{ color: #2ecc71; }}
                .section-block.decisions li::before {{ color: #f39c12; }}
                .section-block.timeline li::before {{ color: #9b59b6; }}
                .section-block.challenges li::before {{ color: #e67e22; }}
                .section-block.action-plan li::before {{ color: #1abc9c; }}
                
                .content-container p {{
                    margin-bottom: 15px;
                    line-height: 1.7;
                }}
                .content-container strong {{
                    color: #2c3e50;
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
                footer a {{
                    color: #4b6cb7;
                    text-decoration: none;
                    font-weight: bold;
                }}
                footer a:hover {{
                    text-decoration: underline;
                }}
            </style>
        </head>
        <body>
            <header>
                <img src="https://i.imgur.com/0LXUWvj.png" alt="會議摘要圖示">
                <h1>{en_title}</h1>
                {f'<a href="{video_url}" class="video-link" target="_blank"><i>▶</i> 會議影片超連結</a>' if video_url else ''}
                <p>{zh_title}</p>
            </header>
            <main>
                <div class="content-container">
                    <div class="section-block meeting-topic">
                        <h2 class="section-title">1. 核心觀點</h2>
                        {core_html}
                    </div>
                    <div class="section-block tech-points">
                        <h2 class="section-title">2. 詳細內容</h2>
                        {detail_html}
                    </div>
                    <div class="section-block conclusion">
                        <h2 class="section-title">3. 重要結論</h2>
                        {conclusion_html}
                    </div>
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
        
        return html_template
    
    def save_email_html(self, summary, output_path, meeting_title=None):
        """
        將會議摘要保存為 Email HTML 文件
        
        Args:
            summary (dict): 包含摘要內容的字典
            output_path (str): 輸出文件路徑
            meeting_title (str, optional): 會議標題
        """
        if summary["status"] != "success":
            print(f"錯誤: 無法生成 Email HTML，摘要生成失敗")
            return
        
        # 獲取會議URL
        url = ""
        if meeting_title:
            url = meeting_list.get_url(meeting_title)
        
        html_content = self.generate_email_html(summary["summary"], meeting_title)
        
        # 如果有URL但HTML中沒有包含，手動添加
        if url and "會議影片超連結" not in html_content:
            html_content = html_content.replace(
                f'<h1>{meeting_title}</h1>',
                f'<h1>{meeting_title}</h1>\n<a href="{url}" class="video-link" target="_blank"><i>▶</i> 會議影片超連結</a>'
            )
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Email HTML 已保存到: {output_path}")


if __name__ == "__main__":
    # 簡單的命令行介面
    if len(sys.argv) < 2:
        print("用法: python transcript_summarizer.py <逐字稿文件路徑> [輸出文件路徑]")
        sys.exit(1)
    
    transcript_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "meeting_summary.json"
    
    if not os.path.exists(transcript_path):
        print(f"錯誤: 找不到文件 {transcript_path}")
        sys.exit(1)
    
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript_text = f.read()
    
    summarizer = TranscriptSummarizer()
    summary = summarizer.summarize(transcript_text)
    
    # 保存 JSON 格式摘要
    summarizer.save_summary(summary, output_path)
    
    # 同時保存 HTML 格式摘要
    html_output_path = output_path.rsplit('.', 1)[0] + '.html'
    summarizer.save_email_html(summary, html_output_path)