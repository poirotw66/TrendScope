"""
FastAPI 應用程式
提供 API 端點以供前端呼叫爬蟲和查詢 BigQuery 資料
"""
import os
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs"), exist_ok=True)
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import logging
from datetime import datetime
import json
import uuid

# 導入爬蟲
from scrapers.parsers.aws_london import AWSLondonScraper
from scrapers.parsers.aicon_infoq import AiconInfoqScraper
from bigquery.client import BigQueryClient

# 配置日誌
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"logs/api_{datetime.now().strftime('%Y%m%d')}.log")
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

# 模型定義
class ScraperRequest(BaseModel):
    """爬蟲請求模型"""
    scraper_type: str
    headless: bool = True
    wait_time: int = 30
    use_bigquery: bool = False

class ScraperResponse(BaseModel):
    """爬蟲響應模型"""
    task_id: str
    message: str
    status: str

class ScraperResult(BaseModel):
    """爬蟲結果模型"""
    task_id: str
    status: str
    file_path: Optional[str] = None
    message: Optional[str] = None
    data: Optional[List[Dict[str, Any]]] = None

# 保存運行中的任務
tasks = {}

# 依賴項：獲取 BigQuery 客戶端
def get_bigquery_client():
    """獲取 BigQuery 客戶端"""
    try:
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        
        if not credentials_path:
            # 在生產環境中，應該提供適當的錯誤處理
            logger.warning("未設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量")
            return None
            
        return BigQueryClient(credentials_path=credentials_path, project_id=project_id)
    except Exception as e:
        logger.error(f"初始化 BigQuery 客戶端失敗: {str(e)}")
        return None

# 爬蟲任務函數
def run_scraper_task(task_id: str, scraper_type: str, headless: bool, wait_time: int, use_bigquery: bool):
    """在背景執行爬蟲任務"""
    try:
        logger.info(f"開始任務 {task_id}: {scraper_type}")
        tasks[task_id]["status"] = "running"
        output_dir = os.path.join("data", "sheet")
        os.makedirs(output_dir, exist_ok=True)
        bq_credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        bq_project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        if scraper_type == "aws_london":
            scraper = AWSLondonScraper(
                headless=headless,
                wait_time=wait_time,
                use_bigquery=use_bigquery,
                bq_credentials=bq_credentials,
                bq_project_id=bq_project_id
            )
        elif scraper_type == "aicon_infoq":
            scraper = AiconInfoqScraper(
                headless=headless,
                wait_time=wait_time,
                use_bigquery=use_bigquery,
                bq_credentials=bq_credentials,
                bq_project_id=bq_project_id
            )
        else:
            tasks[task_id].update({
                "status": "failed",
                "message": f"不支援的爬蟲類型: {scraper_type}"
            })
            logger.error(f"任務 {task_id} 失敗: 不支援的爬蟲類型 {scraper_type}")
            return
        file_path = scraper.run(output_dir=output_dir)
        if file_path:
            import pandas as pd
            if file_path.endswith(".xlsx"):
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)
            data = df.to_dict('records')
            tasks[task_id].update({
                "status": "completed",
                "file_path": file_path,
                "data": data,
                "message": "爬蟲任務完成"
            })
            logger.info(f"任務 {task_id} 完成: {file_path}")
        else:
            tasks[task_id].update({
                "status": "failed",
                "message": "爬蟲未獲取到資料或發生錯誤"
            })
            logger.error(f"任務 {task_id} 失敗: 未獲取到資料或發生錯誤")
    except Exception as e:
        logger.exception(f"任務 {task_id} 發生錯誤: {str(e)}")
        tasks[task_id].update({
            "status": "failed",
            "message": f"爬蟲過程中發生錯誤: {str(e)}"
        })

# API 端點
@app.get("/")
def read_root():
    """API 根端點"""
    return {"message": "歡迎使用 TrendScope API"}

@app.post("/scrapers/run", response_model=ScraperResponse)
def run_scraper(request: ScraperRequest, background_tasks: BackgroundTasks):
    """啟動爬蟲任務"""
    task_id = str(uuid.uuid4())
    
    # 初始化任務狀態
    tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "scraper_type": request.scraper_type,
        "start_time": datetime.now().isoformat()
    }
    
    # 添加背景任務
    background_tasks.add_task(
        run_scraper_task,
        task_id,
        request.scraper_type,
        request.headless,
        request.wait_time,
        request.use_bigquery
    )
    
    return ScraperResponse(
        task_id=task_id,
        message=f"已啟動爬蟲任務: {request.scraper_type}",
        status="pending"
    )

@app.get("/scrapers/status/{task_id}", response_model=ScraperResult)
def get_scraper_status(task_id: str):
    """獲取爬蟲任務狀態"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"找不到任務 ID: {task_id}")
    
    return ScraperResult(**tasks[task_id])

@app.get("/scrapers/list")
def list_available_scrapers():
    """列出可用的爬蟲"""
    return {
        "scrapers": [
            {
                "id": "aws_london",
                "name": "AWS London Summit",
                "description": "爬取 AWS London Summit 的會議資訊"
            },
            {
                "id": "aicon_infoq",
                "name": "AICon InfoQ 2025 Shanghai",
                "description": "爬取 AICon (InfoQ) 2025 上海議程與摘要"
            }
        ]
    }

@app.get("/data/sessions")
def get_sessions(
    source: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """從 BigQuery 獲取會議資料"""
    if not bq_client:
        raise HTTPException(status_code=500, detail="無法連接到 BigQuery")
    
    try:
        # 構建查詢
        query = "SELECT * FROM `conference_data.sessions`"
        if source:
            query += f" WHERE source = '{source}'"
        query += f" LIMIT {limit}"
        
        # 執行查詢
        results = bq_client.query(query)
        
        # 轉換為列表
        sessions = []
        for row in results:
            session = dict(row.items())
            # 處理特殊類型（如果需要）
            if "created_at" in session:
                session["created_at"] = session["created_at"].isoformat()
            if "updated_at" in session:
                session["updated_at"] = session["updated_at"].isoformat()
            sessions.append(session)
            
        return {"sessions": sessions}
    except Exception as e:
        logger.exception(f"查詢 BigQuery 時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"查詢資料時發生錯誤: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # 確保日誌目錄存在
    os.makedirs("logs", exist_ok=True)
    # 啟動 API 服務
    uvicorn.run(app, host="0.0.0.0", port=8000)
