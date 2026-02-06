"""
Enhanced Batch Report Generation API Routes
完全重構的批量報告生成系統 - 符合 plan.md 規範

Features:
- Phase 1: LLM Trend Analysis (第一階段：LLM 趨勢分析)
- Phase 2: Automatic Tagging System (第二階段：自動標記系統)
- Phase 3: Three-Tier Hugo Site Generation (第三階段：三階層 Hugo 網站建構)
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

from base.bigquery.client import BigQueryClient
from base.bigquery.report_archive_manager import ReportArchiveManager
from base.gcs.client import get_gcs_client
from config.settings import settings

# 設置日誌
logger = logging.getLogger("NeoTrendHub-api")

# 依賴項：獲取 BigQuery 客戶端
def get_bigquery_client():
    """獲取 BigQuery 客戶端"""
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

# 導入報告生成模組（專注於 Markdown 生成）
try:
    from base.api.modules.enhanced_report_generator import EnhancedReportGenerator
    from base.api.modules.trend_analyzer import TrendAnalyzer
    from base.api.modules.trend_recommendation_engine import TrendRecommendationEngine

    # 初始化核心組件
    enhanced_generator = EnhancedReportGenerator()
    trend_analyzer = TrendAnalyzer()
    recommendation_engine = TrendRecommendationEngine()

    logger.info("✅ 成功導入報告生成模組（專注於 Markdown 生成）")

except ImportError as e:
    logger.error(f"❌ 無法導入報告生成模組: {e}")
    logger.error("請確保所有必要的模組都已正確安裝")

    # 創建備用實例
    enhanced_generator = None
    trend_analyzer = None
    recommendation_engine = None

    def batch_convert_markdown_files(md_dir, html_dir, template_style="professional"):
        """備用 Markdown 到 HTML 轉換函數"""
        logger.warning("使用備用 Markdown 轉換功能")
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
genai.configure(api_key=settings.gemini_api_key)

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
    enable_trend_analysis: bool = True  # 啟用 LLM 趨勢分析 (plan.md 功能)
    enable_recommendations: bool = False  # 啟用智慧推薦引擎

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
def upload_zip_to_gcs(zip_file_path: str, bucket_name: str = None) -> Dict[str, Any]:
    """
    上傳 ZIP 文件到 Google Cloud Storage

    Args:
        zip_file_path (str): 本地 ZIP 文件路徑
        bucket_name (str): GCS bucket 名稱，如果為 None 則從環境變量獲取

    Returns:
        Dict[str, Any]: 上傳結果
            - success (bool): 上傳是否成功
            - public_url (str): 公開訪問 URL（如果成功）
            - gs_url (str): GCS URL（如果成功）
            - error (str): 錯誤信息（如果失敗）
    """
    try:
        # 獲取 bucket 名稱
        if bucket_name is None:
            bucket_name = os.environ.get("GCS_BUCKET_NAME", "neo-trend-hub-documents")

        # 獲取 GCS 客戶端
        gcs_client = get_gcs_client()
        if not gcs_client:
            return {
                "success": False,
                "error": "無法初始化 GCS 客戶端，請檢查 GOOGLE_APPLICATION_CREDENTIALS 環境變量"
            }

        # 檢查 bucket 是否存在（使用更詳細的錯誤處理）
        try:
            bucket_accessible = gcs_client.check_bucket_exists(bucket_name)
            if not bucket_accessible:
                return {
                    "success": False,
                    "error": f"GCS bucket '{bucket_name}' 不存在或無法訪問",
                    "suggestion": "請運行 'python fix_gcs_permissions.py' 修復權限問題"
                }
        except Exception as bucket_error:
            # 提供更詳細的錯誤信息和修復建議
            error_msg = str(bucket_error)
            if "storage.buckets.get" in error_msg:
                return {
                    "success": False,
                    "error": f"服務帳戶缺少 Storage 權限: {error_msg}",
                    "suggestion": "需要為服務帳戶添加 'roles/storage.objectAdmin' 和 'roles/storage.legacyBucketReader' 權限",
                    "fix_command": f"gcloud projects add-iam-policy-binding {gcs_client.project_id} --member='serviceAccount:{gcs_client.credentials.service_account_email}' --role='roles/storage.objectAdmin'"
                }
            else:
                return {
                    "success": False,
                    "error": f"GCS bucket 檢查失敗: {error_msg}",
                    "suggestion": "請檢查 bucket 名稱和權限配置"
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
<em>本報告由 NeoTrendHub 自動生成 | 生成時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</em>
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
*技術文檔 | NeoTrendHub 自動生成*
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

<small>*由 NeoTrendHub 自動生成*</small>

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

def _initialize_task(task_id: str) -> BigQueryClient:
    """初始化任務狀態並獲取 BigQuery 客戶端"""
    tasks[task_id]["status"] = "running"
    tasks[task_id]["progress"] = {"current": 0, "total": 0, "current_session": "初始化中..."}

    bq_client = get_bigquery_client()
    if not bq_client:
        raise Exception("無法連接到 BigQuery")

    return bq_client

def _setup_output_directories(include_html: bool) -> tuple:
    """創建輸出目錄結構"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_base_dir = pathlib.Path("reports") / f"batch_{timestamp}"
    output_md_dir = output_base_dir / "md"
    output_html_dir = output_base_dir / "html"

    output_md_dir.mkdir(parents=True, exist_ok=True)
    if include_html:
        output_html_dir.mkdir(parents=True, exist_ok=True)

    return output_base_dir, output_md_dir, output_html_dir

