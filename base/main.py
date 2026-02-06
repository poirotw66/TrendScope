#!/usr/bin/env python3
"""
NeoTrendHub base 主啟動檔案
"""

import os
import uvicorn

from config.settings import settings
from base.api.app import app
from base.utils.logger import get_api_logger

logger = get_api_logger()

if __name__ == "__main__":
    project_root = settings.PROJECT_ROOT
    
    # 確保環境變數設置
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        logger.warning("未設置 GOOGLE_APPLICATION_CREDENTIALS 環境變數")
    
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        logger.warning("未設置 GOOGLE_CLOUD_PROJECT 環境變數")
    
    # 確保日誌目錄存在
    os.makedirs(project_root / "logs", exist_ok=True)
    
    logger.info("🚀 啟動 NeoTrendHub base API 服務...")
    logger.info("專案根目錄: %s", project_root)
    logger.info("API 文檔: http://localhost:8001/docs")
    logger.info("API 根端點: http://localhost:8001/")
    
    # 啟動 API 服務
    uvicorn.run(
        "base.api.app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
