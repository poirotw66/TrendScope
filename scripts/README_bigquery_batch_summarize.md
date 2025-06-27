# BigQuery 批量會議報告生成器

## 概述

這是一個現代化的會議報告生成工具，已從原始的本地 PDF 文件處理升級為使用 BigQuery 雲端數據庫作為數據源。該腳本能夠從 BigQuery 中的 `conference_data.sessions` 表獲取會議數據，並使用 Google Gemini AI 生成高質量的會議摘要報告。

## 主要特性

### 🔄 數據源現代化
- **從本地文件到雲端數據庫**: 不再依賴本地 PDF 文件，直接從 BigQuery 獲取結構化數據
- **實時數據訪問**: 可以獲取最新的會議數據，無需手動文件管理
- **靈活的數據過濾**: 支持按研討會、會議數量等條件過濾數據

### 🤖 AI 驅動的內容生成
- **Google Gemini 集成**: 使用最新的 Gemini 2.5 Flash 模型生成高質量摘要
- **智能內容處理**: 自動將簡體中文轉換為繁體中文
- **結構化輸出**: 生成包含核心觀點、詳細內容、重要結論的完整報告

### ⚡ 高效處理
- **多線程並行處理**: 支持同時處理多個會議，提高效率
- **錯誤重試機制**: 自動重試失敗的請求，確保處理完整性
- **進度追蹤**: 實時顯示處理進度和狀態

### 📊 靈活的輸出格式
- **Markdown 格式**: 生成易於閱讀和編輯的 Markdown 文件
- **HTML 報告**: 可選生成美觀的 HTML 報告頁面
- **批量處理**: 支持一次性處理多個會議並生成統一報告

## 安裝要求

### 環境變數設置
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
export GOOGLE_CLOUD_PROJECT="your-project-id"
export GEMINI_API_KEY="your-gemini-api-key"
```

### Python 依賴
```bash
pip install google-cloud-bigquery google-generativeai pathlib
```

## 使用方法

### 1. 列出可用的研討會
```bash
python scripts/00_batch_summarize_pdf.py --list-seminars
```

輸出示例：
```
可用的研討會:
--------------------------------------------------------------------------------
研討會名稱                                    總會議數       有PPT內容    
--------------------------------------------------------------------------------
202503 QCon Beijing                      120        13        
202505 AICon Shanghai                    57         26        
```

### 2. 生成特定研討會的報告
```bash
python scripts/00_batch_summarize_pdf.py --seminar "202505 AICon Shanghai" --limit 10
```

### 3. 生成所有會議的報告
```bash
python scripts/00_batch_summarize_pdf.py --output-md-dir "reports/md" --output-html-dir "reports/html"
```

### 4. 只生成 Markdown 文件（跳過 HTML）
```bash
python scripts/00_batch_summarize_pdf.py --seminar "202503 QCon Beijing" --skip-html
```

## 命令行參數

| 參數 | 說明 | 默認值 |
|------|------|--------|
| `--seminar` | 研討會過濾條件 | 無（處理所有研討會） |
| `--limit` | 處理的會議數量限制 | 無限制 |
| `--output-md-dir` | Markdown 輸出目錄 | `reports/md` |
| `--output-html-dir` | HTML 輸出目錄 | `reports/html` |
| `--skip-html` | 跳過 HTML 生成 | False |
| `--list-seminars` | 列出可用研討會 | False |

## 輸出格式

### Markdown 報告結構
每個生成的 Markdown 文件包含：

```markdown
# 會議標題
主題演講
[會議影片連結](URL)
會議標題（繁體中文）

## 1. 核心觀點
會議的主要觀點和核心思想...

## 2. 詳細內容
會議的詳細內容展開...

## 3. 重要結論
會議的重要結論和總結...
```

### 文件命名規則
- 格式：`{conference_id}_{session_name}.md`
- 自動處理特殊字符，確保文件名安全
- 限制文件名長度，避免系統限制

## 技術架構

### 數據流程
1. **BigQuery 連接**: 使用服務帳戶憑證連接到 BigQuery
2. **數據查詢**: 執行 SQL 查詢獲取會議數據
3. **數據過濾**: 只處理包含 PPT 內容的會議
4. **AI 處理**: 使用 Gemini API 生成摘要
5. **文件輸出**: 保存為 Markdown 和 HTML 格式

### 核心組件
- `BigQueryClient`: 處理 BigQuery 連接和查詢
- `summarize_session_from_bigquery()`: 核心的會議摘要生成函數
- `worker()`: 多線程工作函數
- `batch_md_to_html()`: HTML 報告生成

## 配置參數

```python
MAX_THREADS = 4          # 最大並行線程數
REQUEST_INTERVAL = 4     # 請求間隔（秒）
MAX_RETRIES = 3          # 最大重試次數
RETRY_DELAY = 10         # 重試延遲（秒）
```

## 錯誤處理

- **連接錯誤**: 自動重試 BigQuery 和 Gemini API 連接
- **數據錯誤**: 跳過無效或缺失數據的會議
- **API 限制**: 內建請求間隔和重試機制
- **文件錯誤**: 自動創建輸出目錄，處理文件名衝突

## 性能優化

- **並行處理**: 多線程同時處理多個會議
- **智能過濾**: 只處理有 PPT 內容的會議
- **緩存機制**: 避免重複查詢相同數據
- **資源管理**: 控制並發數量，避免 API 限制

## 從舊版本遷移

### 主要變更
1. **數據源**: 從本地 PDF 文件改為 BigQuery 數據庫
2. **輸入參數**: 不再需要 PDF 目錄和 CSV 文件路徑
3. **過濾邏輯**: 使用 SQL 查詢替代文件系統遍歷
4. **錯誤處理**: 增強的網絡錯誤處理和重試機制

### 兼容性
- 保持相同的輸出格式和結構
- 保持相同的 HTML 生成功能
- 保持相同的多線程處理邏輯

## 故障排除

### 常見問題
1. **BigQuery 連接失敗**: 檢查環境變數和服務帳戶權限
2. **Gemini API 錯誤**: 確認 API 密鑰有效且有足夠配額
3. **沒有數據**: 確認 BigQuery 表中有 PPT 內容的會議
4. **文件權限錯誤**: 確保輸出目錄有寫入權限

### 調試模式
添加更詳細的日誌輸出：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 未來改進

- [ ] 支持更多輸出格式（PDF、Word）
- [ ] 添加會議內容相似度分析
- [ ] 實現增量處理（只處理新增會議）
- [ ] 添加會議標籤和分類功能
- [ ] 支持自定義摘要模板
