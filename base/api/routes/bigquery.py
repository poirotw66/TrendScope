"""
BigQuery 資料查詢相關的 API 路由
"""
import os
import logging
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from base.bigquery.client import BigQueryClient

# 依賴項：獲取 BigQuery 客戶端
def get_bigquery_client():
    """
    獲取 BigQuery 客戶端
    
    Raises:
        BigQueryError: 當 BigQuery 客戶端無法初始化時
    """
    from base.api.middleware.error_handler import BigQueryError
    from config.settings import settings
    
    try:
        credentials_path = settings.google_application_credentials or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = settings.google_cloud_project or os.environ.get("GOOGLE_CLOUD_PROJECT")

        if not credentials_path:
            raise BigQueryError(
                message="BigQuery 服務未配置",
                detail="請設置 GOOGLE_APPLICATION_CREDENTIALS 環境變數或配置 google_application_credentials"
            )

        if not project_id:
            raise BigQueryError(
                message="BigQuery 專案 ID 未配置",
                detail="請設置 GOOGLE_CLOUD_PROJECT 環境變數或配置 google_cloud_project"
            )

        return BigQueryClient(credentials_path=credentials_path, project_id=project_id)
    except BigQueryError:
        # 重新拋出 BigQueryError
        raise
    except Exception as e:
        logger.error(f"初始化 BigQuery 客戶端失敗: {str(e)}", exc_info=True)
        raise BigQueryError(
            message="BigQuery 客戶端初始化失敗",
            detail=str(e)
        )

# 設置日誌
logger = logging.getLogger("NeoTrendHub-api")

# 創建路由器
router = APIRouter(prefix="/data", tags=["BigQuery Data"])

# 模型定義
class SessionData(BaseModel):
    """會議資料模型"""
    id: str
    title: str
    description: Optional[str] = None
    speaker: Optional[str] = None
    seminar: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    ppt_context: Optional[str] = None

class SeminarData(BaseModel):
    """研討會資料模型"""
    name: str
    session_count: int

class DataStats(BaseModel):
    """資料統計模型"""
    total_sessions: int
    total_seminars: int
    sessions_with_ppt: int
    latest_update: Optional[str] = None

# API 端點
@router.get("/sessions")
def get_sessions(
    source: Optional[str] = None,
    seminar: Optional[str] = None,
    limit: int = Query(20, ge=1, le=500),
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """從 BigQuery 獲取會議資料
    
    Args:
        source: 資料來源篩選
        seminar: 研討會名稱篩選
        limit: 返回結果數量限制
        bq_client: BigQuery 客戶端
    
    Returns:
        包含會議資料的 JSON 響應
    """
    if not bq_client:
        raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

    try:
        project_id = bq_client.project_id
        
        # 構建查詢條件
        where_conditions = []
        if source:
            where_conditions.append(f"source = '{source}'")
        if seminar:
            where_conditions.append(f"seminar = '{seminar}'")
        
        where_clause = ""
        if where_conditions:
            where_clause = "WHERE " + " AND ".join(where_conditions)
        
        query = f"""
        SELECT *
        FROM `{project_id}.conference_data.sessions`
        {where_clause}
        ORDER BY name
        LIMIT {limit}
        """

        results = bq_client.query(query)
        sessions = []

        for row in results:
            # 將 BigQuery 行轉換為字典，處理日期時間欄位
            session = dict(row)

            # 處理日期時間欄位
            for key, value in session.items():
                if hasattr(value, 'isoformat'):  # 檢查是否為日期時間對象
                    session[key] = value.isoformat()

            sessions.append(session)

        return {"sessions": sessions}
    except Exception as e:
        logger.exception(f"查詢 BigQuery 時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"查詢資料時發生錯誤: {str(e)}")

@router.get("/seminars")
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

@router.get("/stats")
def get_data_stats(
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """從 BigQuery 獲取資料統計資訊

    Returns:
        包含資料統計的 JSON 響應
    """
    if not bq_client:
        raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

    try:
        project_id = bq_client.project_id
        
        # 獲取總會議數
        total_sessions_query = f"SELECT COUNT(*) as total FROM `{project_id}.conference_data.sessions`"
        total_sessions_result = list(bq_client.query(total_sessions_query))
        total_sessions = total_sessions_result[0]['total'] if total_sessions_result else 0
        
        # 獲取研討會數量
        seminars_query = f"SELECT COUNT(DISTINCT seminar) as total FROM `{project_id}.conference_data.sessions`"
        seminars_result = list(bq_client.query(seminars_query))
        total_seminars = seminars_result[0]['total'] if seminars_result else 0
        
        # 獲取有 PPT 內容的會議數
        ppt_sessions_query = f"""
        SELECT COUNT(*) as total 
        FROM `{project_id}.conference_data.sessions` 
        WHERE ppt_context IS NOT NULL AND LENGTH(TRIM(ppt_context)) > 0
        """
        ppt_sessions_result = list(bq_client.query(ppt_sessions_query))
        sessions_with_ppt = ppt_sessions_result[0]['total'] if ppt_sessions_result else 0

        return {
            "total_sessions": total_sessions,
            "total_seminars": total_seminars,
            "sessions_with_ppt": sessions_with_ppt,
            "latest_update": None  # 可以後續添加時間戳查詢
        }
    except Exception as e:
        logger.exception(f"查詢統計資訊時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"查詢統計資訊時發生錯誤: {str(e)}")

# BigQuery 健康檢查端點
@router.get("/health")
def check_bigquery_health(
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """檢查 BigQuery 連接健康狀態

    Returns:
        BigQuery 連接狀態資訊
    """
    if not bq_client:
        return {
            "status": "error",
            "message": "無法初始化 BigQuery 客戶端",
            "connected": False
        }

    try:
        # 嘗試執行一個簡單的查詢來測試連接
        test_query = f"SELECT 1 as test_value"
        results = list(bq_client.query(test_query))
        
        if results and results[0]['test_value'] == 1:
            return {
                "status": "healthy",
                "message": "BigQuery 連接正常",
                "project_id": bq_client.project_id,
                "connected": True
            }
        else:
            return {
                "status": "error",
                "message": "BigQuery 查詢測試失敗",
                "connected": False
            }
    except Exception as e:
        logger.exception(f"BigQuery 健康檢查失敗: {str(e)}")
        return {
            "status": "error",
            "message": f"BigQuery 連接錯誤: {str(e)}",
            "connected": False
        }
