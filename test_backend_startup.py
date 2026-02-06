#!/usr/bin/env python3
"""
測試後端啟動問題
"""

import sys
import os
import traceback

# 使用標準導入（專案應作為 package 安裝：pip install -e .）
# 測試檔案可以保留路徑設置以便獨立運行
project_root = os.path.dirname(__file__)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

def test_imports():
    """測試各個模組的導入"""
    print("🧪 測試模組導入...")
    
    try:
        print("1. 測試基本導入...")
        import logging
        from datetime import datetime
        print("   ✅ 基本模組導入成功")
        
        print("2. 測試 FastAPI 導入...")
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        print("   ✅ FastAPI 導入成功")
        
        print("3. 測試路由導入...")
        from base.api.routes.ppt_upload import router as ppt_router
        print("   ✅ ppt_upload 路由導入成功")
        
        from base.api.routes.scrapers import router as scrapers_router
        print("   ✅ scrapers 路由導入成功")
        
        from base.api.routes.bigquery import router as bigquery_router
        print("   ✅ bigquery 路由導入成功")
        
        from base.api.routes.batch_reports import router as batch_reports_router
        print("   ✅ batch_reports 路由導入成功")
        
        print("4. 測試應用程式導入...")
        from base.api.app import app
        print("   ✅ 應用程式導入成功")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 導入失敗: {e}")
        traceback.print_exc()
        return False

def test_app_creation():
    """測試應用程式創建"""
    print("\n🏗️ 測試應用程式創建...")
    
    try:
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        # 創建簡單的測試應用
        test_app = FastAPI(
            title="Test API",
            description="測試 API",
            version="1.0.0"
        )
        
        # 配置 CORS
        test_app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # 添加測試端點
        @test_app.get("/")
        def read_root():
            return {"message": "測試成功"}
        
        print("   ✅ 測試應用程式創建成功")
        return test_app
        
    except Exception as e:
        print(f"   ❌ 應用程式創建失敗: {e}")
        traceback.print_exc()
        return None

def test_route_registration():
    """測試路由註冊"""
    print("\n🛣️ 測試路由註冊...")
    
    try:
        from fastapi import FastAPI
        from base.api.routes.ppt_upload import router as ppt_router
        from base.api.routes.scrapers import router as scrapers_router
        from base.api.routes.bigquery import router as bigquery_router
        from base.api.routes.batch_reports import router as batch_reports_router
        
        test_app = FastAPI()
        
        # 註冊路由器
        test_app.include_router(ppt_router)
        print("   ✅ ppt_upload 路由註冊成功")
        
        test_app.include_router(scrapers_router)
        print("   ✅ scrapers 路由註冊成功")
        
        test_app.include_router(bigquery_router)
        print("   ✅ bigquery 路由註冊成功")
        
        test_app.include_router(batch_reports_router)
        print("   ✅ batch_reports 路由註冊成功")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 路由註冊失敗: {e}")
        traceback.print_exc()
        return False

def test_dependencies():
    """測試依賴項"""
    print("\n🔗 測試依賴項...")
    
    try:
        print("1. 測試 BigQuery 客戶端...")
        from base.bigquery.client import BigQueryClient
        print("   ✅ BigQuery 客戶端導入成功")
        
        print("2. 測試 GCS 客戶端...")
        from base.gcs.client import get_gcs_client
        print("   ✅ GCS 客戶端導入成功")
        
        print("3. 測試配置...")
        from config.config import GEMINI_API_KEY
        print(f"   ✅ 配置導入成功 (GEMINI_API_KEY: {'已設置' if GEMINI_API_KEY else '未設置'})")
        
        print("4. 測試增強模組...")
        from base.api.modules.enhanced_report_generator import EnhancedReportGenerator
        print("   ✅ EnhancedReportGenerator 導入成功")
        
        from base.api.modules.trend_analyzer import TrendAnalyzer
        print("   ✅ TrendAnalyzer 導入成功")
        
        from base.api.modules.trend_recommendation_engine import TrendRecommendationEngine
        print("   ✅ TrendRecommendationEngine 導入成功")
        
        return True
        
    except Exception as e:
        print(f"   ❌ 依賴項測試失敗: {e}")
        traceback.print_exc()
        return False

def main():
    """主函數"""
    print("🔍 後端啟動問題診斷")
    print("=" * 50)
    
    # 測試各個組件
    tests = [
        ("模組導入", test_imports),
        ("應用程式創建", test_app_creation),
        ("路由註冊", test_route_registration),
        ("依賴項", test_dependencies),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            if test_name == "應用程式創建":
                result = test_func()
                results[test_name] = result is not None
            else:
                result = test_func()
                results[test_name] = result
        except Exception as e:
            print(f"❌ {test_name} 測試異常: {e}")
            results[test_name] = False
    
    # 總結
    print("\n" + "=" * 50)
    print("📊 測試結果總結:")
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✅ 通過" if passed else "❌ 失敗"
        print(f"   {test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n🎯 診斷結論:")
    if all_passed:
        print("✅ 所有測試通過，後端應該可以正常啟動")
        print("💡 建議檢查:")
        print("   1. 環境變數是否正確設置")
        print("   2. 端口是否被其他程序佔用")
        print("   3. 防火牆設置")
    else:
        print("❌ 發現問題，需要修復失敗的組件")
        print("💡 建議:")
        print("   1. 檢查缺失的依賴項")
        print("   2. 修復導入錯誤")
        print("   3. 檢查配置文件")

if __name__ == "__main__":
    main()
