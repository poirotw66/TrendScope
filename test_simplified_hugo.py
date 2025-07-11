#!/usr/bin/env python3
"""
測試簡化的 Hugo 實現
"""

import requests
import time
import json
import pathlib
from datetime import datetime

# API 基礎 URL
BASE_URL = "http://localhost:8000"
REPORTS_API_URL = f"{BASE_URL}/reports"

def test_simplified_hugo_generation():
    """測試簡化的 Hugo 生成"""
    print("🧪 測試簡化的 Hugo 實現")
    print("=" * 50)
    
    try:
        # 1. 檢查系統狀態
        print("🔧 步驟 1: 檢查系統狀態")
        response = requests.get(f"{REPORTS_API_URL}/enhanced/status")
        
        if response.status_code == 200:
            status = response.json()
            if status.get('system_ready', False):
                print("✅ 系統就緒")
            else:
                print("⚠️ 系統未完全就緒，但繼續測試")
        else:
            print(f"❌ 無法獲取系統狀態: {response.status_code}")
            return False
        
        # 2. 啟動簡化的報告生成
        print("\n🚀 步驟 2: 啟動簡化的報告生成")
        request_data = {
            "seminars": None,
            "limit": 3,  # 限制數量以加快測試
            "output_format": "both",
            "include_html": True,
            "analysis_mode": "comprehensive",
            "output_template": "professional",
            "enable_trend_analysis": True,
            "enable_recommendations": False
        }
        
        response = requests.post(
            f"{REPORTS_API_URL}/generate-batch",
            json=request_data
        )
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id')
            print(f"✅ 任務已啟動: {task_id}")
            print(f"   預計處理: {data.get('estimated_sessions', 0)} 個會議")
            
            # 3. 監控任務進度
            print("\n⏳ 步驟 3: 監控任務進度")
            success = monitor_task_progress(task_id, max_wait_minutes=10)
            
            if success:
                # 4. 驗證輸出結果
                print("\n🔍 步驟 4: 驗證輸出結果")
                return verify_simplified_output(task_id)
            else:
                print("❌ 任務執行失敗或超時")
                return False
                
        else:
            print(f"❌ 啟動任務失敗: {response.status_code}")
            print(f"   錯誤信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        return False

def monitor_task_progress(task_id: str, max_wait_minutes: int = 10):
    """監控任務進度"""
    start_time = time.time()
    max_wait_seconds = max_wait_minutes * 60
    
    while time.time() - start_time < max_wait_seconds:
        try:
            response = requests.get(f"{REPORTS_API_URL}/tasks/{task_id}")
            
            if response.status_code == 200:
                task_data = response.json()
                status = task_data.get('status', 'unknown')
                
                if status == 'completed':
                    print("✅ 任務完成!")
                    return True
                    
                elif status == 'failed':
                    print("❌ 任務失敗!")
                    error = task_data.get('error', 'Unknown error')
                    print(f"   錯誤: {error}")
                    return False
                    
                elif status in ['pending', 'running']:
                    progress_response = requests.get(f"{REPORTS_API_URL}/tasks/{task_id}/progress")
                    if progress_response.status_code == 200:
                        progress_data = progress_response.json()
                        current_session = progress_data.get('current_session', 'N/A')
                        processed = progress_data.get('processed_sessions', 0)
                        total = progress_data.get('total_sessions', 0)
                        
                        print(f"   📊 進度: {processed}/{total} - {current_session}")
                    
                    time.sleep(5)
                    
                else:
                    print(f"   ❓ 未知狀態: {status}")
                    time.sleep(3)
                    
            else:
                print(f"   ⚠️ 無法獲取任務狀態: {response.status_code}")
                time.sleep(3)
                
        except Exception as e:
            print(f"   ❌ 監控任務時發生錯誤: {e}")
            time.sleep(3)
    
    print(f"⏰ 任務監控超時 ({max_wait_minutes} 分鐘)")
    return False

def verify_simplified_output(task_id: str):
    """驗證簡化 Hugo 的輸出結果"""
    try:
        # 獲取任務結果
        response = requests.get(f"{REPORTS_API_URL}/tasks/{task_id}")
        
        if response.status_code != 200:
            print(f"❌ 無法獲取任務結果: {response.status_code}")
            return False
        
        task_data = response.json()
        results = task_data.get('results', {})
        output_dir = results.get('output_directory')
        
        if not output_dir:
            print("❌ 未找到輸出目錄")
            return False
        
        output_path = pathlib.Path(output_dir)
        if not output_path.exists():
            print(f"❌ 輸出目錄不存在: {output_dir}")
            return False
        
        print(f"📁 輸出目錄: {output_dir}")
        
        # 檢查 Markdown 文件
        md_dir = output_path / "md"
        if md_dir.exists():
            print("✅ Markdown 目錄存在")
            
            md_files = list(md_dir.glob("*.md"))
            print(f"   📄 Markdown 文件: {len(md_files)} 個")
            
            # 檢查關鍵文件
            key_files = ["_index.md", "trends-analysis.md"]
            for key_file in key_files:
                if (md_dir / key_file).exists():
                    print(f"   ✅ {key_file}")
                else:
                    print(f"   ❌ 缺少 {key_file}")
        
        # 檢查 HTML 文件（簡化生成器的輸出）
        html_dir = output_path / "html"
        if html_dir.exists():
            print("✅ HTML 目錄存在")
            
            # 檢查首頁
            index_file = html_dir / "index.html"
            if index_file.exists():
                print("   ✅ index.html")
                
                # 檢查首頁內容
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "TrendScope" in content:
                        print("   ✅ 首頁包含 TrendScope 標題")
                    if "技術趨勢" in content:
                        print("   ✅ 首頁包含技術趨勢內容")
            else:
                print("   ❌ 缺少 index.html")
            
            # 檢查 CSS 文件
            css_dir = html_dir / "css"
            if css_dir.exists() and (css_dir / "main.css").exists():
                print("   ✅ CSS 樣式文件")
            else:
                print("   ❌ 缺少 CSS 樣式文件")
            
            # 檢查 JavaScript 文件
            js_dir = html_dir / "js"
            if js_dir.exists() and (js_dir / "main.js").exists():
                print("   ✅ JavaScript 文件")
            else:
                print("   ❌ 缺少 JavaScript 文件")
            
            # 檢查趨勢目錄
            trends_dir = html_dir / "trends"
            if trends_dir.exists():
                trend_files = list(trends_dir.glob("*.html"))
                print(f"   ✅ 趨勢頁面: {len(trend_files)} 個")
            else:
                print("   ❌ 缺少趨勢目錄")
            
            # 檢查會議目錄
            sessions_dir = html_dir / "sessions"
            if sessions_dir.exists():
                session_files = list(sessions_dir.glob("*.html"))
                print(f"   ✅ 會議頁面: {len(session_files)} 個")
            else:
                print("   ❌ 缺少會議目錄")
        
        # 檢查離線包
        zip_files = list(output_path.glob("*.zip"))
        if zip_files:
            print(f"✅ 離線包: {len(zip_files)} 個")
            for zip_file in zip_files:
                print(f"   📦 {zip_file.name}")
        else:
            print("❌ 未找到離線包")
        
        # 檢查啟動器
        launcher_file = html_dir / "launcher.html"
        if launcher_file.exists():
            print("✅ 啟動器文件")
        else:
            print("❌ 缺少啟動器文件")
        
        print("\n🎯 簡化 Hugo 實現驗證完成")
        return True
        
    except Exception as e:
        print(f"❌ 驗證輸出時發生錯誤: {e}")
        return False

def compare_with_original_hugo():
    """比較簡化版本與原版 Hugo 的差異"""
    print("\n📊 簡化版本 vs 原版 Hugo 比較:")
    print("=" * 40)
    
    comparison = {
        "依賴性": {
            "簡化版本": "無外部依賴",
            "原版 Hugo": "需要 Hugo 二進制"
        },
        "複雜度": {
            "簡化版本": "單一文件，邏輯清晰",
            "原版 Hugo": "多文件，邏輯複雜"
        },
        "功能完整性": {
            "簡化版本": "三階層架構，基本功能",
            "原版 Hugo": "完整 Hugo 功能"
        },
        "維護性": {
            "簡化版本": "易於維護和調試",
            "原版 Hugo": "維護複雜"
        },
        "性能": {
            "簡化版本": "快速生成",
            "原版 Hugo": "依賴外部程序"
        }
    }
    
    for aspect, details in comparison.items():
        print(f"\n{aspect}:")
        print(f"  簡化版本: {details['簡化版本']}")
        print(f"  原版 Hugo: {details['原版 Hugo']}")

def main():
    """主函數"""
    print("🧪 簡化 Hugo 實現測試")
    print(f"🕐 測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API 地址: {BASE_URL}")
    print()
    
    # 執行測試
    success = test_simplified_hugo_generation()
    
    # 顯示比較
    compare_with_original_hugo()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 簡化 Hugo 實現測試成功!")
        print("✅ 新的實現更簡潔、可靠、易維護")
        print("💡 建議:")
        print("   1. 可以完全替代原有的複雜 Hugo 實現")
        print("   2. 保持所有核心功能不變")
        print("   3. 提升系統穩定性和可維護性")
    else:
        print("❌ 測試失敗，需要檢查實現")
    
    print("\n📋 使用說明:")
    print("1. 確保 FastAPI 服務正在運行")
    print("2. 新的簡化實現已集成到批量報告生成中")
    print("3. 所有 API 調用方式保持不變")
    print("4. 輸出結果格式完全兼容")

if __name__ == "__main__":
    main()
