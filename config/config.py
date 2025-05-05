import os
from pathlib import Path
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

# 專案根目錄
PROJECT_ROOT = Path(__file__).parent.parent

# API 配置
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MAX_REQUESTS_PER_MINUTE = int(os.environ.get("MAX_REQUESTS_PER_MINUTE", "15"))
REQUEST_INTERVAL = float(os.environ.get("REQUEST_INTERVAL", "4"))
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", "10"))

# 檔案路徑
DEFAULT_INPUT_DIR = os.environ.get("DEFAULT_INPUT_DIR", os.path.join(PROJECT_ROOT, "data/test"))
DEFAULT_OUTPUT_DIR = os.environ.get("DEFAULT_OUTPUT_DIR", os.path.join(PROJECT_ROOT, "output/summaries"))
SUPPORTED_FILE_EXTENSIONS = ['.txt', '.md', '.text']

# 處理配置
DEFAULT_OUTPUT_FORMAT = os.environ.get("DEFAULT_OUTPUT_FORMAT", "md")
DEFAULT_WORKERS = int(os.environ.get("DEFAULT_WORKERS", "4"))
MAX_TRANSCRIPT_LENGTH = int(os.environ.get("MAX_TRANSCRIPT_LENGTH", "30000"))