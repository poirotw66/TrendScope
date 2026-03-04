#!/bin/bash
# filepath: /Users/cfh00896102/Github/TrendScope/start_api.sh
# 啟動 TrendScope Backend API 服務的腳本

# 切換到腳本所在目錄（專案根目錄），確保 Python 能正確解析 config 與 base
cd "$(dirname "$0")"

# 設置環境變數
export GOOGLE_APPLICATION_CREDENTIALS="${GOOGLE_APPLICATION_CREDENTIALS:-$(pwd)/itr-aimasteryhub-lab-1a116262496d.json}"
export GOOGLE_CLOUD_PROJECT="${GOOGLE_CLOUD_PROJECT:-itr-aimasteryhub-lab}"

# 確保日誌目錄存在
mkdir -p logs

echo "🚀 啟動 TrendScope Backend API..."
echo "API 文檔: http://localhost:8001/docs"
echo "API 根端點: http://localhost:8001/"

# 以模組方式啟動，使專案根目錄在 sys.path 中，才能 import config
python -m base.main
