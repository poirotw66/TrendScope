#!/usr/bin/env python3
"""
測試 PPT 內容更新功能
"""

import os
import sys
import pathlib

# 添加專案根目錄到 Python 路徑
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from google.cloud import bigquery

# BigQuery 配置
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"

def update_ppt_content_in_bigquery(client: bigquery.Client, conference_id: str, ppt_content: str) -> bool:
    """更新 BigQuery 中的 ppt_context 欄位"""
    try:
        # 使用參數化查詢避免 SQL 注入和字符轉義問題
        update_query = f"""
        UPDATE `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
        SET ppt_context = @ppt_content
        WHERE conference_id = @conference_id
        """
        
        # 配置查詢參數
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("ppt_content", "STRING", ppt_content),
                bigquery.ScalarQueryParameter("conference_id", "STRING", conference_id),
            ]
        )
        
        job = client.query(update_query, job_config=job_config)
        job.result()  # 等待查詢完成
        
        print(f"✅ 成功更新會議 {conference_id} 的 PPT 內容")
        return True
        
    except Exception as e:
        print(f"❌ 更新 BigQuery 時發生錯誤: {e}")
        return False

def test_ppt_update():
    """測試 PPT 內容更新"""
    client = bigquery.Client()
    
    # 測試內容 - 包含各種特殊字符
    test_content = """# 測試 PPT 內容

## 包含特殊字符的測試
- 單引號: It's a test
- 雙引號: "Hello World"
- 反斜線: C:\\Users\\test
- 換行符和特殊符號: 
  * 百分號: 100%
  * 美元符號: $100
  * 井號: #hashtag

## 中文內容
這是一個包含中文的測試內容，用來驗證 BigQuery 更新功能。

### 程式碼範例
```python
def hello_world():
    print("Hello, World!")
    return True
```

### 結論
如果這個內容能夠成功更新到 BigQuery，說明我們的參數化查詢修正是有效的。
"""

    # 使用已知的會議 ID 進行測試
    test_conference_id = "815e7965-1e3e-419e-b52a-0287c80a603d"
    
    print("開始測試 PPT 內容更新...")
    print(f"目標會議 ID: {test_conference_id}")
    print(f"測試內容長度: {len(test_content)} 字符")
    
    # 執行更新
    success = update_ppt_content_in_bigquery(client, test_conference_id, test_content)
    
    if success:
        print("\n🎉 測試成功！")
        
        # 驗證更新結果
        verify_query = f"""
        SELECT conference_id, name, 
               CASE WHEN ppt_context IS NOT NULL THEN LENGTH(ppt_context) ELSE 0 END as ppt_length
        FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
        WHERE conference_id = @conference_id
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("conference_id", "STRING", test_conference_id),
            ]
        )
        
        results = client.query(verify_query, job_config=job_config)
        for row in results:
            print(f"驗證結果:")
            print(f"  會議: {row['name']}")
            print(f"  PPT 長度: {row['ppt_length']} 字符")
            break
    else:
        print("\n❌ 測試失敗！")

def main():
    """主函數"""
    print("PPT 內容更新測試")
    print("=" * 50)
    
    # 檢查環境變數
    if not BQ_PROJECT_ID:
        print("❌ 請設置 GOOGLE_CLOUD_PROJECT 環境變數")
        return
    
    test_ppt_update()

if __name__ == "__main__":
    main()
