import os
import re
import difflib
import pandas as pd
import sys

# 1. 讀取 Excel 檔案，取得 session 標題
excel_path = "google_next_sessions.xlsx"
df = pd.read_excel(excel_path)
# 假設 session 標題在第一欄
session_titles = df.iloc[:, 0].astype(str).tolist()

# 2. 取得 txt 檔案名稱
txt_dir = "google_next_txt"
txt_files = [f for f in os.listdir(txt_dir) if f.endswith(".txt")]

# 3. 標準化 session 標題為檔名
# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.utils.string_utils import normalize_string

def normalize_filename(title):
    # 移除不合法字元，只保留中英文、數字、空格、底線、點
    normalized = normalize_string(title)
    return normalized + ".txt"

# 4. 建立對應關係
mapping = {}
used_titles = set()
for txt_file in txt_files:
    txt_name = os.path.splitext(txt_file)[0]
    # 找出最相近的 session 標題
    matches = difflib.get_close_matches(txt_name, session_titles, n=1, cutoff=0.5)
    if matches:
        best_match = matches[0]
        norm_name = normalize_filename(best_match)
        # 避免重複命名
        if norm_name in used_titles:
            base, ext = os.path.splitext(norm_name)
            i = 2
            while f"{base}_{i}{ext}" in used_titles:
                i += 1
            norm_name = f"{base}_{i}{ext}"
        mapping[txt_file] = norm_name
        used_titles.add(norm_name)
    else:
        # 若找不到相近，保留原名
        mapping[txt_file] = txt_file

# 5. 執行重新命名
for old_name, new_name in mapping.items():
    if old_name != new_name:
        old_path = os.path.join(txt_dir, old_name)
        new_path = os.path.join(txt_dir, new_name)
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"已將 {old_name} 重新命名為 {new_name}")
        else:
            print(f"檔案 {new_name} 已存在，跳過 {old_name}")