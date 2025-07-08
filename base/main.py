#!/usr/bin/env python3
"""
TrendScope base 主啟動檔案
"""

import os
import sys
import uvicorn

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, project_root)

from base.api.app import app

if __name__ == "__main__":
    # 確保環境變數設置
    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("警告: 未設置 GOOGLE_APPLICATION_CREDENTIALS 環境變數")
    
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("警告: 未設置 GOOGLE_CLOUD_PROJECT 環境變數")
    
    # 確保日誌目錄存在
    os.makedirs(os.path.join(project_root, "logs"), exist_ok=True)
    
    print("🚀 啟動 TrendScope base API 服務...")
    print(f"專案根目錄: {project_root}")
    print("API 文檔: http://localhost:8001/docs")
    print("API 根端點: http://localhost:8001/")
    
    # 啟動 API 服務
    uvicorn.run(
        "base.api.app:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        log_level="info"
    )
