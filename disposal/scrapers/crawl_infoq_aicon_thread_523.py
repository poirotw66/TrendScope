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
    chrome_options.add_argument('--headless')  # Add headless mode for better performance
    
    # Add user agent to appear more like a regular browser
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    return webdriver.Chrome(options=chrome_options)

def random_delay(min_seconds=0.5, max_seconds=1.5):
    """Add a random delay between actions to mimic human behavior"""
    time.sleep(random.uniform(min_seconds, max_seconds))

# Thread-safe data writing
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
            
            # Try to find PDF link element
            pdf_url = None
            try:
                pdf_element = driver.find_element(By.XPATH, '//a[contains(@class, "item ppt") or contains(@class, "icon-ppt")]')
                if pdf_element:
                    pdf_url = pdf_element.get_attribute("href")
                    print(f"Found PDF link: {pdf_url}")
            except Exception as e:
                print(f"PDF link not found or error occurred during search: {e}")
                
            return content_text, pdf_url
        except Exception as e:
            retries += 1
            print(f"Scraping failed, retrying attempt {retries}: {e}")
            random_delay(1, 2)  # Slight delay before retry
    
    # All retries failed
    return "Scraping failed, maximum retry attempts reached", None

def process_link(link_info, driver, seminar, index, total_links, output_file):
    try:
        text, href = link_info  # Use passed link information instead of getting directly from link object
        print(f"Processing item {index + 1}/{total_links}")
        description, pdf_url = scrape_content(driver, href)
        print(f"Item {index + 1}:")
        print(f"Text content: {text}")
        print(f"Link: {href}\n")
        
        with data_lock:
            data.append({
                "seminar": seminar,
                "name": text,
                "description": description,
                "url": href,
                "pdf_url": pdf_url if pdf_url else ""
            })
            
            # Save progress every 10 links processed
            if len(data) % 10 == 0:
                df = pd.DataFrame(data)
                df.to_csv(f"{output_file}_temp", index=False, encoding="utf-8-sig")
        return True
    except Exception as e:
        print(f"Error processing link: {e}")
        return False

def scrape_track(url, output_file="links_with_empty_class.txt", seminar="default", max_workers=5):
    main_driver = setup_driver()
    wait = WebDriverWait(main_driver, 10)
    global data
    data = []
    
    try:
        print(f"Starting to scrape webpage: {url}")
        main_driver.get(url)
        links = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "title")]/a'))
        )
        
        # Pre-fetch all link information to avoid sharing WebElement objects between threads
        link_info_list = []
        with open('output.txt', "w", encoding="utf-8") as file:
            for index, link in enumerate(links):
                text = link.text.strip()
                href = link.get_attribute("href")
                link_info_list.append((text, href))
                file.write(f"Item {index + 1}:\nText content: {text}\nLink: {href}\n\n")
        
        total_links = len(link_info_list)
        print(f"Found {total_links} presentation topics")
        
        # Create thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create independent WebDriver instance for each thread
            drivers = [setup_driver() for _ in range(max_workers)]
            
            # Submit tasks to thread pool
            futures = []
            for index, link_info in enumerate(link_info_list):
                driver = drivers[index % max_workers]
                future = executor.submit(process_link, link_info, driver, seminar, index, total_links, output_file)
                futures.append(future)
                
                # Brief delay after submitting each batch of tasks to avoid too many simultaneous requests
                if (index + 1) % max_workers == 0:
                    random_delay(0.5, 1)
            
            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f"Task execution error: {e}")
            
            # Close all WebDriver instances
            for driver in drivers:
                driver.quit()
        
        # Save results
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        
    finally:
        main_driver.quit()

if __name__ == "__main__":
    start_time = time.time()
    url = "https://aicon.infoq.cn/2025/shanghai/track"
    seminar = "20250523_Shanghai_AICon"
    output_file = f'{seminar}.csv'
    
    # Set the number of threads for parallel processing, adjust based on your computer's performance
    max_workers = 5
    
    scrape_track(url, output_file, seminar, max_workers)
    
    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time} s.")