# 專案優化指南

本文檔說明專案的優化改進，特別是導入路徑、設定管理和程式碼重複的處理。

## 📋 優化內容

### 1. 路徑與 Import 優化

#### 問題
- 多處手動使用 `sys.path.insert(0, project_root)` 或 `sys.path.append(...)`
- 導入路徑不一致，難以維護

#### 解決方案

**A. 創建 `pyproject.toml`**
- 將專案配置為標準 Python package
- 可使用 `pip install -e .` 安裝為可編輯模式
- 支援標準導入：`from config import ...`, `from base import ...`

**B. 統一導入輔助模組**
- 創建 `scripts/_setup_path.py` 供腳本檔案使用
- 腳本檔案統一使用：`from scripts._setup_path import setup_path; setup_path()`

**C. 更新所有檔案**
- 移除不必要的 `sys.path` 操作
- 統一使用標準導入路徑
- 舊版 `from bigquery.client` → 新版 `from base.bigquery.client`

#### 使用方式

**開發環境設置：**
```bash
# 安裝專案為可編輯模式（推薦）
pip install -e .

# 之後就可以直接使用標準導入
python scripts/01_batch_summarize_process.py
```

**腳本檔案範例：**
```python
# 舊方式（已移除）
import sys
sys.path.append(str(Path(__file__).parent.parent))

# 新方式（腳本檔案）
from scripts._setup_path import setup_path
setup_path()

# 標準導入
from config.config import GEMINI_API_KEY
from base.bigquery.client import BigQueryClient
```

**模組檔案範例：**
```python
# 直接使用標準導入（無需 sys.path）
from config.settings import settings
from base.bigquery.client import BigQueryClient
```

### 2. 設定管理優化

#### 問題
- 設定分散在多個檔案：`config/config.py`、`.env`、腳本內寫死路徑
- 環境變數命名不一致

#### 解決方案

**A. 完善 `config/settings.py`**
- 使用 Pydantic Settings 集中管理所有配置
- 支援從 `.env` 檔案讀取
- 提供預設值和路徑自動補全
- 向後相容舊的配置名稱（透過 property）

**B. 統一配置項**
- 所有配置項都在 `config/settings.py` 定義
- `config/config.py` 保留為向後相容層
- 建議新程式碼使用：`from config.settings import settings`

#### 配置項清單

```python
# API / Gemini 配置
settings.gemini_api_key
settings.gemini_model_name
settings.max_requests_per_minute
settings.request_interval
settings.max_retries
settings.retry_delay

# 檔案路徑配置
settings.data_dir
settings.default_input_dir
settings.default_output_dir
settings.sheet_dir
settings.base_output_dir
settings.output_md_dir
settings.output_html_dir
settings.session_html_dir
settings.input_csv_path

# 處理配置
settings.default_output_format
settings.default_workers
settings.max_transcript_length
settings.top_n_meetings
settings.batch_md_to_html_index

# Google Cloud 配置
settings.google_application_credentials
settings.google_cloud_project
settings.google_cloud_storage_bucket
```

#### 使用範例

```python
# 推薦方式（新程式碼）
from config.settings import settings

api_key = settings.gemini_api_key
input_dir = settings.default_input_dir

# 向後相容（舊程式碼仍可使用）
from config.config import GEMINI_API_KEY, DEFAULT_INPUT_DIR
```

### 3. 重複程式碼處理

#### 問題
- `disposal/` 與 `base/` 有重複的 BigQuery、scraper 邏輯
- 維護困難，容易出現不一致

#### 解決方案

**A. 標記 `disposal/` 為舊版**
- 創建 `disposal/README.md` 說明此目錄為舊版/廢棄程式碼
- 明確標示遷移路徑：
  - `disposal/bigquery/` → `base/bigquery/`
  - `disposal/scrapers/` → `base/scrapers/`

**B. 更新所有引用**
- 將所有 `from bigquery.client` 改為 `from base.bigquery.client`
- 將所有 `from disposal.xxx` 改為 `from base.xxx`

**C. 未來清理計劃**
- `disposal/tool/` 中有用的腳本可遷移至 `scripts/`
- 完全遷移後可考慮刪除 `disposal/` 目錄

## 🚀 遷移步驟

### 對於開發者

1. **安裝專案為 package：**
   ```bash
   pip install -e .
   ```

2. **更新導入語句：**
   - 檢查是否有使用 `sys.path.insert` 或 `sys.path.append`
   - 改為使用標準導入或 `scripts/_setup_path.py`

3. **更新配置讀取：**
   - 新程式碼使用 `from config.settings import settings`
   - 舊程式碼可繼續使用 `from config.config import ...`

4. **檢查 BigQuery/Scraper 導入：**
   - 確保使用 `from base.bigquery.client` 而非 `from bigquery.client`
   - 確保使用 `from base.scrapers.xxx` 而非 `from disposal.scrapers.xxx`

### 對於 CI/CD

更新部署腳本，確保在執行前安裝專案：
```bash
pip install -e .
# 或
pip install -r requirements.txt
```

## 📝 注意事項

1. **向後相容性**
   - `config/config.py` 保留所有舊的配置變數名稱
   - 舊的導入路徑仍可使用，但建議遷移

2. **測試檔案**
   - 測試檔案可以保留 `sys.path` 設置以便獨立運行
   - 但建議改為使用標準導入

3. **腳本檔案**
   - 腳本檔案統一使用 `scripts/_setup_path.py`
   - 確保在執行前已安裝專案：`pip install -e .`

## 🔍 檢查清單

- [x] 創建 `pyproject.toml`
- [x] 完善 `config/settings.py` 包含所有配置項
- [x] 更新 `config/config.py` 向後相容層
- [x] 創建 `scripts/_setup_path.py` 統一導入輔助
- [x] 更新所有腳本檔案使用標準導入
- [x] 更新所有模組檔案移除 `sys.path` 操作
- [x] 標記 `disposal/` 為舊版並創建 README
- [x] 更新所有 BigQuery/Scraper 導入路徑

## 📚 相關檔案

- `pyproject.toml` - 專案配置和 package 定義
- `config/settings.py` - 集中化設定管理
- `config/config.py` - 向後相容層
- `scripts/_setup_path.py` - 腳本導入輔助
- `disposal/README.md` - 舊版程式碼說明
