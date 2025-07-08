"""
PPT 上傳和處理 API 端點
"""

import os
import tempfile
import asyncio
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
import uuid
import time
from concurrent.futures import ThreadPoolExecutor
import threading

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from google import genai
from google.cloud import bigquery
from config.config import GEMINI_API_KEY
import opencc

# 路由器
router = APIRouter(prefix="/ppt", tags=["PPT Upload"])

# 配置
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"

# 初始化客戶端
genai_client = genai.Client(api_key=GEMINI_API_KEY)

# 初始化 OpenCC 轉換器
cc = opencc.OpenCC('t2s')  # 繁體轉簡體

# 數據模型
class FileProcessingResult(BaseModel):
    """單個檔案的處理結果"""
    filename: str
    status: str  # 'pending', 'processing', 'success', 'error'
    progress: int
    matched_session: Optional[str] = None
    similarity: Optional[float] = None
    ppt_length: Optional[int] = None
    error: Optional[str] = None

class ProcessingStatus(BaseModel):
    task_id: str
    status: str  # 'pending', 'processing', 'success', 'error'
    progress: int
    message: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    files: Optional[List[FileProcessingResult]] = None  # 每個檔案的詳細狀態

class UploadResponse(BaseModel):
    task_id: str
    message: str
    files_count: int

# 全局任務狀態存儲（實際應用中應使用 Redis 或數據庫）
task_status: Dict[str, ProcessingStatus] = {}

# 並行處理配置
MAX_CONCURRENT_FILES = 3  # 最多同時處理 3 個檔案
processing_lock = threading.Lock()  # 用於保護共享狀態

def convert_traditional_to_simplified(text: str) -> str:
    """將繁體中文轉換為簡體中文"""
    try:
        return cc.convert(text)
    except Exception as e:
        print(f"繁簡轉換失敗: {e}")
        return text  # 如果轉換失敗，返回原文

def calculate_similarity(text1: str, text2: str) -> float:
    """計算兩個文本的相似度"""
    text1_simplified = convert_traditional_to_simplified(text1.lower())
    text2_simplified = convert_traditional_to_simplified(text2.lower())
    
    if text1_simplified == text2_simplified:
        return 1.0
    
    # 計算最長公共子序列相似度
    import re
    text1_clean = re.sub(r'[^\w]', '', text1_simplified)
    text2_clean = re.sub(r'[^\w]', '', text2_simplified)
    
    if not text1_clean or not text2_clean:
        return 0.0
    
    def lcs_length(s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    lcs_len = lcs_length(text1_clean, text2_clean)
    max_len = max(len(text1_clean), len(text2_clean))
    
    return lcs_len / max_len if max_len > 0 else 0.0

def find_best_match(session_name: str, bq_sessions: List[tuple]) -> Optional[tuple]:
    """找到最佳匹配的會議"""
    best_match = None
    best_score = 0.0
    
    for conf_id, bq_name in bq_sessions:
        score = calculate_similarity(session_name, bq_name)
        if score > best_score:
            best_score = score
            best_match = (conf_id, bq_name, score)
    
    # 設定相似度閾值
    if best_match and best_match[2] >= 0.7:  # 70% 相似度
        return best_match
    
    return None

async def extract_ppt_content(file_path: Path) -> Optional[str]:
    """使用 Gemini API 提取 PPT 內容（真正的異步版本）"""

    def _sync_extract_ppt_content(file_path: Path) -> Optional[str]:
        """同步版本的 PPT 內容提取"""
        try:
            # 上傳檔案到 Gemini
            sample_file = genai_client.files.upload(file=file_path)

            # 提取內容的 prompt
            prompt = f"""
請提取這個 PPT 簡報的完整內容，並按照以下格式整理：

## 簡報標題
{file_path.stem}

## 簡報內容
請逐頁提取簡報的文字內容，包括：
- 標題
- 重點內容
- 圖表說明
- 結論

要求：
1. 保持原始內容的邏輯結構
2. 使用 Markdown 格式
3. 保留重要的技術術語和專有名詞
4. 如果有圖表，請描述其主要內容
5. 內容要完整但簡潔

請直接輸出整理後的內容，不需要額外說明。
"""

            # 呼叫 Gemini API
            response = genai_client.models.generate_content(
                model="gemini-2.5-flash-preview-05-20",
                contents=[sample_file, prompt]
            )

            return response.text

        except Exception as e:
            print(f"提取 PPT 內容時發生錯誤: {e}")
            return None

    # 使用線程池執行器來並行執行阻塞的 Gemini API 調用
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_FILES) as executor:
        result = await loop.run_in_executor(executor, _sync_extract_ppt_content, file_path)

    return result

