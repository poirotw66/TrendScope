#!/usr/bin/env python3
"""
更新 BigQuery 表結構，添加 ppt_context 欄位
"""

import os
import sys
import pathlib

# 使用標準導入（專案應作為 package 安裝：pip install -e .）
from scripts._setup_path import setup_path
setup_path()

from google.cloud import bigquery
from base.bigquery.client import BigQueryClient

# BigQuery 配置
BQ_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"

def update_table_schema():
    """更新表結構，添加 ppt_context 欄位"""
    try:
        # 初始化 BigQuery 客戶端
        bq_client = BigQueryClient(credentials_path=BQ_CREDENTIALS, project_id=BQ_PROJECT_ID)
        print("✅ BigQuery 客戶端初始化成功")
        
        # 獲取現有表
        table_ref = bq_client.client.dataset(DATASET_ID).table(TABLE_ID)
        table = bq_client.client.get_table(table_ref)
        
        print(f"當前表結構:")
        for field in table.schema:
            print(f"  - {field.name} ({field.field_type}, mode={field.mode})")
        
        # 檢查是否已經有 ppt_context 欄位
        existing_fields = [field.name for field in table.schema]
        if "ppt_context" in existing_fields:
            print("✅ ppt_context 欄位已存在，無需更新")
            return True
        
        # 創建新的 schema，添加 ppt_context 欄位
        new_schema = list(table.schema)
        
        # 在 tags 欄位之前插入 ppt_context 欄位
        ppt_context_field = bigquery.SchemaField(
            "ppt_context", 
            "STRING", 
            description="PPT 簡報內容"
        )
        
        # 找到 tags 欄位的位置
        tags_index = None
        for i, field in enumerate(new_schema):
            if field.name == "tags":
                tags_index = i
                break
        
        if tags_index is not None:
            new_schema.insert(tags_index, ppt_context_field)
        else:
            # 如果找不到 tags 欄位，就添加到最後
            new_schema.append(ppt_context_field)
        
        # 更新表結構
        table.schema = new_schema
        updated_table = bq_client.client.update_table(table, ["schema"])
        
        print("✅ 表結構更新成功！")
        print(f"新的表結構:")
        for field in updated_table.schema:
            print(f"  - {field.name} ({field.field_type}, mode={field.mode})")
        
        return True
        
    except Exception as e:
        print(f"❌ 更新表結構時發生錯誤: {e}")
        return False

def main():
    """主函數"""
    print("開始更新 BigQuery 表結構...")
    
    # 檢查必要的環境變數
    if not BQ_CREDENTIALS or not BQ_PROJECT_ID:
        print("❌ 請設置 GOOGLE_APPLICATION_CREDENTIALS 和 GOOGLE_CLOUD_PROJECT 環境變數")
        return
    
    print(f"專案 ID: {BQ_PROJECT_ID}")
    print(f"資料集: {DATASET_ID}")
    print(f"表名: {TABLE_ID}")
    
    success = update_table_schema()
    
    if success:
        print("\n🎉 表結構更新完成！現在可以執行 PPT 內容處理腳本。")
    else:
        print("\n❌ 表結構更新失敗。")

if __name__ == "__main__":
    main()
