"""
PPT 上傳和處理 API 端點 - 重構版本
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

# 導入共享任務管理
from backend.api.shared.tasks import tasks

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

# 並行處理配置
MAX_CONCURRENT_FILES = 3  # 最多同時處理 3 個檔案
processing_lock = threading.Lock()  # 用於保護共享狀態

# 任務管理輔助函數
def get_ppt_task_status(task_id: str) -> Optional[ProcessingStatus]:
    """從共享任務中獲取 PPT 任務狀態"""
    if task_id not in tasks:
        return None
    
    task_data = tasks[task_id]
    if task_data.get("type") != "ppt_upload":
        return None
    
    return ProcessingStatus(
        task_id=task_id,
        status=task_data.get("status", "pending"),
        progress=task_data.get("progress", 0),
        message=task_data.get("message", ""),
        result=task_data.get("result"),
        error=task_data.get("error"),
        files=[FileProcessingResult(**f) if isinstance(f, dict) else f for f in task_data.get("files", [])]
    )

def set_ppt_task_status(task_id: str, status: ProcessingStatus):
    """將 PPT 任務狀態保存到共享任務中"""
    tasks[task_id] = {
        "type": "ppt_upload",
        "task_id": task_id,
        "status": status.status,
        "progress": status.progress,
        "message": status.message,
        "result": status.result,
        "error": status.error,
        "files": [f.dict() if hasattr(f, 'dict') else f for f in (status.files or [])]
    }

def update_file_status(task_id: str, filename: str, updates: Dict[str, Any]):
    """更新特定檔案的狀態"""
    with processing_lock:
        current_status = get_ppt_task_status(task_id)
        if current_status and current_status.files:
            for file_result in current_status.files:
                if file_result.filename == filename:
                    for key, value in updates.items():
                        setattr(file_result, key, value)
                    break
            set_ppt_task_status(task_id, current_status)

def update_task_status(task_id: str, updates: Dict[str, Any]):
    """更新任務狀態"""
    with processing_lock:
        current_status = get_ppt_task_status(task_id)
        if current_status:
            for key, value in updates.items():
                setattr(current_status, key, value)
            set_ppt_task_status(task_id, current_status)

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

def find_best_matching_session(ppt_filename: str, seminar: str) -> Tuple[Optional[str], float]:
    """在指定研討會中找到最匹配的會議"""
    try:
        client = bigquery.Client()
        
        # 查詢指定研討會的所有會議
        query = f"""
        SELECT name
        FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE seminar = @seminar
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("seminar", "STRING", seminar)
            ]
        )
        
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        
        best_match = None
        best_score = 0.0
        
        # 移除檔案副檔名進行比較
        ppt_name_clean = Path(ppt_filename).stem
        
        for row in results:
            bq_name = row['name']
            if bq_name:  # 確保名稱不為空
                score = calculate_similarity(ppt_name_clean, bq_name)
                if score > best_score:
                    best_score = score
                    best_match = bq_name
        
        return best_match, best_score
        
    except Exception as e:
        print(f"查詢 BigQuery 時發生錯誤: {e}")
        return None, 0.0

def extract_ppt_content_with_gemini(file_path: Path) -> str:
    """使用 Gemini API 提取 PPT 內容"""
    try:
        # 讀取檔案
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # 上傳檔案到 Gemini
        uploaded_file = genai_client.files.upload(
            path=str(file_path),
            display_name=file_path.name
        )
        
        # 等待檔案處理完成
        import time
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_file = genai_client.files.get(name=uploaded_file.name)
        
        if uploaded_file.state.name == "FAILED":
            raise Exception(f"檔案上傳失敗: {uploaded_file.state}")
        
        # 使用 Gemini 分析 PPT 內容
        prompt = """
        請詳細分析這個 PPT 檔案的內容，並提供以下資訊：
        1. 簡報的主要標題
        2. 每一頁的標題和主要內容
        3. 重要的技術概念、方法或工具
        4. 關鍵數據或統計資訊
        5. 結論或要點總結
        
        請用繁體中文回答，並盡可能詳細地描述簡報內容。
        """
        
        response = genai_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=[
                prompt,
                uploaded_file
            ]
        )
        
        # 清理上傳的檔案
        genai_client.files.delete(name=uploaded_file.name)
        
        return response.text if response.text else "無法提取內容"
        
    except Exception as e:
        print(f"使用 Gemini 提取 PPT 內容時發生錯誤: {e}")
        return f"提取失敗: {str(e)}"

