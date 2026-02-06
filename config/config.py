"""
設定模組 - 由 config.settings 集中提供，此檔保留向後相容匯出
請改為使用: from config.settings import settings
"""
from config.settings import get_settings

_settings = get_settings()

# 向後相容：舊程式可繼續 from config.config import PROJECT_ROOT, GEMINI_API_KEY 等
PROJECT_ROOT = _settings.PROJECT_ROOT
GEMINI_API_KEY = _settings.GEMINI_API_KEY
GEMINI_MODEL_NAME = _settings.GEMINI_MODEL_NAME
MAX_REQUESTS_PER_MINUTE = _settings.MAX_REQUESTS_PER_MINUTE
REQUEST_INTERVAL = _settings.REQUEST_INTERVAL
MAX_RETRIES = _settings.MAX_RETRIES
RETRY_DELAY = _settings.RETRY_DELAY
DEFAULT_INPUT_DIR = _settings.DEFAULT_INPUT_DIR
DEFAULT_OUTPUT_DIR = _settings.DEFAULT_OUTPUT_DIR
SUPPORTED_FILE_EXTENSIONS = _settings.SUPPORTED_FILE_EXTENSIONS
DEFAULT_OUTPUT_FORMAT = _settings.DEFAULT_OUTPUT_FORMAT
DEFAULT_WORKERS = _settings.DEFAULT_WORKERS
MAX_TRANSCRIPT_LENGTH = _settings.MAX_TRANSCRIPT_LENGTH
OUTPUT_MD_DIR = _settings.OUTPUT_MD_DIR
OUTPUT_HTML_DIR = _settings.OUTPUT_HTML_DIR
SESSION_HTML_DIR = _settings.SESSION_HTML_DIR
INPUT_CSV_PATH = _settings.INPUT_CSV_PATH
TOP_N_MEETINGS = _settings.TOP_N_MEETINGS
BATCH_MD_TO_HTML_INDEX = _settings.BATCH_MD_TO_HTML_INDEX

# 新增的配置項（向後相容）
DATA_DIR = _settings.data_dir
SHEET_DIR = _settings.sheet_dir
BASE_OUTPUT_DIR = _settings.base_output_dir
MEETING_EXCEL_FILENAME = _settings.meeting_excel_filename
MEETING_COL = _settings.meeting_col
URL_COL = _settings.url_col
CONTEXT_CSV_PATH = _settings.context_csv_path
CONTEXT_DIAGRAM_OUTPUT_PATH = _settings.context_diagram_output_path
