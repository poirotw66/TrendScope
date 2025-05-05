import logging

logger = logging.getLogger(__name__)

class SummaryParser:
    """負責解析 Gemini API 回傳的摘要文本"""

    def extract_key_takeaways(self, summary_text):
        """
        從摘要文本中提取核心觀點 (Key Takeaways) 部分

        Args:
            summary_text (str): 摘要文本

        Returns:
            str: 核心觀點內容，如果找不到則返回空字串
        """
        if not summary_text:
            logger.warning("無法提取核心觀點：摘要文本為空。")
            return ""

        lines = summary_text.strip().split('\n')
        key_takeaways = ""
        in_key_takeaways = False

        for i, line in enumerate(lines):
            # 尋找核心觀點標題
            if line.strip().startswith('## 1. 核心觀點'):
                in_key_takeaways = True
                continue # 跳過標題行

            if in_key_takeaways:
                # 如果遇到下一個 H2 標題，或文件結尾，結束提取
                if line.strip().startswith('## ') and not line.strip().startswith('## 1. 核心觀點'):
                    break
                # 避免加入分隔線 ---
                if line.strip() == "---":
                    continue
                # 加入非空行
                if line.strip():
                    key_takeaways += line + '\n'

        if not key_takeaways:
             logger.warning("在摘要中未找到 '## 1. 核心觀點' 部分。")

        return key_takeaways.strip()

    # 可以根據需要添加更多解析方法，例如提取詳細內容、重要結論等
    # def extract_detailed_content(self, summary_text): ...
    # def extract_conclusions(self, summary_text): ...
