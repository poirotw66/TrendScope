#!/usr/bin/env python3
"""
檢查 Google Cloud Storage 配置
快速驗證 GCS 設置是否正確
"""
import os
import sys
from pathlib import Path

def check_environment_variables():
    """檢查必要的環境變量"""
    print("🔍 檢查環境變量...")
    
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    print(f"📋 GOOGLE_APPLICATION_CREDENTIALS: {credentials_path}")
    print(f"📋 GOOGLE_CLOUD_PROJECT: {project_id}")
    
    issues = []
    
    if not credentials_path:
        issues.append("❌ GOOGLE_APPLICATION_CREDENTIALS 環境變量未設置")
    elif not os.path.exists(credentials_path):
        issues.append(f"❌ 憑證文件不存在: {credentials_path}")
    else:
        print("✅ 憑證文件路徑正確")
    
    if not project_id:
        issues.append("❌ GOOGLE_CLOUD_PROJECT 環境變量未設置")
    else:
        print("✅ 項目 ID 已設置")
    
    return issues

def check_dependencies():
    """檢查必要的 Python 依賴項"""
    print("\n📦 檢查 Python 依賴項...")
    
    required_packages = [
        "google-cloud-storage",
        "google-cloud-bigquery",
        "fastapi",
        "pydantic"
    ]
    
    issues = []
    
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} 已安裝")
        except ImportError:
            issues.append(f"❌ {package} 未安裝")
    
    return issues

def check_project_structure():
    """檢查項目結構"""
    print("\n📁 檢查項目結構...")
    
    required_files = [
        "base/gcs/__init__.py",
        "base/gcs/client.py",
        "base/api/routes/batch_reports.py",
        "requirements.txt"
    ]
    
    issues = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} 存在")
        else:
            issues.append(f"❌ {file_path} 不存在")
    
    return issues

def check_gcs_client():
    """檢查 GCS 客戶端是否可以初始化"""
    print("\n🔧 檢查 GCS 客戶端...")
    
    try:
        # 添加專案根目錄到 Python 路徑
        project_root = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, project_root)
        
        from base.gcs.client import get_gcs_client
        
        gcs_client = get_gcs_client()
        if gcs_client:
            print("✅ GCS 客戶端初始化成功")
            
            # 檢查 bucket 訪問
            bucket_name = "neo-trend-hub-documents"
            if gcs_client.check_bucket_exists(bucket_name):
                print(f"✅ Bucket '{bucket_name}' 可訪問")
                return []
            else:
                return [f"❌ Bucket '{bucket_name}' 不存在或無法訪問"]
        else:
            return ["❌ GCS 客戶端初始化失敗"]
            
    except ImportError as e:
        return [f"❌ 無法導入 GCS 客戶端: {e}"]
    except Exception as e:
        return [f"❌ GCS 客戶端檢查失敗: {e}"]

def main():
    """主檢查函數"""
    print("🚀 Google Cloud Storage 配置檢查")
    print("=" * 50)
    
    all_issues = []
    
    # 檢查環境變量
    all_issues.extend(check_environment_variables())
    
    # 檢查依賴項
    all_issues.extend(check_dependencies())
    
    # 檢查項目結構
    all_issues.extend(check_project_structure())
    
    # 檢查 GCS 客戶端
    all_issues.extend(check_gcs_client())
    
    # 顯示結果
    print("\n" + "=" * 50)
    print("📊 檢查結果:")
    
    if not all_issues:
        print("🎉 所有檢查通過！GCS 配置正確。")
        print("\n📝 下一步:")
        print("1. 運行 'python test_gcs_upload.py' 進行完整測試")
        print("2. 啟動 FastAPI 應用並測試批量報告生成")
    else:
        print(f"❌ 發現 {len(all_issues)} 個問題:")
        for issue in all_issues:
            print(f"   {issue}")
        
        print("\n🔧 解決建議:")
        print("1. 檢查 docs/GCS_UPLOAD_SETUP.md 獲取詳細設置指南")
        print("2. 確保已正確設置 Google Cloud 憑證")
        print("3. 安裝缺失的依賴項: pip install -r requirements.txt")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
