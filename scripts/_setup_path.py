"""
腳本路徑設置輔助模組
用於腳本檔案中確保專案路徑正確設置，以便使用標準導入

使用方式：
    from scripts._setup_path import setup_path
    setup_path()
    
或者直接導入：
    from scripts._setup_path import project_root
"""
import sys
from pathlib import Path

# 計算專案根目錄（scripts/ 的上一層）
_project_root = Path(__file__).resolve().parent.parent

def setup_path():
    """
    將專案根目錄添加到 sys.path（如果尚未存在）
    這樣腳本就可以使用標準導入：from config import ..., from base import ...
    """
    project_root_str = str(_project_root)
    if project_root_str not in sys.path:
        sys.path.insert(0, project_root_str)
    return _project_root

# 匯出專案根目錄供其他腳本使用
project_root = _project_root

# 自動設置（當此模組被導入時）
setup_path()
