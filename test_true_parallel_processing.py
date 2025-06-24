#!/usr/bin/env python3
"""
測試真正的並行處理功能
"""

import requests
import time
import json
from datetime import datetime

def create_test_pdf(filename, content_text):
    """創建測試 PDF 內容"""
    return f"""%PDF-1.4
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
/Length {len(content_text) + 100}
>>
stream
BT
/F1 12 Tf
72 720 Td
({content_text}) Tj
0 -20 Td
(Test file: {filename}) Tj
0 -20 Td
(True parallel processing test) Tj
0 -20 Td
(Created at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}) Tj
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
{len(content_text) + 500}
%%EOF""".encode('utf-8')

def test_true_parallel_processing():
    """測試真正的並行處理功能"""
    
    base_url = "http://localhost:8001"
    
    print("🚀 測試真正的並行處理功能")
    print("=" * 60)
    
    # 創建多個測試檔案，使用真實的會議名稱
    test_files = [
        ("从碎片到统一：如何用元数据湖解决多 Lakehouse 治理难题.pdf", "从碎片到统一：如何用元数据湖解决多 Lakehouse 治理难题"),
        ("可觀測性的新探索：eBPF技術在小紅書的大規模實踐.pdf", "可觀測性的新探索：eBPF技術在小紅書的大規模實踐"),
        ("打造研發交付的"黃金鍊路" —— 標準研發模式驅動平臺工程規模化應用.pdf", "打造研發交付的黃金鍊路標準研發模式驅動平臺工程規模化應用"),
    ]
    
    print(f"1. 準備上傳 {len(test_files)} 個測試檔案...")
    print("檔案列表:")
    for i, (filename, _) in enumerate(test_files, 1):
        print(f"  {i}. {filename}")
    
    # 準備檔案數據
    files_data = []
    for filename, content in test_files:
        pdf_content = create_test_pdf(filename, content)
        files_data.append(('files', (filename, pdf_content, 'application/pdf')))
    
    data = {'seminar': '202503 QCon Beijing'}
    
    try:
        print(f"\n2. 開始上傳檔案... ({datetime.now().strftime('%H:%M:%S')})")
        start_time = time.time()
        
        response = requests.post(f"{base_url}/ppt/upload", files=files_data, data=data, timeout=180)
        
        upload_time = time.time() - start_time
        print(f"上傳耗時: {upload_time:.2f} 秒")
        
        if response.status_code == 200:
            upload_result = response.json()
            task_id = upload_result['task_id']
            print(f"✅ 上傳成功，任務ID: {task_id}")
            print(f"檔案數量: {upload_result['files_count']}")
            
            # 監控真正的並行處理進度
            print(f"\n3. 監控並行處理進度...")
            print("時間     | 狀態      | 進度 | 訊息")
            print("-" * 80)
            
            processing_start_times = {}
            processing_end_times = {}
            
            max_polls = 60
            for i in range(max_polls):
                try:
                    status_response = requests.get(f"{base_url}/ppt/status/{task_id}", timeout=15)
                    
                    if status_response.status_code == 200:
                        status = status_response.json()
                        current_time = time.strftime('%H:%M:%S')
                        
                        print(f"{current_time} | {status['status']:9s} | {status['progress']:3d}% | {status['message']}")
                        
                        # 追蹤每個檔案的處理時間
                        if status.get('files'):
                            parallel_count = 0
                            for file_info in status['files']:
                                filename = file_info['filename']
                                file_status = file_info['status']
                                file_progress = file_info['progress']
                                
                                # 記錄開始處理時間
                                if file_status == 'processing' and filename not in processing_start_times:
                                    processing_start_times[filename] = time.time()
                                    print(f"  🚀 {filename} 開始處理")
                                
                                # 記錄完成時間
                                if file_status in ['success', 'error'] and filename not in processing_end_times:
                                    processing_end_times[filename] = time.time()
                                    if filename in processing_start_times:
                                        duration = processing_end_times[filename] - processing_start_times[filename]
                                        status_icon = "✅" if file_status == 'success' else "❌"
                                        print(f"  {status_icon} {filename} 處理完成 (耗時: {duration:.1f}秒)")
                                
                                # 計算並行處理的檔案數量
                                if file_status == 'processing':
                                    parallel_count += 1
                            
                            if parallel_count > 1:
                                print(f"  🔥 並行處理中: {parallel_count} 個檔案同時進行")
                        
                        if status['status'] == 'success':
                            print("🎉 並行處理成功完成！")
                            result = status.get('result', {})
                            print(f"總計: {result.get('total', 0)}")
                            print(f"成功: {result.get('success', 0)}")
                            print(f"失敗: {result.get('failed', 0)}")
                            
                            # 分析並行處理效果
                            analyze_parallel_performance(processing_start_times, processing_end_times)
                            break
                            
                        elif status['status'] == 'error':
                            print(f"❌ 並行處理失敗: {status.get('error', '未知錯誤')}")
                            break
                            
                        elif status['status'] in ['pending', 'processing']:
                            time.sleep(3)  # 每3秒查詢一次
                            
                    else:
                        print(f"❌ 狀態查詢失敗: {status_response.status_code}")
                        break
                        
                except Exception as e:
                    print(f"❌ 狀態查詢錯誤: {e}")
                    time.sleep(3)
            else:
                print("⏰ 監控超時，但處理可能仍在進行中")
            
        else:
            print(f"❌ 上傳失敗: {response.status_code}")
            print(f"響應: {response.text}")
            
    except Exception as e:
        print(f"❌ 測試失敗: {e}")

