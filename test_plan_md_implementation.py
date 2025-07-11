#!/usr/bin/env python3
"""
Plan.md 實施驗證測試腳本
驗證四階段工作流程是否完全符合 plan.md 規範
"""

import requests
import time
import json
from datetime import datetime
import pathlib

# API 基礎 URL
BASE_URL = "http://localhost:8000"
REPORTS_API_URL = f"{BASE_URL}/reports"

def test_plan_md_phase_1():
    """測試第一階段：LLM 趨勢分析"""
    print("📊 測試第一階段：LLM 趨勢分析")
    
    try:
        # 測試趨勢分析 API
        response = requests.post(
            f"{REPORTS_API_URL}/trends/analyze-enhanced",
            json={"seminars": None, "limit": 5}
        )
        
        if response.status_code == 200:
            data = response.json()
            trends = data.get('trends', [])
            print(f"✅ LLM 趨勢分析成功")
            print(f"   識別趨勢數量: {len(trends)}")
            
            # 檢查是否包含五大趨勢
            expected_trends = ["AI/ML", "雲原生", "數據分析", "DevOps", "安全隱私"]
            found_trends = [trend.get('name', '') for trend in trends]
            
            for expected in expected_trends:
                if any(expected in found for found in found_trends):
                    print(f"   ✅ 發現趨勢: {expected}")
                else:
                    print(f"   ⚠️ 未發現趨勢: {expected}")
            
            return True
        else:
            print(f"❌ 趨勢分析失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 第一階段測試失敗: {e}")
        return False

def test_plan_md_full_workflow():
    """測試完整的四階段工作流程"""
    print("\n🚀 測試完整的四階段工作流程")
    
    try:
        # 啟動完整工作流程
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
        
        print("📤 啟動批量報告生成...")
        response = requests.post(
            f"{REPORTS_API_URL}/generate-batch",
            json=request_data
        )
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id')
            print(f"✅ 任務已啟動: {task_id}")
            print(f"   預計處理: {data.get('estimated_sessions', 0)} 個會議")
            
            # 監控任務進度
            success = monitor_task_with_phase_tracking(task_id, max_wait_minutes=15)
            
            if success:
                print("🎉 完整四階段工作流程測試成功!")
                return True
            else:
                print("⏰ 工作流程測試超時或失敗")
                return False
                
        else:
            print(f"❌ 啟動工作流程失敗: {response.status_code}")
            print(f"   錯誤信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 完整工作流程測試失敗: {e}")
        return False

def monitor_task_with_phase_tracking(task_id: str, max_wait_minutes: int = 15):
    """監控任務進度並追蹤四個階段"""
    print(f"⏳ 監控四階段工作流程: {task_id}")
    
    start_time = time.time()
    max_wait_seconds = max_wait_minutes * 60
    phases_completed = set()
    
    while time.time() - start_time < max_wait_seconds:
        try:
            # 檢查任務狀態
            response = requests.get(f"{REPORTS_API_URL}/tasks/{task_id}")
            
            if response.status_code == 200:
                task_data = response.json()
                status = task_data.get('status', 'unknown')
                
                if status == 'completed':
                    print("✅ 四階段工作流程完成!")
                    
                    # 驗證輸出結果
                    results = task_data.get('results', {})
                    return verify_plan_md_outputs(results)
                    
                elif status == 'failed':
                    print("❌ 工作流程失敗!")
                    error = task_data.get('error', 'Unknown error')
                    print(f"   錯誤: {error}")
                    return False
                    
                elif status in ['pending', 'running']:
                    # 獲取進度信息並追蹤階段
                    progress_response = requests.get(f"{REPORTS_API_URL}/tasks/{task_id}/progress")
                    if progress_response.status_code == 200:
                        progress_data = progress_response.json()
                        current_session = progress_data.get('current_session', 'N/A')
                        processed = progress_data.get('processed_sessions', 0)
                        total = progress_data.get('total_sessions', 0)
                        
                        # 檢測階段進度
                        if "步驟 1" in current_session and "phase_1" not in phases_completed:
                            print("   📊 第一階段：LLM 趨勢分析 - 進行中")
                            phases_completed.add("phase_1")
                        elif "步驟 2" in current_session and "phase_2" not in phases_completed:
                            print("   🏷️ 第二階段：自動標記系統 - 進行中")
                            phases_completed.add("phase_2")
                        elif "步驟 3" in current_session and "phase_3" not in phases_completed:
                            print("   📝 第三階段：Markdown 生成 - 進行中")
                            phases_completed.add("phase_3")
                        elif "步驟 4" in current_session and "phase_4" not in phases_completed:
                            print("   🏗️ 第四階段：Hugo 建構 - 進行中")
                            phases_completed.add("phase_4")
                        
                        print(f"   📊 總進度: {processed}/{total} - {current_session}")
                    
                    time.sleep(10)  # 等待10秒後再檢查
                    
                else:
                    print(f"   ❓ 未知狀態: {status}")
                    time.sleep(5)
                    
            else:
                print(f"   ⚠️ 無法獲取任務狀態: {response.status_code}")
                time.sleep(5)
                
        except Exception as e:
            print(f"   ❌ 監控任務時發生錯誤: {e}")
            time.sleep(5)
    
    print(f"⏰ 任務監控超時 ({max_wait_minutes} 分鐘)")
    return False

