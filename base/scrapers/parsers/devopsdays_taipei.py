"""
DevOpsDays Taipei 會議爬蟲
用於爬取 DevOpsDays Taipei 會議議程與摘要
"""
import sys
import os
import urllib.parse
import time
import threading
import concurrent.futures
import random
import re
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# 添加專案根目錄到 Python 路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
sys.path.insert(0, project_root)

from base.scrapers.base_scraper import BaseScraper
from base.scrapers.utils.driver_setup import setup_driver


class DevOpsDaysTaipeiScraper(BaseScraper):
    """
    DevOpsDays Taipei 會議爬蟲類
    """
    def __init__(self, headless=True, wait_time=10, use_bigquery=False, bq_credentials=None, bq_project_id=None):
        super().__init__(
            headless=headless,
            wait_time=wait_time,
            use_bigquery=use_bigquery,
            bq_credentials=bq_credentials,
            bq_project_id=bq_project_id
        )
        self.base_url = "https://devopsdays.tw/2025/agenda"
        self.seminar = "202506 DevOpsDays Taipei"
        self.data_lock = threading.Lock()
        self.data = []
        self.max_workers = 3  # 預設工作線程數，考慮到網站負載設定較少

    def get_scraper_name(self):
        return "202506 DevOpsDays Taipei"

    def get_filename_prefix(self):
        return "20250605_Taipei_DevOpsDays"

    def setup_thread_driver(self):
        """為多線程創建獨立的WebDriver實例"""
        driver = setup_driver(headless=self.headless)
        driver.wait = WebDriverWait(driver, self.wait_time)
        return driver

    def random_delay(self, min_seconds=0.5, max_seconds=1.5):
        """添加隨機延遲以模擬人類行為"""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def get_session_links(self):
        """獲取所有會議連結"""
        session_links = []
        
        try:
            # 開啟網頁
            self.driver.get(self.base_url)
            print(f"開始爬取網頁: {self.base_url}")
            
            # 有兩天會議
            for day in range(1, 3):
                date = "2025-06-05" if day == 1 else "2025-06-06"
                
                if day == 2:
                    # 按一下按鈕讓第二天的議程載入
                    day2_button = self.wait.until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, '//*[@id="event02-tab"]')
                        )
                    )
                    day2_button[0].click()
                    time.sleep(2)
                    
                # 會議標題
                seminar_elements_name = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f'//*[@id="agenda0{day}"]//div/div[2]/h5')
                    )
                )
                
                # 會議連結
                seminar_elements_url = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f'//*[@id="agenda0{day}"]//div/a')
                    )
                )
                
                # 檢查名稱和連結數量是否一致
                if len(seminar_elements_name) != len(seminar_elements_url):
                    print(f"警告：第 {day} 天的名稱和連結數量不一致")
                    continue
                    
                # 將會議名稱和連結存入 session_links
                for idx in range(len(seminar_elements_name)):
                    name = seminar_elements_name[idx].text.strip()
                    url = seminar_elements_url[idx].get_attribute("href")
                    
                    if name and url:
                        print(f"找到會議: {name}")
                        session_links.append({
                            "name": name,
                            "url": url,
                            "date": date
                        })
                        
            print(f"✅ 共找到 {len(session_links)} 個會議連結")
            return session_links
            
        except Exception as e:
            print(f"獲取會議連結時發生錯誤: {e}")
            return []

    def scrape_session_detail(self, session_info):
        """爬取單個會議的詳細資訊"""
        url = session_info['url']
        name = session_info['name']
        date = session_info['date']
        
        try:
            # 開啟網頁
            self.driver.get(url)
            # 隨機等待時間，避免被封鎖
            self.random_delay(0.5, 1.5)

            # 初始化返回資料
            session_data = {
                "conference_id": str(uuid.uuid4()),
                "seminar": self.seminar,
                "name": name,
                "description": "",
                "url": url,
                "pdf_url": "",
                "hashtags": [],
                "date": date
            }

            # 抓取 description
            try:
                description_elements = self.wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "session-txt"))
                )
                session_data["description"] = description_elements[0].text.strip()
            except TimeoutException:
                session_data["description"] = ""
                print(f"未找到描述內容: {name}")

            # 抓取 PDF URL
            try:
                pdf_elements = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//*[@id="__layout"]/div/section[2]/div/div/div[2]/div/div[2]/div/button[1]/a')
                    )
                )
                session_data["pdf_url"] = pdf_elements[0].get_attribute("href")
            except TimeoutException:
                session_data["pdf_url"] = ""
                print(f"未找到PDF連結: {name}")

            # 抓取 hashtags
            try:
                hashtag_elements = self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, '//*[@id="__layout"]/div/section[2]/div/div/div[2]/div/div[1]/span[1]')
                    )
                )
                hashtag_text = hashtag_elements[0].text.strip()
                # 將單個hashtag字符串轉換為列表
                session_data["hashtags"] = [hashtag_text] if hashtag_text else []
            except TimeoutException:
                session_data["hashtags"] = []
                print(f"未找到標籤: {name}")

            print(f"✅ 成功爬取: {name}")
            return session_data

        except TimeoutException:
            print(f"❌ 超時: {url}")
            return None
        except WebDriverException as e:
            print(f"❌ WebDriver 錯誤: {e}")
            return None
        except Exception as e:
            print(f"❌ 爬取會議詳情時發生錯誤: {e}")
            return None

    def scrape(self):
        """使用多線程爬取網頁內容"""
        # 清空數據
        self.data = []
        
        # 獲取所有會議連結
        session_links = self.get_session_links()
        
        if not session_links:
            print("未找到任何會議連結")
            return []

        total_sessions = len(session_links)
        print(f"找到 {total_sessions} 個會議連結")
        
        # 創建線程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 為每個線程創建一個獨立的WebDriver實例
            drivers = [self.setup_thread_driver() for _ in range(self.max_workers)]
            
            # 提交任務到線程池
            futures = []
            for index, session_info in enumerate(session_links):
                driver = drivers[index % self.max_workers]
                future = executor.submit(self.process_session, session_info, driver, index, total_sessions)
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
            
        print(f"\n✅ 共成功爬取 {len(self.data)} 個會議資料")
        return self.data

    def process_session(self, session_info, driver, index, total_sessions):
        """處理單個會議連結，為多線程設計"""
        try:
            url = session_info['url']
            name = session_info['name']
            date = session_info['date']
            
            print(f"正在處理第 {index + 1}/{total_sessions} 個會議: {name}")
            
            # 使用提供的driver而不是self.driver，因為每個線程有自己的driver
            wait = driver.wait
            
            # 爬取內容
            retries = 0
            max_retries = 3
            session_data = None
            
            while retries < max_retries:
                try:
                    # 開啟網頁
                    driver.get(url)
                    # 隨機等待時間，避免被封鎖
                    self.random_delay(0.5, 1.5)

                    # 初始化返回資料
                    session_data = {
                        "conference_id": str(uuid.uuid4()),
                        "seminar": self.seminar,
                        "name": name,
                        "description": "",
                        "url": url,
                        "pdf_url": "",
                        "hashtags": [],
                        "date": date
                    }

                    # 抓取 description
                    try:
                        description_elements = wait.until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "session-txt"))
                        )
                        session_data["description"] = description_elements[0].text.strip()
                    except TimeoutException:
                        session_data["description"] = ""
                        print(f"未找到描述內容: {name}")

                    # 抓取 PDF URL
                    try:
                        pdf_elements = wait.until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, '//*[@id="__layout"]/div/section[2]/div/div/div[2]/div/div[2]/div/button[1]/a')
                            )
                        )
                        session_data["pdf_url"] = pdf_elements[0].get_attribute("href")
                    except TimeoutException:
                        session_data["pdf_url"] = ""
                        print(f"未找到PDF連結: {name}")

                    # 抓取 hashtags
                    try:
                        hashtag_elements = wait.until(
                            EC.presence_of_all_elements_located(
                                (By.XPATH, '//*[@id="__layout"]/div/section[2]/div/div/div[2]/div/div[1]/span[1]')
                            )
                        )
                        hashtag_text = hashtag_elements[0].text.strip()
                        # 將單個hashtag字符串轉換為列表
                        session_data["hashtags"] = [hashtag_text] if hashtag_text else []
                    except TimeoutException:
                        session_data["hashtags"] = []
                        print(f"未找到標籤: {name}")

                    break  # 成功爬取，跳出循環
                    
                except TimeoutException:
                    retries += 1
                    print(f"超時錯誤，重試 {retries}/{max_retries}: {url}")
                    self.random_delay(1, 2)
                except WebDriverException as e:
                    retries += 1
                    print(f"WebDriver 錯誤，重試 {retries}/{max_retries}: {e}")
                    self.random_delay(1, 2)
                except Exception as e:
                    retries += 1
                    print(f"爬取失敗，重試 {retries}/{max_retries}: {e}")
                    self.random_delay(1, 2)
                    
            if retries == max_retries:
                print(f"❌ 已達最大重試次數，跳過: {name}")
                return None

            # 使用線程鎖確保數據安全
            if session_data:
                with self.data_lock:
                    self.data.append(session_data)
                print(f"✅ 成功爬取: {name}")
                
            return session_data

        except Exception as e:
            print(f"處理會議連結時出錯: {e}")
            return None

    def scrape_single_thread(self):
        """單線程版本的爬蟲，作為備選方案"""
        self.data = []
        
        # 獲取所有會議連結
        session_links = self.get_session_links()
        
        if not session_links:
            print("未找到任何會議連結")
            return []

        total_sessions = len(session_links)
        print(f"找到 {total_sessions} 個會議連結")
        
        # 逐個爬取會議詳情
        for idx, session_info in enumerate(session_links):
            print(f"\n處理第 {idx + 1}/{total_sessions} 個會議...")
            
            session_data = self.scrape_session_detail(session_info)
            if session_data:
                self.data.append(session_data)
                
            # 在每個請求之間添加隨機延遲
            self.random_delay(1, 3)
            
        print(f"\n✅ 共成功爬取 {len(self.data)} 個會議資料")
        return self.data


