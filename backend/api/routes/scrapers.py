"""
爬蟲相關的 API 路由
"""
import os
import sys
import uuid
import logging
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

# 設置日誌
logger = logging.getLogger("trendscope-api")

# 創建路由器
router = APIRouter(prefix="/scrapers", tags=["Scrapers"])

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

# 導入共享任務管理
from backend.api.shared.tasks import tasks, get_task, set_task, update_task, task_exists

def run_scraper_task(task_id: str, scraper_type: str, headless: bool, wait_time: int, use_bigquery: bool):
    """
    執行爬蟲任務的背景函數
    """
    try:
        # 更新任務狀態
        tasks[task_id]["status"] = "running"
        tasks[task_id]["message"] = f"正在執行 {scraper_type} 爬蟲..."
        
        logger.info(f"開始執行爬蟲任務 {task_id}: {scraper_type}")
        
        # 根據爬蟲類型執行相應的爬蟲
        if scraper_type == "aws_london":
            from scrapers.parsers.aws_london import run_aws_london_scraper
            result = run_aws_london_scraper(headless=headless, wait_time=wait_time, use_bigquery=use_bigquery)
        elif scraper_type == "aicon_infoq":
            from scrapers.parsers.aicon_infoq import run_aicon_infoq_scraper
            result = run_aicon_infoq_scraper(headless=headless, wait_time=wait_time, use_bigquery=use_bigquery)
        elif scraper_type == "qcon_infoq":
            from scrapers.parsers.qcon_infoq import run_qcon_infoq_scraper
            result = run_qcon_infoq_scraper(headless=headless, wait_time=wait_time, use_bigquery=use_bigquery)
        else:
            raise ValueError(f"不支援的爬蟲類型: {scraper_type}")
        
        # 更新任務狀態為成功
        tasks[task_id].update({
            "status": "completed",
            "message": f"{scraper_type} 爬蟲執行完成",
            "file_path": result.get("file_path"),
            "data": result.get("data", [])
        })
        
        logger.info(f"爬蟲任務 {task_id} 執行完成")
        
    except Exception as e:
        logger.error(f"爬蟲任務 {task_id} 執行失敗: {str(e)}")
        tasks[task_id].update({
            "status": "failed",
            "message": f"爬蟲過程中發生錯誤: {str(e)}"
        })

# API 端點
@router.post("/run", response_model=ScraperResponse)
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

@router.get("/status/{task_id}", response_model=ScraperResult)
def get_scraper_status(task_id: str):
    """獲取爬蟲任務狀態"""
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"找不到任務 ID: {task_id}")

    task_data = tasks[task_id]

    # 只提取 ScraperResult 模型需要的欄位
    return ScraperResult(
        task_id=task_data.get("task_id", task_id),
        status=task_data.get("status", "unknown"),
        file_path=task_data.get("file_path"),
        message=task_data.get("message"),
        data=task_data.get("data", [])
    )

@router.get("/list")
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
