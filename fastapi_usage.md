# TrendScope FastAPI 應用程式 API 使用指南

## 概述

TrendScope 後端基於 FastAPI 框架構建，提供模組化的 API 服務，包含 PPT 上傳處理、爬蟲控制、BigQuery 資料查詢和批量報告生成功能。

## 應用程式結構

### 主要文件
- **主啟動文件**: `backend/main.py`
- **FastAPI 應用**: `backend/api/app.py`
- **路由模組**: `backend/api/routes/`

### 已註冊的路由器

| 路由器 | 前綴 | 功能模組 | 描述 |
|--------|------|----------|------|
| `ppt_router` | `/ppt` | PPT Upload | PPT/PDF 文件上傳和處理 |
| `scrapers_router` | `/scrapers` | Scrapers | 網站爬蟲控制和管理 |
| `bigquery_router` | `/data` | BigQuery Data | BigQuery 資料查詢和統計 |
| `batch_reports_router` | `/reports` | Batch Reports | 批量報告生成和下載 |

## 服務配置

- **基礎 URL**: `http://localhost:8001`
- **API 文檔**: `http://localhost:8001/docs`
- **CORS**: 允許所有來源（生產環境需限制）

## API 端點詳細說明

### 1. 根端點

#### GET /
- **功能**: API 根端點，返回歡迎信息
- **響應**: `{"message": "歡迎使用 TrendScope API"}`

```bash
curl -X GET "http://localhost:8001/"
```

---

## 2. PPT 上傳處理功能 (`/ppt`)

### 2.1 上傳 PPT 文件

#### POST /ppt/upload
- **功能**: 上傳 PPT/PDF 文件並開始處理
- **支援格式**: .ppt, .pptx, .pdf
- **處理流程**: 文件匹配 → 內容提取 → BigQuery 更新

**請求參數**:
- `files`: 多個文件（multipart/form-data）
- `seminar`: 研討會名稱（form field）

```bash
curl -X POST "http://localhost:8001/ppt/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "files=@presentation1.pptx" \
  -F "files=@presentation2.pdf" \
  -F "seminar=QCon Beijing 2025"
```

**響應**:
```json
{
  "task_id": "uuid-string",
  "message": "已開始處理 2 個 PPT 檔案",
  "files_count": 2
}
```

### 2.2 查詢處理狀態

#### GET /ppt/status/{task_id}
- **功能**: 獲取 PPT 處理任務狀態
- **參數**: `task_id` - 任務 ID

```bash
curl -X GET "http://localhost:8001/ppt/status/{task_id}"
```

**響應**:
```json
{
  "task_id": "uuid-string",
  "status": "processing",
  "progress": 60,
  "message": "已完成 1/2 個檔案",
  "files": [
    {
      "filename": "presentation1.pptx",
      "status": "success",
      "progress": 100,
      "matched_session": "AI 技術趨勢分析",
      "similarity": 0.85,
      "ppt_length": 1500
    }
  ]
}
```

### 2.3 獲取可用研討會

#### GET /ppt/seminars
- **功能**: 獲取 BigQuery 中可用的研討會列表

```bash
curl -X GET "http://localhost:8001/ppt/seminars"
```

**響應**:
```json
{
  "seminars": [
    {
      "name": "QCon Beijing 2025",
      "session_count": 45
    },
    {
      "name": "AICon Shanghai 2025",
      "session_count": 38
    }
  ]
}
```

### 2.4 調試端點

#### GET /ppt/debug/tasks
- **功能**: 獲取所有 PPT 處理任務狀態（調試用）

```bash
curl -X GET "http://localhost:8001/ppt/debug/tasks"
```

---

## 3. 爬蟲控制功能 (`/scrapers`)

### 3.1 啟動爬蟲任務

#### POST /scrapers/run
- **功能**: 啟動指定的爬蟲任務
- **支援爬蟲**: aws_london, aicon_infoq, qcon_infoq

**請求體**:
```json
{
  "scraper_type": "qcon_infoq",
  "headless": true,
  "wait_time": 30,
  "use_bigquery": true
}
```

```bash
curl -X POST "http://localhost:8001/scrapers/run" \
  -H "Content-Type: application/json" \
  -d '{
    "scraper_type": "qcon_infoq",
    "headless": true,
    "wait_time": 30,
    "use_bigquery": true
  }'
```

**響應**:
```json
{
  "task_id": "uuid-string",
  "message": "已啟動爬蟲任務: qcon_infoq",
  "status": "pending"
}
```

### 3.2 查詢爬蟲狀態

#### GET /scrapers/status/{task_id}
- **功能**: 獲取爬蟲任務執行狀態

```bash
curl -X GET "http://localhost:8001/scrapers/status/{task_id}"
```

**響應**:
```json
{
  "task_id": "uuid-string",
  "status": "completed",
  "file_path": "/path/to/scraped_data.xlsx",
  "message": "qcon_infoq 爬蟲執行完成",
  "data": [...]
}
```

### 3.3 列出可用爬蟲

#### GET /scrapers/list
- **功能**: 獲取所有可用的爬蟲列表

```bash
curl -X GET "http://localhost:8001/scrapers/list"
```

