"""
Selenium WebDriver 設置工具
提供 Chrome WebDriver 的設置功能，用於爬蟲操作
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

def setup_driver(headless=True):
    """
    設置並返回 Chrome WebDriver
    
    Args:
        headless (bool): 是否啟用無頭模式，默認為 True
        
    Returns:
        webdriver.Chrome: 設置好的 Chrome WebDriver 實例
    """
    chrome_options = Options()
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-logging')
    
    if headless:
        chrome_options.add_argument('--headless')
    
    # 模擬真實使用者 - 使用隨機用戶代理
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ]
    
    chrome_options.add_argument(f'--user-agent={random.choice(user_agents)}')
    
    return webdriver.Chrome(options=chrome_options)
