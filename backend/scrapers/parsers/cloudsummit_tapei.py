"""
CloudSummit Taipei 會議爬蟲
用於爬取 CloudSummit (IT Home) 會議議程與摘要
"""
import urllib.parse
import time
import random
import re
import uuid
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from backend.scrapers.base_scraper import BaseScraper


class CloudSummitTaipeiScraper(BaseScraper):
    """
    CloudSummit Taipei 會議爬蟲類
    """
    def __init__(self, headless=True, wait_time=10, use_bigquery=False, bq_credentials=None, bq_project_id=None):
        super().__init__(
            headless=headless,
            wait_time=wait_time,
            use_bigquery=use_bigquery,
            bq_credentials=bq_credentials,
            bq_project_id=bq_project_id
        )
        self.base_url = "https://cloudsummit.ithome.com.tw/2025/agenda"
        self.seminar = "202507 CloudSummit Taipei"
        self.data = []

    def get_scraper_name(self):
        return "202507 CloudSummit Taipei"

    def get_filename_prefix(self):
        return "20250702_Taipei_CloudSummit"

    def decode_url(self, url):
        """將 URL 中的 Unicode 編碼斜線和其他特殊字符解碼為正常的 URL"""
        # 替換 Unicode 斜線
        url = url.replace(r"\u002F", "/").replace("https:", "https://")

        # 解析查詢參數
        try:
            parsed_url = urllib.parse.urlparse(url)
            params = urllib.parse.parse_qs(parsed_url.query)
            decoded_link = urllib.parse.unquote(params['l'][0])
            return decoded_link
        except Exception as e:
            print(f"解碼 URL 失敗: {e}")
            return url

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
            
            # 嘗試從多個索引範圍獲取連結
            for idx in range(2, 62):
                try:
                    # 執行爬蟲
                    seminar_elements = self.wait.until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, f'//*[@id="__layout"]/div/div[1]/div[2]/div/div[2]/div/div[{idx}]/h4/a')
                        )
                    )
                    
                    # 一抓下來是個 list
                    elem = seminar_elements[0]
                    # 抓取標題和連結
                    name = elem.text.strip()
                    link = elem.get_attribute("href")
                    
                    if name and link:
                        print(f"找到會議: {name}")
                        session_links.append({
                            "name": name,
                            "href": link
                        })
                        
                except TimeoutException:
                    print(f"索引 {idx} 未找到元素，跳過...")
                    continue
                except Exception as e:
                    print(f"處理索引 {idx} 時發生錯誤: {e}")
                    continue
                    
            print(f"✅ 共找到 {len(session_links)} 個會議連結")
            return session_links
            
        except Exception as e:
            print(f"獲取會議連結時發生錯誤: {e}")
            return []

    def scrape_session_detail(self, session_info):
        """爬取單個會議的詳細資訊"""
        url = session_info['href']
        name = session_info['name']
        
        # 跳過空白議程
        if name == "此時段目前未安排議程":
            return None
            
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
                "hashtags": []
            }

            # 嘗試抓取 PDF 下載連結
            try:
                pdf_link_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/script[1]'))
                )
                # 抓到 script 標籤中的內容
                script_text = pdf_link_element.get_attribute("innerText")
                # 使用正則表達式提取 PDF 連結
                pdf_url_match = re.search(r'https:[^"]+?\.pdf', script_text)

                # 如果找到 PDF 連結，則解碼
                if pdf_url_match:
                    pdf_url = pdf_url_match.group(0)
                    session_data["pdf_url"] = self.decode_url(pdf_url)
                else:
                    session_data["pdf_url"] = ""
                    
            except Exception as e:
                print(f"抓取 PDF 連結失敗: {e}")
                session_data["pdf_url"] = ""

            # 抓取 description
            try:
                description_elements = self.wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/section/div/div/div[2]/div[1]/div/div'))
                )
                session_data["description"] = description_elements[0].text.strip()
            except Exception as e:
                print(f"抓取描述失敗: {e}")
                session_data["description"] = ""

            # 抓取 hashtags
            try:
                ul_element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__layout"]/div/div[1]/section/div/div/div[3]/ul'))
                )
                # 抓所有 li
                li_elements = ul_element.find_elements(By.TAG_NAME, "li")
                # 過濾出 class 為 "fas fa-hashtag" 的 i 所在 li，並取 li 的文字
                hashtags = []
                for li in li_elements:
                    try:
                        icon = li.find_element(By.TAG_NAME, "i")
                        if icon.get_attribute("class") == "fas fa-hashtag":
                            hashtags.append(li.text.strip())
                    except:
                        pass  # 忽略沒有 i 的 li
                        
                session_data["hashtags"] = hashtags
            except Exception as e:
                print(f"抓取標籤失敗: {e}")
                session_data["hashtags"] = []

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
        """執行爬蟲主要邏輯"""
        self.data = []
        
        # 獲取所有會議連結
        session_links = self.get_session_links()
        
        if not session_links:
            print("未找到任何會議連結")
            return []
            
        # 逐個爬取會議詳情
        for idx, session_info in enumerate(session_links):
            print(f"\n處理第 {idx + 1}/{len(session_links)} 個會議...")
            
            session_data = self.scrape_session_detail(session_info)
            if session_data:
                self.data.append(session_data)
                
            # 在每個請求之間添加隨機延遲
            self.random_delay(1, 3)
            
        print(f"\n✅ 共成功爬取 {len(self.data)} 個會議資料")
        return self.data


def run_cloudsummit_taipei_scraper(headless=True, wait_time=10, use_bigquery=False):
    """
    執行 CloudSummit Taipei 爬蟲的入口函數

    Args:
        headless (bool): 是否使用無頭模式
        wait_time (int): 等待時間
        use_bigquery (bool): 是否上傳到 BigQuery

    Returns:
        dict: 包含爬取結果的字典
    """
    try:
        scraper = CloudSummitTaipeiScraper(
            headless=headless,
            wait_time=wait_time,
            use_bigquery=use_bigquery
        )

        # 執行爬蟲，返回文件路徑
        file_path = scraper.run()

        # 獲取爬取的數據
        scraped_data = getattr(scraper, 'data', [])

        return {
            "status": "success",
            "message": "CloudSummit Taipei 爬蟲執行完成",
            "data": scraped_data,
            "file_path": file_path
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"CloudSummit Taipei 爬蟲執行失敗: {str(e)}",
            "data": [],
            "file_path": None
        }


if __name__ == "__main__":
    # 直接運行爬蟲
    result = run_cloudsummit_taipei_scraper(headless=True, wait_time=10)
    
    if result["status"] == "success":
        print(f"\n🎉 爬蟲執行成功！")
        print(f"📁 文件路徑: {result['file_path']}")
        print(f"📊 共爬取 {len(result['data'])} 筆資料")
    else:
        print(f"\n❌ 爬蟲執行失敗: {result['message']}")