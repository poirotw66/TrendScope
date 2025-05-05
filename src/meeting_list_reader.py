"""
會議清單 Excel 讀取工具 - 直接查詢會議名稱對應影片連結
"""

import os
import pandas as pd
from pathlib import Path
import logging
import re
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 從環境變數讀取設定，若不存在則使用預設值
MEETING_COL = os.environ.get("MEETING_COL", "Meeting")
URL_COL = os.environ.get("URL_COL", "URL")
DEFAULT_EXCEL_FILENAME = os.environ.get("MEETING_EXCEL_FILENAME", "GTC25.csv")

class MeetingList:
    """直接用 pandas 查詢 Excel 會議名稱對應 URL"""
    def __init__(self, csv_path=None):
        if csv_path is None:
            project_root = Path(__file__).parent.parent
            csv_path = os.path.join(project_root, DEFAULT_EXCEL_FILENAME)
        self.csv_path = csv_path
        self.df = self._load_excel()

    def _load_excel(self):
        if not os.path.isfile(self.csv_path):
            logging.error(f"找不到檔案 {self.csv_path}")
            return pd.DataFrame()
        try:
            df = pd.read_csv(self.csv_path)
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
            title = re.sub(r'[\\/:_*?"<>|]', '', title)
            title = title.strip()
            return title
        target = normalize(meeting_name)
        for idx, row in self.df.iterrows():
            if normalize(row[MEETING_COL]) == target:
                return str(row[URL_COL]) if pd.notna(row[URL_COL]) else ""
        return ""

# 提供一個函數來獲取 MeetingList 實例，可選擇性地傳入 csv_path
def get_meeting_list(csv_path=None):
    return MeetingList(csv_path)

# 建立全域單例，方便直接 import 使用
meeting_list = get_meeting_list()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # 測試查詢
    test_name = input("請輸入你要查詢的會議名稱: ")
    print(f"查詢結果: {meeting_list.get_url(test_name)}")