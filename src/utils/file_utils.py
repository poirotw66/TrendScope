import os
from pathlib import Path
from src.utils.logging_utils import logger

def read_file(file_path, encoding='utf-8'):
    """安全讀取檔案內容"""
    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.read()
    except Exception as e:
        logger.error(f"讀取檔案 {Path(file_path).name} 時出錯: {e}")
        return None

def write_file(content, file_path, encoding='utf-8'):
    """安全寫入檔案內容"""
    try:
        # 確保目錄存在
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)
        logger.info(f"檔案已保存: {file_path}")
        return True
    except Exception as e:
        logger.error(f"寫入檔案 {file_path} 時出錯: {e}")
        return False

def get_files_by_extensions(directory, extensions):
    """取得指定目錄中符合副檔名的所有檔案"""
    files = []
    for ext in extensions:
        files.extend(Path(directory).glob(f'*{ext}'))
    return files

def normalize_filename(title):
    """標準化檔名，移除不合法字元"""
    import re
    # 移除不合法字元，只保留中英文、數字、底線、減號
    title = re.sub(r'[\\/:*?"<>|]', '', title)
    return title.strip()