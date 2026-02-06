"""
統一的日誌配置模組
提供標準化的日誌設定，供整個專案使用
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from config.settings import settings


def setup_logger(
    name: str,
    log_file: Optional[Path] = None,
    level: Optional[int] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    設定並返回一個配置好的 logger
    
    Args:
        name: logger 名稱（通常是 __name__）
        log_file: 日誌檔案路徑（可選）
        level: 日誌級別（可選，預設從 settings 讀取）
        format_string: 自定義格式字串（可選）
    
    Returns:
        配置好的 logger 實例
    """
    logger = logging.getLogger(name)
    
    # 避免重複添加 handler
    if logger.handlers:
        return logger
    
    # 設定日誌級別
    if level is None:
        if settings.api_environment == "development":
            level = logging.DEBUG
        else:
            level = logging.INFO
    logger.setLevel(level)
    
    # 預設格式
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    formatter = logging.Formatter(
        format_string,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Console handler（總是添加）
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler（如果指定了日誌檔案）
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str, log_file: Optional[Path] = None) -> logging.Logger:
    """
    取得或創建一個 logger（簡化版）
    
    Args:
        name: logger 名稱
        log_file: 可選的日誌檔案路徑
    
    Returns:
        logger 實例
    """
    return setup_logger(name, log_file)


# 預設 logger（用於腳本和模組）
def get_default_logger(module_name: str = "trendscope") -> logging.Logger:
    """
    取得預設 logger，自動設定日誌檔案
    
    Args:
        module_name: 模組名稱，用於日誌檔案命名
    
    Returns:
        配置好的 logger
    """
    log_dir = settings.PROJECT_ROOT / "logs"
    log_file = log_dir / f"{module_name}_{datetime.now().strftime('%Y%m%d')}.log"
    return get_logger(module_name, log_file)


# 為不同模組提供便捷函數
def get_scraper_logger() -> logging.Logger:
    """取得爬蟲模組的 logger"""
    return get_default_logger("scraper")


def get_bigquery_logger() -> logging.Logger:
    """取得 BigQuery 模組的 logger"""
    return get_default_logger("bigquery")


def get_api_logger() -> logging.Logger:
    """取得 API 模組的 logger"""
    return get_default_logger("api")


def get_script_logger(script_name: str) -> logging.Logger:
    """取得腳本的 logger"""
    return get_default_logger(script_name)
