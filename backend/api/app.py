"""
FastAPI 應用程式
提供 API 端點以供前端呼叫爬蟲和查詢 BigQuery 資料
"""
import os
import sys

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

os.makedirs(os.path.join(project_root, "logs"), exist_ok=True)
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import json
import uuid

# 導入爬蟲
from backend.scrapers.parsers.aws_london import AWSLondonScraper
from backend.scrapers.parsers.aicon_infoq import AiconInfoqScraper
from backend.scrapers.parsers.qcon_infoq import QconInfoqScraper
from backend.bigquery.client import BigQueryClient

# 導入 PPT 上傳路由器
from backend.api.ppt_upload import router as ppt_router

# 配置日誌
# 確保日誌目錄存在
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
logs_dir = os.path.join(project_root, "logs")
os.makedirs(logs_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(logs_dir, f"api_{datetime.now().strftime('%Y%m%d')}.log"))
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

# 包含路由器
app.include_router(ppt_router)

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
        elif scraper_type == "qcon_infoq":
            scraper = QconInfoqScraper(
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

@app.post("/scrapers/run", response_model=ScraperResponse, tags=["Scrapers"])
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

@app.get("/scrapers/status/{task_id}", response_model=ScraperResult, tags=["Scrapers"])
def get_scraper_status(task_id: str):
    """獲取爬蟲任務狀態"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"找不到任務 ID: {task_id}")
    
    return ScraperResult(**tasks[task_id])

@app.get("/scrapers/list", tags=["Scrapers"])
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
            },
            {
                "id": "qcon_infoq",
                "name": "QCon InfoQ 2025 Beijing",
                "description": "爬取 QCon (InfoQ) 2025 北京議程與摘要"
            }
        ]
    }

@app.get("/data/sessions", tags=["BigQuery Data"])
def get_sessions(
    source: Optional[str] = None,
    seminar: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """從 BigQuery 獲取會議資料

    Args:
        source: 可選的資料來源過濾
        seminar: 可選的研討會過濾
        limit: 最大結果數量 (1-100)

    Returns:
        包含會議資料列表的 JSON 響應
    """
    if not bq_client:
        raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

    try:
        # 構建查詢 - 添加項目 ID 和排序
        project_id = bq_client.project_id
        query = f"SELECT * FROM `{project_id}.conference_data.sessions`"

        # 添加 WHERE 條件
        where_conditions = []
        if source:
            where_conditions.append(f"source = '{source}'")
        if seminar:
            where_conditions.append(f"seminar = '{seminar}'")

        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)

        # 添加排序和限制
        query += f" ORDER BY created_at DESC LIMIT {limit}"

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

@app.get("/data/seminars", tags=["BigQuery Data"])
def get_seminars(
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """從 BigQuery 獲取所有可用的研討會列表

    Returns:
        包含研討會列表的 JSON 響應，每個研討會包含名稱和會議數量
    """
    if not bq_client:
        raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

    try:
        project_id = bq_client.project_id
        query = f"""
        SELECT seminar, COUNT(*) as session_count
        FROM `{project_id}.conference_data.sessions`
        GROUP BY seminar
        ORDER BY session_count DESC
        """

        results = bq_client.query(query)
        seminars = [{"name": row['seminar'], "session_count": row['session_count']} for row in results]

        return {"seminars": seminars}
    except Exception as e:
        logger.exception(f"查詢研討會列表時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"查詢研討會列表時發生錯誤: {str(e)}")

@app.get("/data/stats", tags=["BigQuery Data"])
def get_data_stats(
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """從 BigQuery 獲取資料統計資訊

    Returns:
        包含總會議數、研討會數等統計資訊的 JSON 響應
    """
    if not bq_client:
        raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

    try:
        project_id = bq_client.project_id

        # 獲取總會議數
        total_sessions_query = f"SELECT COUNT(*) as total FROM `{project_id}.conference_data.sessions`"
        total_sessions_result = list(bq_client.query(total_sessions_query))
        total_sessions = total_sessions_result[0]['total'] if total_sessions_result else 0

        # 獲取研討會數
        seminars_query = f"SELECT COUNT(DISTINCT seminar) as total FROM `{project_id}.conference_data.sessions`"
        seminars_result = list(bq_client.query(seminars_query))
        total_seminars = seminars_result[0]['total'] if seminars_result else 0

        # 獲取有 PPT 內容的會議數
        ppt_sessions_query = f"SELECT COUNT(*) as total FROM `{project_id}.conference_data.sessions` WHERE ppt_context IS NOT NULL AND ppt_context != ''"
        ppt_sessions_result = list(bq_client.query(ppt_sessions_query))
        ppt_sessions = ppt_sessions_result[0]['total'] if ppt_sessions_result else 0

        return {
            "total_sessions": total_sessions,
            "total_seminars": total_seminars,
            "sessions_with_ppt": ppt_sessions,
            "sessions_without_ppt": total_sessions - ppt_sessions
        }
    except Exception as e:
        logger.exception(f"查詢統計資訊時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"查詢統計資訊時發生錯誤: {str(e)}")

@app.get("/bigquery/health", tags=["BigQuery Data"])
def check_bigquery_health(
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """檢查 BigQuery 連接健康狀態

    Returns:
        BigQuery 連接狀態和基本資訊
    """
    if not bq_client:
        return {
            "status": "error",
            "message": "無法連接到 BigQuery",
            "connected": False
        }

    try:
        # 測試連接
        project_id = bq_client.project_id
        test_query = "SELECT 1 as test"
        list(bq_client.query(test_query))

        return {
            "status": "healthy",
            "message": "BigQuery 連接正常",
            "connected": True,
            "project_id": project_id,
            "dataset": "conference_data",
            "table": "sessions"
        }
    except Exception as e:
        logger.exception(f"BigQuery 健康檢查失敗: {str(e)}")
        return {
            "status": "error",
            "message": f"BigQuery 連接異常: {str(e)}",
            "connected": False
        }

if __name__ == "__main__":
    import uvicorn
    # 確保日誌目錄存在
    os.makedirs("logs", exist_ok=True)
    # 啟動 API 服務
    uvicorn.run(app, host="0.0.0.0", port=8000)
