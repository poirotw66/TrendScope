# TrendScope 整合系統

TrendScope 是一個用於爬取、分析和展示會議資料的系統。該系統整合了爬蟲、BigQuery 雲端儲存和 FastAPI 後端，並使用 React 前端進行展示。

## 系統架構

整個系統由以下主要部分組成：

1. **爬蟲模組**：使用 Selenium 爬取各種會議網站的資料
2. **BigQuery 整合**：將爬取的資料上傳到 Google BigQuery 雲端資料倉庫
3. **FastAPI 後端**：提供 API 接口供前端呼叫，實現爬蟲控制和資料查詢
4. **React 前端**：為使用者提供友善的介面以控制爬蟲和查看資料

## 目錄結構

```
TrendScope/
├── scrapers/                # 爬蟲模組
│   ├── base_scraper.py      # 爬蟲基類
│   ├── main.py              # 爬蟲主程式
│   ├── parsers/             # 各種爬蟲實現
│   │   └── aws_london.py    # AWS London Summit 爬蟲
│   └── utils/               # 爬蟲工具類
│       ├── driver_setup.py  # WebDriver 設置
│       └── file_handler.py  # 文件處理
├── bigquery/                # BigQuery 整合
│   ├── client.py            # BigQuery 客戶端
│   ├── upload.py            # 資料上傳功能
│   └── schemas/             # 資料表結構定義
│       └── conferences.py   # 會議資料結構
├── src/                     # 核心代碼
│   ├── api/                 # FastAPI 後端
│   │   └── app.py           # API 應用程式
│   └── ...                  # 其他核心代碼
├── frontend/                # React 前端
│   ├── components/          # React 組件
│   ├── services/            # 服務類
│   │   └── api.ts           # API 服務
│   └── ...                  # 其他前端代碼
└── ...                      # 其他檔案
```

## 安裝與配置

### 前置需求

- Python 3.9+
- Node.js 16+
- Google Cloud 帳號（用於 BigQuery）
- Chrome 瀏覽器（用於爬蟲）

### 安裝步驟

1. **安裝 Python 依賴：**

```bash
pip install -r requirements.txt
```

2. **配置 Google Cloud 認證：**

在 Google Cloud Console 建立服務帳戶，下載金鑰文件，然後設置環境變數：

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/credentials.json
export GOOGLE_CLOUD_PROJECT=your-project-id
```

3. **安裝前端依賴：**

```bash
cd frontend
npm install
```

## 運行系統

### 1. 從命令行運行爬蟲

```bash
# 使用 CLI 運行爬蟲
python -m scrapers.main aws_london --headless --use-bigquery
```

### 2. 啟動 FastAPI 後端

```bash
# 啟動 API 服務
cd src
uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

訪問 http://localhost:8000/docs 可查看 API 文檔。

### 3. 啟動前端開發服務器

```bash
cd frontend
npm run dev
```

訪問 http://localhost:3000 可使用前端介面。

## 使用說明

### 爬蟲控制面板

爬蟲控制面板位於前端應用程式中，提供以下功能：

1. 選擇要運行的爬蟲
2. 配置爬蟲參數（無頭模式、等待時間等）
3. 設置是否將資料上傳到 BigQuery
4. 執行爬蟲並即時顯示進度和結果

### 會議資料查看器

會議資料查看器顯示從 BigQuery 獲取的資料，提供以下功能：

1. 按來源過濾會議資料
2. 分頁顯示會議列表
3. 查看會議詳細資訊

## 擴展系統

### 添加新的爬蟲

1. 在 `scrapers/parsers/` 目錄下創建新的爬蟲文件
2. 從 `BaseScraper` 繼承並實現 `scrape()` 方法
3. 在 `scrapers/main.py` 中註冊新的爬蟲
4. 在 FastAPI 中添加新的爬蟲選項

### 擴展 BigQuery 結構

1. 在 `bigquery/schemas/` 中定義新的資料表結構
2. 更新 `bigquery/upload.py` 中的上傳邏輯
3. 在 FastAPI 中添加新的查詢端點

## 故障排除

### 爬蟲問題

- **爬蟲啟動失敗**：確保 Chrome 瀏覽器已安裝且路徑正確
- **網站結構變化**：更新相應的爬蟲解析邏輯
- **網站需要登入**：將爬蟲設置為非無頭模式，然後手動登入

### BigQuery 問題

- **上傳失敗**：檢查 Google Cloud 認證和權限
- **結構錯誤**：確保資料符合定義的結構
- **配額限制**：檢查 Google Cloud 用量和配額

### API 服務問題

- **服務無法啟動**：檢查依賴安裝和端口佔用
- **跨域問題**：配置適當的 CORS 設置
- **效能問題**：考慮添加資料緩存和優化查詢

## 常見問題

**Q: 如何添加對新會議網站的支援？**

A: 參考「添加新的爬蟲」部分，為新的網站創建專門的爬蟲類。

**Q: 如何修改資料庫結構？**

A: 更新 `bigquery/schemas/` 中的結構定義，然後使用 BigQuery 遷移工具進行結構更新。

**Q: 如何處理大量資料？**

A: 使用 BigQuery 的批量上傳功能，並考慮分頁獲取和處理資料。
