"""
會議數據表結構定義
用於 BigQuery 表創建和數據上傳
"""
from google.cloud import bigquery

# 會議表結構
CONFERENCE_SCHEMA = [
    bigquery.SchemaField("conference_id", "STRING", mode="REQUIRED", description="唯一識別碼"),
    bigquery.SchemaField("seminar", "STRING", mode="REQUIRED", description="研討會 ID"),
    bigquery.SchemaField("name", "STRING", mode="REQUIRED", description="會議名稱"),
    bigquery.SchemaField("description", "STRING", description="會議描述"),
    bigquery.SchemaField("url", "STRING", description="會議連結"),
    bigquery.SchemaField("pdf_url", "STRING", description="PDF 連結"),
    bigquery.SchemaField("tags", "STRING", mode="REPEATED", description="會議標籤"),
    bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED", description="創建時間")
]

# 會議摘要表結構
CONFERENCE_SUMMARY_SCHEMA = [
    bigquery.SchemaField("conference_id", "STRING", mode="REQUIRED", description="會議 ID"),
    bigquery.SchemaField("summary", "STRING", description="會議摘要"),
    bigquery.SchemaField("keywords", "STRING", mode="REPEATED", description="關鍵詞"),
    bigquery.SchemaField("created_at", "TIMESTAMP", mode="REQUIRED", description="創建時間")
]
