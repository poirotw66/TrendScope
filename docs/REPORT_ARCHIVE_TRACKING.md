# 📋 報告檔案追蹤系統使用指南

## 概述

報告檔案追蹤系統提供了集中式的批量報告檔案管理機制，在每次成功生成報告並創建ZIP檔案時，自動在BigQuery中記錄詳細的檔案信息。

## 功能特點

- ✅ 自動記錄每個批量報告的詳細信息
- ✅ 追蹤本地和GCS存儲路徑
- ✅ 記錄檔案元數據和生成參數
- ✅ 提供完整的API接口查詢檔案記錄
- ✅ 支援檔案狀態管理和軟刪除
- ✅ 集成GCS上傳狀態追蹤

## 數據結構

### BigQuery 表結構 (`conference_data.report_archives`)

| 欄位名稱 | 類型 | 描述 |
|---------|------|------|
| `task_id` | STRING | 任務ID（主鍵） |
| `batch_id` | STRING | 報告批次ID |
| `zip_filename` | STRING | ZIP檔案名稱 |
| `gcs_path` | STRING | GCS存儲路徑 |
| `gcs_public_url` | STRING | GCS公開下載URL |
| `seminars` | STRING[] | 包含的研討會列表 |
| `session_count` | INTEGER | 包含的會議數量 |
| `analysis_mode` | STRING | 分析模式 |
| `output_template` | STRING | 輸出模板 |
| `updated_at` | TIMESTAMP | 更新時間 |

## API 端點

### 1. 列出檔案記錄

```http
GET /reports/archives?limit=50
```

**參數：**
- `limit` (可選): 返回記錄數量限制，默認50

**響應：**
```json
{
  "archives": [
    {
      "task_id": "task-uuid",
      "batch_id": "batch_20250109_143022",
      "zip_filename": "TrendScope-會議報告-batch_20250109_143022-20250109_143045.zip",
      "gcs_public_url": "https://storage.googleapis.com/neo-trend-hub-documents/seminar_report/...",
      "seminars": ["202503 AICon Shanghai"],
      "session_count": 10,
      "analysis_mode": "comprehensive",
      "output_template": "professional",
      "updated_at": "2025-01-09T14:30:45.123Z"
    }
  ],
  "total": 1
}
```

### 2. 根據批次ID獲取記錄

```http
GET /reports/archives/batch/{batch_id}
```

**響應：**
```json
{
  "task_id": "uuid-string",
  "batch_id": "batch_20250109_143022",
  "zip_filename": "TrendScope-會議報告-batch_20250109_143022-20250109_143045.zip",
  "gcs_public_url": "https://storage.googleapis.com/...",
  "metadata": {
    "hugo_info": {...},
    "total_pages": 15,
    "gcs_upload_success": true
  }
}
```

### 3. 根據任務ID獲取記錄

```http
GET /reports/archives/task/{task_id}
```

### 4. 刪除檔案記錄

```http
DELETE /reports/archives/task/{task_id}
```

**響應：**
```json
{
  "message": "任務 uuid-string 的檔案記錄已刪除"
}
```

## 自動記錄流程

當批量報告生成完成時，系統會自動：

1. **創建ZIP檔案** - 生成包含所有報告的離線分享包
2. **上傳到GCS** - 如果啟用GCS上傳功能
3. **記錄到BigQuery** - 自動創建檔案追蹤記錄
4. **更新狀態** - 根據GCS上傳結果更新記錄狀態

## 使用範例

### 查詢最近的報告檔案

```bash
curl "http://localhost:8000/reports/archives?limit=10"
```

### 查詢特定批次的檔案信息

```bash
curl "http://localhost:8000/reports/archives/batch/batch_20250109_143022"
```

### 查詢特定任務的檔案信息

```bash
curl "http://localhost:8000/reports/archives/task/aa440537-a837-4371-be18-f3801914c7eb"
```

### 查詢最近的10個檔案

```bash
curl "http://localhost:8000/reports/archives?limit=10"
```

## 元數據信息

`metadata` 欄位包含額外的詳細信息：

```json
{
  "hugo_info": {
    "site_title": "TrendScope 會議報告",
    "total_pages": 15
  },
  "total_pages": 15,
  "launcher_file": "/path/to/launcher.html",
  "instructions_file": "/path/to/instructions.txt",
  "gcs_upload_enabled": true,
  "gcs_upload_success": true
}
```

## 測試功能

運行測試腳本驗證檔案追蹤功能：

```bash
python test_report_archive_manager.py
```

測試腳本會：
1. 創建測試ZIP檔案
2. 測試BigQuery連接
3. 創建檔案追蹤記錄
4. 測試記錄檢索功能
5. 測試記錄更新功能
6. 清理測試數據

## 故障排除

### 常見問題

1. **BigQuery表不存在**
   ```
   錯誤: Table not found
   解決: 系統會自動創建表，確保BigQuery權限正確
   ```

2. **記錄創建失敗**
   ```
   錯誤: 創建檔案追蹤記錄失敗
   解決: 檢查BigQuery連接和權限設置
   ```

3. **檔案路徑錯誤**
   ```
   錯誤: 檔案大小獲取失敗
   解決: 確保ZIP檔案路徑正確且檔案存在
   ```

### 日誌檢查

查看應用程序日誌以獲取詳細信息：

```bash
# 檢查檔案追蹤相關日誌
tail -f /path/to/your/app.log | grep "檔案追蹤"
```

## 數據備份和維護

### 定期清理

建議定期清理舊的檔案記錄：

```sql
-- 軟刪除30天前的記錄
UPDATE `your-project.conference_data.report_archives`
SET status = 'archived', updated_at = CURRENT_TIMESTAMP()
WHERE created_at < TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
  AND status = 'active'
```

### 數據導出

導出檔案追蹤記錄：

```sql
-- 導出最近7天的記錄
SELECT *
FROM `your-project.conference_data.report_archives`
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY created_at DESC
```

## 集成前端

前端可以使用這些API端點來：

1. **顯示檔案列表** - 在管理界面顯示所有報告檔案
2. **提供下載連結** - 直接連結到GCS或本地下載URL
3. **檔案狀態監控** - 顯示檔案上傳和處理狀態
4. **搜索和過濾** - 根據日期、狀態、研討會等條件過濾檔案

這個系統提供了完整的檔案生命週期管理，確保每個生成的報告都有完整的追蹤記錄。
