#!/usr/bin/env python3
"""
調試上傳問題的腳本
"""

import requests
import time
import json

def debug_upload_issue():
    """調試上傳問題"""
    
    base_url = "http://localhost:8001"
    
    print("🔍 調試 PPT 上傳問題")
    print("=" * 50)
    
    # 1. 檢查服務狀態
    print("1. 檢查後端服務狀態...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ 後端服務正常")
        else:
            print(f"❌ 後端服務異常: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ 無法連接後端服務: {e}")
        return
    
    # 2. 檢查現有任務
    print("\n2. 檢查現有任務狀態...")
    try:
        response = requests.get(f"{base_url}/ppt/debug/tasks")
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ 總任務數: {tasks['total_tasks']}")
            
            if tasks['tasks']:
                print("現有任務:")
                for task_id, task_info in tasks['tasks'].items():
                    print(f"  - {task_id}: {task_info['status']} ({task_info['progress']}%)")
                    if task_info['message']:
                        print(f"    訊息: {task_info['message']}")
                    if task_info['error']:
                        print(f"    錯誤: {task_info['error']}")
            else:
                print("沒有現有任務")
        else:
            print(f"❌ 無法獲取任務狀態: {response.status_code}")
    except Exception as e:
        print(f"❌ 檢查任務狀態失敗: {e}")
    
    # 3. 測試檔案名稱匹配
    print("\n3. 測試檔案名稱匹配...")
    filename = "大模型安全挑戰與實踐：構建 AI 時代的安全防線"
    
    try:
        # 檢查研討會
        response = requests.get(f"{base_url}/ppt/seminars")
        if response.status_code == 200:
            seminars = response.json()['seminars']
            print(f"可用研討會: {[s['name'] for s in seminars]}")
            
            # 檢查會議匹配
            for seminar in seminars:
                print(f"\n檢查 {seminar['name']} 中的匹配會議:")
                
                # 搜尋包含關鍵字的會議
                response = requests.get(f"{base_url}/data/sessions", params={
                    'seminar': seminar['name'],
                    'limit': 100
                })
                
                if response.status_code == 200:
                    sessions = response.json()['sessions']
                    print(f"  總會議數: {len(sessions)}")
                    
                    # 檢查是否有匹配的會議
                    keywords = ['大模型', '安全', '挑戰', '實踐', 'AI', '防線']
                    matches = []
                    
                    for session in sessions:
                        for keyword in keywords:
                            if keyword in session['name']:
                                matches.append(session)
                                break
                    
                    if matches:
                        print(f"  找到 {len(matches)} 個可能匹配的會議:")
                        for match in matches[:5]:  # 只顯示前5個
                            print(f"    - {match['name']}")
                    else:
                        print("  沒有找到匹配的會議")
                else:
                    print(f"  ❌ 無法獲取會議列表: {response.status_code}")
        else:
            print(f"❌ 無法獲取研討會列表: {response.status_code}")
    except Exception as e:
        print(f"❌ 檢查檔案匹配失敗: {e}")
    
    # 4. 模擬上傳測試
    print("\n4. 模擬上傳測試...")
    
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
/Length 200
>>
stream
BT
/F1 12 Tf
72 720 Td
(大模型安全挑戰與實踐：構建 AI 時代的安全防線) Tj
0 -20 Td
(Large Model Security Challenges and Practices) Tj
0 -20 Td
(Building AI Era Security Defense) Tj
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
450
%%EOF"""
    
    try:
        files = {'files': ('大模型安全挑戰與實踐：構建 AI 時代的安全防線.pdf', test_content, 'application/pdf')}
        data = {'seminar': '202503 QCon Beijing'}  # 假設使用這個研討會
        
        print("正在上傳測試檔案...")
        response = requests.post(f"{base_url}/ppt/upload", files=files, data=data)
        
        if response.status_code == 200:
            upload_result = response.json()
            task_id = upload_result['task_id']
            print(f"✅ 上傳成功，任務ID: {task_id}")
            
            # 立即檢查任務狀態
            print("\n5. 檢查任務狀態...")
            for i in range(5):
                time.sleep(2)
                try:
                    status_response = requests.get(f"{base_url}/ppt/status/{task_id}")
                    if status_response.status_code == 200:
                        status = status_response.json()
                        print(f"  檢查 {i+1}: {status['status']} - {status['progress']}% - {status['message']}")
                        
                        if status['status'] in ['success', 'error']:
                            break
                    else:
                        print(f"  檢查 {i+1}: HTTP {status_response.status_code}")
                except Exception as e:
                    print(f"  檢查 {i+1}: 錯誤 - {e}")
            
        else:
            print(f"❌ 上傳失敗: {response.status_code}")
            print(f"響應: {response.text}")
            
    except Exception as e:
        print(f"❌ 模擬上傳失敗: {e}")
    
    print("\n🎯 調試建議:")
    print("1. 檢查瀏覽器開發者工具的 Network 標籤")
    print("2. 查看 Console 標籤的詳細錯誤信息")
    print("3. 確認檔案名稱是否能匹配到會議記錄")
    print("4. 檢查後端日誌的詳細處理過程")

def main():
    """主函數"""
    debug_upload_issue()

if __name__ == "__main__":
    main()