def _handle_empty_sessions(task_id: str):
    """處理沒有找到會議的情況"""
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["progress"]["current_session"] = "沒有找到符合條件的會議"
    tasks[task_id]["end_time"] = datetime.now().isoformat()
    tasks[task_id]["results"] = {"processed_sessions": 0, "generated_reports": 0}

def _save_markdown_file(result: Dict[str, Any], output_md_dir: pathlib.Path) -> Dict[str, Any]:
    """保存 Markdown 文件並返回更新的結果"""
    session_id = result["session_id"]
    title = result["title"]
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')[:50]  # 限制文件名長度

    md_filename = f"{session_id}_{safe_title}.md"
    md_file_path = output_md_dir / md_filename

    with open(md_file_path, 'w', encoding='utf-8') as f:
        f.write(result["content"])

    result["file_path"] = str(md_file_path)
    return result

def _process_sessions_parallel(task_id: str, sessions: List[Dict], analysis_mode: str,
                              output_template: str, output_md_dir: pathlib.Path) -> tuple:
    """使用線程池並行處理會議數據"""
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
                    result = _save_markdown_file(result, output_md_dir)
                    processed_sessions.append(result)
                    logger.info(f"[任務 {task_id}] 已完成會議: {result['title']}")
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

    return processed_sessions, failed_sessions

def _generate_html_files(task_id: str, output_md_dir: pathlib.Path, output_html_dir: pathlib.Path,
                        output_template: str) -> Dict[str, Any]:
    """生成 HTML 文件"""
    try:
        tasks[task_id]["progress"]["current_session"] = "正在生成 HTML 文件..."

        # 使用 Hugo SSG 將 Markdown 轉換為靜態網站
        hugo_result = batch_convert_markdown_files(
            str(output_md_dir),
            str(output_html_dir),
            template_style=output_template,
            create_offline_package=True
        )

        # 處理返回格式
        if isinstance(hugo_result, dict):
            return hugo_result
        else:
            # 向後兼容舊格式
            return {
                'html_files': hugo_result if hugo_result else [],
                'zip_file': None,
                'launcher_file': None,
                'instructions_file': None,
                'site_info': {},
                'total_pages': len(hugo_result) if hugo_result else 0
            }

    except ImportError as e:
        logger.warning(f"[任務 {task_id}] 無法導入 SSG 模組，使用備用方案: {e}")
        # 使用備用的簡單 HTML 生成
        backup_result = batch_convert_markdown_files(
            str(output_md_dir),
            str(output_html_dir),
            template_style=output_template,
            create_offline_package=False
        )

        html_files = []
        if isinstance(backup_result, dict):
            html_files = backup_result.get('html_files', [])
        else:
            html_files = backup_result if backup_result else []

        # 收集所有HTML文件
        for html_file in output_html_dir.glob("*.html"):
            if str(html_file) not in html_files:
                html_files.append(str(html_file))

        return {
            'html_files': html_files,
            'zip_file': None,
            'launcher_file': None,
            'instructions_file': None,
            'site_info': {},
            'total_pages': len(html_files)
        }

def _handle_gcs_upload(task_id: str, zip_file_path: str) -> Dict[str, Any]:
    """處理 GCS 上傳"""
    enable_gcs_upload = os.environ.get("ENABLE_GCS_UPLOAD", "true").lower() == "true"

    if enable_gcs_upload:
        tasks[task_id]["progress"]["current_session"] = "正在上傳到 Google Cloud Storage..."
        gcs_upload_result = upload_zip_to_gcs(zip_file_path)

        if gcs_upload_result["success"]:
            logger.info(f"[任務 {task_id}] ZIP 文件已成功上傳到 GCS: {gcs_upload_result.get('public_url')}")
        else:
            logger.warning(f"[任務 {task_id}] ZIP 文件上傳到 GCS 失敗: {gcs_upload_result.get('error')}")

        return gcs_upload_result
    else:
        logger.info(f"[任務 {task_id}] GCS 上傳已禁用，跳過雲端備份")
        return {"success": False, "disabled": True}

