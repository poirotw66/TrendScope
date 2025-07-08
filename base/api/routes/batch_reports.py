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
import google.generativeai as genai

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.insert(0, project_root)

from base.bigquery.client import BigQueryClient
from base.gcs.client import get_gcs_client

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

# 設置日誌
logger = logging.getLogger("trendscope-api")

# 添加項目根目錄到 Python 路徑以導入 SSG 模組
project_root_path = pathlib.Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root_path))

try:
    from base.api.modules.hugo_report import HugoReportGenerator
    hugo_generator = HugoReportGenerator()

    def batch_convert_markdown_files(md_dir, html_dir, template_style="professional",
                                    create_offline_package=True):
        """Hugo-based static site generation function with offline package support"""
        result = hugo_generator.generate_hugo_site(
            md_dir, html_dir, template_style, create_offline_package
        )

        # 為了向後兼容，如果調用者期望舊格式，返回 HTML 文件列表
        if isinstance(result, dict):
            return result
        else:
            # 如果返回的是列表（舊格式），包裝成新格式
            return {
                'html_files': result,
                'zip_file': None,
                'launcher_file': None,
                'instructions_file': None,
                'total_pages': len(result) if result else 0,
                'site_info': {}
            }

except ImportError as e:
    logger.warning(f"無法導入 Hugo 報告生成器: {e}")
    # 如果無法導入，創建一個簡單的替代函數

    def batch_convert_markdown_files(md_dir, html_dir, template_style="professional"):
        """簡單的 Markdown 到 HTML 轉換函數（Hugo 不可用時的備用方案）"""
        import markdown
        md_path = pathlib.Path(md_dir)
        html_path = pathlib.Path(html_dir)
        html_path.mkdir(parents=True, exist_ok=True)

        generated_files = []
        for md_file in md_path.glob('*.md'):
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()

            html_content = markdown.markdown(md_content)
            html_file = html_path / f"{md_file.stem}.html"

            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)

            generated_files.append(str(html_file))

        return generated_files

# 創建路由器
router = APIRouter(prefix="/reports", tags=["Batch Reports"])

# 初始化 Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# 導入共享任務管理
from base.api.shared.tasks import tasks, get_task, set_task, update_task, task_exists

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
    analysis_mode: str = "comprehensive"  # "technical", "business", "trend", "comprehensive"
    output_template: str = "professional"  # "professional", "technical", "concise", "presentation"

class BatchReportResponse(BaseModel):
    """批量報告生成響應模型"""
    task_id: str
    message: str
    status: str
    seminars_to_process: List[str]
    estimated_sessions: int
    estimated_time: Optional[str] = None

class OfflinePackageInfo(BaseModel):
    """離線分享包信息模型"""
    zip_file: str
    launcher_file: Optional[str] = None
    instructions_file: Optional[str] = None
    download_url: str
    gcs_url: Optional[str] = None  # GCS 存儲 URL
    gcs_public_url: Optional[str] = None  # GCS 公開訪問 URL
    gcs_size: Optional[int] = None  # 文件大小（字節）
    site_info: Optional[Dict[str, Any]] = None

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
def upload_zip_to_gcs(zip_file_path: str, bucket_name: str = "neo-trend-hub-documents") -> Dict[str, Any]:
    """
    上傳 ZIP 文件到 Google Cloud Storage

    Args:
        zip_file_path (str): 本地 ZIP 文件路徑
        bucket_name (str): GCS bucket 名稱，默認為 "neo-trend-hub-documents"

    Returns:
        Dict[str, Any]: 上傳結果
            - success (bool): 上傳是否成功
            - public_url (str): 公開訪問 URL（如果成功）
            - gs_url (str): GCS URL（如果成功）
            - error (str): 錯誤信息（如果失敗）
    """
    try:
        # 獲取 GCS 客戶端
        gcs_client = get_gcs_client()
        if not gcs_client:
            return {
                "success": False,
                "error": "無法初始化 GCS 客戶端，請檢查 GOOGLE_APPLICATION_CREDENTIALS 環境變量"
            }

        # 檢查 bucket 是否存在
        if not gcs_client.check_bucket_exists(bucket_name):
            return {
                "success": False,
                "error": f"GCS bucket '{bucket_name}' 不存在或無法訪問"
            }

        # 上傳 ZIP 文件到 seminar_report/ 目錄
        result = gcs_client.upload_zip_file(
            local_zip_path=zip_file_path,
            bucket_name=bucket_name,
            folder_prefix="seminar_report/"
        )

        if result["success"]:
            logger.info(f"ZIP 文件已成功上傳到 GCS: {result.get('public_url', result.get('gs_url'))}")
        else:
            logger.error(f"ZIP 文件上傳到 GCS 失敗: {result.get('error')}")

        return result

    except Exception as e:
        error_msg = f"上傳 ZIP 文件到 GCS 時發生異常: {str(e)}"
        logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg
        }

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

