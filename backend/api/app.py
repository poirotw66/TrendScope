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
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, Query, Response
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import json
import uuid
import pathlib
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from config.config import GEMINI_API_KEY

# 添加項目根目錄到 Python 路徑以導入 SSG 模組
project_root = pathlib.Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from src.batch_md_to_html import batch_md_to_html
except ImportError:
    # 如果無法導入，創建一個簡單的替代函數
    def batch_md_to_html(md_dir, html_dir, index_param=0):
        """簡單的 Markdown 到 HTML 轉換函數"""
        import markdown
        md_path = pathlib.Path(md_dir)
        html_path = pathlib.Path(html_dir)
        html_path.mkdir(parents=True, exist_ok=True)

        for md_file in md_path.glob('*.md'):
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            html_content = markdown.markdown(md_content)
            html_file = html_path / f"{md_file.stem}.html"

            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{md_file.stem}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
        h1, h2, h3 {{ color: #333; }}
        pre {{ background: #f4f4f4; padding: 10px; border-radius: 5px; }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
                """)

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


# 批量報告生成相關模型
class SeminarInfo(BaseModel):
    """研討會信息模型"""
    name: str
    session_count: int
    sessions_with_ppt: int


class BatchReportRequest(BaseModel):
    """批量報告生成請求模型"""
    seminars: Optional[List[str]] = None  # 如果為 None 則處理所有研討會
    limit: Optional[int] = None  # 每個研討會的會議數量限制
    output_format: str = "markdown"  # "markdown", "html", "both"
    include_html: bool = True


class BatchReportResponse(BaseModel):
    """批量報告生成響應模型"""
    task_id: str
    message: str
    status: str
    seminars_to_process: List[str]
    estimated_sessions: int
    estimated_time: Optional[str] = None


class BatchReportStatus(BaseModel):
    """批量報告狀態模型"""
    task_id: str
    status: str  # "pending", "running", "completed", "failed"
    progress: Dict[str, Any]  # 進度信息
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    error_message: Optional[str] = None
    results: Optional[Dict[str, Any]] = None  # 完成後的結果信息

# 保存運行中的任務
tasks = {}

# 初始化 Gemini 客戶端
genai_client = genai.Client(api_key=GEMINI_API_KEY)

# 批量報告生成相關函數
def get_sessions_from_bigquery_for_reports(bq_client: BigQueryClient, seminars: Optional[List[str]] = None,
                                          limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    從 BigQuery 獲取會議數據用於報告生成
    """
    try:
        project_id = bq_client.project_id
        query = f"SELECT * FROM `{project_id}.conference_data.sessions`"

        # 添加過濾條件
        where_conditions = []
        if seminars:
            seminar_list = "', '".join(seminars)
            where_conditions.append(f"seminar IN ('{seminar_list}')")

        # 只處理有 PPT 內容的會議
        where_conditions.append("ppt_context IS NOT NULL AND LENGTH(TRIM(ppt_context)) > 0")

        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)

        # 添加排序
        query += " ORDER BY seminar, created_at DESC"

        # 添加限制
        if limit:
            query += f" LIMIT {limit}"

        logger.info(f"執行查詢: {query}")
        results = bq_client.query(query)

        sessions = []
        for row in results:
            session = dict(row.items())
            # 處理時間戳
            if "created_at" in session and session["created_at"]:
                session["created_at"] = session["created_at"].isoformat()
            if "updated_at" in session and session["updated_at"]:
                session["updated_at"] = session["updated_at"].isoformat()
            sessions.append(session)

        logger.info(f"獲取到 {len(sessions)} 個會議數據")
        return sessions

    except Exception as e:
        logger.error(f"從 BigQuery 獲取數據時發生錯誤: {e}")
        raise


def summarize_session_for_api(session_data: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
    """
    使用 BigQuery 中的會議數據生成摘要（API 版本）
    """
    try:
        conference_id = session_data.get('conference_id', 'unknown')
        name = session_data.get('name', 'Unknown Session')
        seminar = session_data.get('seminar', 'Unknown Seminar')
        url = session_data.get('url', 'TEST.com')
        ppt_context = session_data.get('ppt_context', '')
        description = session_data.get('description', '')

        category = "主題演講"  # 默認類型

        if not ppt_context:
            return {"status": "skipped", "reason": "沒有 PPT 內容"}

        logger.info(f"正在處理會議: {name}")

        # 構建 Gemini 提示詞
        prompt = f"""
## 處理指示

請依照以下步驟處理我提供的「簡報內容」，並遵循所有格式要求：

### 1. 內部校對（不輸出）
- 仔細閱讀提供的「簡報內容」。
- 將簡報內容中的簡體中文翻譯成繁體中文。
- 僅作為後續撰寫會議總結的依據，不需要輸出校對結果或任何校對過程。

### 2. 撰寫會議總結（僅輸出此部分）
根據內部校對後的簡報內容，撰寫一份有完整脈絡的簡報內容。具體要求如下：

- 總結標題：
  - 第一行輸出提供的 {name} 原文。
  - 第二行輸出{category}
  - 第三行輸出格式： `[會議影片連結]({url})`
  - 第四行中文翻譯：{name}

- 內容結構（需依下列順序分段撰寫、並且儘量詳細）：
  - **1. 核心觀點**
  - **2. 詳細內容**
  - **3. 重要結論**

- 各段落之間需有明確分隔（如空行）。

### 3. 輸出要求
- 請僅輸出步驟2的「會議總結」。
- 嚴禁輸出校對內容、校對過程、任何額外說明或多餘文字。
- 使用 Markdown 格式。
- 全文必須使用繁體中文。

---

## 簡報內容：

{ppt_context}

---

請根據以上簡報內容生成會議總結。
"""

        # 調用 Gemini API（添加隨機延遲避免並發限制）
        import random
        delay = random.uniform(1, 3)  # 1-3秒隨機延遲
        time.sleep(delay)

        response = genai_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt]
        )

        markdown_content = response.text

        # 保存到文件
        output_dir = pathlib.Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        # 使用 conference_id 作為文件名，確保唯一性
        safe_filename = f"{conference_id}_{name}".replace("/", "_").replace("\\", "_")
        # 限制文件名長度
        if len(safe_filename) > 100:
            safe_filename = safe_filename[:100]

        output_filename = safe_filename + ".md"
        output_path = output_dir / output_filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        logger.info(f"已將摘要儲存至 {output_path}")

        return {
            "status": "completed",
            "file_path": str(output_path),
            "conference_id": conference_id,
            "session_name": name,
            "seminar": seminar
        }

    except Exception as e:
        logger.error(f"處理會議 {session_data.get('name', 'unknown')} 時發生錯誤: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "conference_id": session_data.get('conference_id', 'unknown'),
            "session_name": session_data.get('name', 'unknown')
        }

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


def process_single_session(session_data: Dict[str, Any], output_dir: str, task_id: str, session_index: int) -> Dict[str, Any]:
    """
    處理單個會議的函數（用於多線程）
    """
    try:
        session_name = session_data.get('name', 'Unknown Session')
        logger.info(f"[任務 {task_id}] 開始處理會議 {session_index}: {session_name}")

        # 生成摘要
        result = summarize_session_for_api(session_data, output_dir)

        # 更新進度（線程安全）
        if task_id in tasks:
            current_progress = tasks[task_id]["progress"]["current"]
            tasks[task_id]["progress"]["current"] = current_progress + 1
            tasks[task_id]["progress"]["current_session"] = f"已完成: {session_name}"

        logger.info(f"[任務 {task_id}] 完成處理會議 {session_index}: {session_name}")
        return result

    except Exception as e:
        logger.error(f"[任務 {task_id}] 處理會議 {session_index} 時發生錯誤: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "conference_id": session_data.get('conference_id', 'unknown'),
            "session_name": session_data.get('name', 'unknown')
        }


def run_batch_report_task(task_id: str, seminars: Optional[List[str]], limit: Optional[int],
                         include_html: bool, output_format: str):
    """
    執行批量報告生成任務（多線程版本）
    """
    try:
        # 更新任務狀態
        tasks[task_id]["status"] = "running"
        tasks[task_id]["progress"] = {"current": 0, "total": 0, "current_session": "初始化中..."}

        # 獲取 BigQuery 客戶端
        bq_client = get_bigquery_client()
        if not bq_client:
            raise Exception("無法連接到 BigQuery")

        # 獲取會議數據
        sessions = get_sessions_from_bigquery_for_reports(bq_client, seminars, limit)

        if not sessions:
            tasks[task_id]["status"] = "completed"
            tasks[task_id]["progress"]["current_session"] = "沒有找到符合條件的會議"
            tasks[task_id]["end_time"] = datetime.now().isoformat()
            tasks[task_id]["results"] = {"processed_sessions": 0, "generated_reports": 0}
            return

        # 更新總數
        tasks[task_id]["progress"]["total"] = len(sessions)
        tasks[task_id]["progress"]["current_session"] = f"準備處理 {len(sessions)} 個會議..."

        # 創建輸出目錄
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_base_dir = pathlib.Path(f"reports/batch_{timestamp}")
        output_md_dir = output_base_dir / "md"
        output_html_dir = output_base_dir / "html"

        # 確保輸出目錄存在
        output_md_dir.mkdir(parents=True, exist_ok=True)
        if include_html:
            output_html_dir.mkdir(parents=True, exist_ok=True)

        # 使用多線程處理會議
        processed_sessions = []
        failed_sessions = []

        # 設置線程池大小（根據 API 限制調整）
        max_workers = min(4, len(sessions))  # 最多4個並發線程，避免 API 限制

        logger.info(f"[任務 {task_id}] 使用 {max_workers} 個線程並行處理 {len(sessions)} 個會議")
        tasks[task_id]["progress"]["current_session"] = f"使用 {max_workers} 個線程並行處理中..."

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 提交所有任務
            future_to_session = {
                executor.submit(process_single_session, session, str(output_md_dir), task_id, i): (session, i)
                for i, session in enumerate(sessions)
            }

            # 收集結果
            for future in as_completed(future_to_session):
                session, session_index = future_to_session[future]
                try:
                    result = future.result()
                    if result["status"] == "completed":
                        processed_sessions.append(result)
                    else:
                        failed_sessions.append(result)

                except Exception as e:
                    logger.error(f"[任務 {task_id}] 線程執行失敗: {e}")
                    failed_sessions.append({
                        "status": "failed",
                        "error": str(e),
                        "conference_id": session.get('conference_id', 'unknown'),
                        "session_name": session.get('name', 'unknown')
                    })

        # 生成 HTML 報告（如果需要）
        html_files = []
        if include_html and processed_sessions:
            try:
                tasks[task_id]["progress"]["current_session"] = "生成 HTML 報告中..."
                logger.info(f"[任務 {task_id}] 開始生成 HTML 報告...")

                # 使用 SSG 將 Markdown 轉換為 HTML
                batch_md_to_html(str(output_md_dir), str(output_html_dir), index_param=3)

                # 收集生成的 HTML 文件
                for html_file in output_html_dir.glob('*.html'):
                    html_files.append(str(html_file))

                logger.info(f"[任務 {task_id}] HTML 報告生成完成，共 {len(html_files)} 個文件")

            except Exception as e:
                logger.error(f"[任務 {task_id}] 生成 HTML 報告時發生錯誤: {e}")
                # HTML 生成失敗不影響整體任務狀態

        # 完成任務
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["end_time"] = datetime.now().isoformat()
        tasks[task_id]["progress"]["current_session"] = "完成"
        tasks[task_id]["results"] = {
            "processed_sessions": len(processed_sessions),
            "failed_sessions": len(failed_sessions),
            "output_directory": str(output_base_dir),
            "md_directory": str(output_md_dir),
            "html_directory": str(output_html_dir) if include_html else None,
            "processed_files": [s["file_path"] for s in processed_sessions if s["status"] == "completed"],
            "failed_files": failed_sessions,
            "html_files": html_files if include_html else []
        }

        logger.info(f"[任務 {task_id}] 批量報告生成完成: {len(processed_sessions)} 成功, {len(failed_sessions)} 失敗")

    except Exception as e:
        logger.error(f"[任務 {task_id}] 批量報告生成任務失敗: {e}")
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["error_message"] = str(e)
        tasks[task_id]["end_time"] = datetime.now().isoformat()


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
    limit: int = Query(20, ge=1, le=500),
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """從 BigQuery 獲取會議資料

    Args:
        source: 可選的資料來源過濾
        seminar: 可選的研討會過濾
        limit: 最大結果數量 (1-500)

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


# 批量報告生成 API 端點
@app.get("/reports/seminars", tags=["Batch Reports"])
def get_available_seminars_for_reports(
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """獲取可用於報告生成的研討會列表

    Returns:
        包含研討會信息的列表，包括會議總數和有PPT內容的會議數
    """
    if not bq_client:
        raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

    try:
        project_id = bq_client.project_id
        query = f"""
        SELECT
            seminar,
            COUNT(*) as session_count,
            SUM(CASE WHEN ppt_context IS NOT NULL AND LENGTH(TRIM(ppt_context)) > 0 THEN 1 ELSE 0 END) as sessions_with_ppt
        FROM `{project_id}.conference_data.sessions`
        GROUP BY seminar
        ORDER BY session_count DESC
        """

        results = bq_client.query(query)
        seminars = []

        for row in results:
            seminars.append(SeminarInfo(
                name=row['seminar'],
                session_count=row['session_count'],
                sessions_with_ppt=row['sessions_with_ppt']
            ))

        return {"seminars": seminars}

    except Exception as e:
        logger.exception(f"獲取研討會列表時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"獲取研討會列表時發生錯誤: {str(e)}")


@app.post("/reports/generate-batch", tags=["Batch Reports"])
def generate_batch_reports(
    request: BatchReportRequest,
    background_tasks: BackgroundTasks,
    bq_client: Optional[BigQueryClient] = Depends(get_bigquery_client)
):
    """啟動批量報告生成任務

    Args:
        request: 批量報告生成請求
        background_tasks: FastAPI 背景任務
        bq_client: BigQuery 客戶端

    Returns:
        任務信息和預估完成時間
    """
    if not bq_client:
        raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

    try:
        task_id = str(uuid.uuid4())

        # 獲取項目 ID
        project_id = bq_client.project_id

        # 如果沒有指定研討會，獲取所有研討會
        seminars_to_process = request.seminars
        if not seminars_to_process:
            # 獲取所有有PPT內容的研討會
            query = f"""
            SELECT DISTINCT seminar
            FROM `{project_id}.conference_data.sessions`
            WHERE ppt_context IS NOT NULL AND LENGTH(TRIM(ppt_context)) > 0
            ORDER BY seminar
            """
            results = bq_client.query(query)
            seminars_to_process = [row['seminar'] for row in results]

        # 估算會議數量
        seminar_list = "', '".join(seminars_to_process)
        count_query = f"""
        SELECT COUNT(*) as total_sessions
        FROM `{project_id}.conference_data.sessions`
        WHERE seminar IN ('{seminar_list}')
        AND ppt_context IS NOT NULL AND LENGTH(TRIM(ppt_context)) > 0
        """
        if request.limit:
            count_query += f" LIMIT {request.limit}"

        count_results = list(bq_client.query(count_query))
        estimated_sessions = count_results[0]['total_sessions'] if count_results else 0

        # 估算完成時間（每個會議約需要30秒）
        estimated_minutes = (estimated_sessions * 30) // 60
        estimated_time = f"約 {estimated_minutes} 分鐘" if estimated_minutes > 0 else "少於 1 分鐘"

        # 初始化任務狀態
        tasks[task_id] = {
            "task_id": task_id,
            "type": "batch_report",
            "status": "pending",
            "seminars": seminars_to_process,
            "estimated_sessions": estimated_sessions,
            "start_time": datetime.now().isoformat(),
            "progress": {"current": 0, "total": 0, "current_session": "等待開始..."}
        }

        # 添加背景任務
        background_tasks.add_task(
            run_batch_report_task,
            task_id,
            seminars_to_process,
            request.limit,
            request.include_html,
            request.output_format
        )

        return BatchReportResponse(
            task_id=task_id,
            message=f"已啟動批量報告生成任務，將處理 {len(seminars_to_process)} 個研討會",
            status="pending",
            seminars_to_process=seminars_to_process,
            estimated_sessions=estimated_sessions,
            estimated_time=estimated_time
        )

    except Exception as e:
        logger.exception(f"啟動批量報告生成任務時發生錯誤: {str(e)}")
        raise HTTPException(status_code=500, detail=f"啟動任務時發生錯誤: {str(e)}")


@app.get("/reports/status/{task_id}", tags=["Batch Reports"])
def get_batch_report_status(task_id: str):
    """獲取批量報告生成任務狀態

    Args:
        task_id: 任務 ID

    Returns:
        任務狀態信息
    """
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"找不到任務 ID: {task_id}")

    task_data = tasks[task_id]

    return BatchReportStatus(
        task_id=task_id,
        status=task_data.get("status", "unknown"),
        progress=task_data.get("progress", {}),
        start_time=task_data.get("start_time"),
        end_time=task_data.get("end_time"),
        error_message=task_data.get("error_message"),
        results=task_data.get("results")
    )


@app.get("/reports/list", tags=["Batch Reports"])
def list_batch_report_tasks():
    """列出所有批量報告生成任務

    Returns:
        所有任務的列表
    """
    batch_tasks = {
        task_id: task_data
        for task_id, task_data in tasks.items()
        if task_data.get("type") == "batch_report"
    }

    return {"tasks": batch_tasks}


@app.get("/reports/files", tags=["Batch Reports"])
def list_report_files():
    """獲取所有生成的報告文件列表，包含任務狀態信息"""
    try:
        reports_dir = pathlib.Path("reports")
        if not reports_dir.exists():
            return {"reports": []}

        report_batches = []
        for batch_dir in reports_dir.iterdir():
            if batch_dir.is_dir() and batch_dir.name.startswith("batch_"):
                batch_info = {
                    "batch_id": batch_dir.name,
                    "created_time": batch_dir.stat().st_ctime,
                    "md_files": [],
                    "html_files": [],
                    "task_info": None,
                    "seminars": [],
                    "session_count": 0,
                    "status": "completed"  # 默認為已完成，因為文件夾存在
                }

                # 嘗試從任務記錄中找到對應的任務信息
                for task_id, task_data in tasks.items():
                    if (task_data.get("type") == "batch_report" and
                        task_data.get("results", {}).get("output_directory", "").endswith(batch_dir.name)):
                        batch_info["task_info"] = {
                            "task_id": task_id,
                            "status": task_data.get("status", "unknown"),
                            "start_time": task_data.get("start_time"),
                            "end_time": task_data.get("end_time"),
                            "seminars": task_data.get("seminars", []),
                            "results": task_data.get("results", {})
                        }
                        batch_info["seminars"] = task_data.get("seminars", [])
                        batch_info["status"] = task_data.get("status", "completed")
                        if task_data.get("results"):
                            batch_info["session_count"] = task_data["results"].get("processed_sessions", 0)
                        break

                # 收集 Markdown 文件
                md_dir = batch_dir / "md"
                if md_dir.exists():
                    for md_file in md_dir.glob("*.md"):
                        # 使用相對於 reports 目錄的路徑
                        relative_path = md_file.relative_to(reports_dir)
                        batch_info["md_files"].append({
                            "filename": md_file.name,
                            "path": str(relative_path),
                            "size": md_file.stat().st_size
                        })

                # 收集 HTML 文件
                html_dir = batch_dir / "html"
                if html_dir.exists():
                    for html_file in html_dir.glob("*.html"):
                        # 使用相對於 reports 目錄的路徑
                        relative_path = html_file.relative_to(reports_dir)
                        batch_info["html_files"].append({
                            "filename": html_file.name,
                            "path": str(relative_path),
                            "size": html_file.stat().st_size
                        })

                report_batches.append(batch_info)

        # 按創建時間排序（最新的在前）
        report_batches.sort(key=lambda x: x["created_time"], reverse=True)

        return {"reports": report_batches}

    except Exception as e:
        logger.error(f"獲取報告文件列表失敗: {e}")
        raise HTTPException(status_code=500, detail=f"獲取報告文件列表失敗: {str(e)}")


@app.get("/reports/preview/{file_path:path}", tags=["Batch Reports"])
def preview_report_file(file_path: str):
    """預覽報告文件內容"""
    try:
        # 安全檢查：確保文件路徑在 reports 目錄內
        file_path = pathlib.Path(file_path)
        reports_dir = pathlib.Path("reports")

        # 解析相對路徑
        if not file_path.is_absolute():
            full_path = reports_dir / file_path
        else:
            full_path = file_path

        # 確保文件在 reports 目錄內
        try:
            full_path.resolve().relative_to(reports_dir.resolve())
        except ValueError:
            raise HTTPException(status_code=403, detail="訪問被拒絕：文件不在允許的目錄內")

        if not full_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")

        # 讀取文件內容
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 根據文件類型返回不同的響應
        if full_path.suffix.lower() == '.html':
            return Response(content=content, media_type="text/html")
        elif full_path.suffix.lower() == '.md':
            return {"content": content, "type": "markdown"}
        else:
            return {"content": content, "type": "text"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"預覽文件失敗: {e}")
        raise HTTPException(status_code=500, detail=f"預覽文件失敗: {str(e)}")


@app.get("/reports/download/{file_path:path}", tags=["Batch Reports"])
def download_report_file(file_path: str):
    """下載報告文件"""
    try:
        # 安全檢查：確保文件路徑在 reports 目錄內
        file_path = pathlib.Path(file_path)
        reports_dir = pathlib.Path("reports")

        # 解析相對路徑
        if not file_path.is_absolute():
            full_path = reports_dir / file_path
        else:
            full_path = file_path

        # 確保文件在 reports 目錄內
        try:
            full_path.resolve().relative_to(reports_dir.resolve())
        except ValueError:
            raise HTTPException(status_code=403, detail="訪問被拒絕：文件不在允許的目錄內")

        if not full_path.exists():
            raise HTTPException(status_code=404, detail="文件不存在")

        # 返回文件下載響應
        return FileResponse(
            path=str(full_path),
            filename=full_path.name,
            media_type='application/octet-stream'
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"下載文件失敗: {e}")
        raise HTTPException(status_code=500, detail=f"下載文件失敗: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    # 確保日誌目錄存在
    os.makedirs("logs", exist_ok=True)
    # 啟動 API 服務
    uvicorn.run(app, host="0.0.0.0", port=8000)
