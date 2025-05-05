import logging
import threading
from datetime import datetime

# 線程安全的日誌設定
class ThreadSafeLogger:
    def __init__(self, name="google_next", level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.lock = threading.Lock()
        
        # 避免重複設定
        if not self.logger.handlers:
            # 控制台輸出
            console = logging.StreamHandler()
            console.setLevel(level)
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console.setFormatter(formatter)
            self.logger.addHandler(console)
            
            # 檔案輸出
            log_file = f"google_next_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message):
        with self.lock:
            self.logger.info(message)
    
    def error(self, message):
        with self.lock:
            self.logger.error(message)
    
    def warning(self, message):
        with self.lock:
            self.logger.warning(message)
    
    def debug(self, message):
        with self.lock:
            self.logger.debug(message)

# 全域日誌實例
logger = ThreadSafeLogger()