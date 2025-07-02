"""
AWS London Summit 爬蟲
用於爬取 AWS London Summit 的會議資訊
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from scrapers.base_scraper import BaseScraper

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
        print("正在載入頁面，請等待...")
        
        # 等待手動登入（如果需要）
        print("如需登入，請在 20 秒內完成")
        time.sleep(20)  # 等待頁面加載和可能的手動登入
        
        # 創建一個空的列表來存儲數據
        data = []
        
        # 找到所有會議卡片
        try:
            # 等待會議卡片元素加載
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-t4lfxt-card')))
            
            # 抓取所有會議卡片
            cards = self.driver.find_elements(By.CLASS_NAME, 'css-t4lfxt-card')
            print(f"找到 {len(cards)} 個會議卡片")
            
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
                    
                    print(f"{idx}. 會議名稱: {title}")
                    print(f"   會議連結: {link}")
                    
                except Exception as inner_e:
                    print(f"{idx}. 抓取失敗: {str(inner_e)}")
        
        except Exception as e:
            print(f"抓取數據時發生錯誤: {str(e)}")
            
        return data
