"""
批量報告生成相關的 API 路由
"""
import os
import sys
import uuid
import logging
import pathlib
import time
from datetime import datetime
from typing import List, Optional, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Response
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

from backend.bigquery.client import BigQueryClient

# 依賴項：獲取 BigQuery 客戶端
def get_bigquery_client():
    """獲取 BigQuery 客戶端"""
    import os
    try:
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

        if not credentials_path:
            logger.warning("未設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量")
            return None

        return BigQueryClient(credentials_path=credentials_path, project_id=project_id)
    except Exception as e:
        logger.error(f"初始化 BigQuery 客戶端失敗: {str(e)}")
        return None
from config.config import GEMINI_API_KEY

# 添加項目根目錄到 Python 路徑以導入 SSG 模組
project_root_path = pathlib.Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root_path))

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
                f.write(html_content)

# 設置日誌
logger = logging.getLogger("trendscope-api")

# 創建路由器
router = APIRouter(prefix="/reports", tags=["Batch Reports"])

# 初始化 Gemini 客戶端
genai_client = genai.Client(api_key=GEMINI_API_KEY)

# 導入共享任務管理
from backend.api.shared.tasks import tasks, get_task, set_task, update_task, task_exists

# 模型定義
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

# 工具函數
def get_sessions_from_bigquery_for_reports(bq_client: BigQueryClient, seminars: Optional[List[str]] = None,
                                         limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    從 BigQuery 獲取會議數據用於報告生成
    """
    try:
        project_id = bq_client.project_id
        
        # 構建查詢條件
        where_conditions = ["ppt_context IS NOT NULL", "LENGTH(TRIM(ppt_context)) > 0"]
        
        if seminars:
            seminar_list = "', '".join(seminars)
            where_conditions.append(f"seminar IN ('{seminar_list}')")
        
        where_clause = "WHERE " + " AND ".join(where_conditions)
        
        limit_clause = ""
        if limit:
            limit_clause = f"LIMIT {limit}"
        
        query = f"""
        SELECT *
        FROM `{project_id}.conference_data.sessions`
        {where_clause}
        ORDER BY seminar, name
        {limit_clause}
        """

        results = bq_client.query(query)
        sessions = []

        for row in results:
            # 將 BigQuery 行轉換為字典
            session = dict(row)

            # 處理日期時間欄位
            for key, value in session.items():
                if hasattr(value, 'isoformat'):
                    session[key] = value.isoformat()

            sessions.append(session)

        return sessions
    except Exception as e:
        logger.error(f"從 BigQuery 獲取會議數據失敗: {e}")
        raise

def generate_session_report(session_data: Dict[str, Any], genai_client) -> Dict[str, Any]:
    """
    為單個會議生成報告
    """
    try:
        # 使用正確的欄位名稱
        session_id = session_data.get('conference_id', session_data.get('id', 'unknown'))
        title = session_data.get('name', session_data.get('title', 'Unknown Title'))
        speaker = session_data.get('speaker', 'Unknown Speaker')
        seminar = session_data.get('seminar', 'Unknown Seminar')
        url = session_data.get('url', 'TEST.com')
        ppt_context = session_data.get('ppt_context', '')

        category = "主題演講"  # 默認類型

        # 構建提示詞
        prompt = f"""
請根據以下會議的 PPT 內容，生成一份詳細的技術報告。

會議信息：
- 標題：{title}
- 講者：{speaker}
- 研討會：{seminar}
- 類型：{category}

PPT 內容：
{ppt_context}

請生成一份包含以下部分的技術報告：
1. 會議概述
2. 主要技術要點
3. 創新亮點
4. 實際應用場景
5. 技術趨勢分析

請用繁體中文撰寫，內容要專業且具有技術深度。
"""

        # 調用 Gemini API
        response = genai_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=prompt
        )

        if response and response.text:
            report_content = response.text
        else:
            report_content = f"無法生成 {title} 的報告內容"

        # 構建 Markdown 格式的報告
        markdown_content = f"""# {title}

**講者：** {speaker}  
**研討會：** {seminar}  
**類型：** {category}  
**來源：** [{url}]({url})

---

{report_content}

---

*本報告由 TrendScope 自動生成*
"""

        return {
            "status": "completed",
            "session_id": session_id,
            "title": title,
            "content": markdown_content,
            "file_path": None  # 將在保存文件後設置
        }

    except Exception as e:
        logger.error(f"生成會議報告失敗 {session_data.get('id', 'unknown')}: {e}")
        return {
            "status": "failed",
            "session_id": session_data.get('id', 'unknown'),
            "title": session_data.get('title', 'Unknown'),
            "error": str(e)
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

        # 更新進度
        tasks[task_id]["progress"]["total"] = len(sessions)
        logger.info(f"[任務 {task_id}] 開始處理 {len(sessions)} 個會議")

        # 創建輸出目錄
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_base_dir = pathlib.Path("reports") / f"batch_{timestamp}"
        output_md_dir = output_base_dir / "md"
        output_html_dir = output_base_dir / "html"

        output_md_dir.mkdir(parents=True, exist_ok=True)
        if include_html:
            output_html_dir.mkdir(parents=True, exist_ok=True)

        # 使用線程池並行處理
        processed_sessions = []
        failed_sessions = []

        with ThreadPoolExecutor(max_workers=3) as executor:
            # 提交所有任務
            future_to_session = {
                executor.submit(generate_session_report, session, genai_client): (session, i)
                for i, session in enumerate(sessions)
            }

            # 收集結果
            for future in as_completed(future_to_session):
                session, session_index = future_to_session[future]
                try:
                    result = future.result()
                    if result["status"] == "completed":
                        # 保存 Markdown 文件
                        session_id = result["session_id"]
                        title = result["title"]
                        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                        safe_title = safe_title.replace(' ', '_')[:50]  # 限制文件名長度

                        md_filename = f"{session_id}_{safe_title}.md"
                        md_file_path = output_md_dir / md_filename

                        with open(md_file_path, 'w', encoding='utf-8') as f:
                            f.write(result["content"])

                        result["file_path"] = str(md_file_path)
                        processed_sessions.append(result)

                        logger.info(f"[任務 {task_id}] 已完成會議: {title}")
                    else:
                        failed_sessions.append(result)
                        logger.error(f"[任務 {task_id}] 處理失敗: {result.get('title', 'Unknown')} - {result.get('error', 'Unknown error')}")

                except Exception as e:
                    logger.error(f"[任務 {task_id}] 處理會議時發生異常: {e}")
                    failed_sessions.append({
                        "session_id": session.get('id', 'unknown'),
                        "title": session.get('title', 'Unknown'),
                        "error": str(e)
                    })

                # 更新進度
                current_progress = len(processed_sessions) + len(failed_sessions)
                tasks[task_id]["progress"]["current"] = current_progress
                tasks[task_id]["progress"]["current_session"] = f"已處理 {current_progress}/{len(sessions)} 個會議"

        # 生成 HTML 文件（如果需要）
        html_files = []
        if include_html and processed_sessions:
            try:
                tasks[task_id]["progress"]["current_session"] = "正在生成 HTML 文件..."

                # 使用 SSG 將 Markdown 轉換為 HTML
                batch_md_to_html(str(output_md_dir), str(output_html_dir), index_param=3)

                # 收集生成的 HTML 文件
                for html_file in output_html_dir.glob("*.html"):
                    html_files.append(str(html_file))

                logger.info(f"[任務 {task_id}] 已生成 {len(html_files)} 個 HTML 文件")

            except ImportError as e:
                logger.warning(f"[任務 {task_id}] 無法導入 SSG 模組，跳過 HTML 生成: {e}")
                # 使用備用的簡單 HTML 生成
                batch_md_to_html(str(output_md_dir), str(output_html_dir), index_param=3)
                for html_file in output_html_dir.glob("*.html"):
                    html_files.append(str(html_file))
            except Exception as e:
                logger.error(f"[任務 {task_id}] 生成 HTML 報告時發生錯誤: {e}")

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
        tasks[task_id]["end_time"] = datetime.now().isoformat()
        tasks[task_id]["error_message"] = str(e)
        tasks[task_id]["progress"]["current_session"] = f"任務失敗: {str(e)}"

# API 端點
@router.get("/seminars")
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

@router.post("/generate-batch")
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

@router.get("/status/{task_id}")
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

@router.get("/list")
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

@router.get("/files")
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

@router.get("/preview/{file_path:path}")
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

        # 根據文件類型返回適當的響應
        if full_path.suffix.lower() == '.html':
            return Response(content=content, media_type="text/html")
        else:
            return Response(content=content, media_type="text/plain")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"預覽文件失敗: {e}")
        raise HTTPException(status_code=500, detail=f"預覽文件失敗: {str(e)}")

@router.get("/download/{file_path:path}")
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