def update_bigquery_with_ppt_content(session_name: str, seminar: str, ppt_content: str) -> bool:
    """更新 BigQuery 中的 PPT 內容"""
    try:
        client = bigquery.Client()

        # 更新查詢
        query = f"""
        UPDATE `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        SET ppt_context = @ppt_content
        WHERE name = @session_name AND seminar = @seminar
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("ppt_content", "STRING", ppt_content),
                bigquery.ScalarQueryParameter("session_name", "STRING", session_name),
                bigquery.ScalarQueryParameter("seminar", "STRING", seminar)
            ]
        )

        query_job = client.query(query, job_config=job_config)
        query_job.result()  # 等待查詢完成

        print(f"成功更新 BigQuery 中的 PPT 內容: {session_name}")
        return True

    except Exception as e:
        print(f"更新 BigQuery 時發生錯誤: {e}")
        return False

async def process_single_file(file_path: Path, seminar: str, task_id: str) -> Dict[str, Any]:
    """處理單個 PPT 檔案"""
    try:
        print(f"開始處理檔案: {file_path.name}")

        # 更新檔案狀態
        update_file_status(task_id, file_path.name, {
            "status": "processing",
            "progress": 10
        })

        # 1. 找到最匹配的會議
        print(f"為檔案 {file_path.name} 尋找匹配的會議...")
        best_match, score = find_best_matching_session(file_path.name, seminar)

        if not best_match or score < 0.3:  # 相似度閾值
            update_file_status(task_id, file_path.name, {
                "status": "error",
                "progress": 100,
                "error": f"找不到匹配的會議 (相似度: {score:.2f})"
            })
            return {
                "filename": file_path.name,
                "status": "error",
                "error": f"找不到匹配的會議 (相似度: {score:.2f})"
            }

        print(f"找到匹配會議: {best_match} (相似度: {score:.2f})")

        # 更新檔案狀態
        update_file_status(task_id, file_path.name, {
            "matched_session": best_match,
            "similarity": score,
            "progress": 30
        })

        # 2. 提取 PPT 內容
        print(f"提取 PPT 內容: {file_path.name}")
        ppt_content = extract_ppt_content_with_gemini(file_path)

        if not ppt_content or "提取失敗" in ppt_content:
            update_file_status(task_id, file_path.name, {
                "status": "error",
                "progress": 100,
                "error": f"PPT 內容提取失敗: {ppt_content}"
            })
            return {
                "filename": file_path.name,
                "status": "error",
                "error": f"PPT 內容提取失敗: {ppt_content}"
            }

        # 更新檔案狀態
        update_file_status(task_id, file_path.name, {
            "ppt_length": len(ppt_content),
            "progress": 70
        })

        # 3. 更新 BigQuery
        print(f"更新 BigQuery: {best_match}")
        success = update_bigquery_with_ppt_content(best_match, seminar, ppt_content)

        if success:
            update_file_status(task_id, file_path.name, {
                "status": "success",
                "progress": 100
            })
            return {
                "filename": file_path.name,
                "status": "success",
                "matched_session": best_match,
                "similarity": score,
                "ppt_length": len(ppt_content)
            }
        else:
            update_file_status(task_id, file_path.name, {
                "status": "error",
                "progress": 100,
                "error": "BigQuery 更新失敗"
            })
            return {
                "filename": file_path.name,
                "status": "error",
                "error": "BigQuery 更新失敗"
            }

    except Exception as e:
        error_msg = f"處理檔案時發生錯誤: {str(e)}"
        print(error_msg)
        update_file_status(task_id, file_path.name, {
            "status": "error",
            "progress": 100,
            "error": error_msg
        })
        return {
            "filename": file_path.name,
            "status": "error",
            "error": error_msg
        }

async def process_ppt_files_background(file_paths: List[Path], seminar: str, task_id: str):
    """背景處理 PPT 檔案"""
    try:
        print(f"開始背景處理任務 {task_id}，共 {len(file_paths)} 個檔案")

        # 初始化檔案結果
        file_results = [
            FileProcessingResult(
                filename=file_path.name,
                status="pending",
                progress=0
            )
            for file_path in file_paths
        ]

        # 更新任務狀態
        update_task_status(task_id, {
            "status": "processing",
            "message": f"開始並行處理 {len(file_paths)} 個檔案",
            "files": file_results
        })

        # 並行處理檔案
        results = []
        with ThreadPoolExecutor(max_workers=MAX_CONCURRENT_FILES) as executor:
            # 提交所有任務
            future_to_file = {
                executor.submit(asyncio.run, process_single_file(file_path, seminar, task_id)): file_path
                for file_path in file_paths
            }

            # 收集結果
            completed_count = 0
            for future in future_to_file:
                try:
                    result = future.result()
                    results.append(result)
                    completed_count += 1

                    # 更新整體進度
                    overall_progress = int((completed_count / len(file_paths)) * 100)
                    update_task_status(task_id, {
                        "progress": overall_progress,
                        "message": f"已完成 {completed_count}/{len(file_paths)} 個檔案"
                    })

                except Exception as e:
                    file_path = future_to_file[future]
                    print(f"處理檔案 {file_path.name} 時發生錯誤: {e}")
                    results.append({
                        "filename": file_path.name,
                        "status": "error",
                        "error": str(e)
                    })

        # 統計結果
        success_count = sum(1 for r in results if r["status"] == "success")
        error_count = len(results) - success_count

        # 更新最終狀態
        final_status = "success" if error_count == 0 else ("partial" if success_count > 0 else "error")
        update_task_status(task_id, {
            "status": final_status,
            "progress": 100,
            "message": f"處理完成: {success_count} 成功, {error_count} 失敗",
            "result": {
                "total_files": len(file_paths),
                "success_count": success_count,
                "error_count": error_count,
                "results": results
            }
        })

        print(f"任務 {task_id} 完成: {success_count} 成功, {error_count} 失敗")

    except Exception as e:
        print(f"背景處理任務 {task_id} 失敗: {e}")
        update_task_status(task_id, {
            "status": "error",
            "progress": 100,
            "error": str(e),
            "message": f"處理失敗: {str(e)}"
        })

    finally:
        # 清理臨時檔案
        for file_path in file_paths:
            try:
                if file_path.exists():
                    file_path.unlink()
                    print(f"已刪除臨時檔案: {file_path}")
            except Exception as e:
                print(f"刪除臨時檔案失敗: {file_path}, 錯誤: {e}")

        # 清理臨時目錄
        try:
            temp_dir = file_paths[0].parent if file_paths else None
            if temp_dir and temp_dir.exists():
                temp_dir.rmdir()
                print(f"已刪除臨時目錄: {temp_dir}")
        except Exception as e:
            print(f"刪除臨時目錄失敗: {e}")

# API 端點
@router.post("/upload", response_model=UploadResponse)
async def upload_ppt_files(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    seminar: str = Form(...)
):
    """上傳 PPT 檔案並開始處理"""
    if not files:
        raise HTTPException(status_code=400, detail="沒有上傳任何檔案")

    # 驗證檔案類型
    allowed_extensions = {'.ppt', '.pptx'}
    for file in files:
        if not any(file.filename.lower().endswith(ext) for ext in allowed_extensions):
            raise HTTPException(
                status_code=400,
                detail=f"不支援的檔案類型: {file.filename}。只支援 .ppt 和 .pptx 檔案"
            )

    try:
        # 生成任務 ID
        task_id = str(uuid.uuid4())

        # 創建臨時目錄
        temp_dir = Path(tempfile.mkdtemp(prefix=f"ppt_upload_{task_id}_"))
        file_paths = []

        # 保存上傳的檔案
        for file in files:
            file_path = temp_dir / file.filename
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            file_paths.append(file_path)
            print(f"已保存檔案: {file_path}")

        # 初始化任務狀態
        initial_status = ProcessingStatus(
            task_id=task_id,
            status="pending",
            progress=0,
            message=f"已接收 {len(files)} 個檔案，準備開始處理",
            files=[]
        )
        set_ppt_task_status(task_id, initial_status)

        # 啟動背景處理
        background_tasks.add_task(process_ppt_files_background, file_paths, seminar, task_id)

        return UploadResponse(
            task_id=task_id,
            message=f"已開始處理 {len(files)} 個 PPT 檔案",
            files_count=len(files)
        )

    except Exception as e:
        # 清理已創建的檔案
        if 'temp_dir' in locals() and temp_dir.exists():
            for file_path in temp_dir.glob("*"):
                file_path.unlink()
            temp_dir.rmdir()

        raise HTTPException(status_code=500, detail=f"檔案處理失敗: {str(e)}")

@router.get("/status/{task_id}", response_model=ProcessingStatus)
async def get_processing_status(task_id: str):
    """獲取處理狀態"""
    print(f"查詢任務狀態: {task_id}")

    status = get_ppt_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail=f"找不到任務: {task_id}")

    print(f"任務 {task_id} 狀態: {status.status}, 進度: {status.progress}%")
    return status

@router.get("/seminars")
async def get_available_seminars():
    """獲取可用的研討會列表，包含會議數量信息"""
    try:
        client = bigquery.Client()

        query = f"""
        SELECT
            seminar,
            COUNT(*) as session_count
        FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE seminar IS NOT NULL
        GROUP BY seminar
        ORDER BY seminar
        """

        query_job = client.query(query)
        results = query_job.result()

        seminars = [
            {
                "name": row['seminar'],
                "session_count": row['session_count']
            }
            for row in results
        ]
        return {"seminars": seminars}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"獲取研討會列表失敗: {str(e)}")

@router.get("/debug/tasks")
async def get_all_tasks():
    """調試端點：獲取所有任務狀態"""
    ppt_tasks = {
        task_id: task_data
        for task_id, task_data in tasks.items()
        if task_data.get("type") == "ppt_upload"
    }

    return {
        "total_tasks": len(ppt_tasks),
        "tasks": {
            task_id: {
                "status": task_data.get("status"),
                "progress": task_data.get("progress"),
                "message": task_data.get("message"),
                "files_count": len(task_data.get("files", []))
            }
            for task_id, task_data in ppt_tasks.items()
        }
    }