def _generate_enhanced_reports(task_id: str, sessions: List[Dict],
                              output_md_dir: pathlib.Path,
                              analysis_mode: str, output_template: str,
                              enable_trend_analysis: bool = True,
                              enable_recommendations: bool = False) -> Dict[str, Any]:
    """
    生成符合 plan.md 規劃的完整三階層報告結構

    Phase 1: LLM Trend Analysis (第一階段：LLM 趨勢分析)
    Phase 2: Automatic Tagging System (第二階段：自動標記系統)
    Phase 3: Three-Tier Markdown Generation (第三階段：三階層 Markdown 文件生成)
    """
    try:
        if not enhanced_generator:
            raise ImportError("增強報告生成器未正確初始化")

        logger.info(f"[任務 {task_id}] 🚀 開始執行增強報告生成流程...")

        # Phase 1: 更新進度 - 趨勢分析階段
        tasks[task_id]["progress"]["current_session"] = "第一階段：正在執行 LLM 趨勢分析..."
        logger.info(f"[任務 {task_id}] 📊 Phase 1: LLM 趨勢分析開始")

        # Phase 2: 更新進度 - 自動標記階段
        tasks[task_id]["progress"]["current_session"] = "第二階段：正在執行自動標記系統..."
        logger.info(f"[任務 {task_id}] 🏷️ Phase 2: 自動標記系統開始")

        # Phase 3: 更新進度 - Markdown 生成階段
        tasks[task_id]["progress"]["current_session"] = "第三階段：正在生成三階層 Markdown 文件..."
        logger.info(f"[任務 {task_id}] 📝 Phase 3: 三階層 Markdown 文件生成開始")

        # 執行完整的三階層報告生成
        enhanced_result = enhanced_generator.generate_comprehensive_reports(
            sessions=sessions,
            output_dir=output_md_dir,
            analysis_mode=analysis_mode,
            output_template=output_template,
            enable_trend_analysis=enable_trend_analysis,
            enable_recommendations=enable_recommendations
        )

        # 驗證生成結果
        if not enhanced_result:
            raise Exception("增強報告生成失敗：返回空結果")

        # 統計處理結果
        total_sessions = len(sessions)
        session_files = enhanced_result.get('session_files', [])
        trend_files = enhanced_result.get('trend_files', [])
        trends_analysis_file = enhanced_result.get('trends_analysis_file')
        index_file = enhanced_result.get('index_file')

        processed_count = len(session_files)
        failed_count = total_sessions - processed_count

        logger.info(f"[任務 {task_id}] ✅ 增強報告生成完成:")
        logger.info(f"  📄 趨勢分析文件: {trends_analysis_file}")
        logger.info(f"  📂 趨勢分類文件: {len(trend_files)} 個")
        logger.info(f"  📋 會議詳細文件: {len(session_files)} 個")
        logger.info(f"  🏠 首頁文件: {index_file}")
        logger.info(f"  ✅ 成功處理: {processed_count}/{total_sessions} 個會議")

        # 構建處理結果
        processed_sessions = []
        failed_sessions = []

        # 為每個成功處理的會議創建結果記錄
        for i, session_file in enumerate(session_files):
            if i < len(sessions):
                session = sessions[i]
                processed_sessions.append({
                    "status": "completed",
                    "session_id": session.get('conference_id', session.get('id', f'session_{i}')),
                    "title": session.get('name', 'Unknown'),
                    "file_path": session_file
                })

        # 為失敗的會議創建失敗記錄
        for i in range(processed_count, total_sessions):
            if i < len(sessions):
                session = sessions[i]
                failed_sessions.append({
                    "session_id": session.get('conference_id', session.get('id', f'session_{i}')),
                    "title": session.get('name', 'Unknown'),
                    "error": "增強報告生成過程中處理失敗"
                })

        logger.info(f"[任務 {task_id}] 增強報告生成完成: {processed_count} 成功, {failed_count} 失敗")
        logger.info(f"[任務 {task_id}] 生成文件統計: {enhanced_result.get('total_files', 0)} 個文件")

        return {
            'processed_sessions': processed_sessions,
            'failed_sessions': failed_sessions,
            'enhanced_result': enhanced_result,
            'statistics': enhanced_result.get('statistics', {})
        }

    except Exception as e:
        logger.error(f"[任務 {task_id}] 增強報告生成失敗: {e}")

        # 回退到原有的並行處理方式
        logger.info(f"[任務 {task_id}] 回退到標準報告生成方式...")
        processed_sessions, failed_sessions = _process_sessions_parallel(
            task_id, sessions, analysis_mode, output_template, output_md_dir
        )

        return {
            'processed_sessions': processed_sessions,
            'failed_sessions': failed_sessions,
            'enhanced_result': None,
            'fallback_used': True
        }

def _create_file_tracking_record(task_id: str, bq_client: BigQueryClient, output_base_dir: pathlib.Path,
                                zip_file_path: str, seminars: List[str], processed_sessions: List,
                                analysis_mode: str, output_template: str, gcs_upload_result: Dict,
                                site_info: Dict, total_pages: int, launcher_file_path: str,
                                instructions_file_path: str, enable_gcs_upload: bool) -> str:
    """創建檔案追蹤記錄"""
    try:
        tasks[task_id]["progress"]["current_session"] = "正在記錄檔案追蹤信息..."
        archive_manager = ReportArchiveManager(bq_client)

        # 創建檔案追蹤記錄（不使用metadata，因為表結構中沒有）
        created_task_id = archive_manager.create_archive_record(
            task_id=task_id,
            batch_id=output_base_dir.name,
            zip_file_path=zip_file_path,
            seminars=seminars or [],
            session_count=len(processed_sessions),
            analysis_mode=analysis_mode,
            output_template=output_template,
            gcs_info=gcs_upload_result if gcs_upload_result.get("success") else None,
            metadata=None  # 不使用metadata
        )

        logger.info(f"[任務 {task_id}] 檔案追蹤記錄已創建: {created_task_id}")
        return created_task_id

    except Exception as archive_error:
        logger.warning(f"[任務 {task_id}] 創建檔案追蹤記錄失敗: {archive_error}")
        return ""

