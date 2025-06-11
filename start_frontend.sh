#!/bin/bash
# filepath: /Users/cfh00896102/Github/TrendScope/start_frontend.sh
# 啟動前端開發服務器的腳本

# 進入前端目錄
cd frontend

# 安裝依賴（如果需要）
if [ ! -d "node_modules" ]; then
  echo "正在安裝前端依賴..."
  npm install
fi

# 啟動開發服務器
npm run dev