def generate_session_report(session_data: Dict[str, Any], analysis_mode: str = "comprehensive", output_template: str = "professional") -> Dict[str, Any]:
    """
    為單個會議生成報告

    Args:
        session_data: 會議數據
        analysis_mode: 分析模式 ("technical", "business", "trend", "comprehensive")
        output_template: 輸出樣板 ("professional", "technical", "concise", "presentation")
    """
    try:
        # 使用正確的欄位名稱
        session_id = session_data.get('conference_id', session_data.get('id', 'unknown'))
        title = session_data.get('name', session_data.get('title', 'Unknown Title'))
        seminar = session_data.get('seminar', 'Unknown Seminar')
        url = session_data.get('url', 'TEST.com')
        ppt_context = session_data.get('ppt_context', '')

        category = "主題演講"  # 默認類型

        # 根據分析模式構建不同的提示詞
        analysis_prompts = {
            "technical": """
請根據以下會議的 PPT 內容，生成一份專注於技術深度的分析報告。

重點分析方向：
1. 技術架構和實現細節
2. 核心算法和技術原理
3. 系統設計和性能優化
4. 技術挑戰和解決方案
5. 代碼實現和最佳實踐

請深入分析技術實現細節，適合技術專家閱讀。
""",
            "business": """
請根據以下會議的 PPT 內容，生成一份專注於商業價值的分析報告。

重點分析方向：
1. 商業應用場景和價值主張
2. 市場機會和競爭優勢
3. 投資回報和成本效益
4. 商業模式和盈利潛力
5. 行業影響和市場前景

請重點分析商業價值和市場應用，適合商業決策者閱讀。
""",
            "trend": """
請根據以下會議的 PPT 內容，生成一份專注於技術趨勢的洞察報告。

重點分析方向：
1. 技術發展趨勢和未來方向
2. 行業變革和創新機會
3. 新興技術和前沿研究
4. 技術演進路徑和時間線
5. 對未來技術生態的影響

請重點分析技術趨勢和未來發展，適合戰略規劃者閱讀。
""",
            "comprehensive": """
請根據以下會議的 PPT 內容，生成一份全方位的綜合分析報告。

重點分析方向：
1. 會議概述和核心內容
2. 技術要點和實現細節
3. 商業價值和應用場景
4. 創新亮點和技術突破
5. 趨勢洞察和未來展望

請提供技術、商業和趨勢的全面分析，適合各類讀者。
"""
        }

        # 構建提示詞
        analysis_instruction = analysis_prompts.get(analysis_mode, analysis_prompts["comprehensive"])

        prompt = f"""
{analysis_instruction}

會議信息：
- 標題：{title}
- 研討會：{seminar}
- 類型：{category}

PPT 內容：
{ppt_context}

請用繁體中文撰寫，內容要專業且具有深度。
"""

        # 調用 Gemini API
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)

        if response and response.text:
            report_content = response.text
        else:
            report_content = f"無法生成 {title} 的報告內容"

        # 根據輸出樣板構建不同格式的 Markdown 報告
        template_formats = {
            "professional": f"""# {title}

## 會議資訊
- **研討會：** {seminar}
- **類型：** {category}
- **來源：** [{url}]({url})

---

## 報告內容

{report_content}

---

<div style="text-align: center; color: #666; font-size: 0.9em; margin-top: 2em;">
<em>本報告由 TrendScope 自動生成 | 生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em>
</div>
""",
            "technical": f"""# 技術分析報告：{title}

```yaml
會議資訊:
  研討會: {seminar}
  類型: {category}
  來源: {url}
```

## 📋 執行摘要

{report_content}

## 🔗 參考資料
- 原始來源：[{url}]({url})

---
*技術文檔 | TrendScope 自動生成*
""",
            "concise": f"""# {title}

**{seminar}** | {category}

{report_content}

[查看原始資料]({url})
""",
            "presentation": f"""<div style="text-align: center;">

# 🎯 {title}

### 📅 {seminar}
### 📋 {category}

</div>

---

## 📊 重點內容

{report_content}

---

<div style="text-align: center;">

### 🔗 更多資訊
[點擊查看原始資料]({url})

<small>*由 TrendScope 自動生成*</small>

</div>
"""
        }

        # 選擇對應的樣板格式
        markdown_content = template_formats.get(output_template, template_formats["professional"])

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
                         include_html: bool, output_format: str, analysis_mode: str = "comprehensive",
                         output_template: str = "professional"):
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
                executor.submit(generate_session_report, session, analysis_mode, output_template): (session, i)
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
        zip_file_path = None
        launcher_file_path = None
        instructions_file_path = None
        site_info = {}

        if include_html and processed_sessions:
            try:
                tasks[task_id]["progress"]["current_session"] = "正在生成 HTML 文件..."

                # 使用 Hugo SSG 將 Markdown 轉換為靜態網站，傳遞樣板參數
                hugo_result = batch_convert_markdown_files(
                    str(output_md_dir),
                    str(output_html_dir),
                    template_style=output_template,
                    create_offline_package=True
                )

                # 處理新的返回格式
                if isinstance(hugo_result, dict):
                    html_files = hugo_result.get('html_files', [])
                    zip_file_path = hugo_result.get('zip_file')
                    launcher_file_path = hugo_result.get('launcher_file')
                    instructions_file_path = hugo_result.get('instructions_file')
                    site_info = hugo_result.get('site_info', {})
                    total_pages = hugo_result.get('total_pages', 0)

                    logger.info(f"[任務 {task_id}] Hugo 生成了 {total_pages} 個頁面")
                    if zip_file_path:
                        logger.info(f"[任務 {task_id}] 離線分享包已創建: {zip_file_path}")

                        # 上傳 ZIP 文件到 GCS
                        tasks[task_id]["progress"]["current_session"] = "正在上傳到 Google Cloud Storage..."
                        gcs_upload_result = upload_zip_to_gcs(zip_file_path)

                        if gcs_upload_result["success"]:
                            logger.info(f"[任務 {task_id}] ZIP 文件已成功上傳到 GCS: {gcs_upload_result.get('public_url')}")
                        else:
                            logger.warning(f"[任務 {task_id}] ZIP 文件上傳到 GCS 失敗: {gcs_upload_result.get('error')}")
                            # 上傳失敗不影響整個任務的完成
                else:
                    # 向後兼容舊格式
                    html_files = hugo_result if hugo_result else []
                    logger.info(f"[任務 {task_id}] Hugo 生成了 {len(html_files)} 個文件")

                # 收集生成的 HTML 文件（如果使用舊格式）
                if not html_files:
                    for html_file in output_html_dir.glob("*.html"):
                        html_files.append(str(html_file))

                logger.info(f"[任務 {task_id}] 已生成 {len(html_files)} 個 HTML 文件")

            except ImportError as e:
                logger.warning(f"[任務 {task_id}] 無法導入 SSG 模組，跳過 HTML 生成: {e}")
                # 使用備用的簡單 HTML 生成
                backup_result = batch_convert_markdown_files(
                    str(output_md_dir),
                    str(output_html_dir),
                    template_style=output_template,
                    create_offline_package=False
                )
                if isinstance(backup_result, dict):
                    html_files = backup_result.get('html_files', [])
                else:
                    html_files = backup_result if backup_result else []

                for html_file in output_html_dir.glob("*.html"):
                    if str(html_file) not in html_files:
                        html_files.append(str(html_file))
            except Exception as e:
                logger.error(f"[任務 {task_id}] 生成 HTML 報告時發生錯誤: {e}")

        # 完成任務
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["end_time"] = datetime.now().isoformat()
        tasks[task_id]["progress"]["current_session"] = "完成"

        # 構建結果信息
        results = {
            "processed_sessions": len(processed_sessions),
            "failed_sessions": len(failed_sessions),
            "output_directory": str(output_base_dir),
            "md_directory": str(output_md_dir),
            "html_directory": str(output_html_dir) if include_html else None,
            "processed_files": [s["file_path"] for s in processed_sessions if s["status"] == "completed"],
            "failed_files": failed_sessions,
            "html_files": html_files if include_html else []
        }

        # 添加離線分享包信息
        if zip_file_path:
            offline_package = {
                "zip_file": zip_file_path,
                "launcher_file": launcher_file_path,
                "instructions_file": instructions_file_path,
                "download_url": f"/reports/download-zip/{pathlib.Path(zip_file_path).name}",
                "site_info": site_info
            }

            # 如果有GCS上傳結果，添加GCS URL
            if 'gcs_upload_result' in locals() and gcs_upload_result["success"]:
                offline_package["gcs_url"] = gcs_upload_result.get("gs_url")
                offline_package["gcs_public_url"] = gcs_upload_result.get("public_url")
                offline_package["gcs_size"] = gcs_upload_result.get("size")
                logger.info(f"[任務 {task_id}] GCS URL 已添加到結果中: {gcs_upload_result.get('public_url')}")

            results["offline_package"] = offline_package

        tasks[task_id]["results"] = results

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
            request.output_format,
            request.analysis_mode,
            request.output_template
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

