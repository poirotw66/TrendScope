#!/usr/bin/env python3
"""
Direct Enhanced Report Generation Test
直接測試增強版報告生成功能（不需要 API 服務器）

This script directly tests the enhanced report generation modules
without requiring the FastAPI server to be running.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# 使用標準導入（專案應作為 package 安裝：pip install -e .）
# 測試檔案可以保留路徑設置以便獨立運行
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

def test_enhanced_modules_import():
    """測試增強模組導入"""
    print("🔍 測試增強模組導入...")
    
    try:
        from base.api.modules.enhanced_report_generator import EnhancedReportGenerator
        print("✅ EnhancedReportGenerator 導入成功")
        
        from base.api.modules.trend_analyzer import TrendAnalyzer
        print("✅ TrendAnalyzer 導入成功")
        
        from base.api.modules.trend_recommendation_engine import TrendRecommendationEngine
        print("✅ TrendRecommendationEngine 導入成功")
        
        from base.api.modules.hugo_report import HugoReportGenerator
        print("✅ HugoReportGenerator 導入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 模組導入失敗: {e}")
        return False

def test_enhanced_report_generator():
    """測試增強報告生成器"""
    print("\n📊 測試增強報告生成器...")
    
    try:
        from base.api.modules.enhanced_report_generator import EnhancedReportGenerator
        
        # 創建測試實例
        generator = EnhancedReportGenerator()
        print("✅ 增強報告生成器實例創建成功")
        
        # 創建測試數據
        test_sessions = [
            {
                "conference_id": "test-001",
                "name": "AI 晶片設計的未來趨勢",
                "seminar": "QCon Beijing 2025",
                "content": "本次演講探討了 AI 晶片設計的最新發展，包括神經網路處理器、邊緣計算晶片等關鍵技術。",
                "url": "https://example.com/ai-chips",
                "date": "2025-07-10"
            },
            {
                "conference_id": "test-002", 
                "name": "多模態大型語言模型的應用",
                "seminar": "QCon Beijing 2025",
                "content": "介紹多模態 LLM 在圖像理解、語音處理等領域的突破性應用。",
                "url": "https://example.com/multimodal-llm",
                "date": "2025-07-10"
            },
            {
                "conference_id": "test-003",
                "name": "雲原生架構的演進",
                "seminar": "QCon Beijing 2025", 
                "content": "探討雲原生技術的發展歷程，包括容器化、微服務、服務網格等關鍵概念。",
                "url": "https://example.com/cloud-native",
                "date": "2025-07-10"
            }
        ]
        
        # 創建測試輸出目錄
        test_output_dir = Path("test_output") / f"enhanced_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        test_output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 測試輸出目錄: {test_output_dir}")
        
        # 執行增強報告生成
        print("🚀 開始執行增強報告生成...")
        result = generator.generate_comprehensive_reports(
            sessions=test_sessions,
            output_dir=test_output_dir,
            analysis_mode="comprehensive",
            output_template="professional",
            enable_trend_analysis=True,
            enable_recommendations=False
        )
        
        if result:
            print("✅ 增強報告生成成功!")
            print(f"📄 生成的文件:")
            
            # 檢查生成的文件
            if result.get('trends_analysis_file'):
                print(f"  📊 趨勢分析文件: {result['trends_analysis_file']}")
            
            if result.get('index_file'):
                print(f"  🏠 首頁文件: {result['index_file']}")
                
            trend_files = result.get('trend_files', [])
            print(f"  📂 趨勢分類文件: {len(trend_files)} 個")
            for trend_file in trend_files[:3]:  # 顯示前3個
                print(f"    - {Path(trend_file).name}")
            
            session_files = result.get('session_files', [])
            print(f"  📋 會議詳細文件: {len(session_files)} 個")
            for session_file in session_files[:3]:  # 顯示前3個
                print(f"    - {Path(session_file).name}")
            
            # 檢查文件結構是否符合 plan.md
            check_plan_md_compliance(test_output_dir)
            
            return True
        else:
            print("❌ 增強報告生成失敗")
            return False
            
    except Exception as e:
        print(f"❌ 測試增強報告生成器時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_hugo_report_generator():
    """測試 Hugo 報告生成器"""
    print("\n🏗️ 測試 Hugo 報告生成器...")
    
    try:
        from base.api.modules.hugo_report import HugoReportGenerator
        
        # 創建測試實例
        hugo_generator = HugoReportGenerator()
        print("✅ Hugo 報告生成器實例創建成功")
        
        # 查找最新的測試輸出目錄
        test_output_base = Path("test_output")
        if not test_output_base.exists():
            print("❌ 找不到測試輸出目錄，請先運行增強報告生成測試")
            return False
        
        # 找到最新的測試目錄
        test_dirs = [d for d in test_output_base.iterdir() if d.is_dir() and d.name.startswith("enhanced_test_")]
        if not test_dirs:
            print("❌ 找不到增強測試目錄")
            return False
        
        latest_test_dir = max(test_dirs, key=lambda x: x.stat().st_mtime)
        print(f"📁 使用測試目錄: {latest_test_dir}")
        
        # 創建 Hugo 輸出目錄
        hugo_output_dir = latest_test_dir / "hugo_output"
        hugo_output_dir.mkdir(exist_ok=True)
        
        # 執行 Hugo 網站生成
        print("🚀 開始執行 Hugo 網站生成...")
        result = hugo_generator.generate_hugo_site(
            md_dir=str(latest_test_dir),
            html_dir=str(hugo_output_dir),
            template_style="professional",
            create_offline_package=True
        )
        
        if result and isinstance(result, dict):
            print("✅ Hugo 網站生成成功!")
            print(f"🌐 生成的 HTML 文件: {len(result.get('html_files', []))} 個")
            
            if result.get('zip_file'):
                print(f"📦 離線包: {result['zip_file']}")
            
            if result.get('launcher_file'):
                print(f"🚀 啟動器: {result['launcher_file']}")
            
            # 檢查 Hugo 網站結構
            check_hugo_site_structure(hugo_output_dir)
            
            return True
        else:
            print("❌ Hugo 網站生成失敗")
            return False
            
    except Exception as e:
        print(f"❌ 測試 Hugo 報告生成器時發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_plan_md_compliance(output_dir):
    """檢查生成的文件是否符合 plan.md 規範"""
    print(f"\n🔍 檢查 plan.md 合規性: {output_dir}")
    
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
        file_path = output_dir / filename
        if file_path.exists():
            print(f"✅ {description}: {filename}")
            compliance_score += 1
        else:
            print(f"❌ 缺少 {description}: {filename}")
    
    # 檢查必要目錄
    for dirname, description in required_dirs.items():
        dir_path = output_dir / dirname
        if dir_path.exists() and dir_path.is_dir():
            files_count = len(list(dir_path.glob("*.md")))
            print(f"✅ {description}: {dirname} ({files_count} 個文件)")
            compliance_score += 1
        else:
            print(f"❌ 缺少 {description}: {dirname}")
    
    compliance_percentage = (compliance_score / total_checks) * 100
    print(f"📊 plan.md 合規性: {compliance_percentage:.1f}% ({compliance_score}/{total_checks})")
    
    return compliance_percentage >= 80

def check_hugo_site_structure(hugo_output_dir):
    """檢查 Hugo 網站結構"""
    print(f"\n🏗️ 檢查 Hugo 網站結構: {hugo_output_dir}")
    
    # 檢查關鍵文件
    key_files = {
        "index.html": "首頁",
        "css/styles.css": "樣式文件",
        "js/main.js": "JavaScript 文件"
    }
    
    structure_score = 0
    total_checks = len(key_files)
    
    for filename, description in key_files.items():
        file_path = hugo_output_dir / filename
        if file_path.exists():
            print(f"✅ {description}: {filename}")
            structure_score += 1
        else:
            print(f"❌ 缺少 {description}: {filename}")
    
    # 檢查目錄結構
    expected_dirs = ["trends", "sessions", "css", "js"]
    for dirname in expected_dirs:
        dir_path = hugo_output_dir / dirname
        if dir_path.exists():
            print(f"✅ 目錄: {dirname}/")
        else:
            print(f"⚠️ 目錄不存在: {dirname}/")
    
    structure_percentage = (structure_score / total_checks) * 100
    print(f"📊 Hugo 網站結構完整性: {structure_percentage:.1f}% ({structure_score}/{total_checks})")

def main():
    """主測試函數"""
    print("🧪 Enhanced Report Generation Direct Test")
    print("=" * 50)
    
    test_results = []
    
    # 1. 測試模組導入
    test_results.append(("模組導入", test_enhanced_modules_import()))
    
    # 2. 測試增強報告生成器
    test_results.append(("增強報告生成", test_enhanced_report_generator()))

    # 3. 測試 Hugo 報告生成器
    test_results.append(("Hugo 網站生成", test_hugo_report_generator()))
    
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
        print("🎉 增強版報告生成系統直接測試通過!")
        return True
    else:
        print("⚠️ 增強版報告生成系統需要進一步調試")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