def analyze_parallel_performance(start_times, end_times):
    """分析並行處理性能"""
    
    print(f"\n📊 並行處理性能分析")
    print("=" * 60)
    
    if not start_times or not end_times:
        print("❌ 沒有足夠的時間數據進行分析")
        return
    
    # 計算每個檔案的處理時間
    processing_times = {}
    for filename in start_times:
        if filename in end_times:
            processing_times[filename] = end_times[filename] - start_times[filename]
    
    if not processing_times:
        print("❌ 沒有完整的處理時間數據")
        return
    
    print("各檔案處理時間:")
    total_individual_time = 0
    for filename, duration in processing_times.items():
        print(f"  - {filename}: {duration:.1f} 秒")
        total_individual_time += duration
    
    # 計算總體處理時間
    overall_start = min(start_times.values())
    overall_end = max(end_times.values())
    total_parallel_time = overall_end - overall_start
    
    print(f"\n時間統計:")
    print(f"  順序處理預估時間: {total_individual_time:.1f} 秒")
    print(f"  並行處理實際時間: {total_parallel_time:.1f} 秒")
    
    if total_individual_time > 0:
        speedup = total_individual_time / total_parallel_time
        efficiency = (speedup / len(processing_times)) * 100
        print(f"  加速比: {speedup:.2f}x")
        print(f"  並行效率: {efficiency:.1f}%")
        
        if speedup > 1.5:
            print("  🎉 並行處理效果顯著！")
        elif speedup > 1.1:
            print("  ✅ 並行處理有效果")
        else:
            print("  ⚠️ 並行處理效果不明顯")

def main():
    """主函數"""
    print("🧪 真正的並行處理功能測試")
    print("=" * 70)
    
    # 測試真正的並行處理
    test_true_parallel_processing()
    
    print("\n💡 並行處理改進總結:")
    print("1. 使用 ThreadPoolExecutor 執行阻塞的 Gemini API 調用")
    print("2. 使用 asyncio.gather 真正並行執行多個檔案")
    print("3. 每個檔案獨立處理，錯誤隔離")
    print("4. 實時監控並行處理狀態")
    print("5. 性能分析和加速比計算")

if __name__ == "__main__":
    main()
