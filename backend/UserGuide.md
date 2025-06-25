### TrendScope API 使用者指南

歡迎使用 TrendScope API！本指南旨在協助您了解並使用 TrendScope 的各項服務，包括爬蟲啟動、資料查詢以及 PPT 檔案處理等功能。

### 目錄
- [TrendScope API 使用者指南](#trendscope-api-使用者指南)
- [目錄](#目錄)
- [1. PPT 檔案上傳與處理](#1-ppt-檔案上傳與處理)
  - [1.1 上傳 PPT 檔案](#11-上傳-ppt-檔案)
  - [1.2 查詢處理狀態](#12-查詢處理狀態)
  - [1.3 獲取可用的研討會列表](#13-獲取可用的研討會列表)
- [2. 爬蟲服務](#2-爬蟲服務)
  - [2.1 啟動爬蟲任務](#21-啟動爬蟲任務)
  - [2.2 查詢爬蟲狀態](#22-查詢爬蟲狀態)
  - [2.3 列出可用的爬蟲](#23-列出可用的爬蟲)
- [3. BigQuery 資料查詢](#3-bigquery-資料查詢)
  - [3.1 獲取會議資料](#31-獲取會議資料)
  - [3.2 獲取研討會列表](#32-獲取研討會列表)
  - [3.3 獲取資料統計](#33-獲取資料統計)
  - [3.4 檢查 BigQuery 健康狀態](#34-檢查-bigquery-健康狀態)
- [4. 資料模型（Schemas）](#4-資料模型schemas)

---

### 1. PPT 檔案上傳與處理

此系列 API 用於上傳 PPT 簡報檔案，並追蹤其後續處理進度。

#### 1.1 上傳 PPT 檔案

此端點允許您上傳一個或多個 `.pptx` 或 `.ppt` 檔案，並指定其所屬的研討會，以啟動後續的分析處理流程。

*   **方法:** `POST`
*   **路徑:** `/ppt/upload`
*   **請求格式:** `multipart/form-data`
    *   `files`: (必需) 一個或多個檔案。
    *   `seminar`: (必需, string) 檔案所屬的研討會名稱。

**範例 (使用 cURL):**
```bash
curl -X POST "http://your-api-host/ppt/upload" \
     -F "files=@/path/to/your/presentation1.pptx" \
     -F "files=@/path/to/your/presentation2.pptx" \
     -F "seminar=2024_tech_conference"
```

**成功回應 (200 OK):**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "message": "Files uploaded successfully. Processing started.",
  "files_count": 2
}
```

#### 1.2 查詢處理狀態

上傳檔案後，您會獲得一個 `task_id`。使用此 ID，您可以查詢所有檔案的整體處理進度與各個檔案的詳細狀態。

*   **方法:** `GET`
*   **路徑:** `/ppt/status/{task_id}`

**範例 (使用 cURL):**
```bash
curl -X GET "http://your-api-host/ppt/status/a1b2c3d4-e5f6-7890-1234-567890abcdef"
```

**成功回應 (200 OK):**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "PROCESSING",
  "progress": 50,
  "message": "Processing 1 of 2 files.",
  "result": null,
  "error": null,
  "files": [
    {
      "filename": "presentation1.pptx",
      "status": "COMPLETED",
      "progress": 100,
      "matched_session": "AI in Modern Applications",
      "similarity": 0.92,
      "ppt_length": 35,
      "error": null
    },
    {
      "filename": "presentation2.pptx",
      "status": "PROCESSING",
      "progress": 25,
      "matched_session": null,
      "similarity": null,
      "ppt_length": null,
      "error": null
    }
  ]
}
```

#### 1.3 獲取可用的研討會列表

在執行上傳前，您可以透過此端點獲取目前系統中已設定、可供選擇的研討會清單。

*   **方法:** `GET`
*   **路徑:** `/ppt/seminars`

**範例 (使用 cURL):**
```bash
curl -X GET "http://your-api-host/ppt/seminars"
```

**成功回應 (200 OK):**
```json
[
  "2024_tech_conference",
  "annual_marketing_summit",
  "global_finance_forum"
]
```

---

### 2. 爬蟲服務

此系列 API 用於啟動和監控網路爬蟲任務。

#### 2.1 啟動爬蟲任務

透過此端點可以啟動一個指定類型的爬蟲任務。

*   **方法:** `POST`
*   **路徑:** `/scrapers/run`
*   **請求 Body (JSON):**
    *   `scraper_type`: (必需, string) 爬蟲的類型。
    *   `headless`: (可選, boolean, 預設 `true`) 是否以無頭模式運行瀏覽器。
    *   `wait_time`: (可選, integer, 預設 `30`) 頁面加載等待時間（秒）。
    *   `use_bigquery`: (可選, boolean, 預設 `false`) 是否將結果直接存入 BigQuery。

**範例 (使用 cURL):**
```bash
curl -X POST "http://your-api-host/scrapers/run" \
     -H "Content-Type: application/json" \
     -d '{
           "scraper_type": "ieee_conference_scraper",
           "use_bigquery": true
         }'
```

**成功回應 (200 OK):**
```json
{
  "task_id": "s-z9y8x7w6-v5u4-3210-fedc-ba9876543210",
  "message": "Scraper task started.",
  "status": "PENDING"
}
```

#### 2.2 查詢爬蟲狀態

使用啟動任務時獲取的 `task_id`，查詢爬蟲的執行狀態和結果。

*   **方法:** `GET`
*   **路徑:** `/scrapers/status/{task_id}`

**範例 (使用 cURL):**
```bash
curl -X GET "http://your-api-host/scrapers/status/s-z9y8x7w6-v5u4-3210-fedc-ba9876543210"
```

**成功回應 (200 OK) - 任務完成:**
```json
{
  "task_id": "s-z9y8x7w6-v5u4-3210-fedc-ba9876543210",
  "status": "SUCCESS",
  "file_path": "/path/to/scraped_data.json",
  "message": "Scraping completed successfully.",
  "data": [
    { "title": "Article 1", "url": "http://example.com/1" },
    { "title": "Article 2", "url": "http://example.com/2" }
  ]
}
```

#### 2.3 列出可用的爬蟲

獲取系統支援的所有爬蟲類型列表。

*   **方法:** `GET`
*   **路徑:** `/scrapers/list`

**範例 (使用 cURL):**
```bash
curl -X GET "http://your-api-host/scrapers/list"
```

**成功回應 (200 OK):**
```json
[
  "ieee_conference_scraper",
  "acm_digital_library_scraper",
  "arxiv_cs_paper_scraper"
]
```
---

### 3. BigQuery 資料查詢

此系列 API 提供從 BigQuery 資料倉儲中查詢已處理資料的介面。

#### 3.1 獲取會議資料

查詢符合特定條件的會議（session）資料。

*   **方法:** `GET`
*   **路徑:** `/data/sessions`
*   **查詢參數:**
    *   `source`: (可選, string) 資料來源過濾。
    *   `seminar`: (可選, string) 研討會名稱過濾。
    *   `limit`: (可選, integer, 預設 `20`, 最大 `100`) 返回的最大結果數量。

**範例 (使用 cURL):**
```bash
curl -X GET "http://your-api-host/data/sessions?seminar=2024_tech_conference&limit=2"
```

**成功回應 (200 OK):**
```json
[
  {
    "session_id": "sess_101",
    "title": "The Future of Quantum Computing",
    "speaker": "Dr. Evelyn Reed",
    "seminar": "2024_tech_conference",
    "source": "ieee_conference_scraper"
  },
  {
    "session_id": "sess_102",
    "title": "AI in Modern Applications",
    "speaker": "John Smith",
    "seminar": "2024_tech_conference",
    "source": "ieee_conference_scraper"
  }
]
```

#### 3.2 獲取研討會列表

從 BigQuery 獲取所有研討會的列表及其包含的會議數量。

*   **方法:** `GET`
*   **路徑:** `/data/seminars`

**範例 (使用 cURL):**
```bash
curl -X GET "http://your-api-host/data/seminars"
```

**成功回應 (200 OK):**
```json
[
  { "seminar": "2024_tech_conference", "session_count": 88 },
  { "seminar": "annual_marketing_summit", "session_count": 45 }
]
```

#### 3.3 獲取資料統計

獲取 BigQuery 中的整體資料統計數據。

*   **方法:** `GET`
*   **路徑:** `/data/stats`

**範例 (使用 cURL):**
```bash
curl -X GET "http://your-api-host/data/stats"
```

**成功回應 (200 OK):**
```json
{
  "total_sessions": 133,
  "total_seminars": 2,
  "last_updated": "2023-10-27T10:00:00Z"
}
```

#### 3.4 檢查 BigQuery 健康狀態

檢查 API 服務與 BigQuery 之間的連線是否正常。

*   **方法:** `GET`
*   **路徑:** `/bigquery/health`

**範例 (使用 cURL):**
```bash
curl -X GET "http://your-api-host/bigquery/health"
```

**成功回應 (200 OK):**
```json
{
  "status": "ok",
  "project_id": "your-gcp-project-id",
  "location": "US"
}
```

---

### 4. 資料模型（Schemas）

以下是 API 中使用的主要資料模型：

*   **UploadResponse**: 上傳檔案後的回應。
    *   `task_id` (string): 異步處理任務的唯一標識符。
    *   `message` (string): 狀態訊息。
    *   `files_count` (integer): 本次上傳的檔案總數。

*   **ProcessingStatus**: 查詢 PPT 處理狀態的回應。
    *   `task_id` (string): 任務 ID。
    *   `status` (string): 整體任務狀態 (e.g., "PROCESSING", "COMPLETED", "FAILED")。
    *   `progress` (integer): 整體進度百分比 (0-100)。
    *   `message` (string): 狀態描述。
    *   `files` (array): `FileProcessingResult` 物件的陣列，包含每個檔案的詳細狀態。

*   **FileProcessingResult**: 單一檔案的處理結果。
    *   `filename` (string): 檔案名稱。
    *   `status` (string): 該檔案的處理狀態。
    *   `progress` (integer): 該檔案的處理進度。
    *   `matched_session` (string | null): 匹配到的會議名稱。
    *   `similarity` (number | null): 與會議內容的相似度。
    *   `ppt_length` (integer | null): PPT 的頁數。
    *   `error` (string | null): 錯誤訊息。

*   **ScraperResponse**: 啟動爬蟲任務後的回應。
    *   `task_id` (string): 爬蟲任務的 ID。
    *   `message` (string): 狀態訊息。
    *   `status` (string): 任務初始狀態 (e.g., "PENDING")。

*   **ScraperResult**: 查詢爬蟲任務狀態的回應。
    *   `task_id` (string): 任務 ID。
    *   `status` (string): 當前任務狀態 (e.g., "RUNNING", "SUCCESS", "FAILURE")。
    *   `file_path` (string | null): 結果檔案的路徑。
    *   `message` (string | null): 狀態或錯誤訊息。
    *   `data` (array | null): 爬取到的資料。