#!/bin/bash
# filepath: /Users/cfh00896102/Github/TrendScope/start_api.sh
# 啟動 TrendScope Backend API 服務的腳本

# 設置環境變數
export GOOGLE_APPLICATION_CREDENTIALS="/Users/cfh00896102/Github/TrendScope/itr-aimasteryhub-lab-1a116262496d.json"
export GOOGLE_CLOUD_PROJECT="itr-aimasteryhub-lab"

# 確保日誌目錄存在
mkdir -p logs

echo "🚀 啟動 TrendScope Backend API..."
echo "API 文檔: http://localhost:8001/docs"
echo "API 根端點: http://localhost:8001/"

# 啟動後端 API
python backend/main.py