async def update_ppt_content_in_bigquery(client: bigquery.Client, conference_id: str, ppt_content: str) -> bool:
    """更新 BigQuery 中的 ppt_context 欄位（異步版本）"""

    def _sync_update_bigquery(client: bigquery.Client, conference_id: str, ppt_content: str) -> bool:
        """同步版本的 BigQuery 更新"""
        try:
            update_query = f"""
            UPDATE `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
            SET ppt_context = @ppt_content
            WHERE conference_id = @conference_id
            """

            job_config = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter("ppt_content", "STRING", ppt_content),
                    bigquery.ScalarQueryParameter("conference_id", "STRING", conference_id),
                ]
            )

            job = client.query(update_query, job_config=job_config)
            job.result()

            return True

        except Exception as e:
            print(f"更新 BigQuery 時發生錯誤: {e}")
            return False

    # 使用線程池執行器來並行執行阻塞的 BigQuery 操作
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_FILES) as executor:
        result = await loop.run_in_executor(executor, _sync_update_bigquery, client, conference_id, ppt_content)

    return result

async def process_single_file(
    file_path: Path,
    bq_sessions: List[Tuple[str, str]],
    client: bigquery.Client,
    task_id: str,
    file_index: int
) -> FileProcessingResult:
    """處理單個檔案"""
    result = FileProcessingResult(
        filename=file_path.name,
        status="processing",
        progress=0
    )

    try:
        print(f"[檔案 {file_index}] 開始處理: {file_path.name}")

        # 更新檔案狀態
        with processing_lock:
            if task_status[task_id].files:
                for file_result in task_status[task_id].files:
                    if file_result.filename == file_path.name:
                        file_result.status = "processing"
                        file_result.progress = 10
                        break

        session_name = file_path.stem

        # 尋找最佳匹配
        print(f"[檔案 {file_index}] 尋找匹配會議: {session_name}")
        match = find_best_match(session_name, bq_sessions)

        if not match:
            print(f"[檔案 {file_index}] ❌ 未找到匹配的會議: {session_name}")
            result.status = "error"
            result.error = "未找到匹配的會議"
            result.progress = 100
            return result

        conf_id, bq_name, score = match
        print(f"[檔案 {file_index}] ✅ 找到匹配: {bq_name} (相似度: {score:.2f})")

        result.matched_session = bq_name
        result.similarity = score
        result.progress = 30

        # 更新檔案狀態
        with processing_lock:
            if task_status[task_id].files:
                for file_result in task_status[task_id].files:
                    if file_result.filename == file_path.name:
                        file_result.matched_session = bq_name
                        file_result.similarity = score
                        file_result.progress = 30
                        break

        # 提取 PPT 內容
        print(f"[檔案 {file_index}] 開始提取 PPT 內容")
        ppt_content = await extract_ppt_content(file_path)
        if not ppt_content:
            print(f"[檔案 {file_index}] ❌ 無法提取 PPT 內容")
            result.status = "error"
            result.error = "無法提取 PPT 內容"
            result.progress = 100
            return result

        print(f"[檔案 {file_index}] ✅ 成功提取 PPT 內容，長度: {len(ppt_content)} 字符")
        result.ppt_length = len(ppt_content)
        result.progress = 70

        # 更新檔案狀態
        with processing_lock:
            if task_status[task_id].files:
                for file_result in task_status[task_id].files:
                    if file_result.filename == file_path.name:
                        file_result.ppt_length = len(ppt_content)
                        file_result.progress = 70
                        break

        # 更新 BigQuery
        print(f"[檔案 {file_index}] 開始更新 BigQuery: {conf_id}")
        if await update_ppt_content_in_bigquery(client, conf_id, ppt_content):
            print(f"[檔案 {file_index}] ✅ 成功更新 BigQuery")
            result.status = "success"
            result.progress = 100
        else:
            print(f"[檔案 {file_index}] ❌ 更新 BigQuery 失敗")
            result.status = "error"
            result.error = "更新 BigQuery 失敗"
            result.progress = 100

        return result

    except Exception as e:
        print(f"[檔案 {file_index}] 處理檔案時發生錯誤: {e}")
        result.status = "error"
        result.error = str(e)
        result.progress = 100
        return result
    finally:
        # 清理臨時檔案
        try:
            if file_path.exists():
                file_path.unlink()
                print(f"[檔案 {file_index}] 清理臨時檔案: {file_path.name}")
        except Exception as e:
            print(f"[檔案 {file_index}] 清理檔案失敗: {e}")

