# 爬取consensus列表的會議資訊
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
print("\n開始爬取 Consensus 研討會")
url = "https://consensus-hongkong2025.coindesk.com/agenda/"
driver.get(url)
wait = WebDriverWait(driver, 30)
time.sleep(5)  # 先等待頁面基本加載

# 實現頁面滾動到底部的功能
# 改進頁面滾動算法以爬取完整內容
def scroll_to_bottom(driver, scroll_pause_time=1.0, max_attempts=10):
    print("開始下拉頁面...")
    # 獲取初始頁面高度
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    # 記錄相同高度的次數
    same_height_count = 0
    total_scrolls = 0
    
    while same_height_count < 3 and total_scrolls < max_attempts:  # 如果連續3次高度相同或達到最大嘗試次數，則認為已到底部
        # 滾動到頁面底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        total_scrolls += 1
        
        # 等待頁面加載
        time.sleep(scroll_pause_time)
        
        # 計算新的滾動高度並與上一個滾動高度進行比較
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            same_height_count += 1
            print(f"頁面高度未變化 ({same_height_count}/3)")
            
        else:
            same_height_count = 0  # 重置計數器
            last_height = new_height
            print(f"繼續下拉，當前頁面高度: {new_height}")
    
    if total_scrolls >= max_attempts:
        print(f"已達到最大滾動嘗試次數 ({max_attempts})")
    else:
        print("已到達頁面底部或無法加載更多內容")
    
    # 最後再滾動一次，確保所有內容都被加載
    for i in range(3):
        # 滾動到頂部
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.5)
        # 慢慢滾動到底部
        total_height = driver.execute_script("return document.body.scrollHeight")
        for scroll_height in range(0, total_height, 1500):  # 每次滾動300像素
            driver.execute_script(f"window.scrollTo(0, {scroll_height});")
            time.sleep(0.1)
    
    print("頁面滾動完成，應已加載所有內容")

# 調用滾動函數
scroll_to_bottom(driver)

# 開始爬取數據
print("頁面已完全加載，開始抓取數據")
# time.sleep(30)
# 創建一個空的列表來存儲數據
data = []

# 找到所有會議卡片
try:
    # 等待會議卡片元素加載
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'agenda-card')))
    
    # 抓取所有會議卡片
    cards = driver.find_elements(By.CLASS_NAME, 'agenda-card')
    print(f"找到 {len(cards)} 個會議卡片")
    
    for idx, card in enumerate(cards, start=1):
        try:
            # 抓取會議名稱和連結
            title_element = card.find_element(By.CSS_SELECTOR, '.event-title')
            title = title_element.text.strip()
            link = title_element.get_attribute('href')
            
            # 抓取會議時間
            date_element = card.find_element(By.CSS_SELECTOR, '.event-date') if card.find_elements(By.CSS_SELECTOR, '.event-date') else None
            date = date_element.text.strip() if date_element else "未提供日期"
            
            time_element = card.find_element(By.CSS_SELECTOR, '.event-time') if card.find_elements(By.CSS_SELECTOR, '.event-time') else None
            time_info = time_element.text.strip() if time_element else "未提供時間"
            
            # 抓取會議地點
            venue_element = card.find_element(By.CSS_SELECTOR, '.venue-title') if card.find_elements(By.CSS_SELECTOR, '.venue-title') else None
            venue = venue_element.text.strip() if venue_element else "未提供地點"
            
            # 抓取會議描述
            description_element = card.find_element(By.CSS_SELECTOR, '.card-description-inner') if card.find_elements(By.CSS_SELECTOR, '.card-description-inner') else None
            description = description_element.text.strip() if description_element else "未提供描述"
            
            # 抓取標籤
            tags = []
            tag_elements = card.find_elements(By.CSS_SELECTOR, '.badge-tag')
            for tag_element in tag_elements:
                tags.append(tag_element.text.strip())
            
            # 抓取講者信息
            speakers = []
            speaker_elements = card.find_elements(By.CSS_SELECTOR, '.block-speaker')
            for speaker_element in speaker_elements:
                speaker_name_element = speaker_element.find_element(By.CSS_SELECTOR, '.speaker-name') if speaker_element.find_elements(By.CSS_SELECTOR, '.speaker-name') else None
                speaker_title_element = speaker_element.find_element(By.CSS_SELECTOR, '.speaker-title') if speaker_element.find_elements(By.CSS_SELECTOR, '.speaker-title') else None
                speaker_company_element = speaker_element.find_element(By.CSS_SELECTOR, '.speaker-company') if speaker_element.find_elements(By.CSS_SELECTOR, '.speaker-company') else None
                speaker_role_element = speaker_element.find_element(By.CSS_SELECTOR, '.speaker-role') if speaker_element.find_elements(By.CSS_SELECTOR, '.speaker-role') else None
                
                speaker_info = {
                    "姓名": speaker_name_element.text.strip() if speaker_name_element else "未提供姓名",
                    "職稱": speaker_title_element.text.strip() if speaker_title_element else "未提供職稱",
                    "公司": speaker_company_element.text.strip() if speaker_company_element else "未提供公司",
                    "角色": speaker_role_element.text.strip() if speaker_role_element else ""
                }
                speakers.append(speaker_info)
            
            # 將數據添加到列表中
            data.append({
                "序號": idx,
                "會議名稱": title,
                "會議連結": link,
                "日期": date,
                "時間": time_info,
                "地點": venue,
                "描述": description,
                "標籤": ", ".join(tags),
                "講者": speakers
            })
            
            print(f"{idx}. 會議名稱: {title}")
            print(f"   會議連結: {link}")
            print(f"   標籤: {', '.join(tags)}")
            
        except Exception as inner_e:
            print(f"{idx}. 抓取失敗: {str(inner_e)}")
            traceback.print_exc()
    
    # 確認是否有抓到資料
    if data:
        # 創建DataFrame
        df = pd.DataFrame(data)
        
        # 生成文件名，包含當前日期
        excel_file = f"Consensus_HK_2025_sessions_{today}.xlsx"
        
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