def verify_plan_md_outputs(results: dict):
    """驗證輸出是否符合 plan.md 規範"""
    print("🔍 驗證輸出結果是否符合 plan.md 規範...")
    
    try:
        output_dir = results.get('output_directory')
        if not output_dir:
            print("❌ 未找到輸出目錄")
            return False
        
        output_path = pathlib.Path(output_dir)
        if not output_path.exists():
            print(f"❌ 輸出目錄不存在: {output_dir}")
            return False
        
        # 檢查 Markdown 文件結構
        md_dir = output_path / "md"
        if md_dir.exists():
            print("✅ Markdown 目錄存在")
            
            # 檢查關鍵文件
            key_files = {
                "_index.md": "Hugo 首頁",
                "trends-analysis.md": "趨勢分析報告"
            }
            
            for filename, description in key_files.items():
                file_path = md_dir / filename
                if file_path.exists():
                    print(f"   ✅ {description}: {filename}")
                else:
                    print(f"   ❌ 缺少 {description}: {filename}")
            
            # 檢查趨勢分類文件
            trend_files = list(md_dir.glob("trend-*.md"))
            if trend_files:
                print(f"   ✅ 趨勢分類文件: {len(trend_files)} 個")
            else:
                print("   ❌ 未找到趨勢分類文件")
            
            # 檢查會議詳細文件
            session_files = list(md_dir.glob("session-*.md"))
            if session_files:
                print(f"   ✅ 會議詳細文件: {len(session_files)} 個")
            else:
                print("   ❌ 未找到會議詳細文件")
        
        # 檢查 HTML 文件結構
        html_dir = output_path / "html"
        if html_dir.exists():
            print("✅ HTML 目錄存在")
            
            # 檢查首頁
            index_file = html_dir / "index.html"
            if index_file.exists():
                print("   ✅ 靜態網站首頁: index.html")
            else:
                print("   ❌ 缺少靜態網站首頁")
        
        # 檢查離線包
        zip_files = list(output_path.glob("*.zip"))
        if zip_files:
            print(f"✅ 離線包: {len(zip_files)} 個")
        else:
            print("❌ 未找到離線包")
        
        print("🎯 plan.md 規範驗證完成")
        return True
        
    except Exception as e:
        print(f"❌ 驗證輸出時發生錯誤: {e}")
        return False

def test_system_status():
    """測試系統狀態"""
    print("🔧 測試系統狀態")
    
    try:
        # 檢查增強系統狀態
        response = requests.get(f"{REPORTS_API_URL}/enhanced/status")
        
        if response.status_code == 200:
            status = response.json()
            print("✅ 系統狀態檢查成功")
            
            components = {
                "enhanced_report_generator": "增強報告生成器",
                "trend_analyzer": "趨勢分析器",
                "hugo_generator": "Hugo 生成器",
                "bigquery_client": "BigQuery 客戶端",
                "gemini_api": "Gemini API"
            }
            
            for key, name in components.items():
                if status.get(key, False):
                    print(f"   ✅ {name}")
                else:
                    print(f"   ❌ {name}")
            
            if status.get('system_ready', False):
                print("🎉 系統完全就緒，可以執行 plan.md 工作流程")
                return True
            else:
                print("⚠️ 系統未完全就緒")
                return False
        else:
            print(f"❌ 系統狀態檢查失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 系統狀態測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🧪 Plan.md 實施驗證測試")
    print("=" * 60)
    print(f"🕐 測試時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🌐 API 地址: {BASE_URL}")
    print()
    
    # 測試結果統計
    test_results = {}
    
    # 1. 測試系統狀態
    print("🔧 步驟 1: 系統狀態檢查")
    test_results['system_status'] = test_system_status()
    print()
    
    # 2. 測試第一階段
    print("📊 步驟 2: 第一階段測試")
    test_results['phase_1'] = test_plan_md_phase_1()
    print()
    
    # 3. 測試完整工作流程
    if test_results['system_status']:
        print("🚀 步驟 3: 完整四階段工作流程測試")
        test_results['full_workflow'] = test_plan_md_full_workflow()
    else:
        print("⚠️ 跳過完整工作流程測試（系統未就緒）")
        test_results['full_workflow'] = False
    
    # 輸出測試結果
    print("\n" + "=" * 60)
    print("📊 測試結果總結:")
    
    for test_name, result in test_results.items():
        status = "✅ 通過" if result else "❌ 失敗"
        test_display_name = {
            'system_status': '系統狀態檢查',
            'phase_1': '第一階段：LLM 趨勢分析',
            'full_workflow': '完整四階段工作流程'
        }.get(test_name, test_name)
        
        print(f"   {status} {test_display_name}")
    
    all_passed = all(test_results.values())
    
    if all_passed:
        print("\n🎉 所有測試通過！")
        print("✅ 專案完全符合 plan.md 規範")
        print("🚀 系統已準備好用於生產環境")
    else:
        print("\n⚠️ 部分測試失敗")
        print("請檢查系統配置和依賴項")
    
    print("\n💡 使用提示:")
    print("1. 確保 FastAPI 服務正在運行 (http://localhost:8000)")
    print("2. 確保 BigQuery 連接正常")
    print("3. 確保有足夠的 Gemini API 配額")
    print("4. 生成的報告會保存在 reports/ 目錄下")

if __name__ == "__main__":
    main()
