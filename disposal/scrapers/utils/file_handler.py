"""
文件處理工具
提供各種文件處理功能，例如保存到 Excel、CSV 等
"""
import os
import pandas as pd
from datetime import datetime

def save_to_excel(data, filename_prefix, output_dir=None):
    """
    將數據保存為 Excel 文件
    
    Args:
        data (list): 包含字典的列表，每個字典代表一行數據
        filename_prefix (str): 文件名前綴
        output_dir (str, optional): 輸出目錄，如果未提供則保存在當前目錄
        
    Returns:
        str: 保存的文件路徑
    """
    # 確保數據不為空
    if not data:
        print("沒有數據可保存")
        return None
    
    # 創建 DataFrame
    df = pd.DataFrame(data)
    
    # 生成今天的日期格式
    today = datetime.now().strftime("%Y%m%d")
    
    # 生成文件名
    filename = f"{filename_prefix}_{today}.xlsx"
    
    # 如果提供了輸出目錄，確保它存在
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)
    else:
        file_path = filename
    
    # 保存到 Excel
    df.to_excel(file_path, index=False)
    print(f"數據已成功保存至 {file_path}")
    
    return file_path
