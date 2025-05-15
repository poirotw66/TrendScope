import os
import re
import csv
import pandas as pd
from pathlib import Path

def extract_core_points(md_content):
    """從 Markdown 內容中提取核心觀點區塊"""
    # 使用正則表達式匹配 "## 1. 核心觀點" 區塊
    pattern = r'## 1\. 核心觀點\s+(.*?)(?=\n##|\Z)'
    match = re.search(pattern, md_content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

def normalize(title):
    title = re.sub(r'[\\/“:_\'*?\"<>()-|]', '', title)
    title = title.strip()
    return title

def get_meeting_name_from_filename(filename):
    """從文件名中獲取會議名稱"""
    # 移除 .md 後綴並處理文件名
    meeting_name = os.path.basename(filename).replace('.md', '')
    return normalize(meeting_name)

def main():
    # 設定路徑
    md_dir = '/Users/cfh00896102/Github/TrendScope/GTC_summary/topic/md'
    csv_path = '/Users/cfh00896102/Github/TrendScope/data/sheet/GTC25.csv'
    
    # 確保目錄存在
    if not os.path.exists(md_dir):
        print(f"錯誤: 目錄 {md_dir} 不存在")
        return
    
    if not os.path.exists(csv_path):
        print(f"錯誤: CSV 文件 {csv_path} 不存在")
        return
    
    # 讀取 CSV 文件
    try:
        df = pd.read_csv(csv_path)
        print(f"成功讀取 CSV 文件，共 {len(df)} 行")
    except Exception as e:
        print(f"讀取 CSV 文件時出錯: {e}")
        return
    
    # 創建會議名稱到序號的映射
    meeting_to_index = {}
    for index, row in df.iterrows():
        meeting_name = row['Meeting']
        meeting_to_index[meeting_name] = index
    
    # 處理所有 Markdown 文件
    update_count = 0
    md_files = [f for f in os.listdir(md_dir) if f.endswith('.md')]
    print(f"找到 {len(md_files)} 個 Markdown 文件")
    
    for md_file in md_files:
        md_path = os.path.join(md_dir, md_file)
        meeting_name = get_meeting_name_from_filename(md_file)
        
        # 讀取 Markdown 文件
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
        except Exception as e:
            print(f"讀取文件 {md_path} 時出錯: {e}")
            continue
        
        # 提取核心觀點
        core_points = extract_core_points(md_content)
        if not core_points:
            print(f"警告: 在文件 {md_file} 中未找到核心觀點區塊")
            continue
        
        # 查找對應的 CSV 行
        found = False
        for csv_meeting_name, index in meeting_to_index.items():
            # 嘗試不同的匹配方式，因為文件名和 CSV 中的會議名稱可能有細微差異
            csv_meeting_name = normalize(csv_meeting_name)
            if (meeting_name.lower() in csv_meeting_name.lower() or 
                csv_meeting_name.lower() in meeting_name.lower()):
                df.at[index, 'Key'] = core_points
                found = True
                update_count += 1
                # print(f"更新: {meeting_name} -> 序號 {index+1}")
                break
        
        if not found:
            print(f"警告: 未找到與 {meeting_name} 對應的 CSV 行")
    
    # 保存更新後的 CSV
    try:
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        print(f"成功更新 CSV 文件，共更新 {update_count} 行")
    except Exception as e:
        print(f"保存 CSV 文件時出錯: {e}")

if __name__ == "__main__":
    main()