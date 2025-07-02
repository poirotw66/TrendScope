"""
爬蟲基類
為所有爬蟲提供基本功能和結構
"""
from abc import ABC, abstractmethod
import traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from urllib3.exceptions import MaxRetryError, NewConnectionError
from datetime import datetime

from scrapers.utils.driver_setup import setup_driver
from scrapers.utils.file_handler import save_to_excel
from bigquery.upload import ConferenceUploader

class BaseScraper(ABC):
    """
    爬蟲基類，提供所有爬蟲的基本功能
    """
    
    def __init__(self, headless=True, wait_time=30, use_bigquery=False, bq_credentials=None, bq_project_id=None):
        """
        初始化爬蟲
        
        Args:
            headless (bool): 是否啟用無頭模式，默認為 True
            wait_time (int): WebDriverWait 的等待時間（秒），默認為 30
            use_bigquery (bool): 是否將資料上傳至 BigQuery，默認為 False
            bq_credentials (str): BigQuery 憑證路徑
            bq_project_id (str): BigQuery 項目 ID
        """
        self.driver = None
        self.wait = None
        self.headless = headless
        self.wait_time = wait_time
        self.today = datetime.now().strftime("%Y%m%d")
        
        # BigQuery 相關
        self.use_bigquery = use_bigquery
        self.bq_credentials = bq_credentials
        self.bq_project_id = bq_project_id
        self.bq_uploader = None
        
        if self.use_bigquery:
            try:
                self.bq_uploader = ConferenceUploader(
                    credentials_path=self.bq_credentials,
                    project_id=self.bq_project_id
                )
            except Exception as e:
                print(f"初始化 BigQuery 上傳器失敗: {str(e)}")
                self.use_bigquery = False
        
    def start_driver(self):
        """
        啟動 WebDriver
        """
        try:
            self.driver = setup_driver(headless=self.headless)
            self.wait = WebDriverWait(self.driver, self.wait_time)
            return True
        except Exception as e:
            print(f"啟動 WebDriver 失敗: {str(e)}")
            traceback.print_exc()
            return False
            
    def quit_driver(self):
        """
        關閉 WebDriver
        """
        if self.driver:
            self.driver.quit()
            print("WebDriver 已關閉")
            
    @abstractmethod
    def scrape(self):
        """
        執行爬蟲，子類必須實現此方法
        
        Returns:
            list: 爬取的數據列表
        """
        pass
    
    def run(self, output_dir=None):
        """
        運行爬蟲並保存結果
        
        Args:
            output_dir (str, optional): 輸出目錄
            
        Returns:
            str: 保存的文件路徑，如果失敗則為 None
        """
        try:
            # 啟動 WebDriver
            if not self.start_driver():
                return None
            
            print(f"\n開始爬取 {self.get_scraper_name()}")
            
            # 執行爬蟲
            data = self.scrape()
            
            # 保存數據到文件
            file_path = None
            if data:
                file_path = save_to_excel(data, self.get_filename_prefix(), output_dir)
                
                # 上傳到 BigQuery（如果啟用）
                if self.use_bigquery and self.bq_uploader:
                    try:
                        self.bq_uploader.upload_sessions(data, self.get_scraper_name())
                    except Exception as e:
                        print(f"上傳到 BigQuery 失敗: {str(e)}")
            else:
                print("未獲取到數據")
                
            return file_path
                
        except Exception as e:
            print(f"爬蟲過程中發生錯誤: {str(e)}")
            traceback.print_exc()
            return None
            
        finally:
            # 確保 WebDriver 關閉
            self.quit_driver()
            print("爬蟲程序已完成")
    
    @abstractmethod
    def get_scraper_name(self):
        """
        獲取爬蟲名稱，用於日誌輸出
        
        Returns:
            str: 爬蟲名稱
        """
        pass
        
    @abstractmethod
    def get_filename_prefix(self):
        """
        獲取文件名前綴，用於保存數據
        
        Returns:
            str: 文件名前綴
        """
        pass
