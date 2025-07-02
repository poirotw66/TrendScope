# 爬取 aws summit 研討會資訊
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import os
from datetime import datetime
import random
import traceback
from urllib3.exceptions import MaxRetryError, NewConnectionError
from selenium.common.exceptions import WebDriverException, TimeoutException

# 設定 Chrome Driver 路徑（請依你的環境調整）
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-logging')
    # chrome_options.add_argument('--headless')  # 可選：無頭模式，除錯時可以關掉
    
    # 模擬真實使用者
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    return webdriver.Chrome(options=chrome_options)

# 生成今天的日期格式
today = datetime.now().strftime("%Y%m%d")
driver = setup_driver()
print("\n開始爬取 aws summit 研討會")
url = "https://summitlondon.awslivestream.com/"
driver.get(url)
wait = WebDriverWait(driver, 30)
print("登入！")
time.sleep(20)  # 先等待頁面基本加載


# 開始爬取數據
print("頁面已完全加載，開始抓取數據")
# time.sleep(30) # 根據需要調整等待時間，確保內容完全加載

# 創建一個空的列表來存儲數據
data = []

# 找到所有會議卡片
try:
    # 等待會議卡片元素加載，使用新的 class name
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-t4lfxt-card')))
    
    # 抓取所有會議卡片，使用新的 class name
    cards = driver.find_elements(By.CLASS_NAME, 'css-t4lfxt-card')
    print(f"找到 {len(cards)} 個會議卡片")
    
    for idx, card in enumerate(cards, start=1):
        try:
            # 抓取會議名稱和連結，使用新的 CSS 選擇器
            link_element = card.find_element(By.CSS_SELECTOR, '.css-1bwr4xe-tileLink')
            link = link_element.get_attribute('href')
            
            title_element = link_element.find_element(By.CSS_SELECTOR, '.css-1nsbbif-eventTitle')
            title = title_element.text.strip()
            
            # 將數據添加到列表中
            data.append({
                "序號": idx,
                "會議名稱": title,
                "會議連結": link,
                # 以下是之前 Consensus 網站的抓取邏輯，可能不適用於 AWS 網站，暫時註釋掉
                # "日期": date,
                # "時間": time_info,
                # "地點": venue,
                # "描述": description,
                # "標籤": ", ".join(tags),
                # "講者": speakers
            })
            
            print(f"{idx}. 會議名稱: {title}")
            print(f"   會議連結: {link}")
            # print(f"   標籤: {', '.join(tags)}") # 暫時註釋
            
        except Exception as inner_e:
            print(f"{idx}. 抓取失敗: {str(inner_e)}")
            traceback.print_exc()
    
    # 確認是否有抓到資料
    if data:
        # 創建DataFrame
        df = pd.DataFrame(data)
        
        # 生成文件名，包含當前日期，並更新為 AWS London
        excel_file = f"AWS_London_Summit_sessions_{today}.xlsx"
        
        # 儲存到Excel文件
        df.to_excel(excel_file, index=False)
        print(f"\n資料已成功儲存至 {excel_file}")
    else:
        print("\n未找到資料")

except Exception as e:
    print(f"抓取數據時發生錯誤: {str(e)}")
    traceback.print_exc()

finally:
    # 確保瀏覽器驅動關閉
    driver.quit()
    print("爬蟲程序已完成")