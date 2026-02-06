# 專案設置指南

## 🚀 快速開始

### 1. 安裝專案為 Package（推薦）

```bash
# 在專案根目錄執行
pip install -e .
```

這會將專案安裝為可編輯模式，之後就可以使用標準導入：
```python
from config.settings import settings
from base.bigquery.client import BigQueryClient
```

### 2. 環境變數設置

複製 `.env_example` 為 `.env` 並填入你的配置：
```bash
cp .env_example .env
```

主要配置項：
- `GEMINI_API_KEY` - Gemini API 金鑰
- `GOOGLE_APPLICATION_CREDENTIALS` - Google Cloud 憑證路徑
- `GOOGLE_CLOUD_PROJECT` - Google Cloud 專案 ID

### 3. 安裝依賴

```bash
pip install -r requirements.txt
```

## 📝 使用標準導入

### 配置讀取

```python
# 推薦方式（新程式碼）
from config.settings import settings

api_key = settings.gemini_api_key
input_dir = settings.default_input_dir

# 向後相容（舊程式碼）
from config.config import GEMINI_API_KEY, DEFAULT_INPUT_DIR
```

### 模組導入

```python
# BigQuery
from base.bigquery.client import BigQueryClient

# Scrapers
from base.scrapers.parsers.aws_london import run_aws_london_scraper

# API 模組
from base.api.modules.trend_analyzer import TrendAnalyzer
```

### 腳本檔案

腳本檔案應使用統一的導入輔助：
```python
from scripts._setup_path import setup_path
setup_path()

# 之後使用標準導入
from config.config import GEMINI_API_KEY
from base.bigquery.client import BigQueryClient
```

## ⚠️ 注意事項

1. **不要使用舊的導入路徑：**
   - ❌ `from bigquery.client import ...` 
   - ✅ `from base.bigquery.client import ...`

2. **不要使用 disposal/ 目錄的模組：**
   - ❌ `from disposal.bigquery.client import ...`
   - ✅ `from base.bigquery.client import ...`

3. **設定優先順序：**
   - 環境變數 > `.env` 檔案 > 預設值

## 🔧 開發建議

1. **新程式碼使用：**
   ```python
   from config.settings import settings
   ```

2. **腳本檔案使用：**
   ```python
   from scripts._setup_path import setup_path
   setup_path()
   ```

3. **測試檔案可以保留路徑設置以便獨立運行**

## 📚 更多資訊

- 詳細優化說明：`OPTIMIZATION_GUIDE.md`
- 專案說明：`README_zh.md`
