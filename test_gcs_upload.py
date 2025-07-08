#!/usr/bin/env python3
"""
測試 Google Cloud Storage 上傳功能
用於驗證 GCS 客戶端和上傳功能是否正常工作
"""
import os
import sys
import tempfile
import zipfile
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from base.gcs.client import get_gcs_client

def create_test_zip_file() -> str:
    """創建一個測試用的 ZIP 文件"""
    # 創建臨時目錄
    temp_dir = Path(tempfile.mkdtemp())
    
    # 創建一些測試文件
    test_files = {
        "test_report.md": "# 測試報告\n\n這是一個測試報告文件。",
        "test_data.txt": "這是測試數據文件。",
        "readme.txt": "這是一個測試 ZIP 文件，用於驗證 GCS 上傳功能。"
    }
    
    # 寫入測試文件
    for filename, content in test_files.items():
        file_path = temp_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # 創建 ZIP 文件
    zip_path = temp_dir / "test_report_package.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for filename in test_files.keys():
            file_path = temp_dir / filename
            zipf.write(file_path, filename)
    
    print(f"✅ 測試 ZIP 文件已創建: {zip_path}")
    return str(zip_path)

def test_gcs_client():
    """測試 GCS 客戶端初始化"""
    print("🔧 測試 GCS 客戶端初始化...")
    
    # 檢查環境變量
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    
    print(f"📋 GOOGLE_APPLICATION_CREDENTIALS: {credentials_path}")
    print(f"📋 GOOGLE_CLOUD_PROJECT: {project_id}")
    
    if not credentials_path:
        print("❌ 錯誤: 未設置 GOOGLE_APPLICATION_CREDENTIALS 環境變量")
        return False
    
    if not os.path.exists(credentials_path):
        print(f"❌ 錯誤: 憑證文件不存在: {credentials_path}")
        return False
    
    # 嘗試初始化 GCS 客戶端
    try:
        gcs_client = get_gcs_client()
        if gcs_client:
            print("✅ GCS 客戶端初始化成功")
            return gcs_client
        else:
            print("❌ GCS 客戶端初始化失敗")
            return None
    except Exception as e:
        print(f"❌ GCS 客戶端初始化異常: {e}")
        return None

def test_bucket_access(gcs_client, bucket_name="neo-trend-hub-documents"):
    """測試 bucket 訪問權限"""
    print(f"🪣 測試 bucket 訪問權限: {bucket_name}")
    
    try:
        if gcs_client.check_bucket_exists(bucket_name):
            print(f"✅ Bucket '{bucket_name}' 存在且可訪問")
            return True
        else:
            print(f"❌ Bucket '{bucket_name}' 不存在或無法訪問")
            return False
    except Exception as e:
        print(f"❌ 檢查 bucket 時發生異常: {e}")
        return False

def test_file_upload(gcs_client, test_zip_path, bucket_name="neo-trend-hub-documents"):
    """測試文件上傳"""
    print(f"📤 測試文件上傳到 GCS...")
    
    try:
        # 上傳測試文件
        result = gcs_client.upload_zip_file(
            local_zip_path=test_zip_path,
            bucket_name=bucket_name,
            folder_prefix="test_uploads/"
        )
        
        if result["success"]:
            print("✅ 文件上傳成功!")
            print(f"📍 GCS URL: {result.get('gs_url')}")
            print(f"🌐 公開 URL: {result.get('public_url')}")
            print(f"📏 文件大小: {result.get('size')} 字節")
            return result
        else:
            print(f"❌ 文件上傳失敗: {result.get('error')}")
            return None
            
    except Exception as e:
        print(f"❌ 文件上傳異常: {e}")
        return None

def cleanup_test_file(test_zip_path):
    """清理測試文件"""
    try:
        zip_path = Path(test_zip_path)
        temp_dir = zip_path.parent
        
        # 刪除整個臨時目錄
        import shutil
        shutil.rmtree(temp_dir)
        print(f"🧹 已清理測試文件: {temp_dir}")
    except Exception as e:
        print(f"⚠️  清理測試文件時發生錯誤: {e}")

def main():
    """主測試函數"""
    print("🚀 開始測試 Google Cloud Storage 上傳功能")
    print("=" * 60)
    
    # 1. 創建測試 ZIP 文件
    test_zip_path = create_test_zip_file()
    
    try:
        # 2. 測試 GCS 客戶端初始化
        gcs_client = test_gcs_client()
        if not gcs_client:
            print("\n❌ GCS 客戶端初始化失敗，無法繼續測試")
            return
        
        # 3. 測試 bucket 訪問權限
        if not test_bucket_access(gcs_client):
            print("\n❌ Bucket 訪問失敗，無法繼續測試")
            return
        
        # 4. 測試文件上傳
        upload_result = test_file_upload(gcs_client, test_zip_path)
        
        # 5. 顯示測試結果
        print("\n" + "=" * 60)
        print("📊 測試結果總結:")
        
        if upload_result:
            print("✅ 所有測試通過!")
            print("🎉 GCS 上傳功能正常工作")
            print(f"🔗 測試文件可通過以下 URL 訪問:")
            print(f"   {upload_result.get('public_url')}")
        else:
            print("❌ 測試失敗!")
            print("🔧 請檢查 GCS 配置和權限設置")
            
    finally:
        # 6. 清理測試文件
        cleanup_test_file(test_zip_path)
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
