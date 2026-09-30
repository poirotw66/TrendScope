#!/bin/bash
# Start backend from the repository root
# 啟動 TrendScope Backend API 服務的腳本

# 切換到腳本所在目錄（專案根目錄），確保 Python 能正確解析 config 與 base
cd "$(dirname "$0")"

# 設置環境變數
if [ -z "${GOOGLE_APPLICATION_CREDENTIALS:-}" ]; then
  echo "Set GOOGLE_APPLICATION_CREDENTIALS to a valid credential file before starting." >&2
  exit 1
fi
if [ -z "${GOOGLE_CLOUD_PROJECT:-}" ]; then
  echo "Set GOOGLE_CLOUD_PROJECT before starting." >&2
  exit 1
fi

# 確保日誌目錄存在
mkdir -p logs

echo "🚀 啟動 TrendScope Backend API..."
echo "API 文檔: http://localhost:8001/docs"
echo "API 根端點: http://localhost:8001/"

# 以模組方式啟動，使專案根目錄在 sys.path 中，才能 import config
python -m base.main