def _generate_html_and_track_files(task_id: str, include_html: bool, processed_sessions: List,
                                  output_md_dir: pathlib.Path, output_html_dir: pathlib.Path,
                                  output_base_dir: pathlib.Path, output_template: str,
                                  seminars: List[str], analysis_mode: str,
                                  bq_client: BigQueryClient) -> Dict[str, Any]:
    """生成 HTML 文件並處理檔案追蹤"""
    result = {
        'html_files': [],
        'zip_file_path': None,
        'launcher_file_path': None,
        'instructions_file_path': None,
        'site_info': {},
        'gcs_upload_result': {"success": False},
        'created_task_id': ""
    }

    if not (include_html and processed_sessions):
        return result

    try:
        # 生成 HTML 文件
        hugo_result = _generate_html_files(task_id, output_md_dir, output_html_dir, output_template)

        result['html_files'] = hugo_result.get('html_files', [])
        result['zip_file_path'] = hugo_result.get('zip_file')
        result['launcher_file_path'] = hugo_result.get('launcher_file')
        result['instructions_file_path'] = hugo_result.get('instructions_file')
        result['site_info'] = hugo_result.get('site_info', {})
        total_pages = hugo_result.get('total_pages', 0)

        logger.info(f"[任務 {task_id}] Hugo 生成了 {total_pages} 個頁面")

        # 處理 ZIP 文件上傳和追蹤
        if result['zip_file_path']:
            logger.info(f"[任務 {task_id}] 離線分享包已創建: {result['zip_file_path']}")

            # GCS 上傳
            result['gcs_upload_result'] = _handle_gcs_upload(task_id, result['zip_file_path'])

            # 檔案追蹤記錄
            result['created_task_id'] = _create_file_tracking_record(
                task_id, bq_client, output_base_dir, result['zip_file_path'],
                seminars, processed_sessions, analysis_mode, output_template,
                result['gcs_upload_result'], result['site_info'], total_pages,
                result['launcher_file_path'], result['instructions_file_path'],
                os.environ.get("ENABLE_GCS_UPLOAD", "true").lower() == "true"
            )

        logger.info(f"[任務 {task_id}] 已生成 {len(result['html_files'])} 個 HTML 文件")

    except Exception as e:
        logger.error(f"[任務 {task_id}] 生成 HTML 報告時發生錯誤: {e}")

    return result

def _build_task_results(processed_sessions: List, failed_sessions: List, output_base_dir: pathlib.Path,
                       output_md_dir: pathlib.Path, output_html_dir: pathlib.Path, include_html: bool,
                       html_generation_result: Dict[str, Any], enhanced_result: Dict[str, Any] = None) -> Dict[str, Any]:
    """構建任務結果"""
    results = {
        "processed_sessions": len(processed_sessions),
        "failed_sessions": len(failed_sessions),
        "output_directory": str(output_base_dir),
        "md_directory": str(output_md_dir),
        "html_directory": str(output_html_dir) if include_html else None,
        "processed_files": [s["file_path"] for s in processed_sessions if s.get("status") == "completed"],
        "failed_files": failed_sessions,
        "html_files": html_generation_result.get('html_files', []) if include_html else []
    }

    # 添加增強報告的特殊信息
    if enhanced_result and enhanced_result.get('enhanced_result'):
        enhanced_data = enhanced_result['enhanced_result']
        results.update({
            "enhanced_report": True,
            "trends_analysis_file": enhanced_data.get('trends_analysis_file'),
            "trend_files": enhanced_data.get('trend_files', []),
            "session_files": enhanced_data.get('session_files', []),
            "index_file": enhanced_data.get('index_file'),
            "trends": enhanced_data.get('trends', []),
            "total_trends": len(enhanced_data.get('trends', [])),
            "statistics": enhanced_data.get('statistics', {}),
            "report_structure": "three_tier_architecture"  # 標記為三階層架構
        })
    else:
        results["enhanced_report"] = False
        if enhanced_result and enhanced_result.get('fallback_used'):
            results["fallback_used"] = True

    # 添加離線分享包信息
    zip_file_path = html_generation_result.get('zip_file_path')
    if zip_file_path:
        offline_package = {
            "zip_file": zip_file_path,
            "launcher_file": html_generation_result.get('launcher_file_path'),
            "instructions_file": html_generation_result.get('instructions_file_path'),
            "download_url": f"/reports/download-zip/{pathlib.Path(zip_file_path).name}",
            "site_info": html_generation_result.get('site_info', {})
        }

        # 添加GCS信息
        gcs_upload_result = html_generation_result.get('gcs_upload_result', {})
        if gcs_upload_result.get("success"):
            offline_package["gcs_url"] = gcs_upload_result.get("gs_url")
            offline_package["gcs_public_url"] = gcs_upload_result.get("public_url")
            offline_package["gcs_size"] = gcs_upload_result.get("size")

        # 添加檔案追蹤信息
        created_task_id = html_generation_result.get('created_task_id')
        if created_task_id:
            offline_package["batch_id"] = output_base_dir.name
            offline_package["archive_api_url"] = f"/reports/archives/task/{created_task_id}"

        results["offline_package"] = offline_package

    return results

