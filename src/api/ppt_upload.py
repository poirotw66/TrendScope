"""
PPT 上傳和處理 API 端點
"""

import os
import tempfile
import asyncio
from typing import List, Optional, Dict, Any
from pathlib import Path
import uuid
import time

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
class ProcessingStatus(BaseModel):
    task_id: str
    status: str  # 'pending', 'processing', 'success', 'error'
    progress: int
    message: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class UploadResponse(BaseModel):
    task_id: str
    message: str
    files_count: int

# 全局任務狀態存儲（實際應用中應使用 Redis 或數據庫）
task_status: Dict[str, ProcessingStatus] = {}

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
    """使用 Gemini API 提取 PPT 內容"""
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

def update_ppt_content_in_bigquery(client: bigquery.Client, conference_id: str, ppt_content: str) -> bool:
    """更新 BigQuery 中的 ppt_context 欄位"""
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

async def process_files_background(task_id: str, file_paths: List[Path], seminar: str):
    """背景處理檔案"""
    try:
        print(f"開始背景處理任務 {task_id}: {len(file_paths)} 個檔案")

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

        # 更新任務狀態
        task_status[task_id].status = "processing"
        task_status[task_id].message = f"開始處理 {len(file_paths)} 個檔案"

        success_count = 0
        
        for i, file_path in enumerate(file_paths):
            try:
                # 更新進度
                progress = int((i / len(file_paths)) * 100)
                task_status[task_id].progress = progress
                task_status[task_id].message = f"正在處理: {file_path.name}"
                
                session_name = file_path.stem
                print(f"處理檔案: {session_name}")

                # 尋找最佳匹配
                match = find_best_match(session_name, bq_sessions)

                if not match:
                    print(f"❌ 未找到匹配的會議: {session_name}")
                    continue

                conf_id, bq_name, score = match
                print(f"✅ 找到匹配: {bq_name} (相似度: {score:.2f})")

                # 提取 PPT 內容
                print(f"開始提取 PPT 內容: {file_path.name}")
                ppt_content = await extract_ppt_content(file_path)
                if not ppt_content:
                    print(f"❌ 無法提取 PPT 內容: {file_path.name}")
                    continue

                print(f"✅ 成功提取 PPT 內容，長度: {len(ppt_content)} 字符")

                # 更新 BigQuery
                print(f"開始更新 BigQuery: {conf_id}")
                if update_ppt_content_in_bigquery(client, conf_id, ppt_content):
                    success_count += 1
                    print(f"✅ 成功更新 BigQuery")
                else:
                    print(f"❌ 更新 BigQuery 失敗")
                
                # 添加延遲避免 API 限制
                await asyncio.sleep(2)
                
            except Exception as e:
                print(f"處理檔案 {file_path.name} 時發生錯誤: {e}")
                continue
            finally:
                # 清理臨時檔案
                if file_path.exists():
                    file_path.unlink()
        
        # 完成處理
        task_status[task_id].status = "success"
        task_status[task_id].progress = 100
        task_status[task_id].message = f"處理完成！成功處理 {success_count}/{len(file_paths)} 個檔案"
        task_status[task_id].result = {
            "total": len(file_paths),
            "success": success_count,
            "failed": len(file_paths) - success_count
        }
        
    except Exception as e:
        task_status[task_id].status = "error"
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
        for file in pdf_files:
            file_path = temp_dir / file.filename
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            file_paths.append(file_path)
        
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
    if task_id not in task_status:
        raise HTTPException(status_code=404, detail="任務不存在")
    
    return task_status[task_id]

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
