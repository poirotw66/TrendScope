from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import random
from selenium.common.exceptions import TimeoutException, WebDriverException
import concurrent.futures
import threading

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--headless')  # 添加无头模式，提高效率
    
    # Add user agent to appear more like a regular browser
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    return webdriver.Chrome(options=chrome_options)

def random_delay(min_seconds=0.5, max_seconds=1.5):
    """Add a random delay between actions to mimic human behavior"""
    time.sleep(random.uniform(min_seconds, max_seconds))

# 线程安全的数据写入
data_lock = threading.Lock()
data = []

def scrape_content(driver, url, max_retries=3):
    wait = WebDriverWait(driver, 10)
    retries = 0
    while retries < max_retries:
        try:
            driver.get(url)
            content_element = wait.until(
                EC.visibility_of_element_located((By.XPATH, '//div[@data-v-2c704944][@class="content"]'))
            )
            content_text = content_element.text.strip()
            
            # 尝试查找PDF链接元素
            pdf_url = None
            try:
                pdf_element = driver.find_element(By.XPATH, '//a[contains(@class, "item ppt") or contains(@class, "icon-ppt")]')
                if pdf_element:
                    pdf_url = pdf_element.get_attribute("href")
                    print(f"找到PDF链接: {pdf_url}")
            except Exception as e:
                print(f"未找到PDF链接或查找过程中出错: {e}")
                
            return content_text, pdf_url
        except Exception as e:
            retries += 1
            print(f"爬取失败，正在进行第 {retries} 次重试: {e}")
            random_delay(1, 2)  # 重试前稍微延迟
    
    # 所有重试都失败
    return "爬取失败，已达到最大重试次数", None

def process_link(link_info, driver, seminar, index, total_links, output_file):
    try:
        text, href = link_info  # 使用传入的链接信息，而不是直接从link对象获取
        print(f"正在处理第 {index + 1}/{total_links} 个项目")
        abstract, pdf_url = scrape_content(driver, href)
        print(f"项目 {index + 1}:")
        print(f"文字内容: {text}")
        print(f"连结: {href}\n")
        
        with data_lock:
            data.append({
                "Seminar": seminar,
                "Topic": text,
                "Abstract": abstract,
                "url": href,
                "pdf_url": pdf_url if pdf_url else ""
            })
            
            # 每处理10个链接保存一次进度
            if len(data) % 10 == 0:
                df = pd.DataFrame(data)
                df.to_csv(f"{output_file}_temp", index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        print(f"处理链接时出错: {e}")
        return False

def scrape_track(url, output_file="links_with_empty_class.txt", seminar="default", max_workers=5):
    main_driver = setup_driver()
    wait = WebDriverWait(main_driver, 10)
    global data
    data = []
    
    try:
        print(f"開始爬取網頁: {url}")
        main_driver.get(url)
        links = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "title")]/a'))
        )
        
        # 预先获取所有链接信息，避免线程间共享WebElement对象
        link_info_list = []
        with open('output.txt', "w", encoding="utf-8") as file:
            for index, link in enumerate(links):
                text = link.text.strip()
                href = link.get_attribute("href")
                link_info_list.append((text, href))
                file.write(f"項目 {index + 1}:\n文字內容: {text}\n連結: {href}\n\n")
        
        total_links = len(link_info_list)
        print(f"找到 {total_links} 個演講題目")
        
        # 创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 为每个线程创建一个独立的WebDriver实例
            drivers = [setup_driver() for _ in range(max_workers)]
            
            # 提交任务到线程池
            futures = []
            for index, link_info in enumerate(link_info_list):
                driver = drivers[index % max_workers]
                future = executor.submit(process_link, link_info, driver, seminar, index, total_links, output_file)
                futures.append(future)
                
                # 每提交一批任务后短暂延迟，避免同时发起太多请求
                if (index + 1) % max_workers == 0:
                    random_delay(0.5, 1)
            
            # 等待所有任务完成
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"任务执行出错: {e}")
            
            # 关闭所有WebDriver实例
            for driver in drivers:
                driver.quit()
        
        # 保存结果
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        
    finally:
        main_driver.quit()

if __name__ == "__main__":
    start_time = time.time()
    url = "https://aicon.infoq.cn/2025/shanghai/track"
    seminar = "20250523_上海_AICon"
    output_file = f'{seminar}.csv'
    
    # 设置并行处理的线程数，根据您的计算机性能调整
    max_workers = 5
    
    scrape_track(url, output_file, seminar, max_workers)
    
    end_time = time.time()
    print(f"耗費時間：{end_time - start_time} s.")