@router.get("/{task_id}/download-zip")
def download_task_zip_file(task_id: str):
    """下載指定任務的 ZIP 檔案

    Args:
        task_id: 任務 ID

    Returns:
        ZIP 檔案下載響應
    """
    try:
        # 檢查任務是否存在
        if task_id not in tasks:
            raise HTTPException(status_code=404, detail="任務不存在")

        task_data = tasks[task_id]

        # 檢查任務是否完成
        if task_data.get("status") != "completed":
            raise HTTPException(status_code=400, detail="任務尚未完成")

        # 獲取任務結果中的 ZIP 文件路徑
        results = task_data.get("results", {})
        zip_file_path = results.get("zip_file")

        if not zip_file_path:
            raise HTTPException(status_code=404, detail="該任務沒有生成 ZIP 文件")

        zip_path = pathlib.Path(zip_file_path)
        if not zip_path.exists():
            raise HTTPException(status_code=404, detail="ZIP 文件不存在")

        # 生成下載文件名
        filename = zip_path.name

        # 返回文件下載響應，設置適當的 HTTP 響應頭
        return FileResponse(
            path=str(zip_path),
            filename=filename,
            media_type='application/zip',
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Cache-Control": "no-cache"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"下載任務 ZIP 文件時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"下載 ZIP 文件時發生錯誤: {str(e)}")

