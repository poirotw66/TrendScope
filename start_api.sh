#!/bin/bash
# filepath: /Users/cfh00896102/Github/TrendScope/start_api.sh
# 啟動 FastAPI 服務的腳本

# 確保日誌目錄存在
mkdir -p logs

# 啟動 FastAPI 服務
cd src
PYTHONPATH=.. uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
