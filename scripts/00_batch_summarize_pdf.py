"""
BigQuery 批量會議報告生成器
從 BigQuery 數據庫獲取會議數據並生成報告

修改自原始的 PDF 處理腳本，現在使用 BigQuery 作為數據源
"""

import os
import sys
import pathlib
import threading
import time
import argparse
from typing import Optional, List, Dict, Any
from datetime import datetime

# 使用標準導入（專案應作為 package 安裝：pip install -e .）
from scripts._setup_path import setup_path
setup_path()

from src.batch_md_to_html_pdf import batch_md_to_html
from base.bigquery.client import BigQueryClient
from google import genai
from config.config import GEMINI_API_KEY

# 配置參數
MAX_THREADS = 4
REQUEST_INTERVAL = 4
MAX_RETRIES = 3
RETRY_DELAY = 10  # 秒

# BigQuery 配置
BQ_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"

# 初始化客戶端
genai_client = genai.Client(api_key=GEMINI_API_KEY)
semaphore = threading.Semaphore(MAX_THREADS)

def get_sessions_from_bigquery(bq_client: BigQueryClient, seminar: Optional[str] = None,
                               limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    從 BigQuery 獲取會議數據

    Args:
        bq_client: BigQuery 客戶端
        seminar: 可選的研討會過濾條件
        limit: 可選的結果數量限制

    Returns:
        會議數據列表
    """
    try:
        # 構建查詢
        query = f"SELECT * FROM `{bq_client.project_id}.{DATASET_ID}.{TABLE_ID}`"

        # 添加過濾條件
        where_conditions = []
        if seminar:
            where_conditions.append(f"seminar = '{seminar}'")

        # 只處理有 PPT 內容的會議
        where_conditions.append("ppt_context IS NOT NULL AND LENGTH(TRIM(ppt_context)) > 0")

        if where_conditions:
            query += " WHERE " + " AND ".join(where_conditions)

        # 添加排序
        query += " ORDER BY created_at DESC"

        # 添加限制
        if limit:
            query += f" LIMIT {limit}"

        print(f"執行查詢: {query}")
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

        print(f"獲取到 {len(sessions)} 個會議數據")
        return sessions

    except Exception as e:
        print(f"從 BigQuery 獲取數據時發生錯誤: {e}")
        raise


def summarize_session_from_bigquery(session_data: Dict[str, Any], output_dir: str):
    """
    使用 BigQuery 中的會議數據生成摘要

    Args:
        session_data: 會議數據字典
        output_dir: 輸出目錄
    """
    try:
        conference_id = session_data.get('conference_id', 'unknown')
        name = session_data.get('name', 'Unknown Session')
        seminar = session_data.get('seminar', 'Unknown Seminar')
        url = session_data.get('url', 'TEST.com')
        ppt_context = session_data.get('ppt_context', '')
        description = session_data.get('description', '')

        # 確定會議類型
        category = "主題演講"  # 默認類型，可以根據需要調整

        if not ppt_context:
            print(f"跳過 {name}: 沒有 PPT 內容")
            return

        print(f"正在處理會議: {name}")

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
  - 範例：
    ```
    # OpenAI Developer Day 2024
    主題演講
    [會議影片連結](https://example.com)
    OpenAI 開發者日 2024
    ```

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

        # 調用 Gemini API
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

        print(f"已將摘要儲存至 {output_path}")

    except Exception as e:
        print(f"處理會議 {session_data.get('name', 'unknown')} 時發生錯誤: {e}")
        raise


def worker(session_data: Dict[str, Any], output_dir: str):
    """
    工作線程函數，處理單個會議數據

    Args:
        session_data: 會議數據字典
        output_dir: 輸出目錄
    """
    with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                session_name = session_data.get('name', 'Unknown Session')
                print(f"正在處理: {session_name} (嘗試第{attempt}次)")
                summarize_session_from_bigquery(session_data, output_dir)
                break  # 成功則跳出重試迴圈
            except Exception as e:
                print(f"處理 {session_name} 發生錯誤: {e}")
                if attempt < MAX_RETRIES:
                    print(f"{RETRY_DELAY}秒後重試...")
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"{session_name} 已達最大重試次數，跳過。")
        time.sleep(REQUEST_INTERVAL)

def main():
    """
    主函數：從 BigQuery 獲取數據並生成報告
    """
    parser = argparse.ArgumentParser(description="從 BigQuery 批量生成會議報告")
    parser.add_argument("--seminar", help="研討會過濾條件 (例如: '202503 QCon Beijing')")
    parser.add_argument("--limit", type=int, help="處理的會議數量限制")
    parser.add_argument("--output-md-dir", default="reports/md", help="Markdown 輸出目錄")
    parser.add_argument("--output-html-dir", default="reports/html", help="HTML 輸出目錄")
    parser.add_argument("--skip-html", action="store_true", help="跳過 HTML 生成")
    parser.add_argument("--list-seminars", action="store_true", help="列出可用的研討會")

    args = parser.parse_args()

    # 初始化 BigQuery 客戶端
    try:
        if not BQ_CREDENTIALS:
            print("錯誤: 未設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量")
            return 1

        if not BQ_PROJECT_ID:
            print("錯誤: 未設置 GOOGLE_CLOUD_PROJECT 環境變量")
            return 1

        bq_client = BigQueryClient(
            credentials_path=BQ_CREDENTIALS,
            project_id=BQ_PROJECT_ID
        )
        print(f"已連接到 BigQuery 項目: {BQ_PROJECT_ID}")

    except Exception as e:
        print(f"初始化 BigQuery 客戶端失敗: {e}")
        return 1

    # 列出可用研討會
    if args.list_seminars:
        try:
            query = f"""
            SELECT seminar, COUNT(*) as session_count,
                   SUM(CASE WHEN ppt_context IS NOT NULL AND LENGTH(TRIM(ppt_context)) > 0 THEN 1 ELSE 0 END) as sessions_with_ppt
            FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
            GROUP BY seminar
            ORDER BY session_count DESC
            """
            results = bq_client.query(query)

            print("\n可用的研討會:")
            print("-" * 80)
            print(f"{'研討會名稱':<40} {'總會議數':<10} {'有PPT內容':<10}")
            print("-" * 80)

            for row in results:
                print(f"{row['seminar']:<40} {row['session_count']:<10} {row['sessions_with_ppt']:<10}")

            return 0

        except Exception as e:
            print(f"獲取研討會列表失敗: {e}")
            return 1

    # 獲取會議數據
    try:
        sessions = get_sessions_from_bigquery(bq_client, args.seminar, args.limit)

        if not sessions:
            print("沒有找到符合條件的會議數據")
            return 1

        print(f"找到 {len(sessions)} 個會議，開始處理...")

    except Exception as e:
        print(f"獲取會議數據失敗: {e}")
        return 1

    # 創建輸出目錄
    output_md_dir = pathlib.Path(args.output_md_dir)
    output_html_dir = pathlib.Path(args.output_html_dir)

    # 多線程處理會議數據
    threads = []
    for session in sessions:
        t = threading.Thread(target=worker, args=(session, str(output_md_dir)))
        threads.append(t)
        t.start()

    # 等待所有線程完成
    for t in threads:
        t.join()

    print("所有會議處理完成")

    # 生成 HTML 報告
    if not args.skip_html:
        try:
            print("開始生成 HTML 報告...")
            batch_md_to_html(str(output_md_dir), str(output_html_dir), 3)
            print(f"HTML 報告已生成到: {output_html_dir}")
        except Exception as e:
            print(f"生成 HTML 報告時發生錯誤: {e}")
            return 1

    print("報告生成完成!")
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)