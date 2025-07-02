"""
QCon InfoQ 會議爬蟲
用於爬取 QCon (InfoQ) 會議議程與摘要
"""
import time
import threading
import concurrent.futures
import random
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapers.base_scraper import BaseScraper
from scrapers.utils.driver_setup import setup_driver

class QconInfoqScraper(BaseScraper):
    """
    QCon InfoQ 會議爬蟲類
    """
    def __init__(self, headless=False, wait_time=10, use_bigquery=False, bq_credentials=None, bq_project_id=None):
        super().__init__(
            headless=headless,
            wait_time=wait_time,
            use_bigquery=use_bigquery,
            bq_credentials=bq_credentials,
            bq_project_id=bq_project_id
        )
        self.url = "https://qcon.infoq.cn/2025/beijing/track"
        self.seminar = "202503 QCon Beijing"
        self.data_lock = threading.Lock()
        self.data = []
        self.max_workers = 5  # 預設工作線程數

    def get_scraper_name(self):
        return "202503 QCon Beijing"

    def get_filename_prefix(self):
        return self.seminar
        
    def random_delay(self, min_seconds=0.5, max_seconds=1.5):
        """添加隨機延遲以模擬人類行為"""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def setup_thread_driver(self):
        """為多線程創建獨立的WebDriver實例"""
        driver = setup_driver(headless=self.headless)
        driver.wait = WebDriverWait(driver, self.wait_time)
        return driver

    def scrape(self):
        """使用多線程爬取網頁內容"""
        # 清空數據
        self.data = []
        
        # 使用主驅動獲取主頁內容
        self.driver.get(self.url)
        print(f"開始爬取網頁: {self.url}")
        time.sleep(3)
        
        try:
            # 獲取所有講座連結
            links = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "title")]/a'))
            )
            
            # 先獲取所有連結信息，避免線程間共享WebElement對象
            link_info_list = []
            for link in links:
                text = link.text.strip()
                href = link.get_attribute("href")
                link_info_list.append((text, href))
            
            total_links = len(link_info_list)
            print(f"找到 {total_links} 個演講題目")
            
            # 創建線程池
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # 為每個線程創建一個獨立的WebDriver實例
                drivers = [self.setup_thread_driver() for _ in range(self.max_workers)]
                
                # 提交任務到線程池
                futures = []
                for index, link_info in enumerate(link_info_list):
                    driver = drivers[index % self.max_workers]
                    future = executor.submit(self.process_link, link_info, driver, index, total_links)
                    futures.append(future)
                    
                    # 每提交一批任務後短暫延遲，避免同時發起太多請求
                    if (index + 1) % self.max_workers == 0:
                        self.random_delay(0.5, 1)
                
                # 等待所有任務完成
                for future in concurrent.futures.as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"任務執行出錯: {e}")
                
                # 關閉所有線程的WebDriver實例
                for driver in drivers:
                    driver.quit()
        
        except Exception as e:
            print(f"爬取主頁時發生錯誤: {e}")
        
        # 返回收集的數據
        return self.data

    def scrape_content(self, url, max_retries=3):
        """爬取單個頁面的內容，用於非多線程方式"""
        retries = 0
        while retries < max_retries:
            try:
                self.driver.get(url)
                content_element = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, '//div[@data-v-2c704944][@class="content"]'))
                )
                content_text = content_element.text.strip()
                
                # 嘗試查找PDF連結元素
                pdf_url = None
                try:
                    pdf_element = self.driver.find_element(By.XPATH, '//a[contains(@class, "item ppt") or contains(@class, "icon-ppt")]')
                    if pdf_element:
                        pdf_url = pdf_element.get_attribute("href")
                        print(f"找到PDF連結: {pdf_url}")
                except Exception as e:
                    print(f"未找到PDF連結或查找過程出錯: {e}")
                    
                return content_text, pdf_url
            except Exception as e:
                retries += 1
                print(f"爬取內容失敗，重試 {retries}: {e}")
                self.random_delay(1, 2)  # 重試前稍微延遲
        
        # 所有重試都失敗
        return "爬取失敗，已達最大重試次數", None

    def process_link(self, link_info, driver, index, total_links):
        try:
            text, href = link_info
            print(f"正在處理第 {index + 1}/{total_links} 個項目: {text}")
            
            # 使用提供的driver而不是self.driver，因為每個線程有自己的driver
            wait = driver.wait
            
            # 爬取內容
            retries = 0
            max_retries = 3
            content_text = ""
            pdf_url = None
            
            while retries < max_retries:
                try:
                    driver.get(href)
                    content_element = wait.until(
                        EC.visibility_of_element_located((By.XPATH, '//div[@data-v-2c704944][@class="content"]'))
                    )
                    content_text = content_element.text.strip()
                    
                    # 嘗試查找PDF連結元素
                    try:
                        pdf_element = driver.find_element(By.XPATH, '//a[contains(@class, "item ppt") or contains(@class, "icon-ppt")]')
                        if pdf_element:
                            pdf_url = pdf_element.get_attribute("href")
                            print(f"找到PDF連結: {pdf_url}")
                    except Exception as e:
                        print(f"未找到PDF連結或查找過程出錯: {e}")
                        
                    break  # 成功爬取，跳出循環
                except Exception as e:
                    retries += 1
                    print(f"爬取內容失敗，重試 {retries}: {e}")
                    self.random_delay(1, 2)  # 重試前稍微延遲
            
            if retries == max_retries:
                content_text = "爬取失敗，已達最大重試次數"
            
            # 使用線程鎖確保數據安全
            with self.data_lock:
                self.data.append({
                    "conference_id": str(uuid.uuid4()),
                    "seminar": self.seminar,
                    "name": text,
                    "description": content_text,
                    "url": href,
                    "pdf_url": pdf_url or ""
                })
                
            return True
        except Exception as e:
            print(f"處理連結時出錯: {e}")
            return False
