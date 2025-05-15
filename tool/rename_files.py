import os
import sys
import argparse
from pathlib import Path
import re

def normalize(title):
    title = re.sub(r'[\\/“:_*?"<>|]', '', title)
    title = title.strip()
    return title

def rename_files(directory, prefix_length=4, file_extension='.txt', dry_run=False):
    """
    讀取指定目錄下的所有指定擴展名文件，將文件名前綴刪除
    
    Args:
        directory (str): 要處理的目錄路徑
        prefix_length (int): 要刪除的前綴長度
        file_extension (str): 要處理的文件擴展名
        dry_run (bool): 如果為True，只顯示將要進行的更改而不實際執行
    """
    # 確保目錄存在
    directory_path = Path(directory)
    if not directory_path.is_dir():
        print(f"錯誤：目錄 '{directory}' 不存在")
        return
    
    # 計數器
    renamed_count = 0
    error_count = 0
    skipped_count = 0
    
    # 遍歷目錄中的所有文件
    for file_path in directory_path.glob(f'*{file_extension}'):
        filename = file_path.name
        
        # 檢查文件名長度是否大於指定前綴長度
        if len(filename) > prefix_length:
            new_filename = normalize(filename[prefix_length:])
            new_path = file_path.parent / new_filename
            
            # 檢查新文件名是否已存在
            if new_path.exists():
                print(f"跳過 '{filename}': 目標文件名 '{new_filename}' 已存在")
                error_count += 1
                continue
                
            try:
                if not dry_run:
                    # 重命名文件
                    file_path.rename(new_path)
                action = "將重命名" if dry_run else "已重命名"
                # print(f"{action}: {filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"重命名 '{filename}' 時出錯: {str(e)}")
                error_count += 1
        else:
            print(f"跳過 '{filename}': 文件名長度不足{prefix_length}個字符")
            skipped_count += 1
    
    # 輸出統計信息
    print(f"\n處理完成！")
    if dry_run:
        print(f"預計重命名: {renamed_count} 個文件")
    else:
        print(f"成功重命名: {renamed_count} 個文件")
    print(f"處理失敗: {error_count} 個文件")
    print(f"跳過處理: {skipped_count} 個文件")

def main():
    # 創建命令行參數解析器
    parser = argparse.ArgumentParser(description='批量重命名文件，刪除文件名前綴')
    parser.add_argument('directory', nargs='?', default='.', 
                        help='要處理的目錄路徑（默認為當前目錄）')
    parser.add_argument('-l', '--length', type=int, default=4,
                        help='要刪除的前綴長度（默認為4）')
    parser.add_argument('-e', '--extension', default='.txt',
                        help='要處理的文件擴展名（默認為.txt）')
    parser.add_argument('-d', '--dry-run', action='store_true',
                        help='預覽模式，只顯示將要進行的更改而不實際執行')
    
    # 解析命令行參數
    args = parser.parse_args()
    
    # 如果沒有提供目錄參數且在交互模式下運行
    if args.directory == '.' and sys.stdin.isatty():
        directory = input("請輸入要處理的目錄路徑（默認為當前目錄）: ") or "."
    else:
        directory = args.directory
    
    # 執行重命名操作
    rename_files(directory, args.length, args.extension, args.dry_run)

if __name__ == "__main__":
    main()