#!/usr/bin/env python3
"""
批次處理 PPT 內容並上傳到 BigQuery
基於現有的 PDF 處理邏輯，提取 PPT 內容並更新 BigQuery 中的 ppt_context 欄位
"""

import os
import sys
import pathlib
import threading
import time
import csv
from datetime import datetime
from typing import Dict, List, Optional

# 添加專案根目錄到 Python 路徑
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from google import genai
from config.config import GEMINI_API_KEY
from bigquery.client import BigQueryClient
from bigquery.schemas.conferences import CONFERENCE_SCHEMA

# 配置
PPT_DIR = pathlib.Path("data/202505_aicon_ppt")
CSV_PATH = "data/sheet/20250523_上海_AICon_v1.csv"
SEMINAR_NAME = "202505 AICon Shanghai"

# API 配置
MAX_THREADS = 2  # 降低並發數以避免 API 限制
REQUEST_INTERVAL = 5  # 增加請求間隔
MAX_RETRIES = 3
RETRY_DELAY = 10

# BigQuery 配置
BQ_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"

# 初始化客戶端
genai_client = genai.Client(api_key=GEMINI_API_KEY)
semaphore = threading.Semaphore(MAX_THREADS)

def get_session_info_from_csv(csv_path: str, topic_name: str) -> Dict[str, str]:
    """從 CSV 檔案中獲取會議資訊"""
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get('Topic', '').strip() == topic_name.strip():
                    return {
                        'url': row.get('url', '').strip(),
                        'category': row.get('Type', '主題演講').strip(),
                        'description': row.get('Abstract', '').strip()
                    }
    except Exception as e:
        print(f"讀取 CSV 檔案時發生錯誤: {e}")
    
    return {
        'url': "https://aicon.infoq.cn/2025/shanghai/",
        'category': "主題演講",
        'description': ""
    }

def extract_ppt_content(pdf_path: pathlib.Path) -> Optional[str]:
    """使用 Gemini API 提取 PPT 內容"""
    try:
        file_name = pdf_path.stem
        session_info = get_session_info_from_csv(CSV_PATH, file_name)
        
        # 上傳檔案到 Gemini
        sample_file = genai_client.files.upload(file=pdf_path)
        
        # 提取內容的 prompt
        prompt = f"""
請提取這個 PPT 簡報的完整內容，並按照以下格式整理：

## 簡報標題
{file_name}

## 簡報內容
請逐頁提取簡報的文字內容，包括：
- 標題
- 重點內容
- 圖表說明
- 結論

要求：
1. 保持原始內容的邏輯結構
2. 將簡體中文轉換為繁體中文
3. 使用 Markdown 格式
4. 保留重要的技術術語和專有名詞
5. 如果有圖表，請描述其主要內容

請直接輸出整理後的內容，不需要額外說明。
"""

        # 呼叫 Gemini API
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=[sample_file, prompt]
        )
        
        return response.text
        
    except Exception as e:
        print(f"提取 PPT 內容時發生錯誤 ({pdf_path.name}): {e}")
        return None

def find_matching_session_in_bigquery(bq_client: BigQueryClient, session_name: str) -> Optional[str]:
    """在 BigQuery 中尋找匹配的會議記錄"""
    try:
        # 清理會議名稱，移除特殊字符
        clean_session_name = session_name.replace("'", "''").replace('"', '""')

        # 使用多種匹配策略
        queries = [
            # 精確匹配
            f"""
            SELECT conference_id, name
            FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
            WHERE seminar = '{SEMINAR_NAME}'
            AND LOWER(TRIM(name)) = LOWER(TRIM('{clean_session_name}'))
            LIMIT 1
            """,
            # 包含匹配
            f"""
            SELECT conference_id, name
            FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
            WHERE seminar = '{SEMINAR_NAME}'
            AND (
                LOWER(name) LIKE LOWER('%{clean_session_name}%') OR
                LOWER('{clean_session_name}') LIKE LOWER(CONCAT('%', name, '%'))
            )
            LIMIT 1
            """,
            # 關鍵詞匹配（提取主要詞彙）
            f"""
            SELECT conference_id, name
            FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
            WHERE seminar = '{SEMINAR_NAME}'
            AND (
                LOWER(name) LIKE '%ai%' AND LOWER('{clean_session_name}') LIKE '%ai%' OR
                LOWER(name) LIKE '%大模型%' AND LOWER('{clean_session_name}') LIKE '%大模型%' OR
                LOWER(name) LIKE '%數據%' AND LOWER('{clean_session_name}') LIKE '%數據%' OR
                LOWER(name) LIKE '%智能%' AND LOWER('{clean_session_name}') LIKE '%智能%'
            )
            LIMIT 3
            """
        ]

        for i, query in enumerate(queries):
            print(f"嘗試匹配策略 {i+1}: {session_name}")
            results = bq_client.query(query)

            for row in results:
                print(f"找到匹配的會議: {row['name']} -> {session_name}")
                return row['conference_id']

        # 如果都沒找到，列出所有可能的會議供參考
        print(f"未找到匹配的會議: {session_name}")
        print("可用的會議列表:")
        list_query = f"""
        SELECT conference_id, name
        FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        WHERE seminar = '{SEMINAR_NAME}'
        ORDER BY name
        LIMIT 10
        """
        results = bq_client.query(list_query)
        for row in results:
            print(f"  - {row['name']}")

    except Exception as e:
        print(f"查詢 BigQuery 時發生錯誤: {e}")

    return None