**響應**:
```json
{
  "scrapers": [
    {
      "id": "aws_london",
      "name": "AWS London Summit",
      "description": "爬取 AWS London Summit 的會議資訊"
    },
    {
      "id": "aicon_infoq",
      "name": "AICon InfoQ 2025 Shanghai",
      "description": "爬取 AICon (InfoQ) 2025 上海議程與摘要"
    },
    {
      "id": "qcon_infoq",
      "name": "QCon InfoQ 2025 Beijing",
      "description": "爬取 QCon (InfoQ) 2025 北京議程與摘要"
    }
  ]
}
```

---

## 4. BigQuery 資料查詢功能 (`/data`)

### 4.1 查詢會議資料

#### GET /data/sessions
- **功能**: 從 BigQuery 獲取會議資料
- **查詢參數**:
  - `source`: 資料來源篩選（可選）
  - `seminar`: 研討會名稱篩選（可選）
  - `limit`: 返回結果數量限制（1-500，預設 20）

```bash
# 獲取所有會議資料
curl -X GET "http://localhost:8001/data/sessions?limit=50"

# 篩選特定研討會
curl -X GET "http://localhost:8001/data/sessions?seminar=QCon%20Beijing%202025&limit=20"

# 篩選特定來源
curl -X GET "http://localhost:8001/data/sessions?source=infoq&limit=30"
```

**響應**:
```json
{
  "sessions": [
    {
      "id": "session-id",
      "name": "AI 技術趨勢分析",
      "description": "深入探討當前 AI 技術發展趨勢...",
      "speaker": "張三",
      "seminar": "QCon Beijing 2025",
      "source": "infoq",
      "url": "https://...",
      "ppt_context": "PPT 內容摘要..."
    }
  ]
}
```

### 4.2 獲取研討會列表

#### GET /data/seminars
- **功能**: 獲取所有可用的研討會列表及會議數量

```bash
curl -X GET "http://localhost:8001/data/seminars"
```

**響應**:
```json
{
  "seminars": [
    {
      "name": "QCon Beijing 2025",
      "session_count": 45
    },
    {
      "name": "AICon Shanghai 2025",
      "session_count": 38
    }
  ]
}
```

### 4.3 獲取資料統計

#### GET /data/stats
- **功能**: 獲取 BigQuery 中的資料統計資訊

```bash
curl -X GET "http://localhost:8001/data/stats"
```

**響應**:
```json
{
  "total_sessions": 150,
  "total_seminars": 5,
  "sessions_with_ppt": 45,
  "latest_update": null
}
```

### 4.4 健康檢查

#### GET /data/health
- **功能**: 檢查 BigQuery 連接健康狀態

```bash
curl -X GET "http://localhost:8001/data/health"
```

**響應**:
```json
{
  "status": "healthy",
  "message": "BigQuery 連接正常",
  "project_id": "your-project-id",
  "connected": true
}
```

---

## 5. 批量報告生成功能 (`/reports`)

### 5.1 獲取可用研討會

#### GET /reports/seminars
- **功能**: 獲取可用於報告生成的研討會列表（僅包含有 PPT 內容的會議）

```bash
curl -X GET "http://localhost:8001/reports/seminars"
```

**響應**:
```json
{
  "seminars": [
    {
      "name": "QCon Beijing 2025",
      "session_count": 45,
      "sessions_with_ppt": 12
    },
    {
      "name": "AICon Shanghai 2025",
      "session_count": 38,
      "sessions_with_ppt": 8
    }
  ]
}
```

### 5.2 生成批量報告

#### POST /reports/generate-batch
- **功能**: 啟動批量報告生成任務
- **特色**: 支援多種分析模式和輸出樣板，自動生成 Hugo 靜態網站

**請求體**:
```json
{
  "seminars": ["QCon Beijing 2025", "AICon Shanghai 2025"],
  "limit": 10,
  "output_format": "both",
  "include_html": true,
  "analysis_mode": "comprehensive",
  "output_template": "professional"
}
```

**參數說明**:
- `seminars`: 要處理的研討會列表（可選，null 表示處理所有）
- `limit`: 每個研討會的會議數量限制（可選）
- `output_format`: 輸出格式（"markdown", "html", "both"）
- `include_html`: 是否包含 HTML 輸出
- `analysis_mode`: 分析模式
  - `"technical"`: 技術深度分析
  - `"business"`: 商業價值分析
  - `"trend"`: 趨勢洞察分析
  - `"comprehensive"`: 綜合分析（預設）
- `output_template`: 輸出樣板
  - `"professional"`: 專業商務風格（預設）
  - `"technical"`: 技術文檔風格
  - `"concise"`: 簡潔摘要風格
  - `"presentation"`: 簡報風格

```bash
curl -X POST "http://localhost:8001/reports/generate-batch" \
  -H "Content-Type: application/json" \
  -d '{
    "seminars": ["QCon Beijing 2025"],
    "limit": 5,
    "output_format": "both",
    "include_html": true,
    "analysis_mode": "comprehensive",
    "output_template": "professional"
  }'
```