def _complete_task(task_id: str, results: Dict[str, Any]):
    """完成任務並設置最終狀態"""
    tasks[task_id]["status"] = "completed"
    tasks[task_id]["end_time"] = datetime.now().isoformat()
    tasks[task_id]["progress"]["current_session"] = "完成"
    tasks[task_id]["results"] = results

    processed_count = results["processed_sessions"]
    failed_count = results["failed_sessions"]
    logger.info(f"[任務 {task_id}] 批量報告生成完成: {processed_count} 成功, {failed_count} 失敗")

def _handle_task_failure(task_id: str, error: Exception):
    """處理任務失敗"""
    logger.error(f"[任務 {task_id}] 批量報告生成任務失敗: {error}")
    tasks[task_id]["status"] = "failed"
    tasks[task_id]["end_time"] = datetime.now().isoformat()
    tasks[task_id]["error_message"] = str(error)
    tasks[task_id]["progress"]["current_session"] = f"任務失敗: {str(error)}"

def run_batch_report_task(task_id: str, seminars: Optional[List[str]], limit: Optional[int],
                         include_html: bool, output_format: str, analysis_mode: str = "comprehensive",
                         output_template: str = "professional", enable_trend_analysis: bool = True,
                         enable_recommendations: bool = False):
    """
    執行增強版批量報告生成任務 - 完全符合 plan.md 規範

    工作流程：
    1. 資料提取 - 從 BigQuery 獲取研討會資料
    2. LLM 趨勢分析 - 產生 trends-analysis.md
    3. LLM 標記分類 - 為每場研討會標注趨勢類別
    4. Markdown 生成 - 產生趨勢分類和研討會詳細頁面的 md 檔案
    5. Hugo 建構 - 使用 SSG 生成完整靜態網站
    """
    try:
        logger.info(f"[任務 {task_id}] 🚀 開始執行增強版批量報告生成任務")
        logger.info(f"[任務 {task_id}] 📋 配置: 分析模式={analysis_mode}, 模板={output_template}")
        logger.info(f"[任務 {task_id}] 🔧 功能: 趨勢分析={enable_trend_analysis}, 推薦={enable_recommendations}")

        # 1. 初始化任務和 BigQuery 客戶端
        logger.info(f"[任務 {task_id}] 📊 步驟 1: 初始化任務和資料連接")
        bq_client = _initialize_task(task_id)

        # 2. 從 BigQuery 獲取會議數據
        logger.info(f"[任務 {task_id}] 📥 步驟 2: 從 BigQuery 提取研討會資料")
        sessions = get_sessions_from_bigquery_for_reports(bq_client, seminars, limit)
        if not sessions:
            _handle_empty_sessions(task_id)
            return

        logger.info(f"[任務 {task_id}] ✅ 成功獲取 {len(sessions)} 個會議資料")

        # 3. 設置輸出目錄結構
        logger.info(f"[任務 {task_id}] 📁 步驟 3: 設置輸出目錄結構")
        output_base_dir, output_md_dir, output_html_dir = _setup_output_directories(include_html)

        # 4. 更新任務進度
        tasks[task_id]["progress"]["total"] = len(sessions)
        tasks[task_id]["progress"]["current_session"] = "準備執行三階段報告生成流程..."

        # 5. 執行增強報告生成（三階段流程）
        logger.info(f"[任務 {task_id}] 🔄 步驟 4: 執行三階段增強報告生成")
        enhanced_result = _generate_enhanced_reports(
            task_id, sessions, output_md_dir, analysis_mode, output_template,
            enable_trend_analysis, enable_recommendations
        )

        processed_sessions = enhanced_result.get('processed_sessions', [])
        failed_sessions = enhanced_result.get('failed_sessions', [])

        logger.info(f"[任務 {task_id}] ✅ 增強報告生成完成: {len(processed_sessions)} 成功, {len(failed_sessions)} 失敗")

        # 6. 生成 Hugo 靜態網站和處理檔案追蹤
        logger.info(f"[任務 {task_id}] 🏗️ 步驟 5: 生成 Hugo 靜態網站")
        html_generation_result = _generate_html_and_track_files(
            task_id, include_html, processed_sessions, output_md_dir, output_html_dir,
            output_base_dir, output_template, seminars, analysis_mode, bq_client
        )

        # 7. 構建最終結果並完成任務
        logger.info(f"[任務 {task_id}] 📦 步驟 6: 構建最終結果")
        results = _build_task_results(
            processed_sessions, failed_sessions, output_base_dir,
            output_md_dir, output_html_dir, include_html, html_generation_result, enhanced_result
        )

        _complete_task(task_id, results)
        logger.info(f"[任務 {task_id}] 🎉 增強版批量報告生成任務完成!")

    except Exception as e:
        logger.error(f"[任務 {task_id}] ❌ 增強版批量報告生成任務失敗: {e}")
        _handle_task_failure(task_id, e)

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
            request.output_template,
            request.enable_trend_analysis,
            request.enable_recommendations
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
        bucket_name = os.environ.get("GCS_BUCKET_NAME", "neo-trend-hub-documents")

        status_info = {
            "gcs_available": False,
            "credentials_configured": bool(credentials_path),
            "project_id_configured": bool(project_id),
            "bucket_accessible": False,
            "bucket_name": bucket_name,
            "service_account_email": None,
            "permissions_needed": [
                "storage.buckets.get",
                "storage.objects.create",
                "storage.objects.get"
            ],
            "error_message": None,
            "fix_suggestions": []
        }

        if not credentials_path:
            status_info["error_message"] = "GOOGLE_APPLICATION_CREDENTIALS 環境變量未設置"
            status_info["fix_suggestions"].append("設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量")
            return status_info

        if not os.path.exists(credentials_path):
            status_info["error_message"] = f"憑證文件不存在: {credentials_path}"
            status_info["fix_suggestions"].append("檢查憑證文件路徑是否正確")
            return status_info

        # 讀取服務帳戶信息
        try:
            import json
            with open(credentials_path, 'r') as f:
                creds = json.load(f)
                status_info["service_account_email"] = creds.get('client_email')
        except Exception as e:
            status_info["error_message"] = f"無法讀取憑證文件: {str(e)}"
            return status_info

        # 嘗試初始化 GCS 客戶端
        gcs_client = get_gcs_client()
        if not gcs_client:
            status_info["error_message"] = "無法初始化 GCS 客戶端"
            status_info["fix_suggestions"].append("檢查憑證文件格式是否正確")
            return status_info

        status_info["gcs_available"] = True

        # 檢查 bucket 訪問權限
        if gcs_client.check_bucket_exists(bucket_name):
            status_info["bucket_accessible"] = True
        else:
            status_info["error_message"] = f"無法訪問 bucket: {bucket_name}"
            status_info["fix_suggestions"].extend([
                f"為服務帳戶 {status_info['service_account_email']} 添加 Storage 權限",
                "運行 python fix_gcs_permissions.py 自動修復權限",
                f"手動執行: gcloud projects add-iam-policy-binding {project_id} --member='serviceAccount:{status_info['service_account_email']}' --role='roles/storage.objectAdmin'"
            ])

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

