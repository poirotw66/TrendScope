"""
會議逐字稿總結工具 - 使用 Gemini API
"""

import os
import sys
import json
import google.generativeai as genai
from pathlib import Path
import re
import logging # 引入 logging 模組

# 添加專案根目錄到系統路徑
sys.path.append(str(Path(__file__).parent.parent))

from config.config import GEMINI_API_KEY, MAX_TRANSCRIPT_LENGTH, GEMINI_MODEL_NAME,INPUT_CSV_PATH
from src.meeting_list_reader import meeting_list # 暫時保留，後續考慮注入
from src.utils.summary_parser import SummaryParser
from src.utils.excel_writer import ExcelWriter
from src.utils.html_generator import HtmlGenerator # <<< 新增導入 HtmlGenerator

# 設定日誌記錄器
logger = logging.getLogger(__name__)
# 可以在主程式或 logging_utils 中設定更詳細的日誌格式與級別

class TranscriptSummarizer:
    """使用 Gemini API 總結會議逐字稿的類"""

    def __init__(self, model_name=GEMINI_MODEL_NAME, api_key=GEMINI_API_KEY): # 允許傳入 model_name 和 api_key
        """初始化 Gemini 客戶端"""
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
            self.parser = SummaryParser()
            self.excel_writer = ExcelWriter()
            self.html_generator = HtmlGenerator() # <<< 初始化 HtmlGenerator
            logger.info(f"Gemini model '{model_name}' initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini model: {e}")
            raise # 初始化失敗時拋出例外

    def _build_prompt(self, transcript_text, meeting_title, url):
        """建立傳送給 Gemini API 的提示"""
        # 將原本的 prompt 字串移到這裡，方便管理
        return f"""
        請遵循以下步驟處理提供的會議逐字稿：

        1.  內部校對：
            *   仔細閱讀下方提供的「會議逐字稿」。
            *   在內部處理中，找出並修正逐字稿裡最明顯的錯字或口誤（例如：同音異字、打字錯誤、常見用詞錯誤）。
            *   使用建議的正確詞彙替換錯誤詞彙。
            *   將簡體中文翻譯成繁體中文。
            *   重要限制：校正時必須保持句子原有語氣，忠於原文意涵，僅修正明顯錯誤，避免過度詮釋或修改。
            *   此校對結果不需輸出。

        2.  撰寫會議總結（僅輸出此部分）：
            *   基於內部校對後的逐字稿內容，撰寫一份有完整脈絡的會議總結。具體要求如下：
            - 總結標題：
                - 第一行輸出提供的 {meeting_title} 原文。
                - 第二行輸出格式： `[會議影片連結]({url})`
                - 第三行繁體中文翻譯的{meeting_title}
                - 範例：
                ```
                # OpenAI Developer Day 2024
                [會議影片連結](https://example.com)
                OpenAI 開發者日 2024
                ```

            - 內容結構（需依下列順序分段撰寫、並且儘量詳細）：
            - ## 1. 核心觀點
            - ## 2. 詳細內容
            - ## 3. 重要結論

            - 各段落之間需有明確分隔（如空行）。

        3.  輸出要求：
            *   最終輸出內容僅包含步驟 2所述的會議總結。
            *   請勿輸出校對過程、校對後的逐字稿、或任何非總結內容的額外說明文字。
            *   請產生純文字形式的 markdown 內容，不要加上程式碼區塊（例如 ```markdown``` 或 ```），只要直接輸出結果。
            *   輸出語言必須為繁體中文。
            *   總結的段落之間要有明確的分隔。
        會議逐字稿:
        {transcript_text}

        輸出範例：
        # "谈故障色变”到有章可循：美图 SRE 故障应急与复盘实践
        [會議影片連結](TEST.com)
        "談故障色變"到有章可循：美圖SRE故障排除與複盤實踐

        ---

        ## 1. 核心觀點
        ... (範例內容省略) ...
        ---

        ## 2. 詳細內容
        ... (範例內容省略) ...
        ---

        ## 3. 重要結論
        ... (範例內容省略) ...
        """

    def summarize(self, transcript_text, meeting_title, excel_path=INPUT_CSV_PATH): # <<< 添加 excel_path 參數
        """
        總結會議逐字稿

        Args:
            transcript_text (str): 會議逐字稿文本
            meeting_title (str): 會議標題
            excel_path (str, optional): 要寫入 Key Takeaways 的 Excel 檔案路徑。 Defaults to None.

        Returns:
            dict: 包含總結內容與狀態的字典
        """
        if len(transcript_text) > MAX_TRANSCRIPT_LENGTH:
            logger.warning(f"Transcript length ({len(transcript_text)}) exceeds MAX_TRANSCRIPT_LENGTH ({MAX_TRANSCRIPT_LENGTH}). Consider chunking.")

        url = meeting_list.get_url(meeting_title)
        logger.info(f"Summarizing meeting: {meeting_title} (URL: {url})")

        prompt = self._build_prompt(transcript_text, meeting_title, url)

        try:
            generation_config = genai.GenerationConfig(temperature=0.1)
            response = self.model.generate_content(contents=prompt, generation_config=generation_config)

            if not response or not hasattr(response, 'text'):
                raise Exception("Invalid response from Gemini API")

            summary_text = response.text
            logger.info(f"Successfully generated summary for '{meeting_title}'.")

            # 使用 SummaryParser 提取 Key Takeaways
            key_takeaways = self.parser.extract_key_takeaways(summary_text) # <<< 修改調用

            # 將 Key Takeaways 存入 Excel
            if excel_path and key_takeaways: # <<< 檢查 excel_path 和 key_takeaways 是否有效
                save_success = self.excel_writer.save_key_takeaways(meeting_title, key_takeaways, excel_path) # <<< 使用 ExcelWriter
                if not save_success:
                    logger.warning(f"未能將 '{meeting_title}' 的核心觀點保存到 Excel。")
            elif excel_path:
                logger.warning(f"無法提取 '{meeting_title}' 的核心觀點，因此未寫入 Excel。")


            return {
                "summary": summary_text,
                "status": "success",
                "key_takeaways": key_takeaways
            }
        except Exception as e:
            logger.error(f"Error summarizing '{meeting_title}': {e}")
            return {
                "summary": "",
                "status": "error",
                "error_message": str(e)
            }

    # <<< 移除 _save_key_takeaways_to_excel 方法 >>>

    def save_summary_json(self, summary, output_path): # 改名以更清晰表示格式
        """
        保存總結到 JSON 文件

        Args:
            summary (dict): 總結內容
            output_path (str): 輸出文件路徑
        """
        try:
            output_dir = Path(output_path).parent
            output_dir.mkdir(parents=True, exist_ok=True) # 確保目錄存在
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            logger.info(f"Summary saved to JSON: {output_path}")
        except Exception as e:
            logger.error(f"Error saving summary to JSON '{output_path}': {e}")


    # generate_email_html 和 save_email_html 應移至 HTMLGenerator
    # Placeholder for HTML generation logic
    # _generate_email_html_content 方法保持不變

    # def save_summary_html(self, summary, output_path, meeting_title=None): # 改名
    #     """
    #     將會議摘要保存為 HTML 文件

    #     Args:
    #         summary (dict): 包含摘要內容和狀態的字典
    #         output_path (str): 輸出文件路徑
    #         meeting_title (str, optional): 會議標題. Defaults to None.
    #     """
    #     if summary.get("status") != "success":
    #         logger.error(f"無法生成 HTML：'{meeting_title}' 的摘要生成失敗。")
    #         return
    
    #         summary_markdown = summary.get("summary", "")
    #         if not summary_markdown:
    #             logger.warning(f"無法生成 HTML：'{meeting_title}' 的摘要內容為空。")
    #             return
    
    #         # 獲取 URL (後續應改為注入或傳遞)
    #         url = meeting_list.get_url(meeting_title) if meeting_title else ""
    
    #         # 檢查輸出路徑是否只有副檔名
    #         output_path_obj = Path(output_path)
    #         if output_path_obj.name.startswith('.'):
    #             # 如果檔案名只有副檔名，則使用會議標題作為檔案名
    #             safe_title = self.excel_writer.normalize_title(meeting_title) if meeting_title else "untitled"
    #             # 確保檔案名不為空
    #             if not safe_title:
    #                 safe_title = "untitled"
    #             # 構建新的輸出路徑
    #             new_output_path = output_path_obj.parent / f"{safe_title}{output_path_obj.suffix}"
    #             logger.info(f"檔案名為空，使用會議標題作為檔案名: {new_output_path}")
    #             output_path = str(new_output_path)
    
    #         # 使用 HtmlGenerator 保存 HTML
    #         save_success = self.html_generator.save_summary_html(
    #             summary_markdown,
    #             output_path,
    #             meeting_title=meeting_title,
    #             url=url
    #         )
    
    #         if not save_success:
    #             logger.error(f"未能將 '{meeting_title}' 的摘要保存為 HTML 文件到 {output_path}。")
    def save_summary_html(self, summary, output_path, meeting_title=None):
        """將會議摘要保存為 HTML 文件"""
        if summary.get("status") != "success":
            logger.error(f"無法生成 HTML：'{meeting_title}' 的摘要生成失敗。")
            return False
        
        summary_markdown = summary.get("summary", "")
        if not summary_markdown:
            logger.warning(f"無法生成 HTML：'{meeting_title}' 的摘要內容為空。")
            return False
        
        # 確保輸出目錄存在
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)
        
        # 檢查檔案名是否有效
        filename = os.path.basename(output_path)
        if not filename or filename.startswith('.'):
            # 使用會議標題作為檔案名
            safe_title = self.excel_writer.normalize_title(meeting_title) if meeting_title else "untitled"
            if not safe_title:
                safe_title = "untitled"
            output_path = os.path.join(output_dir, f"{safe_title}.html")
        
        # 記錄實際使用的檔案路徑
        logger.info(f"嘗試保存 HTML 到: {output_path}")
        
        try:
            # 使用 HtmlGenerator 保存 HTML
            url = meeting_list.get_url(meeting_title) if meeting_title else ""
            save_success = self.html_generator.save_summary_html(
                summary_markdown,
                output_path,
                meeting_title=meeting_title,
                url=url
            )
            
            if save_success:
                logger.info(f"HTML 摘要已成功保存到: {output_path}")
                return True
            else:
                logger.error(f"未能將 '{meeting_title}' 的摘要保存為 HTML 文件。")
                return False
        except Exception as e:
            logger.error(f"保存 HTML 時發生錯誤: {e}", exc_info=True)
            return False