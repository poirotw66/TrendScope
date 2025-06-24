#!/usr/bin/env python3
"""
測試前端後端整合功能
"""

import requests
import time
import json

def test_ppt_upload_integration():
    """測試 PPT 上傳整合功能"""
    
    base_url = "http://localhost:8001"
    
    print("🧪 測試 PPT 上傳整合功能")
    print("=" * 50)
    
    # 1. 測試研討會列表 API
    print("1. 測試研討會列表 API...")
    try:
        response = requests.get(f"{base_url}/ppt/seminars")
        if response.status_code == 200:
            seminars = response.json()
            print(f"✅ 成功獲取研討會列表: {len(seminars['seminars'])} 個研討會")
            for seminar in seminars['seminars']:
                print(f"   - {seminar['name']}: {seminar['session_count']} 個會議")
        else:
            print(f"❌ 獲取研討會列表失敗: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 研討會列表 API 錯誤: {e}")
        return False
    
    # 2. 測試檔案上傳 API
    print("\n2. 測試檔案上傳 API...")
    
    # 創建測試檔案
    test_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj

2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj

3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
>>
endobj

4 0 obj
<<
/Length 120
>>
stream
BT
/F1 12 Tf
72 720 Td
(Test PPT Integration) Tj
0 -20 Td
(Frontend Backend Test) Tj
ET
endstream
endobj

xref
0 5
0000000000 65535 f 
0000000009 00000 n 
0000000058 00000 n 
0000000115 00000 n 
0000000206 00000 n 
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
375
%%EOF"""
    
    try:
        files = {'files': ('test_integration.pdf', test_content, 'application/pdf')}
        data = {'seminar': '202503 QCon Beijing'}
        
        response = requests.post(f"{base_url}/ppt/upload", files=files, data=data)
        
        if response.status_code == 200:
            upload_result = response.json()
            task_id = upload_result['task_id']
            print(f"✅ 檔案上傳成功，任務ID: {task_id}")
            print(f"   訊息: {upload_result['message']}")
            print(f"   檔案數量: {upload_result['files_count']}")
        else:
            print(f"❌ 檔案上傳失敗: {response.status_code}")
            print(f"   響應: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 檔案上傳 API 錯誤: {e}")
        return False
    
    # 3. 測試狀態查詢 API（輪詢）
    print(f"\n3. 測試狀態查詢 API（任務ID: {task_id}）...")
    
    max_polls = 20
    poll_interval = 3
    
    for i in range(max_polls):
        try:
            response = requests.get(f"{base_url}/ppt/status/{task_id}")
            
            if response.status_code == 200:
                status = response.json()
                print(f"   輪詢 {i+1}/{max_polls}: {status['status']} - {status['progress']}% - {status['message']}")
                
                if status['status'] == 'success':
                    print("✅ 處理成功完成！")
                    result = status.get('result', {})
                    print(f"   總計: {result.get('total', 0)}")
                    print(f"   成功: {result.get('success', 0)}")
                    print(f"   失敗: {result.get('failed', 0)}")
                    break
                    
                elif status['status'] == 'error':
                    print(f"❌ 處理失敗: {status.get('error', '未知錯誤')}")
                    break
                    
                elif status['status'] in ['pending', 'processing']:
                    print(f"   ⏳ 處理中，{poll_interval} 秒後再次查詢...")
                    time.sleep(poll_interval)
                    
                else:
                    print(f"   ❓ 未知狀態: {status['status']}")
                    time.sleep(poll_interval)
                    
            else:
                print(f"❌ 狀態查詢失敗: {response.status_code}")
                break
                
        except Exception as e:
            print(f"❌ 狀態查詢 API 錯誤: {e}")
            break
    else:
        print("⏰ 輪詢超時，但這可能是正常的（處理時間較長）")
    
    # 4. 測試前端 API 服務
    print("\n4. 測試前端服務...")
    try:
        response = requests.get("http://localhost:5173/")
        if response.status_code == 200:
            print("✅ 前端服務正常運行")
        else:
            print(f"❌ 前端服務異常: {response.status_code}")
    except Exception as e:
        print(f"❌ 前端服務連接失敗: {e}")
    
    print("\n🎉 整合測試完成！")
    return True

def test_api_endpoints():
    """測試所有 API 端點"""
    
    base_url = "http://localhost:8001"
    
    print("\n🔍 測試所有 API 端點")
    print("=" * 50)
    
    endpoints = [
        ("GET", "/", "根端點"),
        ("GET", "/ppt/seminars", "研討會列表"),
        ("GET", "/data/sessions?limit=5", "會議資料"),
    ]
    
    for method, endpoint, description in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}")
            
            if response.status_code == 200:
                print(f"✅ {description}: {endpoint}")
            else:
                print(f"❌ {description}: {endpoint} - {response.status_code}")
                
        except Exception as e:
            print(f"❌ {description}: {endpoint} - 錯誤: {e}")

def main():
    """主函數"""
    print("🚀 前端後端整合測試")
    print("=" * 60)
    
    # 測試 API 端點
    test_api_endpoints()
    
    # 測試 PPT 上傳整合
    test_ppt_upload_integration()
    
    print("\n📋 測試建議:")
    print("1. 如果上傳成功但前端顯示失敗，檢查前端輪詢邏輯")
    print("2. 如果處理時間過長，這是正常的（Gemini API 需要時間）")
    print("3. 檢查瀏覽器控制台的詳細錯誤信息")
    print("4. 確保檔案名稱與 BigQuery 中的會議記錄匹配")

if __name__ == "__main__":
    main()
