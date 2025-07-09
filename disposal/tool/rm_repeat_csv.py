import pandas as pd
import os

def remove_duplicates_by_meeting(csv_path):
    """
    檢查CSV文件中'Meeting'欄位是否有重複，若有重複則只保留一項
    
    Args:
        csv_path (str): CSV文件的路徑
    
    Returns:
        pd.DataFrame: 處理後的DataFrame
    """
    # 檢查文件是否存在
    if not os.path.exists(csv_path):
        print(f"錯誤: 文件 {csv_path} 不存在")
        return None
    
    try:
        # 讀取CSV文件
        df = pd.read_csv(csv_path)
        print(f"成功讀取CSV文件，共 {len(df)} 行")
        
        # 檢查是否有'Meeting'欄位
        if 'Meeting' not in df.columns:
            print(f"錯誤: CSV文件中沒有'Meeting'欄位")
            return None
        
        # 檢查重複項
        duplicates = df[df.duplicated(subset=['Meeting'], keep=False)]
        duplicate_count = len(duplicates)
        
        if duplicate_count > 0:
            print(f"發現 {duplicate_count} 個重複的'Meeting'項目")
            
            # 顯示重複項
            duplicate_meetings = duplicates['Meeting'].unique()
            print("\n重複的會議名稱:")
            for i, meeting in enumerate(duplicate_meetings, 1):
                print(f"{i}. {meeting}")
                
            # 移除重複項，保留第一次出現的項目
            df_no_duplicates = df.drop_duplicates(subset=['Meeting'], keep='first')
            removed_count = len(df) - len(df_no_duplicates)
            print(f"\n已移除 {removed_count} 個重複項，保留 {len(df_no_duplicates)} 行")
            
            return df_no_duplicates
        else:
            print("沒有發現重複的'Meeting'項目")
            return df
    
    except Exception as e:
        print(f"處理CSV文件時出錯: {e}")
        return None

def save_csv(df, output_path):
    """
    保存DataFrame到CSV文件
    
    Args:
        df (pd.DataFrame): 要保存的DataFrame
        output_path (str): 輸出文件路徑
    """
    if df is not None:
        try:
            # 保存為CSV，使用utf-8-sig編碼以支持中文
            df.to_csv(output_path, index=False, encoding='utf-8-sig')
            print(f"已成功保存處理後的CSV文件到 {output_path}")
        except Exception as e:
            print(f"保存CSV文件時出錯: {e}")

def main():
    # 設定輸入和輸出文件路徑
    input_csv = "/Users/cfh00896102/Github/TrendScope/data/sheet/GTC25.csv"
    output_csv = "/Users/cfh00896102/Github/TrendScope/data/sheet/GTC25_no_duplicates.csv"
    
    # 處理CSV文件
    df_processed = remove_duplicates_by_meeting(input_csv)
    
    # 保存處理後的文件
    if df_processed is not None:
        save_csv(df_processed, output_csv)

if __name__ == "__main__":
    main()