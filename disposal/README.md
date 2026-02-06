# disposal/ 目錄說明

⚠️ **此目錄包含舊版/廢棄的程式碼，僅供參考或一次性腳本使用**

## 目錄結構

- `bigquery/` - 舊版 BigQuery 客戶端（已遷移至 `base/bigquery/`）
- `scrapers/` - 舊版爬蟲程式（已遷移至 `base/scrapers/`）
- `tool/` - 一次性工具腳本

## 遷移說明

### BigQuery 客戶端
- **舊版位置**: `disposal/bigquery/client.py`
- **新版位置**: `base/bigquery/client.py`
- **請使用**: `from base.bigquery.client import BigQueryClient`

### 爬蟲程式
- **舊版位置**: `disposal/scrapers/`
- **新版位置**: `base/scrapers/`
- **請使用**: `from base.scrapers.parsers.xxx import run_xxx_scraper`

## 注意事項

1. **不要在新程式碼中引用此目錄的模組**
2. 此目錄的程式碼可能不再維護
3. 如需使用類似功能，請參考 `base/` 目錄下的對應模組
4. `tool/` 目錄下的腳本為一次性工具，可視需要保留或刪除

## 清理計劃

未來可考慮：
- 將 `tool/` 中有用的腳本遷移至 `scripts/` 目錄
- 刪除已完全遷移的舊版程式碼
- 或將整個 `disposal/` 目錄移至版本控制之外