async def process_files_background(task_id: str, file_paths: List[Path], seminar: str):
    """背景並行處理檔案"""
    try:
        print(f"開始背景並行處理任務 {task_id}: {len(file_paths)} 個檔案")

        # 初始化 BigQuery 客戶端
        client = bigquery.Client()

        # 獲取 BigQuery 中的所有會議
        query = f"""
        SELECT conference_id, name
        FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE seminar = @seminar_name
        ORDER BY name
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("seminar_name", "STRING", seminar),
            ]
        )

        results = client.query(query, job_config=job_config)
        bq_sessions = [(row['conference_id'], row['name']) for row in results]
        print(f"從 BigQuery 獲取到 {len(bq_sessions)} 個會議記錄")

        # 初始化檔案狀態
        file_results = [
            FileProcessingResult(
                filename=file_path.name,
                status="pending",
                progress=0
            ) for file_path in file_paths
        ]

        # 更新任務狀態
        with processing_lock:
            task_status[task_id].status = "processing"
            task_status[task_id].message = f"開始並行處理 {len(file_paths)} 個檔案"
            task_status[task_id].files = file_results

        # 並行處理檔案
        print(f"開始並行處理，最大並發數: {MAX_CONCURRENT_FILES}")

        # 創建處理任務
        tasks = []
        for i, file_path in enumerate(file_paths):
            task = process_single_file(file_path, bq_sessions, client, task_id, i + 1)
            tasks.append(task)

        # 使用 asyncio.gather 並行執行，但限制並發數
        completed_results = []

        # 分批處理，每批最多 MAX_CONCURRENT_FILES 個檔案
        for i in range(0, len(tasks), MAX_CONCURRENT_FILES):
            batch = tasks[i:i + MAX_CONCURRENT_FILES]
            print(f"處理第 {i//MAX_CONCURRENT_FILES + 1} 批，包含 {len(batch)} 個檔案")

            # 並行執行當前批次
            batch_results = await asyncio.gather(*batch, return_exceptions=True)

            # 處理結果
            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    print(f"檔案處理異常: {result}")
                    # 創建錯誤結果
                    error_result = FileProcessingResult(
                        filename=file_paths[i + j].name,
                        status="error",
                        progress=100,
                        error=str(result)
                    )
                    completed_results.append(error_result)
                else:
                    completed_results.append(result)

                # 更新檔案狀態
                with processing_lock:
                    if task_status[task_id].files:
                        for file_result in task_status[task_id].files:
                            if file_result.filename == completed_results[-1].filename:
                                file_result.status = completed_results[-1].status
                                file_result.progress = completed_results[-1].progress
                                file_result.matched_session = completed_results[-1].matched_session
                                file_result.similarity = completed_results[-1].similarity
                                file_result.ppt_length = completed_results[-1].ppt_length
                                file_result.error = completed_results[-1].error
                                break

            # 更新總體進度
            overall_progress = int((len(completed_results) / len(file_paths)) * 100)
            with processing_lock:
                task_status[task_id].progress = overall_progress
                task_status[task_id].message = f"已完成 {len(completed_results)}/{len(file_paths)} 個檔案"

            print(f"第 {i//MAX_CONCURRENT_FILES + 1} 批處理完成，總進度: {overall_progress}%")

            # 批次間添加短暫延遲，避免 API 限制
            if i + MAX_CONCURRENT_FILES < len(tasks):
                await asyncio.sleep(1)

        # 統計結果
        success_count = sum(1 for result in completed_results if result.status == "success")
        failed_count = len(completed_results) - success_count

        # 完成處理
        with processing_lock:
            task_status[task_id].status = "success"
            task_status[task_id].progress = 100
            task_status[task_id].message = f"並行處理完成！成功處理 {success_count}/{len(file_paths)} 個檔案"
            task_status[task_id].result = {
                "total": len(file_paths),
                "success": success_count,
                "failed": failed_count
            }

        print(f"✅ 任務 {task_id} 並行處理完成: {success_count}/{len(file_paths)} 成功")

    except Exception as e:
        print(f"❌ 任務 {task_id} 處理失敗: {str(e)}")
        task_status[task_id].status = "error"
        task_status[task_id].progress = 100
        task_status[task_id].error = str(e)
        task_status[task_id].message = f"處理失敗: {str(e)}"

@router.post("/upload", response_model=UploadResponse)
async def upload_ppt_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    seminar: str = Form(...)
):
    """上傳 PPT 檔案並開始處理"""

    print(f"收到上傳請求: {len(files)} 個檔案, 研討會: {seminar}")

    # 驗證檔案
    pdf_files = [f for f in files if f.content_type == 'application/pdf' or f.filename.lower().endswith('.pdf')]

    print(f"PDF 檔案數量: {len(pdf_files)}")
    for f in pdf_files:
        print(f"  - {f.filename} ({f.content_type})")

    if not pdf_files:
        print("❌ 沒有有效的 PDF 檔案")
        raise HTTPException(status_code=400, detail="請上傳 PDF 檔案")

    # 生成任務 ID
    task_id = str(uuid.uuid4())

    # 保存檔案到臨時目錄
    temp_dir = Path(tempfile.mkdtemp())
    file_paths = []

    try:
        # 快速保存檔案，避免前端超時
        for file in pdf_files:
            file_path = temp_dir / file.filename
            print(f"正在保存檔案: {file.filename}")

            # 分塊讀取和寫入，避免大檔案導致超時
            with open(file_path, "wb") as buffer:
                while True:
                    chunk = await file.read(8192)  # 8KB 分塊
                    if not chunk:
                        break
                    buffer.write(chunk)

            file_paths.append(file_path)
            print(f"✅ 檔案保存完成: {file.filename}")

        # 初始化任務狀態
        task_status[task_id] = ProcessingStatus(
            task_id=task_id,
            status="pending",
            progress=0,
            message=f"已接收 {len(file_paths)} 個檔案，準備處理..."
        )

        # 啟動背景處理
        background_tasks.add_task(process_files_background, task_id, file_paths, seminar)

        print(f"✅ 成功創建任務: {task_id}")

        return UploadResponse(
            task_id=task_id,
            message=f"已接收 {len(file_paths)} 個檔案，開始處理...",
            files_count=len(file_paths)
        )

    except Exception as e:
        # 清理臨時檔案
        for file_path in file_paths:
            if file_path.exists():
                file_path.unlink()
        if temp_dir.exists():
            temp_dir.rmdir()

        raise HTTPException(status_code=500, detail=f"檔案處理失敗: {str(e)}")

@router.get("/status/{task_id}", response_model=ProcessingStatus)
async def get_processing_status(task_id: str):
    """獲取處理狀態"""
    print(f"查詢任務狀態: {task_id}")

    if task_id not in task_status:
        print(f"❌ 任務不存在: {task_id}")
        raise HTTPException(status_code=404, detail="任務不存在")

    status = task_status[task_id]
    print(f"任務 {task_id} 狀態: {status.status}, 進度: {status.progress}%")

    return status

@router.get("/seminars")
async def get_available_seminars():
    """獲取可用的研討會列表"""
    try:
        client = bigquery.Client()

        query = f"""
        SELECT seminar, COUNT(*) as session_count
        FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        GROUP BY seminar
        ORDER BY session_count DESC
        """

        results = client.query(query)
        seminars = [{"name": row['seminar'], "session_count": row['session_count']} for row in results]

        return {"seminars": seminars}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取研討會列表失敗: {str(e)}")

@router.get("/debug/tasks")
async def get_all_tasks():
    """調試端點：獲取所有任務狀態"""
    return {
        "total_tasks": len(task_status),
        "tasks": {task_id: {
            "status": status.status,
            "progress": status.progress,
            "message": status.message,
            "error": status.error
        } for task_id, status in task_status.items()}
    }