def update_ppt_content_in_bigquery(bq_client: BigQueryClient, conference_id: str, ppt_content: str) -> bool:
    """更新 BigQuery 中的 ppt_context 欄位"""
    try:
        # 轉義單引號
        escaped_content = ppt_content.replace("'", "''")
        
        update_query = f"""
        UPDATE `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
        SET ppt_context = '{escaped_content}'
        WHERE conference_id = '{conference_id}'
        """
        
        job = bq_client.client.query(update_query)
        job.result()  # 等待查詢完成
        
        print(f"成功更新會議 {conference_id} 的 PPT 內容")
        return True
        
    except Exception as e:
        print(f"更新 BigQuery 時發生錯誤: {e}")
        return False

def process_single_ppt(pdf_path: pathlib.Path, bq_client: BigQueryClient) -> bool:
    """處理單個 PPT 檔案"""
    with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"正在處理: {pdf_path.name} (嘗試第{attempt}次)")
                
                # 提取 PPT 內容
                ppt_content = extract_ppt_content(pdf_path)
                if not ppt_content:
                    print(f"無法提取 {pdf_path.name} 的內容")
                    return False
                
                # 尋找匹配的會議記錄
                session_name = pdf_path.stem
                conference_id = find_matching_session_in_bigquery(bq_client, session_name)
                
                if not conference_id:
                    print(f"在 BigQuery 中找不到匹配的會議: {session_name}")
                    return False
                
                # 更新 BigQuery
                success = update_ppt_content_in_bigquery(bq_client, conference_id, ppt_content)
                if success:
                    print(f"✅ 成功處理: {pdf_path.name}")
                    return True
                else:
                    print(f"❌ 更新失敗: {pdf_path.name}")
                    return False
                    
            except Exception as e:
                print(f"處理 {pdf_path.name} 時發生錯誤: {e}")
                if attempt < MAX_RETRIES:
                    print(f"{RETRY_DELAY}秒後重試...")
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"{pdf_path.name} 已達最大重試次數，跳過。")
                    return False
            finally:
                time.sleep(REQUEST_INTERVAL)
    
    return False

def main():
    """主函數"""
    print("開始批次處理 PPT 內容並上傳到 BigQuery...")
    print(f"PPT 目錄: {PPT_DIR}")
    print(f"CSV 檔案: {CSV_PATH}")
    print(f"研討會: {SEMINAR_NAME}")
    
    # 檢查必要的環境變數
    if not BQ_CREDENTIALS or not BQ_PROJECT_ID:
        print("❌ 請設置 GOOGLE_APPLICATION_CREDENTIALS 和 GOOGLE_CLOUD_PROJECT 環境變數")
        return
    
    # 初始化 BigQuery 客戶端
    try:
        bq_client = BigQueryClient(credentials_path=BQ_CREDENTIALS, project_id=BQ_PROJECT_ID)
        print("✅ BigQuery 客戶端初始化成功")
    except Exception as e:
        print(f"❌ BigQuery 客戶端初始化失敗: {e}")
        return
    
    # 獲取所有 PDF 檔案
    pdf_files = list(PPT_DIR.glob("*.pdf"))
    if not pdf_files:
        print(f"❌ 在 {PPT_DIR} 中找不到 PDF 檔案")
        return
    
    print(f"找到 {len(pdf_files)} 個 PDF 檔案")
    
    # 處理檔案
    success_count = 0
    total_count = len(pdf_files)
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{total_count}] 處理檔案: {pdf_file.name}")
        if process_single_ppt(pdf_file, bq_client):
            success_count += 1
    
    print(f"\n處理完成！成功: {success_count}/{total_count}")

if __name__ == "__main__":
    main()