@router.get("/download-zip/{zip_filename}")
def download_zip_file(zip_filename: str):
    """下載離線分享包 ZIP 文件（舊版本兼容）"""
    try:
        # URL 解碼文件名
        import urllib.parse
        decoded_filename = urllib.parse.unquote(zip_filename)

        logger.info(f"嘗試下載 ZIP 文件: {decoded_filename} (原始: {zip_filename})")

        # 在 reports 目錄中查找 ZIP 文件（使用絕對路徑）
        # 獲取項目根目錄
        current_dir = pathlib.Path.cwd()
        project_root = current_dir
        if current_dir.name == "backend":
            project_root = current_dir.parent

        reports_dir = project_root / "reports"
        zip_file_path = None

        logger.info(f"當前工作目錄: {current_dir}")
        logger.info(f"項目根目錄: {project_root}")
        logger.info(f"reports 目錄: {reports_dir}")
        logger.info(f"reports 目錄是否存在: {reports_dir.exists()}")

        # 搜索所有批量報告目錄中的 ZIP 文件
        batch_dirs = list(reports_dir.glob("batch_*")) if reports_dir.exists() else []
        logger.info(f"找到的批量目錄: {batch_dirs}")

        for batch_dir in batch_dirs:
            # 嘗試原始文件名和解碼後的文件名
            for filename in [zip_filename, decoded_filename]:
                potential_zip = batch_dir / filename
                logger.debug(f"檢查文件: {potential_zip}")
                if potential_zip.exists():
                    zip_file_path = potential_zip
                    logger.info(f"找到 ZIP 文件: {zip_file_path}")
                    break
            if zip_file_path:
                break

        if not zip_file_path or not zip_file_path.exists():
            # 記錄調試信息
            logger.warning(f"未找到 ZIP 文件: {decoded_filename}")
            logger.warning(f"搜索的目錄: {batch_dirs}")
            raise HTTPException(status_code=404, detail="ZIP 文件不存在")

        # 返回文件下載響應（處理中文文件名編碼問題）
        # 對中文文件名進行 RFC 5987 編碼
        import urllib.parse
        encoded_filename_rfc5987 = urllib.parse.quote(decoded_filename.encode('utf-8'))

        return FileResponse(
            path=str(zip_file_path),
            filename=decoded_filename,
            media_type='application/zip',
            headers={
                "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename_rfc5987}",
                "Cache-Control": "no-cache",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "*"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"下載 ZIP 文件時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"下載 ZIP 文件時發生錯誤: {str(e)}")


@router.get("/list-zip-files")
def list_zip_files():
    """列出所有可用的 ZIP 文件"""
    try:
        # 獲取項目根目錄
        current_dir = pathlib.Path.cwd()
        project_root = current_dir
        if current_dir.name == "backend":
            project_root = current_dir.parent

        reports_dir = project_root / "reports"
        zip_files = []

        if reports_dir.exists():
            # 搜索所有批量報告目錄中的 ZIP 文件
            for batch_dir in reports_dir.glob("batch_*"):
                for zip_file in batch_dir.glob("*.zip"):
                    zip_files.append(zip_file.name)

        logger.info(f"找到 {len(zip_files)} 個 ZIP 文件")
        return zip_files

    except Exception as e:
        logger.error(f"列出 ZIP 文件時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"列出 ZIP 文件時發生錯誤: {e}")

@router.get("/gcs-status")
def get_gcs_status():
    """獲取 Google Cloud Storage 連接狀態"""
    try:
        # 檢查環境變量
        credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

        status_info = {
            "gcs_available": False,
            "credentials_configured": bool(credentials_path),
            "project_id_configured": bool(project_id),
            "bucket_accessible": False,
            "bucket_name": "neo-trend-hub-documents",
            "error_message": None
        }

        if not credentials_path:
            status_info["error_message"] = "GOOGLE_APPLICATION_CREDENTIALS 環境變量未設置"
            return status_info

        if not os.path.exists(credentials_path):
            status_info["error_message"] = f"憑證文件不存在: {credentials_path}"
            return status_info

        # 嘗試初始化 GCS 客戶端
        gcs_client = get_gcs_client()
        if not gcs_client:
            status_info["error_message"] = "無法初始化 GCS 客戶端"
            return status_info

        status_info["gcs_available"] = True

        # 檢查 bucket 訪問權限
        bucket_name = "neo-trend-hub-documents"
        if gcs_client.check_bucket_exists(bucket_name):
            status_info["bucket_accessible"] = True
        else:
            status_info["error_message"] = f"無法訪問 bucket: {bucket_name}"

        return status_info

    except Exception as e:
        logger.error(f"檢查 GCS 狀態時發生錯誤: {e}")
        return {
            "gcs_available": False,
            "credentials_configured": False,
            "project_id_configured": False,
            "bucket_accessible": False,
            "bucket_name": "neo-trend-hub-documents",
            "error_message": f"檢查 GCS 狀態時發生錯誤: {str(e)}"
        }
