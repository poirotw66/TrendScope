"""
研討會會議清單讀取工具 - 將 Excel 檔案轉換為會議名稱到URL的映射
"""

import os
import pandas as pd
from pathlib import Path
import openpyxl  # 用於驗證 Excel 檔案
import logging
from typing import Optional, Dict

# Constants for column names
MEETING_COLUMN = "Meeting"
URL_COLUMN = "URL"

class ExcelValidator:
    """負責驗證 Excel 檔案的工具類別"""

    @staticmethod
    def validate_file(file_path: str) -> bool:
        """驗證檔案是否為有效的 Excel 檔案"""
        if not os.path.isfile(file_path):
            logging.error(f"錯誤: 找不到檔案 {file_path}")
            return False
        try:
            with open(file_path, "rb") as f:
                openpyxl.load_workbook(f)
            return True
        except Exception as e:
            logging.error(f"錯誤: 檔案 {file_path} 不是有效的 Excel 檔案: {e}")
            return False


class MeetingListProcessor:
    """負責處理會議清單資料的工具類別"""

    @staticmethod
    def process_data(df: pd.DataFrame) -> Dict[str, str]:
        """處理 Excel 資料並建立會議名稱到URL的映射"""
        missing_columns = [col for col in [MEETING_COLUMN, URL_COLUMN] if col not in df.columns]
        if missing_columns:
            logging.warning(f"Excel 檔案缺少以下必要欄位: {', '.join(missing_columns)}")
            return {}

        meeting_urls = {}
        for _, row in df.iterrows():
            meeting_name = str(row[MEETING_COLUMN])
            url = str(row[URL_COLUMN]) if not pd.isna(row[URL_COLUMN]) else ""
            meeting_urls[meeting_name] = url
        return meeting_urls


class MeetingListReader:
    """讀取研討會會議清單並提供會議名稱到URL的映射"""
    
    def __init__(self, excel_path: Optional[str] = None):
        """
        初始化會議清單讀取器
        
        Args:
            excel_path (str, optional): Excel 檔案路徑，如果為 None 則使用預設路徑
        """
        self.excel_path = excel_path or self._get_default_excel_path()
        self.meeting_urls = {}
        self.loaded = False

    def _get_default_excel_path(self) -> str:
        """取得預設的 Excel 檔案路徑"""
        project_root = Path(__file__).parent.parent
        return os.path.join(project_root, "google_next_sessions.xlsx")

    def load_meeting_list(self) -> Dict[str, str]:
        """
        讀取會議清單 Excel 檔案並建立會議名稱到URL的映射
        
        Returns:
            dict: 會議名稱到URL的映射
        """
        if not ExcelValidator.validate_file(self.excel_path):
            return {}

        try:
            df = pd.read_excel(self.excel_path)
            self.meeting_urls = MeetingListProcessor.process_data(df)
            self.loaded = True
            logging.info(f"成功讀取 {len(self.meeting_urls)} 筆會議URL資料")
            return self.meeting_urls
        except Exception as e:
            logging.error(f"讀取會議清單時發生錯誤: {e}")
            return {}

    def get_meeting_urls(self) -> Dict[str, str]:
        """
        獲取會議名稱到URL的映射
        
        Returns:
            dict: 會議名稱到URL的映射
        """
        if not self.loaded:
            return self.load_meeting_list()
        return self.meeting_urls

    def get_url_by_meeting_name(self, meeting_name: str) -> str:
        """
        根據會議名稱獲取URL
        
        Args:
            meeting_name (str): 會議名稱
            
        Returns:
            str: 會議URL，如果找不到則返回空字串
        """
        if not self.loaded:
            self.load_meeting_list()
        return self.meeting_urls.get(meeting_name, "")


# 單例模式，方便其他模組直接導入使用
meeting_list = MeetingListReader()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    meeting_urls = meeting_list.get_meeting_urls()
    for meeting_name, url in meeting_urls.items():
        print(f"會議名稱: {meeting_name}")
        print(f"URL: {url}")
        print("-" * 50)