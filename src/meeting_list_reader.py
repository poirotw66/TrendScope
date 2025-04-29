"""
會議清單 Excel 讀取工具 - 直接查詢會議名稱對應影片連結
"""

import os
import pandas as pd
from pathlib import Path
import logging
import re

MEETING_COL = "Meeting"
URL_COL = "URL"

class MeetingList:
    """直接用 pandas 查詢 Excel 會議名稱對應 URL"""
    def __init__(self, excel_path=None):
        if excel_path is None:
            project_root = Path(__file__).parent.parent
            excel_path = os.path.join(project_root, "google_next_sessions.xlsx")
        self.excel_path = excel_path
        self.df = self._load_excel()

    def _load_excel(self):
        if not os.path.isfile(self.excel_path):
            logging.error(f"找不到檔案 {self.excel_path}")
            return pd.DataFrame()
        try:
            df = pd.read_excel(self.excel_path)
            if MEETING_COL not in df.columns or URL_COL not in df.columns:
                logging.warning(f"Excel 檔案缺少必要欄位: {MEETING_COL} 或 {URL_COL}")
                return pd.DataFrame()
            return df
        except Exception as e:
            logging.error(f"讀取 Excel 發生錯誤: {e}")
            return pd.DataFrame()

    def get_url(self, meeting_name):
        """根據會議名稱查詢 URL，找不到則回傳空字串（忽略前後空白與全半形引號）"""
        if self.df.empty:
            return ""
        # 標準化查詢字串
        def normalize(title):
            title = re.sub(r'[\\/:*?"<>|]', '', title)
            title = title.strip()
            return title
        target = normalize(meeting_name)
        for idx, row in self.df.iterrows():
            if normalize(row[MEETING_COL]) == target:
                return str(row[URL_COL]) if pd.notna(row[URL_COL]) else ""
        return ""

# 建立全域單例，方便直接 import 使用
meeting_list = MeetingList()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # 測試查詢
    test_name = "請輸入你要查詢的會議名稱"
    print(f"查詢結果: {meeting_list.get_url(test_name)}")