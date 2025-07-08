# Google Cloud Storage 自動上傳功能設置指南

## 概述

本功能實現了將批量報告生成的 ZIP 檔案自動上傳到 Google Cloud Storage (GCS) 作為備份和遠程訪問方案。

## 功能特點

- ✅ 自動上傳 ZIP 檔案到 GCS bucket
- ✅ 生成公開可訪問的 URL
- ✅ 保留本地檔案存儲
- ✅ 完整的錯誤處理機制
- ✅ 上傳失敗不影響整個任務完成
- ✅ API 響應包含 GCS URL

## 環境設置

### 1. 安裝依賴項

確保已安裝 Google Cloud Storage 客戶端庫：

```bash
pip install google-cloud-storage>=2.0.0
```

### 2. 設置 Google Cloud 憑證

#### 方法一：使用服務帳戶金鑰文件

1. 在 Google Cloud Console 中創建服務帳戶
2. 下載服務帳戶金鑰 JSON 文件
3. 設置環境變量：

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

#### 方法二：使用 gcloud CLI

```bash
gcloud auth application-default login
gcloud config set project your-project-id
```

### 3. 配置 GCS Bucket

確保您的 GCS bucket `neo-trend-hub-documents` 已創建並具有適當的權限：

```bash
# 創建 bucket（如果不存在）
gsutil mb gs://neo-trend-hub-documents

# 設置 bucket 權限（可選，用於公開訪問）
gsutil iam ch allUsers:objectViewer gs://neo-trend-hub-documents
```

## 使用方式

### 1. 通過 API 生成批量報告

```bash
curl -X POST "http://localhost:8000/reports/generate-batch" \
  -H "Content-Type: application/json" \
  -d '{
    "seminars": ["202503 AICon Shanghai"],
    "limit": 10,
    "include_html": true,
    "analysis_mode": "comprehensive",
    "output_template": "professional"
  }'
```

### 2. 檢查任務狀態

```bash
curl "http://localhost:8000/reports/status/{task_id}"
```

### 3. 檢查 GCS 連接狀態

```bash
curl "http://localhost:8000/reports/gcs-status"
```

## API 響應格式

### 成功完成的任務響應

```json
{
  "task_id": "uuid-string",
  "status": "completed",
  "results": {
    "processed_sessions": 10,
    "failed_sessions": 0,
    "offline_package": {
      "zip_file": "/path/to/local/file.zip",
      "download_url": "/reports/download-zip/filename.zip",
      "gcs_url": "gs://neo-trend-hub-documents/seminar_report/filename.zip",
      "gcs_public_url": "https://storage.googleapis.com/neo-trend-hub-documents/seminar_report/filename.zip",
      "gcs_size": 1234567,
      "site_info": {...}
    }
  }
}
```

### GCS 狀態檢查響應

```json
{
  "gcs_available": true,
  "credentials_configured": true,
  "project_id_configured": true,
  "bucket_accessible": true,
  "bucket_name": "neo-trend-hub-documents",
  "error_message": null
}
```

## 文件結構

```
base/
├── gcs/
│   ├── __init__.py
│   └── client.py          # GCS 客戶端實現
├── api/
│   └── routes/
│       └── batch_reports.py  # 修改後的批量報告 API
└── ...

test_gcs_upload.py         # GCS 上傳功能測試腳本
docs/
└── GCS_UPLOAD_SETUP.md    # 本文檔
```

## 測試功能

### 運行測試腳本

```bash
python test_gcs_upload.py
```

測試腳本會：
1. 檢查環境變量配置
2. 測試 GCS 客戶端初始化
3. 驗證 bucket 訪問權限
4. 上傳測試文件
5. 清理測試文件

### 預期輸出

```
🚀 開始測試 Google Cloud Storage 上傳功能
============================================================
✅ 測試 ZIP 文件已創建: /tmp/test_report_package.zip
🔧 測試 GCS 客戶端初始化...
📋 GOOGLE_APPLICATION_CREDENTIALS: /path/to/credentials.json
📋 GOOGLE_CLOUD_PROJECT: your-project-id
✅ GCS 客戶端初始化成功
🪣 測試 bucket 訪問權限: neo-trend-hub-documents
✅ Bucket 'neo-trend-hub-documents' 存在且可訪問
📤 測試文件上傳到 GCS...
✅ 文件上傳成功!
📍 GCS URL: gs://neo-trend-hub-documents/test_uploads/test_report_package.zip
🌐 公開 URL: https://storage.googleapis.com/neo-trend-hub-documents/test_uploads/test_report_package.zip
📏 文件大小: 1234 字節
============================================================
📊 測試結果總結:
✅ 所有測試通過!
🎉 GCS 上傳功能正常工作
🔗 測試文件可通過以下 URL 訪問:
   https://storage.googleapis.com/neo-trend-hub-documents/test_uploads/test_report_package.zip
============================================================
```

## 故障排除

### 常見問題

1. **憑證未設置**
   ```
   錯誤: 未設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量
   解決: 設置正確的憑證文件路徑
   ```

2. **Bucket 不存在**
   ```
   錯誤: Bucket 'neo-trend-hub-documents' 不存在或無法訪問
   解決: 創建 bucket 或檢查權限設置
   ```

3. **權限不足**
   ```
   錯誤: 403 Forbidden
   解決: 確保服務帳戶具有 Storage Object Admin 權限
   ```

### 日誌檢查

查看應用程序日誌以獲取詳細的錯誤信息：

```bash
# 檢查 FastAPI 應用日誌
tail -f /path/to/your/app.log | grep GCS
```

## 安全考慮

1. **憑證安全**: 確保服務帳戶金鑰文件安全存儲，不要提交到版本控制系統
2. **Bucket 權限**: 根據需要設置適當的 bucket 權限
3. **網絡安全**: 考慮使用 VPC 和防火牆規則限制訪問

## 監控和維護

1. **定期檢查**: 使用 `/reports/gcs-status` 端點監控 GCS 連接狀態
2. **存儲成本**: 定期清理不需要的文件以控制存儲成本
3. **備份策略**: 考慮設置 bucket 的生命週期管理規則
