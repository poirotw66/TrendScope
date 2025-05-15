import pandas as pd
from pathlib import Path
import re
import logging
from src.utils.string_utils import normalize_string

logger = logging.getLogger(__name__)

class ExcelWriter:
    """負責將資料寫入 Excel 檔案"""

    @staticmethod
    def normalize_title(title):
        """正規化標題，移除不適用於檔名的字元"""
        return normalize_string(title)

    def save_key_takeaways(self, meeting_title, key_takeaways, excel_path):
        """
        將 Key Takeaways 存入指定的 Excel 檔案

        Args:
            meeting_title (str): 會議標題
            key_takeaways (str): Key Takeaways 內容
            excel_path (str): Excel 檔案路徑
        """
        try:
            excel_file = Path(excel_path)

            if not excel_file.exists():
                logger.warning(f"Excel 檔案不存在: {excel_path}。無法保存核心觀點。")
                # 考慮是否要創建新檔案或拋出錯誤
                # df = pd.DataFrame(columns=['Meeting', 'Key']) # 創建新 DataFrame
                return False # 或 raise FileNotFoundError

            try:
                df = pd.read_excel(excel_file)
            except Exception as read_err:
                logger.error(f"讀取 Excel 檔案 {excel_path} 時出錯: {read_err}")
                return False

            if 'Meeting' not in df.columns:
                logger.warning("Excel 檔案中未找到 'Meeting' 欄位。")
                # 可以選擇添加欄位或返回錯誤
                # df['Meeting'] = None # 添加欄位
                return False

            if 'Key' not in df.columns:
                df['Key'] = "" # 或者 pd.NA
                logger.info("Excel 檔案中未找到 'Key' 欄位，已自動添加。")

            normalized_meeting_title = self.normalize_title(meeting_title)
            found = False
            for i, row in df.iterrows():
                # 確保比較時處理 NaN 或 None 的情況
                row_meeting_title = row.get('Meeting')
                if pd.isna(row_meeting_title):
                    continue
                normalized_row_title = self.normalize_title(row_meeting_title)

                if normalized_row_title == normalized_meeting_title:
                    # 使用 .loc 來確保正確更新
                    df.loc[i, 'Key'] = key_takeaways
                    found = True
                    logger.info(f"已更新 '{meeting_title}' 的核心觀點於 {excel_path}")
                    break

            if not found:
                logger.warning(f"在 Excel 檔案中未找到會議標題 '{meeting_title}' (正規化後: '{normalized_meeting_title}')。")
                return False # 目前行為是不新增

            try:
                df.to_excel(excel_file, index=False, engine='openpyxl') # 指定 engine
                return True
            except Exception as write_err:
                 logger.error(f"寫入 Excel 檔案 {excel_path} 時出錯: {write_err}")
                 return False

        except ImportError:
             logger.error("需要 pandas 和 openpyxl 庫才能保存到 Excel。請安裝 (`pip install pandas openpyxl`)。")
             return False
        except Exception as e:
            logger.error(f"保存核心觀點到 Excel 時發生未預期錯誤 ('{meeting_title}'): {e}")
            return False