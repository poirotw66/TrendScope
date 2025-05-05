#!/usr/bin/env python3
"""
批量會議逐字稿總結工具 - 處理整個資料夾的逐字稿 (多線程版本)
"""

import os
import argparse
import time
from pathlib import Path
import concurrent.futures
import threading
from datetime import datetime, timedelta
import logging
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 從環境變數或預設值載入配置
def get_env(key, default):
    """從環境變數獲取配置，若不存在則使用預設值"""
    return os.environ.get(key, default)

# 專案根目錄
PROJECT_ROOT = Path(__file__).parent

# 常量配置
MAX_REQUESTS_PER_MINUTE = int(get_env("MAX_REQUESTS_PER_MINUTE", "15"))  # Gemini API 限制: 15 RPM
DEFAULT_INPUT_DIR = get_env("DEFAULT_INPUT_DIR", str(PROJECT_ROOT / "data/test"))
DEFAULT_OUTPUT_DIR = get_env("DEFAULT_OUTPUT_DIR", str(PROJECT_ROOT / "GTC_summary"))
DEFAULT_OUTPUT_FORMAT = get_env("DEFAULT_OUTPUT_FORMAT", "md")
DEFAULT_WORKERS = int(get_env("DEFAULT_WORKERS", "4"))
SUPPORTED_FILE_EXTENSIONS = ['.txt', '.md', '.text']
REQUEST_INTERVAL = float(get_env("REQUEST_INTERVAL", "4"))  # 每個請求間隔秒數，對應 15RPM
MAX_RETRIES = int(get_env("MAX_RETRIES", "3"))
RETRY_DELAY = int(get_env("RETRY_DELAY", "10"))  # 重試間隔秒數

# 設定日誌
class ThreadSafeLogger:
    """線程安全的日誌類"""
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
            log_dir = PROJECT_ROOT / "logs"
            log_dir.mkdir(exist_ok=True)
            log_file = log_dir / f"batch_process_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def info(self, message):
        """記錄資訊級別日誌"""
        with self.lock:
            self.logger.info(message)
    
    def error(self, message):
        """記錄錯誤級別日誌"""
        with self.lock:
            self.logger.error(message)
    
    def warning(self, message):
        """記錄警告級別日誌"""
        with self.lock:
            self.logger.warning(message)

# 初始化日誌
logger = ThreadSafeLogger()

# API 配額管理
class ApiQuotaManager:
    """API 配額管理器，確保不超過 API 請求限制"""
    def __init__(self, max_requests_per_minute):
        self.max_requests_per_minute = max_requests_per_minute
        self.api_requests = []
        self.api_counter_lock = threading.Lock()
    
    def wait_for_quota(self):
        """等待 API 配額可用，確保每分鐘不超過限制"""
        current_time = datetime.now()
        with self.api_counter_lock:
            one_minute_ago = current_time - timedelta(minutes=1)
            self.api_requests[:] = [req for req in self.api_requests if req >= one_minute_ago]

            if len(self.api_requests) >= self.max_requests_per_minute:
                wait_time = (self.api_requests[0] + timedelta(minutes=1) - current_time).total_seconds()
                logger.info(f"API 請求達到限制，等待 {wait_time:.2f} 秒...")
                time.sleep(wait_time + 0.5)  # 額外等待 0.5 秒作為緩衝
                return self.wait_for_quota()
            
            self.api_requests.append(current_time)
            return True

# 檔案處理工具
class FileUtils:
    """檔案讀寫工具類"""
    @staticmethod
    def read_transcript(file_path):
        """讀取逐字稿文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"讀取文件 {file_path.name} 時出錯: {e}")
            return None
    
    @staticmethod
    def write_file(content, file_path):
        """寫入檔案"""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"檔案已保存: {file_path}")
            return True
        except Exception as e:
            logger.error(f"寫入檔案 {file_path} 時出錯: {e}")
            return False
    
    @staticmethod
    def get_files_by_extensions(directory, extensions):
        """取得指定目錄中符合副檔名的所有檔案"""
        files = []
        for ext in extensions:
            files.extend(Path(directory).glob(f'*{ext}'))
        return files

# 重試裝飾器
def retry_on_exception(max_retries=3, wait_seconds=5):
    """裝飾器：遇到例外時自動重試"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.error(f"錯誤：{e}，第 {attempt} 次重試...")
                    if attempt < max_retries:
                        time.sleep(wait_seconds * attempt)
                    else:
                        logger.error("重試失敗，放棄該任務。")
                        return None
        return wrapper
    return decorator

