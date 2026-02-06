#!/usr/bin/env python3
"""
Enhanced Batch Report System Test Script
測試增強版批量報告生成系統

This script tests the new enhanced batch report generation system
to ensure it properly implements the plan.md specifications.
"""

import os
import sys
import requests
import json
import time
from pathlib import Path

# 使用標準導入（專案應作為 package 安裝：pip install -e .）
# 測試檔案可以保留路徑設置以便獨立運行
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# API 基礎配置
API_BASE_URL = "http://localhost:8001"
REPORTS_API_URL = f"{API_BASE_URL}/reports"

def test_enhanced_system_status():
    """測試增強系統狀態"""
    print("🔍 測試增強系統狀態...")
    
    try:
        response = requests.get(f"{REPORTS_API_URL}/enhanced/status")
        if response.status_code == 200:
            status = response.json()
            print(f"✅ 增強系統狀態: {'系統就緒' if status['system_ready'] else '系統未就緒'}")
            
            for component, available in status.items():
                if component != 'system_ready':
                    status_icon = "✅" if available else "❌"
                    print(f"  {status_icon} {component}: {available}")
            
            return status['system_ready']
        else:
            print(f"❌ 獲取系統狀態失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試系統狀態時發生錯誤: {e}")
        return False

def test_enhanced_features():
    """測試增強功能列表"""
    print("\n🚀 測試增強功能列表...")
    
    try:
        response = requests.get(f"{REPORTS_API_URL}/enhanced/features")
        if response.status_code == 200:
            features_data = response.json()
            features = features_data['features']
            summary = features_data['summary']
            
            print(f"✅ 功能完成度: {summary['completion_rate']}")
            print(f"   可用功能: {summary['available_features']}/{summary['total_features']}")
            
            for feature_name, feature_info in features.items():
                status_icon = "✅" if feature_info['available'] else "❌"
                print(f"  {status_icon} {feature_info['name']} ({feature_info['phase']})")
                print(f"     {feature_info['description']}")
            
            return True
        else:
            print(f"❌ 獲取功能列表失敗: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 測試功能列表時發生錯誤: {e}")
        return False

def test_seminars_api():
    """測試研討會列表 API"""
    print("\n📊 測試研討會列表 API...")
    
    try:
        response = requests.get(f"{REPORTS_API_URL}/seminars")
        if response.status_code == 200:
            data = response.json()
            seminars = data.get('seminars', [])
            print(f"✅ 成功獲取 {len(seminars)} 個研討會")
            
            for seminar in seminars[:3]:  # 顯示前3個
                print(f"  📋 {seminar['name']}: {seminar['session_count']} 個會議")
            
            return seminars
        else:
            print(f"❌ 獲取研討會列表失敗: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ 測試研討會列表時發生錯誤: {e}")
        return []

def test_trend_analysis():
    """測試趨勢分析功能"""
    print("\n🔍 測試趨勢分析功能...")
    
    try:
        # 測試數據
        test_request = {
            "seminars": None,  # 分析所有研討會
            "limit": 10  # 限制會議數量以加快測試
        }
        
        response = requests.post(f"{REPORTS_API_URL}/trends/analyze", json=test_request)
        if response.status_code == 200:
            data = response.json()
            trends = data.get('trends', [])
            statistics = data.get('statistics', {})
            
            print(f"✅ 趨勢分析成功:")
            print(f"   📊 識別趨勢: {len(trends)} 個")
            print(f"   📋 分析會議: {statistics.get('total_sessions', 0)} 個")
            print(f"   🏷️ 映射會議: {statistics.get('mapped_sessions', 0)} 個")
            
            # 顯示前3個趨勢
            for i, trend in enumerate(trends[:3]):
                print(f"  {i+1}. {trend['name']} (重要性: {trend['importance_score']:.2f})")
                print(f"     {trend['description'][:100]}...")
            
            return True
        else:
            print(f"❌ 趨勢分析失敗: {response.status_code}")
            if response.text:
                print(f"   錯誤詳情: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 測試趨勢分析時發生錯誤: {e}")
        return False