**響應**:
```json
{
  "task_id": "uuid-string",
  "message": "已啟動批量報告生成任務",
  "status": "pending",
  "seminars_to_process": ["QCon Beijing 2025"],
  "estimated_sessions": 5,
  "estimated_time": "約 15-20 分鐘"
}
```

### 5.3 查詢報告生成狀態

#### GET /reports/status/{task_id}
- **功能**: 獲取批量報告生成任務狀態

```bash
curl -X GET "http://localhost:8001/reports/status/{task_id}"
```

**響應**:
```json
{
  "task_id": "uuid-string",
  "status": "running",
  "progress": {
    "current_seminar": "QCon Beijing 2025",
    "current_session": "AI 技術趨勢分析",
    "completed_sessions": 3,
    "total_sessions": 5,
    "percentage": 60
  },
  "start_time": "2025-07-07T10:30:00",
  "end_time": null,
  "error_message": null,
  "results": null
}
```

### 5.4 列出所有報告任務

#### GET /reports/list
- **功能**: 列出所有批量報告生成任務

```bash
curl -X GET "http://localhost:8001/reports/list"
```

### 5.5 獲取報告文件列表

#### GET /reports/files
- **功能**: 獲取所有生成的報告文件列表，包含任務狀態信息

```bash
curl -X GET "http://localhost:8001/reports/files"
```

**響應**:
```json
{
  "reports": [
    {
      "batch_id": "batch_20250707_103000",
      "task_status": "completed",
      "creation_time": "2025-07-07T10:30:00",
      "html_files": [
        "reports/batch_20250707_103000/html/posts/report-1/index.html",
        "reports/batch_20250707_103000/html/posts/report-2/index.html"
      ],
      "markdown_files": [
        "reports/batch_20250707_103000/md/report-1.md",
        "reports/batch_20250707_103000/md/report-2.md"
      ],
      "zip_file": "reports/batch_20250707_103000/TrendScope-會議報告-20250707_103000-20250707_104500.zip",
      "total_files": 15,
      "total_reports": 5
    }
  ]
}
```

### 5.6 預覽報告文件

#### GET /reports/preview/{file_path:path}
- **功能**: 預覽報告文件內容（HTML 或 Markdown）

```bash
curl -X GET "http://localhost:8001/reports/preview/batch_20250707_103000/html/posts/report-1/index.html"
```

### 5.7 下載報告文件

#### GET /reports/download/{file_path:path}
- **功能**: 下載單個報告文件

```bash
curl -X GET "http://localhost:8001/reports/download/batch_20250707_103000/md/report-1.md" \
  -o "report-1.md"
```

### 5.8 下載任務 ZIP 文件

#### GET /reports/{task_id}/download-zip
- **功能**: 下載指定任務的完整 ZIP 文件（包含離線瀏覽器）

```bash
curl -X GET "http://localhost:8001/reports/{task_id}/download-zip" \
  -o "reports.zip"
```

### 5.9 下載 ZIP 文件（按文件名）

#### GET /reports/download-zip/{zip_filename}
- **功能**: 按文件名下載 ZIP 文件

```bash
curl -X GET "http://localhost:8001/reports/download-zip/TrendScope-會議報告-20250707_103000-20250707_104500.zip" \
  -o "reports.zip"
```

### 5.10 列出可用 ZIP 文件

#### GET /reports/list-zip-files
- **功能**: 列出所有可用的 ZIP 文件

```bash
curl -X GET "http://localhost:8001/reports/list-zip-files"
```

**響應**:
```json
[
  "TrendScope-會議報告-20250707_103000-20250707_104500.zip",
  "TrendScope-會議報告-20250706_104619-20250706_105702.zip"
]
```

---

## 環境變數配置

### 必要環境變數

```bash
# Google Cloud 配置
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"

# Gemini API 配置
export GEMINI_API_KEY="your-gemini-api-key"
```

### 啟動服務

```bash
# 啟動後端服務
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001

# 或使用主啟動文件
python main.py
```

---

## 錯誤處理

所有 API 端點都遵循標準的 HTTP 狀態碼：

- **200**: 成功
- **400**: 請求錯誤（參數無效等）
- **404**: 資源不存在
- **500**: 服務器內部錯誤

錯誤響應格式：
```json
{
  "detail": "錯誤描述信息"
}
```

---

## 任務管理

TrendScope 使用共享任務管理系統來追蹤長時間運行的操作：

- **PPT 處理任務**: 類型為 `"ppt_upload"`
- **爬蟲任務**: 類型為 `"scraper"`
- **批量報告任務**: 類型為 `"batch_report"`

每個任務都有唯一的 UUID，可以通過相應的狀態端點查詢進度。

---

## 總結

TrendScope FastAPI 後端提供了完整的會議資料處理流水線：

1. **資料收集**: 透過爬蟲自動收集會議資訊
2. **內容增強**: 上傳 PPT 文件並自動匹配到相應會議
3. **資料查詢**: 透過 BigQuery 進行高效的資料查詢和統計
4. **報告生成**: 使用 AI 生成詳細的會議分析報告
5. **靜態網站**: 自動生成 Hugo 靜態網站供離線瀏覽
