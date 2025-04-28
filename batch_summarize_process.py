#!/usr/bin/env python3
"""
批量會議逐字稿總結工具 - 處理整個資料夾的逐字稿 (多線程版本)
"""

import os
import argparse
import time
from pathlib import Path
from src.transcript_summarizer import TranscriptSummarizer
import concurrent.futures
import threading
from datetime import datetime, timedelta

# 常量配置
MAX_REQUESTS_PER_MINUTE = 15  # Gemini API 限制: 15 RPM
DEFAULT_INPUT_DIR = "/Users/cfh00896102/Github/google_next/data/test"
DEFAULT_OUTPUT_DIR = "/Users/cfh00896102/Github/google_next/summaries"
DEFAULT_OUTPUT_FORMAT = "md"
DEFAULT_WORKERS = 4
SUPPORTED_FILE_EXTENSIONS = ['.txt', '.md', '.text']

# 鎖對象
print_lock = threading.Lock()
api_counter_lock = threading.Lock()

# API 請求追蹤
api_requests = []

def safe_print(*args, **kwargs):
    """線程安全的打印函數"""
    with print_lock:
        print(*args, **kwargs)

def wait_for_api_quota():
    """等待 API 配額可用，確保每分鐘不超過 MAX_REQUESTS_PER_MINUTE 個請求"""
    current_time = datetime.now()
    with api_counter_lock:
        one_minute_ago = current_time - timedelta(minutes=1)
        api_requests[:] = [req for req in api_requests if req >= one_minute_ago]

        if len(api_requests) >= MAX_REQUESTS_PER_MINUTE:
            wait_time = (api_requests[0] + timedelta(minutes=1) - current_time).total_seconds()
            safe_print(f"API 請求達到限制，等待 {wait_time:.2f} 秒...")
            time.sleep(wait_time + 0.5)  # 額外等待 0.5 秒作為緩衝
            return wait_for_api_quota()
        
        api_requests.append(current_time)
        return True

def read_transcript(file_path):
    """讀取逐字稿文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        safe_print(f"讀取文件 {file_path.name} 時出錯: {e}")
        return None

def save_summary(summarizer, summary, output_path, output_format, file_path):
    """保存總結到指定格式的文件"""
    try:
        if output_format == "json":
            summarizer.save_summary(summary, output_path)
        else:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(summary["summary"])
            safe_print(f"總結已保存到: {output_path}")
            save_html_summary(summarizer, summary, file_path)
    except Exception as e:
        safe_print(f"保存總結 {output_path} 時出錯: {e}")
        return False
    return True

def save_html_summary(summarizer, summary, file_path):
    """保存 HTML 格式的總結"""
    html_dir = os.path.join(DEFAULT_OUTPUT_DIR, "session")
    os.makedirs(html_dir, exist_ok=True)
    html_output_path = os.path.join(html_dir, file_path.stem + "_summary.html")
    meeting_title = file_path.stem.replace("_", " ").title()
    summarizer.save_email_html(summary, html_output_path, meeting_title)
    safe_print(f"HTML格式總結已保存到: {html_output_path}")

def process_file(file_info):
    """處理單個逐字稿文件"""
    file_path, output_dir, output_format, total_files, file_index = file_info
    summarizer = TranscriptSummarizer()
    safe_print(f"處理 ({file_index + 1}/{total_files}): {file_path.name}")
    
    transcript_text = read_transcript(file_path)
    if not transcript_text:
        return False

    if not wait_for_api_quota():
        safe_print(f"無法獲取 API 配額，跳過處理 {file_path.name}")
        return False

    summary = None
    for retry_count in range(3):
        try:
            print(file_path.name)
            summary = summarizer.summarize(transcript_text, file_path.name[:-4])
            break
        except Exception as e:
            safe_print(f"生成總結時出錯 (嘗試 {retry_count + 1}/3): {e}")
            time.sleep(5 * (retry_count + 1))
    
    if not summary:
        safe_print(f"無法為 {file_path.name} 生成總結，跳過")
        return False

    output_filename = file_path.stem + f"_summary.{output_format}"
    format_dir = os.path.join(output_dir, output_format)
    os.makedirs(format_dir, exist_ok=True)
    output_path = os.path.join(format_dir, output_filename)
    return save_summary(summarizer, summary, output_path, output_format, file_path)

def display_progress(completed, failed, total_files, start_time):
    """顯示進度"""
    elapsed = time.time() - start_time
    progress = (completed + failed) / total_files * 100
    safe_print(f"進度: {progress:.1f}% ({completed + failed}/{total_files}), "
               f"已完成: {completed}, 失敗: {failed}, 已用時間: {elapsed:.1f}秒")

def process_directory(input_dir, output_dir, output_format, max_workers):
    """使用多線程處理指定目錄中的所有逐字稿文件"""
    os.makedirs(output_dir, exist_ok=True)
    transcript_files = [file for ext in SUPPORTED_FILE_EXTENSIONS 
                        for file in Path(input_dir).glob(f'*{ext}')]

    if not transcript_files:
        print(f"在 {input_dir} 中未找到任何文本文件")
        return

    total_files = len(transcript_files)
    max_workers = min(max_workers, MAX_REQUESTS_PER_MINUTE // 4) or 1
    safe_print(f"找到 {total_files} 個逐字稿文件，將使用 {max_workers} 個線程並行處理")

    tasks = [(file_path, output_dir, output_format, total_files, i) 
             for i, file_path in enumerate(transcript_files)]

    start_time = time.time()
    completed, failed = 0, 0

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_file, task): task[0].name for task in tasks}
            for future in concurrent.futures.as_completed(futures):
                if future.result():
                    completed += 1
                else:
                    failed += 1
                display_progress(completed, failed, total_files, start_time)
    except KeyboardInterrupt:
        safe_print("\n程序被用戶中斷。正在等待當前任務完成...")
    except Exception as e:
        safe_print(f"執行過程中發生錯誤: {e}")

    safe_print(f"批量處理完成。成功: {completed}, 失敗: {failed}")
    safe_print(f"總耗時: {time.time() - start_time:.2f} 秒")
    safe_print(f"總結文件保存在: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="批量處理會議逐字稿並生成總結 (多線程版本)")
    parser.add_argument("-i", "--input", default=DEFAULT_INPUT_DIR, help="輸入目錄")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR, help="輸出目錄")
    parser.add_argument("--format", choices=["json", "txt", "md"], default=DEFAULT_OUTPUT_FORMAT, help="輸出格式")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="最大工作線程數")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        safe_print(f"錯誤: 輸入目錄 {args.input} 不存在")
        return 1

    process_directory(args.input, args.output, args.format, args.workers)
    return 0

if __name__ == "__main__":
    exit(main())