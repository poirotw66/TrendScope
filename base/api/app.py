"""
FastAPI 應用程式 - 模組化重構版本
提供 API 端點以供前端呼叫爬蟲和查詢 BigQuery 資料
"""
import os
import logging
from datetime import datetime

from config.settings import settings

# 確保日誌目錄存在
project_root = settings.PROJECT_ROOT
os.makedirs(project_root / "logs", exist_ok=True)

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# 導入錯誤處理器
from base.api.middleware.error_handler import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    APIError,
    BigQueryError,
)

# 導入路由器
from base.api.routes.ppt_upload import router as ppt_router
from base.api.routes.scrapers import router as scrapers_router
from base.api.routes.bigquery import router as bigquery_router
from base.api.routes.batch_reports import router as batch_reports_router

# 配置日誌
log_level = logging.DEBUG if settings.api_environment == "development" else logging.INFO
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(project_root / "logs" / f"api_{datetime.now().strftime('%Y%m%d')}.log")
    ]
)
logger = logging.getLogger("NeoTrendHub-api")

# 創建 FastAPI 應用
app = FastAPI(
    title="NeoTrendHub API",
    description="NeoTrendHub 的 API 服務，提供爬蟲和資料查詢功能",
    version="1.0.0",
    debug=(settings.api_environment == "development")
)

# 配置 CORS（根據環境變數動態設定）
cors_origins = settings.cors_allow_origins
if cors_origins == "*" and settings.api_environment == "production":
    # 生產環境不允許 "*"，使用預設值或警告
    logger.warning(
        "⚠️  生產環境不應使用 CORS allow_origins='*'，"
        "請設置 CORS_ALLOW_ORIGINS 環境變數指定允許的來源"
    )
    cors_origins = ["http://localhost:3000", "http://localhost:5173"]  # 預設開發環境來源

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins if isinstance(cors_origins, list) else ["*"],
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods if isinstance(settings.cors_allow_methods, list) else ["*"],
    allow_headers=settings.cors_allow_headers if isinstance(settings.cors_allow_headers, list) else ["*"],
)

# 註冊全局異常處理器
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# 註冊路由器
app.include_router(ppt_router)
app.include_router(scrapers_router)
app.include_router(bigquery_router)
app.include_router(batch_reports_router)

# 根端點
@app.get("/")
def read_root():
    """API 根端點"""
    return {
        "message": "歡迎使用 NeoTrendHub API",
        "version": "1.0.0",
        "environment": settings.api_environment
    }

# 健康檢查端點
@app.get("/health")
def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "environment": settings.api_environment
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 啟動 NeoTrendHub base API 服務...")
    logger.info("專案根目錄: %s", project_root)
    logger.info("API 文檔: http://localhost:8001/docs")
    logger.info("API 根端點: http://localhost:8001/")
    
    uvicorn.run(
        "base.api.app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
