#!/bin/bash
# 同時啟動 TrendScope 的前端和後端服務

echo "🚀 啟動 TrendScope 服務..."

# 啟動後端 API（在背景運行）
./start_api.sh &
API_PID=$!
echo "✅ 後端 API 服務已在背景啟動 (PID: $API_PID)"
echo "   API 文檔: http://localhost:8001/docs"

# 等待幾秒鐘，確保 API 服務已啟動
sleep 3

# 啟動前端服務（在前台運行）
echo "🚀 啟動前端服務..."
./start_frontend.sh

# 當前端服務停止時，也停止後端服務
echo "正在停止後端 API 服務..."
kill $API_PID
echo "✅ 所有服務已停止"