"""
AICon InfoQ 會議爬蟲
用於爬取 AICon (InfoQ) 會議議程與摘要
"""
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapers.base_scraper import BaseScraper
import uuid

class AiconInfoqScraper(BaseScraper):
    """
    AICon InfoQ 會議爬蟲類
    """
    def __init__(self, headless=False, wait_time=10, use_bigquery=False, bq_credentials=None, bq_project_id=None):
        super().__init__(
            headless=headless,
            wait_time=wait_time,
            use_bigquery=use_bigquery,
            bq_credentials=bq_credentials,
            bq_project_id=bq_project_id
        )
        self.url = "https://aicon.infoq.cn/2025/shanghai/track"
        self.seminar = "202503 AICon Shanghai"

    def get_scraper_name(self):
        return "202503 AICon Shanghai"

    def get_filename_prefix(self):
        return self.seminar

    def scrape(self):
        self.driver.get(self.url)
        print(f"開始爬取網頁: {self.url}")
        time.sleep(3)
        data = []
        try:
            links = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "title")]/a'))
            )
            link_info_list = []
            for link in links:
                text = link.text.strip()
                href = link.get_attribute("href")
                link_info_list.append((text, href))
            print(f"找到 {len(link_info_list)} 個演講題目")
            for idx, (text, href) in enumerate(link_info_list, 1):
                print(f"正在處理第 {idx}/{len(link_info_list)} 個項目: {text}")
                abstract, pdf_url = self.scrape_content(href)
                data.append({
                    "conference_id": str(uuid.uuid4()),
                    "seminar": self.seminar,
                    "name": text,
                    "description": abstract,
                    "url": href,
                    "pdf_url": pdf_url or ""
                })
        except Exception as e:
            print(f"爬取主頁時發生錯誤: {e}")
        return data

    def scrape_content(self, url, max_retries=3):
        retries = 0
        while retries < max_retries:
            try:
                self.driver.get(url)
                content_element = self.wait.until(
                    EC.visibility_of_element_located((By.XPATH, '//div[@data-v-2c704944][@class="content"]'))
                )
                content_text = content_element.text.strip()
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
                time.sleep(1)
        return "爬取失敗，已達最大重試次數", None