def run_devopsdays_taipei_scraper(headless=True, wait_time=10, use_bigquery=False, use_multithreading=True):
    """
    執行 DevOpsDays Taipei 爬蟲的入口函數

    Args:
        headless (bool): 是否使用無頭模式
        wait_time (int): 等待時間
        use_bigquery (bool): 是否上傳到 BigQuery
        use_multithreading (bool): 是否使用多線程

    Returns:
        dict: 包含爬取結果的字典
    """
    try:
        scraper = DevOpsDaysTaipeiScraper(
            headless=headless,
            wait_time=wait_time,
            use_bigquery=use_bigquery
        )

        # 根據參數選擇使用多線程或單線程
        if use_multithreading:
            print("使用多線程模式爬取...")
            # 執行爬蟲，返回文件路徑
            file_path = scraper.run()
        else:
            print("使用單線程模式爬取...")
            # 使用單線程版本
            scraper.scrape_single_thread()
            file_path = scraper.save_to_file()

        # 獲取爬取的數據
        scraped_data = getattr(scraper, 'data', [])

        return {
            "status": "success",
            "message": "DevOpsDays Taipei 爬蟲執行完成",
            "data": scraped_data,
            "file_path": file_path
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"DevOpsDays Taipei 爬蟲執行失敗: {str(e)}",
            "data": [],
            "file_path": None
        }


if __name__ == "__main__":
    # 直接運行爬蟲
    result = run_devopsdays_taipei_scraper(headless=True, wait_time=10, use_multithreading=True)
    
    if result["status"] == "success":
        print("\n🎉 爬蟲執行成功！")
        print(f"📁 文件路徑: {result['file_path']}")
        print(f"📊 共爬取 {len(result['data'])} 筆資料")
    else:
        print(f"\n❌ 爬蟲執行失敗: {result['message']}")
