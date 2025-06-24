# TrendScope Backend

TrendScope 專案的後端 API 服務，提供 PPT 上傳處理、爬蟲管理和資料查詢功能。

## 📁 專案結構

```
backend/
├── api/                    # API 路由和端點
│   ├── __init__.py
│   ├── app.py             # FastAPI 主應用
│   └── ppt_upload.py      # PPT 上傳處理 API
├── utils/                 # 工具函數
│   └── __init__.py
├── main.py               # 主啟動檔案
├── requirements.txt      # Python 依賴
└── README.md            # 本檔案
```

## 🚀 快速開始

### 1. 安裝依賴

```bash
# 在專案根目錄執行
pip install -r backend/requirements.txt
```

### 2. 設置環境變數

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/credentials.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
```

### 3. 啟動服務

#### 方法 1: 使用啟動腳本（推薦）
```bash
# 在專案根目錄執行
./start_api.sh
```

#### 方法 2: 直接啟動
```bash
# 在專案根目錄執行
python backend/main.py
```

### 4. 訪問 API

- **API 根端點**: http://localhost:8001/
- **API 文檔**: http://localhost:8001/docs
- **OpenAPI 規格**: http://localhost:8001/openapi.json

## 📋 API 端點

### 核心功能

| 端點 | 方法 | 描述 |
|------|------|------|
| `/` | GET | API 根端點 |
| `/docs` | GET | API 文檔 (Swagger UI) |

### PPT 上傳功能

| 端點 | 方法 | 描述 |
|------|------|------|
| `/ppt/upload` | POST | 上傳 PPT 檔案並開始處理 |
| `/ppt/status/{task_id}` | GET | 獲取處理狀態 |
| `/ppt/seminars` | GET | 獲取可用的研討會列表 |
| `/ppt/debug/tasks` | GET | 調試端點：獲取所有任務狀態 |

### 爬蟲功能

| 端點 | 方法 | 描述 |
|------|------|------|
| `/scrapers/run` | POST | 啟動爬蟲任務 |
| `/scrapers/status/{task_id}` | GET | 獲取爬蟲任務狀態 |
| `/scrapers/list` | GET | 列出可用的爬蟲 |

### 資料查詢

| 端點 | 方法 | 描述 |
|------|------|------|
| `/data/sessions` | GET | 從 BigQuery 獲取會議資料 |

## 🔧 配置

### 環境變數

- `GOOGLE_APPLICATION_CREDENTIALS`: Google Cloud 服務帳戶金鑰檔案路徑
- `GOOGLE_CLOUD_PROJECT`: Google Cloud 專案 ID

### 並行處理配置

在 `backend/api/ppt_upload.py` 中可以調整：

```python
MAX_CONCURRENT_FILES = 3  # 最多同時處理的檔案數量
```

## 🛠️ 開發

### 開發模式啟動

```bash
# 啟用自動重載
python backend/main.py
```

### 日誌

日誌檔案會自動創建在 `logs/` 目錄中：
- `logs/api_YYYYMMDD.log`: 每日 API 日誌

### 調試

使用調試端點查看系統狀態：
- `GET /ppt/debug/tasks`: 查看所有 PPT 處理任務

## 📦 依賴

主要依賴包括：
- **FastAPI**: Web 框架
- **uvicorn**: ASGI 服務器
- **google-cloud-bigquery**: BigQuery 客戶端
- **google-generativeai**: Gemini API 客戶端
- **opencc-python-reimplemented**: 繁簡轉換

## 🔗 相關連結

- [FastAPI 文檔](https://fastapi.tiangolo.com/)
- [Google Cloud BigQuery](https://cloud.google.com/bigquery)
- [Google Gemini API](https://ai.google.dev/)

## 📝 更新日誌

### v1.0.0 (2024-06-24)
- 重新組織專案結構，將後端功能搬移到 `backend/` 目錄
- 實現 PPT 並行處理功能
- 添加詳細的 API 文檔和配置說明
