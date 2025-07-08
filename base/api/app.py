"""
FastAPI 應用程式 - 模組化重構版本
提供 API 端點以供前端呼叫爬蟲和查詢 BigQuery 資料
"""
import os
import sys
import logging
from datetime import datetime

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

# 確保日誌目錄存在
os.makedirs(os.path.join(project_root, "logs"), exist_ok=True)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 導入路由器
from base.api.routes.ppt_upload import router as ppt_router
from base.api.routes.scrapers import router as scrapers_router
from base.api.routes.bigquery import router as bigquery_router
from base.api.routes.batch_reports import router as batch_reports_router

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(project_root, "logs", f"api_{datetime.now().strftime('%Y%m%d')}.log"))
    ]
)
logger = logging.getLogger("trendscope-api")

# 創建 FastAPI 應用
app = FastAPI(
    title="TrendScope API",
    description="TrendScope 的 API 服務，提供爬蟲和資料查詢功能",
    version="1.0.0"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生產環境中，應該限制為特定來源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由器
app.include_router(ppt_router)
app.include_router(scrapers_router)
app.include_router(bigquery_router)
app.include_router(batch_reports_router)

# 根端點
@app.get("/")
def read_root():
    """API 根端點"""
    return {"message": "歡迎使用 TrendScope API"}

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 啟動 TrendScope Backend API 服務...")
    print(f"專案根目錄: {project_root}")
    print("API 文檔: http://localhost:8001/docs")
    print("API 根端點: http://localhost:8001/")
    
    uvicorn.run(
        "backend.api.app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
