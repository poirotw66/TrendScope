#!/usr/bin/env python3
"""
Gemini API 連接測試
測試 API 密鑰是否正確配置並能正常工作
"""

import os
import sys
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

def test_api_key_loading():
    """測試 API 密鑰加載"""
    print("🔍 測試 API 密鑰加載...")
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY 環境變量未設置")
        return False
    
    print(f"✅ API 密鑰已加載")
    print(f"   長度: {len(api_key)} 字符")
    print(f"   前綴: {api_key[:6]}...")
    print(f"   後綴: ...{api_key[-4:]}")
    
    # 檢查是否為有效的 Gemini API 密鑰格式
    if api_key.startswith('AIza') and len(api_key) >= 35:
        print("✅ API 密鑰格式看起來正確")
        return True
    else:
        print("⚠️ API 密鑰格式可能不正確")
        print("   Gemini API 密鑰通常以 'AIza' 開頭，長度約 39 字符")
        return False

def test_gemini_api_connection():
    """測試 Gemini API 連接"""
    print("\n🌐 測試 Gemini API 連接...")
    
    try:
        import google.generativeai as genai
        
        # 配置 API
        api_key = os.getenv('GEMINI_API_KEY')
        genai.configure(api_key=api_key)
        
        # 創建模型
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        print("✅ Gemini 模型創建成功")
        
        # 測試簡單的生成
        print("🧪 測試簡單的文本生成...")
        response = model.generate_content("請用一句話介紹人工智慧")
        
        if response and response.text:
            print("✅ API 連接成功!")
            print(f"   回應: {response.text[:100]}...")
            return True
        else:
            print("❌ API 回應為空")
            return False
            
    except Exception as e:
        print(f"❌ API 連接失敗: {e}")
        return False

def test_trend_analyzer_integration():
    """測試趨勢分析器整合"""
    print("\n🔬 測試趨勢分析器整合...")
    
    try:
        from base.api.modules.trend_analyzer import TrendAnalyzer
        
        # 創建趨勢分析器實例
        analyzer = TrendAnalyzer()
        print("✅ 趨勢分析器創建成功")
        
        # 測試數據
        test_sessions = [
            {
                "name": "AI 晶片設計的未來趨勢",
                "content": "本次演講探討了 AI 晶片設計的最新發展，包括神經網路處理器、邊緣計算晶片等關鍵技術。",
                "seminar": "QCon Beijing 2025"
            }
        ]
        
        print("🧪 測試趨勢分析功能...")
        trends = analyzer.analyze_trends(test_sessions)
        
        if trends:
            print(f"✅ 趨勢分析成功! 識別出 {len(trends)} 個趨勢")
            for trend in trends[:2]:  # 顯示前2個趨勢
                print(f"   - {trend.name}: {trend.description[:50]}...")
            return True
        else:
            print("⚠️ 趨勢分析返回空結果")
            return False
            
    except Exception as e:
        print(f"❌ 趨勢分析器測試失敗: {e}")
        return False

def main():
    """主測試函數"""
    print("🧪 Gemini API 配置測試")
    print("=" * 50)
    
    test_results = []
    
    # 1. 測試 API 密鑰加載
    test_results.append(("API 密鑰加載", test_api_key_loading()))
    
    # 2. 測試 API 連接
    test_results.append(("API 連接測試", test_gemini_api_connection()))
    
    # 3. 測試趨勢分析器整合
    test_results.append(("趨勢分析器整合", test_trend_analyzer_integration()))
    
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
        print("🎉 Gemini API 配置測試通過!")
        print("💡 您現在可以運行完整的增強報告生成測試")
        return True
    else:
        print("⚠️ Gemini API 配置需要進一步調試")
        print("\n🔧 建議檢查項目:")
        print("1. 確認 .env 文件中的 GEMINI_API_KEY 是有效的")
        print("2. 檢查網絡連接是否正常")
        print("3. 確認 API 密鑰有足夠的配額")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
