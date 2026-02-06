# 日誌系統優化總結

## ✅ 已完成的工作

### 1. 建立統一的日誌配置模組

**新增檔案：**
- `base/utils/logger.py` - 統一的日誌配置模組

**功能：**
- ✅ 標準化的 logger 設定函數 `setup_logger()`
- ✅ 便捷的 logger 取得函數（`get_logger()`, `get_default_logger()`）
- ✅ 模組專用 logger（`get_scraper_logger()`, `get_bigquery_logger()`, `get_api_logger()`）
- ✅ 自動日誌檔案管理（按日期和模組名稱）
- ✅ 根據環境自動設定日誌級別（開發環境 DEBUG，生產環境 INFO）
- ✅ 統一的日誌格式

**使用範例：**
```python
from base.utils.logger import get_scraper_logger, get_bigquery_logger

# 在爬蟲模組中
logger = get_scraper_logger()
logger.info("開始爬取資料")
logger.error("爬取失敗: %s", error_message, exc_info=True)

# 在 BigQuery 模組中
logger = get_bigquery_logger()
logger.info("上傳 %s 筆資料", len(data))
```

### 2. 更新核心模組

**已更新的檔案：**
- ✅ `base/main.py` - 啟動腳本
- ✅ `base/api/app.py` - API 應用主檔案
- ✅ `base/scrapers/base_scraper.py` - 爬蟲基類
- ✅ `base/bigquery/client.py` - BigQuery 客戶端
- ✅ `base/bigquery/upload.py` - BigQuery 上傳模組

**改進：**
- 所有 `print()` 語句已替換為適當的 `logger` 調用
- 使用適當的日誌級別（`info`, `warning`, `error`, `debug`）
- 錯誤記錄包含 `exc_info=True` 以捕獲堆疊追蹤
- 使用 lazy formatting（`%s` 而非 f-string）以提升效能

### 3. 日誌級別使用指南

- **DEBUG**: 詳細的除錯資訊（僅開發環境）
  ```python
  logger.debug("WebDriver 已關閉")
  ```

- **INFO**: 一般資訊性訊息
  ```python
  logger.info("開始爬取 %s", scraper_name)
  logger.info("成功上傳 %s 筆資料", len(data))
  ```

- **WARNING**: 警告訊息（不影響執行但需注意）
  ```python
  logger.warning("未獲取到數據")
  logger.warning("無法獲取表結構: %s", str(e))
  ```

- **ERROR**: 錯誤訊息（包含異常資訊）
  ```python
  logger.error("初始化 BigQuery 上傳器失敗: %s", str(e), exc_info=True)
  logger.error("上傳到 BigQuery 失敗: %s", str(e), exc_info=True)
  ```

## 📋 待完成的工作

### 1. 更新爬蟲解析器模組

以下檔案仍包含大量 `print()` 語句，需要更新：

- `base/scrapers/parsers/devopsdays_taipei.py` (~30+ print)
- `base/scrapers/parsers/aicon_infoq_beijing.py` (~20+ print)
- `base/scrapers/parsers/aicon_infoq.py` (~20+ print)
- `base/scrapers/parsers/cloudsummit_tapei.py` (~30+ print)
- `base/scrapers/parsers/qcon_infoq.py` (~10+ print)
- `base/scrapers/parsers/aws_london.py` (~5+ print)

**建議更新方式：**
```python
# 在檔案開頭添加
from base.utils.logger import get_scraper_logger
logger = get_scraper_logger()

# 替換 print() 為 logger
# print(f"開始爬取網頁: {self.base_url}")
logger.info("開始爬取網頁: %s", self.base_url)

# print(f"❌ 超時: {url}")
logger.error("超時: %s", url)

# print(f"✅ 成功爬取: {name}")
logger.info("成功爬取: %s", name)
```

### 2. 更新 API 路由模組

- `base/api/routes/ppt_upload.py` (~15+ print)
- `base/scrapers/utils/file_handler.py` (~2 print)

### 3. 更新腳本檔案

- `scripts/` 目錄下的腳本檔案（可選，因為腳本通常需要直接輸出）

### 4. 更新 src/ 目錄

- `src/` 目錄下的模組（可選，因為這些是舊版模組）

## 🔧 日誌配置

### 環境變數

日誌級別會根據 `API_ENVIRONMENT` 自動設定：
- `development`: DEBUG 級別
- `production`: INFO 級別
- `testing`: INFO 級別

### 日誌檔案位置

所有日誌檔案儲存在：`{PROJECT_ROOT}/logs/`

檔案命名格式：`{module_name}_{YYYYMMDD}.log`

範例：
- `api_20250115.log`
- `scraper_20250115.log`
- `bigquery_20250115.log`

## 📝 最佳實踐

1. **使用 lazy formatting**
   ```python
   # ✅ 好
   logger.info("處理 %s 個項目", count)
   
   # ❌ 不好
   logger.info(f"處理 {count} 個項目")
   ```

2. **錯誤記錄包含堆疊追蹤**
   ```python
   logger.error("處理失敗: %s", str(e), exc_info=True)
   ```

3. **使用適當的日誌級別**
   - DEBUG: 詳細除錯資訊
   - INFO: 一般資訊
   - WARNING: 警告
   - ERROR: 錯誤

4. **避免在循環中使用高級別日誌**
   ```python
   # ✅ 好：在循環外記錄
   logger.info("開始處理 %s 個項目", len(items))
   for item in items:
       process(item)
   
   # ❌ 不好：在循環內記錄
   for item in items:
       logger.info("處理項目: %s", item)  # 會產生大量日誌
   ```

## 🚀 下一步

1. **完成爬蟲解析器模組的更新**（優先）
2. **更新 API 路由模組**
3. **考慮添加日誌輪轉**（避免日誌檔案過大）
4. **考慮添加結構化日誌**（JSON 格式，便於日誌分析）