@router.get("/archives")
def list_report_archives(limit: int = 50):
    """列出報告檔案追蹤記錄"""
    try:
        bq_client = get_bigquery_client()
        if not bq_client:
            raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

        archive_manager = ReportArchiveManager(bq_client)
        archives = archive_manager.list_archives(limit=limit)

        logger.info(f"返回 {len(archives)} 個檔案追蹤記錄")
        return {
            "archives": archives,
            "total": len(archives)
        }

    except Exception as e:
        logger.error(f"列出檔案追蹤記錄時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"列出檔案追蹤記錄時發生錯誤: {e}")

@router.get("/archives/batch/{batch_id}")
def get_archive_by_batch(batch_id: str):
    """根據批次ID獲取檔案追蹤記錄"""
    try:
        bq_client = get_bigquery_client()
        if not bq_client:
            raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

        archive_manager = ReportArchiveManager(bq_client)
        archive = archive_manager.get_archive_by_batch_id(batch_id)

        if not archive:
            raise HTTPException(status_code=404, detail=f"找不到批次 {batch_id} 的檔案記錄")

        return archive

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"獲取檔案追蹤記錄時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"獲取檔案追蹤記錄時發生錯誤: {e}")

@router.get("/archives/task/{task_id}")
def get_archive_by_task(task_id: str):
    """根據任務ID獲取檔案追蹤記錄"""
    try:
        bq_client = get_bigquery_client()
        if not bq_client:
            raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

        archive_manager = ReportArchiveManager(bq_client)
        archive = archive_manager.get_archive_by_task_id(task_id)

        if not archive:
            raise HTTPException(status_code=404, detail=f"找不到任務 {task_id} 的檔案記錄")

        return archive

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"獲取檔案追蹤記錄時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"獲取檔案追蹤記錄時發生錯誤: {e}")

@router.delete("/archives/task/{task_id}")
def delete_archive_by_task(task_id: str):
    """刪除檔案追蹤記錄（軟刪除）"""
    try:
        bq_client = get_bigquery_client()
        if not bq_client:
            raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

        archive_manager = ReportArchiveManager(bq_client)
        archive_manager.delete_archive(task_id)

        return {"message": f"任務 {task_id} 的檔案記錄已刪除"}

    except Exception as e:
        logger.error(f"刪除檔案追蹤記錄時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"刪除檔案追蹤記錄時發生錯誤: {e}")

# 新增趨勢分析和推薦相關的 API 端點

@router.post("/trends/analyze")
def analyze_trends(seminars: Optional[List[str]] = None, limit: Optional[int] = 50):
    """執行趨勢分析"""
    try:
        bq_client = get_bigquery_client()
        if not bq_client:
            raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

        # 獲取會議數據
        sessions = get_sessions_from_bigquery_for_reports(bq_client, seminars, limit)

        if not sessions:
            return {"trends": [], "message": "沒有找到符合條件的會議"}

        # 執行趨勢分析
        from ..modules.trend_analyzer import TrendAnalyzer
        analyzer = TrendAnalyzer()

        trends = analyzer.analyze_trends(sessions)
        session_mappings = analyzer.classify_sessions(sessions, trends)
        correlation_analysis = analyzer.analyze_trend_correlations(sessions, session_mappings)

        # 構建響應
        result = {
            "trends": [
                {
                    "name": trend.name,
                    "description": trend.description,
                    "keywords": trend.keywords,
                    "importance_score": trend.importance_score,
                    "session_count": trend.session_count
                }
                for trend in trends
            ],
            "session_mappings": [
                {
                    "session_id": mapping.session_id,
                    "title": mapping.title,
                    "trends": mapping.trends,
                    "confidence_scores": mapping.confidence_scores
                }
                for mapping in session_mappings
            ],
            "correlation_analysis": {
                "correlation_insights": correlation_analysis.get('correlation_insights', []),
                "trend_clusters": correlation_analysis.get('trend_clusters', []),
                "analysis_metadata": correlation_analysis.get('analysis_metadata', {})
            },
            "statistics": {
                "total_sessions": len(sessions),
                "total_trends": len(trends),
                "mapped_sessions": len([m for m in session_mappings if m.trends])
            }
        }

        logger.info(f"趨勢分析完成: {len(trends)} 個趨勢, {len(sessions)} 個會議")
        return result

    except Exception as e:
        logger.error(f"趨勢分析時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"趨勢分析時發生錯誤: {e}")

@router.post("/recommendations/personalized")
def get_personalized_recommendations(
    user_interests: List[str],
    preferred_trends: Optional[List[str]] = None,
    expertise_level: str = "intermediate",
    max_recommendations: int = 10,
    seminars: Optional[List[str]] = None,
    limit: Optional[int] = 50
):
    """獲取個性化推薦"""
    try:
        bq_client = get_bigquery_client()
        if not bq_client:
            raise HTTPException(status_code=500, detail="無法連接到 BigQuery")

        # 獲取會議數據
        sessions = get_sessions_from_bigquery_for_reports(bq_client, seminars, limit)

        if not sessions:
            return {"recommendations": [], "message": "沒有找到符合條件的會議"}

        # 執行趨勢分析
        from ..modules.trend_analyzer import TrendAnalyzer
        from ..modules.trend_recommendation_engine import TrendRecommendationEngine, UserProfile

        analyzer = TrendAnalyzer()
        recommendation_engine = TrendRecommendationEngine()

        trends = analyzer.analyze_trends(sessions)
        session_mappings = analyzer.classify_sessions(sessions, trends)

        # 構建用戶檔案
        user_profile = UserProfile(
            user_id="api_user",
            interests=user_interests,
            preferred_trends=preferred_trends or [],
            interaction_history=[],
            expertise_level=expertise_level
        )

        # 轉換數據格式
        trends_data = [
            {
                "name": trend.name,
                "description": trend.description,
                "keywords": trend.keywords,
                "importance_score": trend.importance_score
            }
            for trend in trends
        ]

        session_mappings_data = [
            {
                "session_id": mapping.session_id,
                "title": mapping.title,
                "trends": mapping.trends,
                "confidence_scores": mapping.confidence_scores
            }
            for mapping in session_mappings
        ]

        # 生成推薦
        recommendations = recommendation_engine.generate_personalized_recommendations(
            user_profile=user_profile,
            trends=trends_data,
            sessions=sessions,
            session_mappings=session_mappings_data,
            max_recommendations=max_recommendations
        )

        # 構建響應
        result = {
            "recommendations": [
                {
                    "item_id": rec.item_id,
                    "item_type": rec.item_type,
                    "title": rec.title,
                    "description": rec.description,
                    "relevance_score": rec.relevance_score,
                    "reasoning": rec.reasoning,
                    "metadata": rec.metadata
                }
                for rec in recommendations
            ],
            "user_profile": {
                "interests": user_interests,
                "preferred_trends": preferred_trends or [],
                "expertise_level": expertise_level
            },
            "statistics": {
                "total_recommendations": len(recommendations),
                "total_sessions": len(sessions),
                "total_trends": len(trends)
            }
        }

        logger.info(f"個性化推薦完成: {len(recommendations)} 個推薦項目")
        return result

    except Exception as e:
        logger.error(f"生成個性化推薦時發生錯誤: {e}")
        raise HTTPException(status_code=500, detail=f"生成個性化推薦時發生錯誤: {e}")


# ==================== 新增：增強功能 API 端點 ====================
# 注意：移除重複的 /trends/analyze 端點，使用上方已存在的版本

@router.post("/trends/analyze-enhanced")
async def analyze_trends_enhanced_endpoint(request: dict):
    """
    執行技術趨勢分析 API 端點

    對應前端 TrendAnalysisPage 的趨勢分析功能
    """
    try:
        if not trend_analyzer:
            raise HTTPException(status_code=503, detail="趨勢分析器未正確初始化")

        logger.info("🔍 開始執行趨勢分析...")

        # 獲取請求參數
        seminars = request.get('seminars')
        limit = request.get('limit', 50)

        # 獲取 BigQuery 客戶端
        bq_client = get_bigquery_client()
        if not bq_client:
            raise HTTPException(status_code=503, detail="無法連接到 BigQuery")

        # 獲取會議數據
        sessions = get_sessions_from_bigquery_for_reports(bq_client, seminars, limit)
        if not sessions:
            raise HTTPException(status_code=404, detail="未找到符合條件的會議數據")

        logger.info(f"📊 分析 {len(sessions)} 個會議的技術趨勢")

        # 執行趨勢分析
        trends = trend_analyzer.analyze_trends(sessions)

        # 執行會議分類
        session_mappings = trend_analyzer.classify_sessions(sessions, trends)

        # 執行趨勢關聯分析
        correlation_analysis = trend_analyzer.analyze_trend_correlations(trends, session_mappings)

        # 構建響應
        result = {
            "trends": [
                {
                    "name": trend.name,
                    "description": trend.description,
                    "keywords": trend.keywords,
                    "importance_score": trend.importance_score,
                    "session_count": trend.session_count
                }
                for trend in trends
            ],
            "session_mappings": [
                {
                    "session_id": mapping.session_id,
                    "title": mapping.title,
                    "trends": mapping.trends,
                    "confidence_scores": mapping.confidence_scores,
                    "reasoning": mapping.reasoning
                }
                for mapping in session_mappings
            ],
            "correlation_analysis": {
                "trend_clusters": [
                    {
                        "primary_trend": cluster.primary_trend,
                        "related_trends": [
                            {
                                "trend": related.trend,
                                "correlation_score": related.correlation_score,
                                "shared_sessions": related.shared_sessions
                            }
                            for related in cluster.related_trends
                        ],
                        "description": cluster.description
                    }
                    for cluster in correlation_analysis.trend_clusters
                ],
                "cross_trend_sessions": [
                    {
                        "session_id": session.session_id,
                        "title": session.title,
                        "trends": session.trends,
                        "cross_trend_score": session.cross_trend_score
                    }
                    for session in correlation_analysis.cross_trend_sessions
                ]
            },
            "statistics": {
                "total_sessions": len(sessions),
                "total_trends": len(trends),
                "mapped_sessions": len([m for m in session_mappings if m.trends]),
                "cross_trend_sessions": len(correlation_analysis.cross_trend_sessions)
            }
        }

        logger.info(f"✅ 趨勢分析完成: {len(trends)} 個趨勢, {len(session_mappings)} 個會議映射")
        return result

    except Exception as e:
        logger.error(f"趨勢分析失敗: {e}")
        raise HTTPException(status_code=500, detail=f"趨勢分析失敗: {e}")


@router.get("/enhanced/status")
async def get_enhanced_system_status():
    """
    獲取增強系統狀態

    檢查所有增強功能模組的可用性
    """
    try:
        status = {
            "enhanced_report_generator": enhanced_generator is not None,
            "trend_analyzer": trend_analyzer is not None,
            "recommendation_engine": recommendation_engine is not None,
            "hugo_generator": hugo_generator is not None,
            "bigquery_client": get_bigquery_client() is not None,
            "gemini_api": bool(settings.gemini_api_key),
            "system_ready": all([
                enhanced_generator is not None,
                trend_analyzer is not None,
                hugo_generator is not None,
                get_bigquery_client() is not None,
                bool(settings.gemini_api_key)
            ])
        }

        logger.info(f"增強系統狀態檢查: {'✅ 系統就緒' if status['system_ready'] else '❌ 系統未就緒'}")
        return status

    except Exception as e:
        logger.error(f"獲取增強系統狀態失敗: {e}")
        raise HTTPException(status_code=500, detail=f"獲取增強系統狀態失敗: {e}")


@router.get("/enhanced/features")
async def get_enhanced_features():
    """
    獲取增強功能列表

    返回當前可用的增強功能和其描述
    """
    try:
        features = {
            "three_tier_architecture": {
                "name": "三階層網站架構",
                "description": "首頁 → 趨勢分類 → 會議詳情的完整網站結構",
                "available": enhanced_generator is not None and hugo_generator is not None,
                "phase": "Phase 3"
            },
            "llm_trend_analysis": {
                "name": "LLM 趨勢分析",
                "description": "使用大型語言模型進行深度技術趨勢分析",
                "available": trend_analyzer is not None,
                "phase": "Phase 1"
            },
            "automatic_tagging": {
                "name": "自動標記系統",
                "description": "基於 LLM 的會議內容自動分類和標記",
                "available": trend_analyzer is not None,
                "phase": "Phase 2"
            },
            "personalized_recommendations": {
                "name": "個性化推薦",
                "description": "基於用戶興趣的智慧內容推薦系統",
                "available": recommendation_engine is not None,
                "phase": "Enhanced"
            },
            "hugo_static_site": {
                "name": "Hugo 靜態網站生成",
                "description": "快速、SEO 友好的靜態網站生成",
                "available": hugo_generator is not None,
                "phase": "Phase 3"
            },
            "offline_packages": {
                "name": "離線分享包",
                "description": "ZIP 打包的離線可瀏覽報告",
                "available": hugo_generator is not None,
                "phase": "Enhanced"
            }
        }

        available_count = sum(1 for feature in features.values() if feature["available"])
        total_count = len(features)

        result = {
            "features": features,
            "summary": {
                "total_features": total_count,
                "available_features": available_count,
                "completion_rate": f"{(available_count/total_count)*100:.1f}%"
            }
        }

        logger.info(f"增強功能狀態: {available_count}/{total_count} 可用")
        return result

    except Exception as e:
        logger.error(f"獲取增強功能列表失敗: {e}")
        raise HTTPException(status_code=500, detail=f"獲取增強功能列表失敗: {e}")
