#!/usr/bin/env python3
"""
測試延長的超時設置
"""

import requests
import time
import json

def test_extended_timeout():
    """測試延長的超時設置"""
    
    base_url = "http://localhost:8001"
    
    print("🕐 測試延長的超時設置")
    print("=" * 50)
    
    # 創建測試檔案 - 使用真實的檔案名稱
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
/Length 300
>>
stream
BT
/F1 12 Tf
72 720 Td
(大模型驅動安全升級：騰訊代碼安全應用實踐) Tj
0 -20 Td
(Large Model Driven Security Upgrade) Tj
0 -20 Td
(Tencent Code Security Application Practice) Tj
0 -40 Td
(這是一個測試 PPT 內容，用來驗證延長的超時設置) Tj
0 -20 Td
(包含多行內容以模擬真實的 PPT 檔案) Tj
0 -20 Td
(測試 Gemini API 的處理時間) Tj
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
550
%%EOF"""
    
    try:
        files = {'files': ('大模型驅動安全升級：騰訊代碼安全應用實踐.pdf', test_content, 'application/pdf')}
        data = {'seminar': '202503 QCon Beijing'}
        
        print("1. 上傳測試檔案...")
        response = requests.post(f"{base_url}/ppt/upload", files=files, data=data)
        
        if response.status_code == 200:
            upload_result = response.json()
            task_id = upload_result['task_id']
            print(f"✅ 上傳成功，任務ID: {task_id}")
            
            # 模擬前端的延長輪詢
            print("\n2. 開始延長輪詢測試...")
            print("前端新設置:")
            print("- 最大輪詢次數: 200 次")
            print("- 前30次間隔: 3秒")
            print("- 後續間隔: 5秒")
            print("- 總超時時間: 約10分鐘")
            print()
            
            max_polls = 20  # 測試用，只輪詢20次
            
            for i in range(max_polls):
                try:
                    # 模擬前端的動態間隔
                    poll_interval = 3 if i < 10 else 5
                    
                    status_response = requests.get(f"{base_url}/ppt/status/{task_id}")
                    
                    if status_response.status_code == 200:
                        status = status_response.json()
                        elapsed_time = (i + 1) * poll_interval
                        
                        print(f"輪詢 {i+1:2d}/{max_polls}: {status['status']:10s} - {status['progress']:3d}% - 已等待 {elapsed_time:3d}秒 - {status['message']}")
                        
                        if status['status'] == 'success':
                            print("🎉 處理成功完成！")
                            result = status.get('result', {})
                            print(f"   總計: {result.get('total', 0)}")
                            print(f"   成功: {result.get('success', 0)}")
                            print(f"   失敗: {result.get('failed', 0)}")
                            break
                            
                        elif status['status'] == 'error':
                            print(f"❌ 處理失敗: {status.get('error', '未知錯誤')}")
                            break
                            
                        elif status['status'] in ['pending', 'processing']:
                            print(f"   ⏳ 繼續等待，{poll_interval}秒後再次查詢...")
                            time.sleep(poll_interval)
                            
                    else:
                        print(f"❌ 狀態查詢失敗: {status_response.status_code}")
                        time.sleep(poll_interval)
                        
                except Exception as e:
                    print(f"❌ 輪詢錯誤: {e}")
                    time.sleep(poll_interval)
            else:
                print("⏰ 測試輪詢完成（實際前端會繼續輪詢到200次）")
            
        else:
            print(f"❌ 上傳失敗: {response.status_code}")
            print(f"響應: {response.text}")
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
    
    print("\n📊 新的超時設置總結:")
    print("- 前30次輪詢: 30 × 3秒 = 90秒 (1.5分鐘)")
    print("- 後170次輪詢: 170 × 5秒 = 850秒 (14.2分鐘)")
    print("- 總超時時間: 940秒 ≈ 15.7分鐘")
    print()
    print("這應該足夠處理最複雜的 PPT 檔案！")

def test_current_tasks():
    """檢查當前任務狀態"""
    
    base_url = "http://localhost:8001"
    
    print("\n🔍 檢查當前任務狀態")
    print("=" * 50)
    
    try:
        response = requests.get(f"{base_url}/ppt/debug/tasks")
        if response.status_code == 200:
            tasks = response.json()
            print(f"總任務數: {tasks['total_tasks']}")
            
            if tasks['tasks']:
                print("\n當前任務:")
                for task_id, task_info in tasks['tasks'].items():
                    print(f"任務 ID: {task_id}")
                    print(f"  狀態: {task_info['status']}")
                    print(f"  進度: {task_info['progress']}%")
                    print(f"  訊息: {task_info['message']}")
                    if task_info['error']:
                        print(f"  錯誤: {task_info['error']}")
                    print()
            else:
                print("沒有當前任務")
        else:
            print(f"❌ 無法獲取任務狀態: {response.status_code}")
    except Exception as e:
        print(f"❌ 檢查任務狀態失敗: {e}")

def main():
    """主函數"""
    print("🚀 延長超時設置測試")
    print("=" * 60)
    
    # 檢查當前任務
    test_current_tasks()
    
    # 測試延長超時
    test_extended_timeout()
    
    print("\n💡 使用建議:")
    print("1. PPT 處理現在有充足的時間（最多15.7分鐘）")
    print("2. 前端會顯示處理進度和等待提示")
    print("3. 如果仍然超時，可能是檔案無法匹配或內容提取失敗")
    print("4. 可以在資料庫管理頁面查看最終結果")

if __name__ == "__main__":
    main()