# 摘要處理類
class TranscriptProcessor:
    """逐字稿處理器，負責摘要生成與保存"""
    def __init__(self, output_dir):
        from src.transcript_summarizer import TranscriptSummarizer
        self.summarizer = TranscriptSummarizer()
        self.output_dir = output_dir
        self.api_quota_manager = ApiQuotaManager(MAX_REQUESTS_PER_MINUTE)
    
    def save_summary(self, summary, output_path, output_format, file_path):
        """保存總結到指定格式的文件"""
        try:
            FileUtils.write_file(summary["summary"], output_path)
            self.save_html_summary(summary, file_path)
        except Exception as e:
            logger.error(f"保存總結 {output_path} 時出錯: {e}")
            return False
        return True
    
    def save_html_summary(self, summary, file_path):
        """保存 HTML 格式的總結"""
        html_dir = os.path.join(self.output_dir, "session")
        os.makedirs(html_dir, exist_ok=True)
        html_output_path = os.path.join(html_dir, file_path.stem + ".html")
        meeting_title = file_path.stem.replace("_", " ").title()
        self.summarizer.save_summary_html(summary, html_output_path, meeting_title)
        logger.info(f"HTML格式總結已保存到: {html_output_path}")
    
    @retry_on_exception(max_retries=MAX_RETRIES, wait_seconds=RETRY_DELAY)
    def process_file(self, file_info):
        """處理單個逐字稿文件（自動重試與API限速）"""
        file_path, output_format, total_files, file_index = file_info
        logger.info(f"處理 ({file_index + 1}/{total_files}): {file_path.name}")

        transcript_text = FileUtils.read_transcript(file_path)
        if not transcript_text:
            return False

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                # 等待 API 配額
                self.api_quota_manager.wait_for_quota()
                
                # 從檔名提取會議標題（去除前4個字元和後4個字元，如 "GTC_會議名稱.txt"）
                meeting_title = file_path.name
                if len(meeting_title) > 8:  # 確保檔名足夠長
                    meeting_title = meeting_title[4:-4]
                
                # 生成摘要
                summary = self.summarizer.summarize(transcript_text, meeting_title)
                if not summary or summary.get("status") == "error":
                    raise Exception(summary.get("error_message", "未知錯誤"))
                break
            except Exception as e:
                logger.error(f"生成總結時出錯 (嘗試第{attempt}次): {e}")
                if attempt < MAX_RETRIES:
                    logger.info(f"{RETRY_DELAY}秒後重試...")
                    time.sleep(RETRY_DELAY)
                else:
                    logger.error(f"{file_path.name} 已達最大重試次數，跳過。")
                    return False
            finally:
                time.sleep(REQUEST_INTERVAL)  # 每次API請求後都sleep，確保不超速

        # 保存摘要
        output_filename = file_path.stem + f".{output_format}"
        format_dir = os.path.join(self.output_dir, output_format)
        os.makedirs(format_dir, exist_ok=True)
        output_path = os.path.join(format_dir, output_filename)
        return self.save_summary(summary, output_path, output_format, file_path)

# 批量處理類
class BatchProcessor:
    """批量處理器，負責多線程處理多個文件"""
    def __init__(self, input_dir, output_dir, output_format, max_workers):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.output_format = output_format
        self.max_workers = max_workers
        self.processor = TranscriptProcessor(output_dir)
    
    def display_progress(self, completed, failed, total_files, start_time):
        """顯示進度"""
        elapsed = time.time() - start_time
        progress = (completed + failed) / total_files * 100
        logger.info(f"進度: {progress:.1f}% ({completed + failed}/{total_files}), "
                   f"已完成: {completed}, 失敗: {failed}, 已用時間: {elapsed:.1f}秒")
    
    def process(self):
        """使用多線程處理指定目錄中的所有逐字稿文件"""
        os.makedirs(self.output_dir, exist_ok=True)
        transcript_files = FileUtils.get_files_by_extensions(self.input_dir, SUPPORTED_FILE_EXTENSIONS)

        if not transcript_files:
            logger.warning(f"在 {self.input_dir} 中未找到任何文本文件")
            return

        total_files = len(transcript_files)
        # 根據 API 限制調整線程數
        max_workers = min(self.max_workers, MAX_REQUESTS_PER_MINUTE // 4) or 1
        logger.info(f"找到 {total_files} 個逐字稿文件，將使用 {max_workers} 個線程並行處理")

        tasks = [(file_path, self.output_format, total_files, i) 
                 for i, file_path in enumerate(transcript_files)]

        start_time = time.time()
        completed, failed = 0, 0

        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(self.processor.process_file, task): task[0].name for task in tasks}
                for future in concurrent.futures.as_completed(futures):
                    if future.result():
                        completed += 1
                    else:
                        failed += 1
                    self.display_progress(completed, failed, total_files, start_time)
        except KeyboardInterrupt:
            logger.warning("\n程序被用戶中斷。正在等待當前任務完成...")
        except Exception as e:
            logger.error(f"執行過程中發生錯誤: {e}")

        logger.info(f"批量處理完成。成功: {completed}, 失敗: {failed}")
        logger.info(f"總耗時: {time.time() - start_time:.2f} 秒")
        logger.info(f"總結文件保存在: {self.output_dir}")

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description="批量處理會議逐字稿並生成總結 (多線程版本)")
    parser.add_argument("-i", "--input", default=DEFAULT_INPUT_DIR, help="輸入目錄")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR, help="輸出目錄")
    parser.add_argument("--format", choices=["json", "txt", "md"], default=DEFAULT_OUTPUT_FORMAT, help="輸出格式")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="最大工作線程數")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        logger.error(f"錯誤: 輸入目錄 {args.input} 不存在")
        return 1

    processor = BatchProcessor(args.input, args.output, args.format, args.workers)
    processor.process()
    return 0

if __name__ == "__main__":
    exit(main())