def test_batch_report_generation():
    """測試批量報告生成"""
    print("\n📝 測試批量報告生成...")

    try:
        # 測試數據
        test_request = {
            "seminars": None,  # 處理所有研討會
            "limit": 3,  # 限制會議數量以加快測試
            "output_format": "markdown",
            "include_html": True,
            "analysis_mode": "comprehensive",
            "output_template": "professional",
            "enable_trend_analysis": True,
            "enable_recommendations": False
        }
        
        print("🚀 啟動批量報告生成任務...")
        response = requests.post(f"{REPORTS_API_URL}/generate-batch", json=test_request)
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('task_id')
            print(f"✅ 任務已啟動: {task_id}")
            print(f"   預計處理: {data.get('estimated_sessions', 0)} 個會議")
            
            # 監控任務進度
            print("⏳ 監控任務進度...")
            max_wait_time = 300  # 最多等待5分鐘
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                status_response = requests.get(f"{REPORTS_API_URL}/status/{task_id}")
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    status = status_data.get('status')
                    progress = status_data.get('progress', {})
                    
                    current = progress.get('current', 0)
                    total = progress.get('total', 0)
                    current_session = progress.get('current_session', '')
                    
                    print(f"📊 進度: {current}/{total} - {current_session}")
                    
                    if status == 'completed':
                        print("🎉 批量報告生成完成!")
                        results = status_data.get('results', {})
                        print(f"   📄 生成文件: {len(results.get('markdown_files', []))} 個 Markdown")
                        print(f"   🌐 生成文件: {len(results.get('html_files', []))} 個 HTML")
                        
                        # 檢查是否生成了符合 plan.md 的文件結構
                        output_dir = results.get('output_directory', '')
                        if output_dir:
                            check_plan_md_compliance(output_dir)
                        
                        return True
                    elif status == 'failed':
                        print(f"❌ 任務失敗: {status_data.get('error_message', '未知錯誤')}")
                        return False
                    
                    time.sleep(5)  # 等待5秒後再次檢查
                else:
                    print(f"❌ 獲取任務狀態失敗: {status_response.status_code}")
                    return False
            
            print("⏰ 任務執行超時")
            return False
            
        else:
            print(f"❌ 啟動批量報告生成失敗: {response.status_code}")
            if response.text:
                print(f"   錯誤詳情: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 測試批量報告生成時發生錯誤: {e}")
        return False

def check_plan_md_compliance(output_dir):
    """檢查生成的文件是否符合 plan.md 規範"""
    print(f"\n🔍 檢查 plan.md 合規性: {output_dir}")
    
    output_path = Path(output_dir)
    if not output_path.exists():
        print(f"❌ 輸出目錄不存在: {output_dir}")
        return False
    
    # 檢查必要的文件結構
    required_files = {
        "trends-analysis.md": "趨勢分析報告",
        "_index.md": "Hugo 首頁文件"
    }
    
    required_dirs = {
        "trends": "趨勢分類目錄",
        "sessions": "會議詳細目錄"
    }
    
    compliance_score = 0
    total_checks = len(required_files) + len(required_dirs)
    
    # 檢查必要文件
    for filename, description in required_files.items():
        file_path = output_path / filename
        if file_path.exists():
            print(f"✅ {description}: {filename}")
            compliance_score += 1
        else:
            print(f"❌ 缺少 {description}: {filename}")
    
    # 檢查必要目錄
    for dirname, description in required_dirs.items():
        dir_path = output_path / dirname
        if dir_path.exists() and dir_path.is_dir():
            files_count = len(list(dir_path.glob("*.md")))
            print(f"✅ {description}: {dirname} ({files_count} 個文件)")
            compliance_score += 1
        else:
            print(f"❌ 缺少 {description}: {dirname}")
    
    compliance_percentage = (compliance_score / total_checks) * 100
    print(f"📊 plan.md 合規性: {compliance_percentage:.1f}% ({compliance_score}/{total_checks})")
    
    return compliance_percentage >= 80  # 80% 以上視為合規

def main():
    """主測試函數"""
    print("🧪 Enhanced Batch Report System Test")
    print("=" * 50)
    
    test_results = []
    
    # 1. 測試系統狀態
    test_results.append(("系統狀態", test_enhanced_system_status()))
    
    # 2. 測試功能列表
    test_results.append(("功能列表", test_enhanced_features()))
    
    # 3. 測試研討會 API
    seminars = test_seminars_api()
    test_results.append(("研討會 API", len(seminars) > 0))
    
    # 4. 測試趨勢分析
    test_results.append(("趨勢分析", test_trend_analysis()))
    
    # 5. 測試批量報告生成
    test_results.append(("批量報告生成", test_batch_report_generation()))
    
    # 總結測試結果
    print("\n" + "=" * 50)
    print("🏁 測試結果總結:")
    
    passed_tests = 0
    for test_name, result in test_results:
        status_icon = "✅" if result else "❌"
        print(f"  {status_icon} {test_name}: {'通過' if result else '失敗'}")
        if result:
            passed_tests += 1
    
    total_tests = len(test_results)
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"\n📊 測試通過率: {success_rate:.1f}% ({passed_tests}/{total_tests})")
    
    if success_rate >= 80:
        print("🎉 增強版批量報告系統測試通過!")
        return True
    else:
        print("⚠️ 增強版批量報告系統需要進一步調試")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
