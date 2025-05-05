#!/usr/bin/env python3
"""
批量會議逐字稿總結工具 - 處理整個資料夾的逐字稿 (多線程版本)
"""

import os
import argparse
import time
import concurrent.futures
from pathlib import Path

from config.config import (
    DEFAULT_INPUT_DIR, DEFAULT_OUTPUT_DIR, DEFAULT_OUTPUT_FORMAT,
    DEFAULT_WORKERS, SUPPORTED_FILE_EXTENSIONS, MAX_REQUESTS_PER_MINUTE
)
from src.utils.logging_utils import logger
from src.utils.file_utils import get_files_by_extensions, normalize_filename
from src.models.summarizer import TranscriptSummarizer

def process_file(file_info):
    """處理單個逐字稿文件"""
    file_path, output_dir, output_format, total_files, file_index = file_info
    summarizer = TranscriptSummarizer()
    logger.info(f"處理 ({file_index + 1}/{total_files}): {file_path.name}")
    
    # 處理摘要
    result = summarizer.process_transcript(
        file_path=file_path,
        output_dir=output_dir,
        output_format=output_format
    )
    
    return result

def display_progress(completed, failed, total_files, start_time):
    """顯示進度"""
    elapsed = time.time() - start_time
    progress = (completed + failed) / total_files * 100
    logger.info(f"進度: {progress:.1f}% ({completed + failed}/{total_files}), "
               f"已完成: {completed}, 失敗: {failed}, 已用時間: {elapsed:.1f}秒")

def process_directory(input_dir, output_dir, output_format, max_workers):
    """使用多線程處理指定目錄中的所有逐字稿文件"""
    os.makedirs(output_dir, exist_ok=True)
    transcript_files = get_files_by_extensions(input_dir, SUPPORTED_FILE_EXTENSIONS)

    if not transcript_files:
        logger.warning(f"在 {input_dir} 中未找到任何文本文件")
        return

    total_files = len(transcript_files)
    # 根據 API 限制調整線程數
    max_workers = min(max_workers, MAX_REQUESTS_PER_MINUTE // 4) or 1
    logger.info(f"找到 {total_files} 個逐字稿文件，將使用 {max_workers} 個線程並行處理")

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
        logger.warning("\n程序被用戶中斷。正在等待當前任務完成...")
    except Exception as e:
        logger.error(f"執行過程中發生錯誤: {e}")

    logger.info(f"批量處理完成。成功: {completed}, 失敗: {failed}")
    logger.info(f"總耗時: {time.time() - start_time:.2f} 秒")
    logger.info(f"總結文件保存在: {output_dir}")

def main():
    parser = argparse.ArgumentParser(description="批量處理會議逐字稿並生成總結 (多線程版本)")
    parser.add_argument("-i", "--input", default=DEFAULT_INPUT_DIR, help="輸入目錄")
    parser.add_argument("-o", "--output", default=DEFAULT_OUTPUT_DIR, help="輸出目錄")
    parser.add_argument("--format", choices=["json", "txt", "md"], default=DEFAULT_OUTPUT_FORMAT, help="輸出格式")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="最大工作線程數")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        logger.error(f"錯誤: 輸入目錄 {args.input} 不存在")
        return 1

    process_directory(args.input, args.output, args.format, args.workers)
    return 0

if __name__ == "__main__":
    exit(main())