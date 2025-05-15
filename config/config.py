import os
from pathlib import Path
from dotenv import load_dotenv

# 載入 .env 檔案中的環境變數
load_dotenv()

# 專案根目錄
PROJECT_ROOT = Path(__file__).parent.parent

# API 配置
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL_NAME = os.environ.get("GEMINI_MODEL_NAME", "gemini-2.0-flash")
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

OUTPUT_MD_DIR = os.getenv("OUTPUT_MD_DIR", "./GTC_summary/topic_md")
OUTPUT_HTML_DIR = os.getenv("OUTPUT_HTML_DIR", "./GTC_summary/topic")
SESSION_HTML_DIR = os.getenv("SESSION_HTML_DIR", "./GTC_summary/topic/session")
INPUT_CSV_PATH = os.getenv("INPUT_CSV_PATH", "./data/sheet/GTC25.csv")
TOP_N_MEETINGS = int(os.getenv("TOP_N_MEETINGS", 5)) # 從環境變數讀取 top_n，預設為 3
BATCH_MD_TO_HTML_INDEX = int(os.getenv("BATCH_MD_TO_HTML_INDEX", 1)) # 從環境變數讀取 index，預設為 1

