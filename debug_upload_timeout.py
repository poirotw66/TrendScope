#!/usr/bin/env python3
"""
調試上傳超時問題
"""

import requests
import time
import json

def test_upload_timeout():
    """測試上傳超時問題"""
    
    base_url = "http://localhost:8001"
    
    print("🔍 調試上傳超時問題")
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
(小米資源畫像體系構建與業務實踐) Tj
0 -20 Td
(Xiaomi Resource Portrait System Construction) Tj
0 -20 Td
(and Business Practice) Tj
0 -40 Td
(這是一個測試 PPT 內容，用來調試上傳超時問題) Tj
0 -20 Td
(包含多行內容以模擬真實的 PPT 檔案) Tj
0 -20 Td
(測試前端和後端的超時處理) Tj
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
    
    print("1. 測試上傳請求的響應時間...")
    
    try:
        files = {'files': ('小米資源畫像體系構建與業務實踐.pdf', test_content, 'application/pdf')}
        data = {'seminar': '202503 QCon Beijing'}
        
        start_time = time.time()
        print(f"開始上傳: {time.strftime('%H:%M:%S')}")
        
        # 設置較長的超時時間來測試
        response = requests.post(f"{base_url}/ppt/upload", files=files, data=data, timeout=180)
        
        end_time = time.time()
        upload_duration = end_time - start_time
        
        print(f"上傳完成: {time.strftime('%H:%M:%S')}")
        print(f"上傳耗時: {upload_duration:.2f} 秒")
        
        if response.status_code == 200:
            upload_result = response.json()
            task_id = upload_result['task_id']
            print(f"✅ 上傳成功，任務ID: {task_id}")
            print(f"響應訊息: {upload_result['message']}")
            print(f"檔案數量: {upload_result['files_count']}")
            
            # 立即檢查任務狀態
            print(f"\n2. 立即檢查任務狀態...")
            try:
                status_response = requests.get(f"{base_url}/ppt/status/{task_id}", timeout=15)
                if status_response.status_code == 200:
                    status = status_response.json()
                    print(f"✅ 任務狀態: {status['status']} - {status['progress']}%")
                    print(f"任務訊息: {status['message']}")
                else:
                    print(f"❌ 狀態查詢失敗: {status_response.status_code}")
            except Exception as e:
                print(f"❌ 狀態查詢錯誤: {e}")
            
        else:
            print(f"❌ 上傳失敗: {response.status_code}")
            print(f"響應內容: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"❌ 上傳請求超時（超過180秒）")
        print("這表明後端處理檔案保存的時間過長")
    except requests.exceptions.ConnectionError:
        print(f"❌ 連接錯誤，無法連接到後端服務")
    except Exception as e:
        print(f"❌ 上傳錯誤: {e}")

def test_frontend_timeout_settings():
    """測試前端超時設置"""
    
    print("\n3. 分析前端超時設置...")
    print("=" * 50)
    
    print("前端 axios 超時設置:")
    print("- 默認超時: 60秒 (剛修改)")
    print("- PPT 上傳超時: 120秒 (剛修改)")
    print("- 狀態查詢超時: 15秒 (剛修改)")
    print()
    
    print("可能的超時原因:")
    print("1. 檔案保存時間過長（後端）")
    print("2. 網絡傳輸時間過長")
    print("3. 前端 axios 配置問題")
    print("4. 瀏覽器請求限制")

def test_backend_file_processing():
    """測試後端檔案處理時間"""
    
    print("\n4. 測試後端檔案處理時間...")
    print("=" * 50)
    
    # 創建不同大小的測試檔案
    sizes = [
        ("小檔案", 1024),      # 1KB
        ("中檔案", 1024*100),  # 100KB  
        ("大檔案", 1024*1000), # 1MB
    ]
    
    base_url = "http://localhost:8001"
    
    for name, size in sizes:
        print(f"\n測試 {name} ({size} bytes):")
        
        # 創建指定大小的 PDF 內容
        content = b"""%PDF-1.4
1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R>>endobj
4 0 obj<</Length """ + str(size - 200).encode() + b""">>stream
BT/F1 12 Tf 72 720 Td(""" + b"A" * (size - 300) + b""")Tj ET
endstream endobj
xref 0 5
0000000000 65535 f 
trailer<</Size 5/Root 1 0 R>>startxref """ + str(size - 50).encode() + b""" %%EOF"""
        
        try:
            files = {'files': (f'test_{name}.pdf', content, 'application/pdf')}
            data = {'seminar': '202503 QCon Beijing'}
            
            start_time = time.time()
            response = requests.post(f"{base_url}/ppt/upload", files=files, data=data, timeout=60)
            end_time = time.time()
            
            duration = end_time - start_time
            print(f"  上傳耗時: {duration:.2f} 秒")
            
            if response.status_code == 200:
                print(f"  ✅ 成功")
            else:
                print(f"  ❌ 失敗: {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"  ❌ 超時（超過60秒）")
        except Exception as e:
            print(f"  ❌ 錯誤: {e}")

def main():
    """主函數"""
    print("🚀 上傳超時問題調試")
    print("=" * 60)
    
    # 測試上傳超時
    test_upload_timeout()
    
    # 分析前端設置
    test_frontend_timeout_settings()
    
    # 測試後端處理
    test_backend_file_processing()
    
    print("\n📋 調試結論:")
    print("1. 如果上傳請求本身超時，問題在後端檔案保存")
    print("2. 如果上傳成功但前端顯示失敗，問題在前端錯誤處理")
    print("3. 如果狀態查詢失敗，問題在網絡或後端狀態管理")
    print("4. 檢查瀏覽器開發者工具的 Network 標籤獲取詳細信息")

if __name__ == "__main__":
    main()
