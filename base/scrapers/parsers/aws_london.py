"""
AWS London Summit 爬蟲
用於爬取 AWS London Summit 的會議資訊
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from base.scrapers.base_scraper import BaseScraper
from base.utils.logger import get_scraper_logger

logger = get_scraper_logger()

class AWSLondonScraper(BaseScraper):
    """
    AWS London Summit 爬蟲類
    用於爬取 AWS London Summit 網站的會議資訊
    """
    
    def __init__(self, headless=False, wait_time=30, use_bigquery=False, bq_credentials=None, bq_project_id=None):
        """
        初始化 AWS London Summit 爬蟲
        
        Args:
            headless (bool): 是否啟用無頭模式，默認為 False（因為此網站可能需要手動登入）
            wait_time (int): WebDriverWait 的等待時間（秒），默認為 30
            use_bigquery (bool): 是否將資料上傳至 BigQuery，默認為 False
            bq_credentials (str): BigQuery 憑證路徑
            bq_project_id (str): BigQuery 項目 ID
        """
        super().__init__(
            headless=headless,
            wait_time=wait_time,
            use_bigquery=use_bigquery,
            bq_credentials=bq_credentials,
            bq_project_id=bq_project_id
        )
        self.url = "https://summitlondon.awslivestream.com/"
        
    def get_scraper_name(self):
        """
        獲取爬蟲名稱
        
        Returns:
            str: 爬蟲名稱
        """
        return "AWS London Summit"
        
    def get_filename_prefix(self):
        """
        獲取文件名前綴
        
        Returns:
            str: 文件名前綴
        """
        return "AWS_London_Summit_sessions"
        
    def scrape(self):
        """
        執行爬蟲
        
        Returns:
            list: 爬取的數據列表
        """
        # 打開網頁
        self.driver.get(self.url)
        logger.info("正在載入頁面，請等待...")
        
        # 等待手動登入（如果需要）
        logger.info("如需登入，請在 20 秒內完成")
        time.sleep(20)  # 等待頁面加載和可能的手動登入
        
        # 創建一個空的列表來存儲數據
        data = []
        
        # 找到所有會議卡片
        try:
            # 等待會議卡片元素加載
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-t4lfxt-card')))
            
            # 抓取所有會議卡片
            cards = self.driver.find_elements(By.CLASS_NAME, 'css-t4lfxt-card')
            logger.info("找到 %s 個會議卡片", len(cards))
            
            for idx, card in enumerate(cards, start=1):
                try:
                    # 抓取會議名稱和連結
                    link_element = card.find_element(By.CSS_SELECTOR, '.css-1bwr4xe-tileLink')
                    link = link_element.get_attribute('href')
                    
                    title_element = link_element.find_element(By.CSS_SELECTOR, '.css-1nsbbif-eventTitle')
                    title = title_element.text.strip()
                    
                    # 將數據添加到列表中
                    data.append({
                        "序號": idx,
                        "會議名稱": title,
                        "會議連結": link,
                    })
                    
                    logger.debug("%s. 會議名稱: %s", idx, title)
                    logger.debug("   會議連結: %s", link)
                    
                except Exception as inner_e:
                    logger.warning("%s. 抓取失敗: %s", idx, str(inner_e))
        
        except Exception as e:
            logger.error("抓取數據時發生錯誤: %s", str(e), exc_info=True)

        # 保存數據到實例變量，供後續使用
        self.data = data
        return data


def run_aws_london_scraper(headless=True, wait_time=30, use_bigquery=False):
    """
    執行 AWS London Summit 爬蟲的入口函數

    Args:
        headless (bool): 是否使用無頭模式
        wait_time (int): 等待時間
        use_bigquery (bool): 是否上傳到 BigQuery

    Returns:
        dict: 包含爬取結果的字典
    """
    scraper = None
    try:
        scraper = AWSLondonScraper(
            headless=headless,
            wait_time=wait_time,
            use_bigquery=use_bigquery
        )

        # 使用基類的 run 方法，它會自動處理 WebDriver 的生命週期
        file_path = scraper.run()

        # 獲取爬取的數據（如果有的話）
        scraped_data = getattr(scraper, 'data', [])

        return {
            "status": "success",
            "message": "AWS London Summit 爬蟲執行完成",
            "data": scraped_data,
            "file_path": file_path
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"AWS London Summit 爬蟲執行失敗: {str(e)}",
            "data": [],
            "file_path": None
        }
