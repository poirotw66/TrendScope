"""
集中化設定 - 使用 Pydantic Settings 讀取環境變數與預設值
所有配置項統一在此管理，避免分散在多個檔案
"""
from pathlib import Path
from functools import lru_cache
from pydantic import model_validator, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


def _default_project_root() -> Path:
    """專案根目錄（config 的上一層）"""
    return Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """集中化設定，優先從環境變數與 .env 讀取"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        # 支援環境變數名稱對應（大寫、底線等）
        env_nested_delimiter="__",
    )

    # --- 專案路徑 ---
    project_root: Path = _default_project_root()

    # --- API / Gemini 配置 ---
    gemini_api_key: str = ""
    gemini_model_name: str = "gemini-2.0-flash"
    max_requests_per_minute: int = 15
    request_interval: float = 4.0
    max_retries: int = 3
    retry_delay: int = 10

    # --- 檔案路徑配置 ---
    data_dir: str = "./data"
    default_input_dir: str = ""
    sheet_dir: str = ""
    meeting_excel_filename: str = ""
    base_output_dir: str = ""
    default_output_dir: str = ""
    output_md_dir: str = ""
    output_html_dir: str = ""
    session_html_dir: str = ""
    input_csv_path: str = ""
    supported_file_extensions: List[str] = [".txt", ".md", ".text"]

    # --- 處理配置 ---
    default_output_format: str = "md"
    default_workers: int = 4
    max_transcript_length: int = 30000

    # --- 會議設定 ---
    meeting_col: str = "Meeting"
    url_col: str = "URL"

    # --- 報告生成配置 ---
    top_n_meetings: int = 5
    batch_md_to_html_index: int = 1
    context_csv_path: str = "gtc_session.csv"
    context_diagram_output_path: str = "google_IO_context_diagram.md"

    # --- Google Cloud 配置 ---
    google_application_credentials: str | None = None
    google_cloud_project: str | None = None
    google_cloud_storage_bucket: str | None = None

    # --- API 配置 ---
    api_host: str = "0.0.0.0"
    api_port: int = 8001
    api_reload: bool = True
    api_log_level: str = "info"
    api_environment: str = "development"  # development, production, testing
    
    # --- CORS 配置 ---
    cors_allow_origins: str = "*"  # 逗號分隔的來源列表，或 "*" 表示允許所有
    cors_allow_credentials: bool = True
    cors_allow_methods: str = "*"  # 逗號分隔的方法列表，或 "*" 表示允許所有
    cors_allow_headers: str = "*"  # 逗號分隔的標頭列表，或 "*" 表示允許所有
    
    # --- 錯誤處理配置 ---
    show_traceback_in_errors: bool = False  # 是否在錯誤響應中顯示堆疊追蹤

    @field_validator("supported_file_extensions", mode="before")
    @classmethod
    def parse_file_extensions(cls, v):
        """解析檔案副檔名列表（支援字串或列表）"""
        if isinstance(v, str):
            # 從字串解析，例如 ".txt,.md,.text"
            return [ext.strip() for ext in v.split(",") if ext.strip()]
        return v

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """解析 CORS 允許來源（支援字串或列表）"""
        if isinstance(v, str):
            if v == "*":
                return "*"
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @field_validator("cors_allow_methods", mode="before")
    @classmethod
    def parse_cors_methods(cls, v):
        """解析 CORS 允許方法（支援字串或列表）"""
        if isinstance(v, str):
            if v == "*":
                return "*"
            return [method.strip() for method in v.split(",") if method.strip()]
        return v

    @field_validator("cors_allow_headers", mode="before")
    @classmethod
    def parse_cors_headers(cls, v):
        """解析 CORS 允許標頭（支援字串或列表）"""
        if isinstance(v, str):
            if v == "*":
                return "*"
            return [header.strip() for header in v.split(",") if header.strip()]
        return v

    @field_validator("api_environment", mode="before")
    @classmethod
    def parse_environment(cls, v):
        """解析 API 環境"""
        if isinstance(v, str):
            env = v.lower()
            if env in ["development", "production", "testing"]:
                return env
            # 根據常見環境變數名稱推斷
            if env in ["dev", "local"]:
                return "development"
            if env in ["prod", "production"]:
                return "production"
            if env in ["test", "testing"]:
                return "testing"
        return v or "development"

    @model_validator(mode="after")
    def set_default_paths(self) -> "Settings":
        """若未設定路徑，則依 project_root 給預設值"""
        root = self.project_root

        # 設定預設目錄
        if not self.data_dir or self.data_dir == "./data":
            object.__setattr__(self, "data_dir", str(root / "data"))
        
        if not self.sheet_dir:
            object.__setattr__(self, "sheet_dir", str(root / "data" / "sheet"))

        if not self.default_input_dir:
            object.__setattr__(self, "default_input_dir", str(root / "data" / "test"))
        
        if not self.default_output_dir:
            object.__setattr__(self, "default_output_dir", str(root / "output" / "summaries"))

        if not self.base_output_dir:
            object.__setattr__(self, "base_output_dir", str(root / "googleio_summary"))

        if not self.output_md_dir:
            object.__setattr__(self, "output_md_dir", str(root / "googleio_summary" / "topic_md"))

        if not self.output_html_dir:
            object.__setattr__(self, "output_html_dir", str(root / "googleio_summary" / "topic"))

        if not self.session_html_dir:
            object.__setattr__(self, "session_html_dir", str(root / "googleio_summary" / "topic" / "session"))

        if not self.input_csv_path:
            object.__setattr__(self, "input_csv_path", str(root / "data" / "sheet" / "Google_IO.csv"))

        if not self.meeting_excel_filename:
            object.__setattr__(self, "meeting_excel_filename", str(root / "data" / "sheet" / "Google_IO.csv"))

        # 根據環境設定錯誤處理
        if self.api_environment == "development":
            object.__setattr__(self, "show_traceback_in_errors", True)
        else:
            object.__setattr__(self, "show_traceback_in_errors", False)

        return self

    @property
    def PROJECT_ROOT(self) -> Path:
        """專案根目錄（相容舊名稱）"""
        return self.project_root

    @property
    def GEMINI_API_KEY(self) -> str:
        """Gemini API Key（相容舊名稱）"""
        return self.gemini_api_key

    @property
    def GEMINI_MODEL_NAME(self) -> str:
        """Gemini Model Name（相容舊名稱）"""
        return self.gemini_model_name

    @property
    def MAX_REQUESTS_PER_MINUTE(self) -> int:
        """最大請求數（相容舊名稱）"""
        return self.max_requests_per_minute

    @property
    def REQUEST_INTERVAL(self) -> float:
        """請求間隔（相容舊名稱）"""
        return self.request_interval

    @property
    def MAX_RETRIES(self) -> int:
        """最大重試次數（相容舊名稱）"""
        return self.max_retries

    @property
    def RETRY_DELAY(self) -> int:
        """重試延遲（相容舊名稱）"""
        return self.retry_delay

    @property
    def DEFAULT_INPUT_DIR(self) -> str:
        """預設輸入目錄（相容舊名稱）"""
        return self.default_input_dir

    @property
    def DEFAULT_OUTPUT_DIR(self) -> str:
        """預設輸出目錄（相容舊名稱）"""
        return self.default_output_dir

    @property
    def SUPPORTED_FILE_EXTENSIONS(self) -> List[str]:
        """支援的檔案副檔名（相容舊名稱）"""
        return self.supported_file_extensions

    @property
    def DEFAULT_OUTPUT_FORMAT(self) -> str:
        """預設輸出格式（相容舊名稱）"""
        return self.default_output_format

    @property
    def DEFAULT_WORKERS(self) -> int:
        """預設工作線程數（相容舊名稱）"""
        return self.default_workers

    @property
    def MAX_TRANSCRIPT_LENGTH(self) -> int:
        """最大轉錄長度（相容舊名稱）"""
        return self.max_transcript_length

    @property
    def OUTPUT_MD_DIR(self) -> str:
        """輸出 Markdown 目錄（相容舊名稱）"""
        return self.output_md_dir

    @property
    def OUTPUT_HTML_DIR(self) -> str:
        """輸出 HTML 目錄（相容舊名稱）"""
        return self.output_html_dir

    @property
    def SESSION_HTML_DIR(self) -> str:
        """Session HTML 目錄（相容舊名稱）"""
        return self.session_html_dir

    @property
    def INPUT_CSV_PATH(self) -> str:
        """輸入 CSV 路徑（相容舊名稱）"""
        return self.input_csv_path

    @property
    def TOP_N_MEETINGS(self) -> int:
        """Top N 會議數（相容舊名稱）"""
        return self.top_n_meetings

    @property
    def BATCH_MD_TO_HTML_INDEX(self) -> int:
        """批次 MD 轉 HTML 索引（相容舊名稱）"""
        return self.batch_md_to_html_index


@lru_cache
def get_settings() -> Settings:
    """取得單例設定（建議在 FastAPI 用 Depends(get_settings)）"""
    return Settings()

# 預設匯出單例，供直接 import
settings = get_settings()
