#!/usr/bin/env python3
"""
測試 PPT 檔案名稱與 BigQuery 會議記錄的匹配
"""

import os
import pathlib
from google.cloud import bigquery

# 配置
PPT_DIR = pathlib.Path("data/202505_aicon_ppt")
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"
SEMINAR_NAME = "202505 AICon Shanghai"

def test_matching():
    """測試匹配邏輯"""
    client = bigquery.Client()
    
    # 獲取所有 PDF 檔案
    pdf_files = list(PPT_DIR.glob("*.pdf"))
    print(f"找到 {len(pdf_files)} 個 PDF 檔案")
    
    # 獲取 BigQuery 中的所有會議
    query = f"""
    SELECT conference_id, name, description
    FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
    WHERE seminar = '{SEMINAR_NAME}' 
    ORDER BY name
    """
    
    results = client.query(query)
    bq_sessions = [(row['conference_id'], row['name'], row['description']) for row in results]
    print(f"BigQuery 中有 {len(bq_sessions)} 個會議記錄")
    
    print("\n=== 匹配測試 ===")
    
    # 測試每個 PDF 檔案
    for pdf_file in pdf_files[:5]:  # 只測試前5個
        session_name = pdf_file.stem
        print(f"\nPDF: {session_name}")
        
        # 尋找最佳匹配
        best_match = None
        best_score = 0
        
        for conf_id, bq_name, bq_desc in bq_sessions:
            # 簡單的相似度計算
            score = calculate_similarity(session_name, bq_name)
            if score > best_score:
                best_score = score
                best_match = (conf_id, bq_name, score)
        
        if best_match and best_match[2] > 0.3:  # 相似度閾值
            print(f"  ✅ 匹配: {best_match[1]} (相似度: {best_match[2]:.2f})")
            print(f"     ID: {best_match[0]}")
        else:
            print(f"  ❌ 未找到匹配")
            # 顯示最相似的幾個
            print("     最相似的會議:")
            similarities = []
            for conf_id, bq_name, bq_desc in bq_sessions:
                score = calculate_similarity(session_name, bq_name)
                similarities.append((score, bq_name, conf_id))
            
            similarities.sort(reverse=True)
            for score, name, conf_id in similarities[:3]:
                print(f"       {score:.2f}: {name}")

def calculate_similarity(text1: str, text2: str) -> float:
    """計算兩個文本的相似度"""
    # 簡單的關鍵詞匹配
    keywords1 = set(extract_keywords(text1))
    keywords2 = set(extract_keywords(text2))
    
    if not keywords1 or not keywords2:
        return 0.0
    
    intersection = keywords1.intersection(keywords2)
    union = keywords1.union(keywords2)
    
    return len(intersection) / len(union) if union else 0.0

def extract_keywords(text: str) -> list:
    """提取關鍵詞"""
    # 移除標點符號，分割成詞
    import re
    
    # 常見的技術關鍵詞
    tech_keywords = [
        'AI', 'ai', '人工智能', '人工智慧',
        '大模型', '大語言模型', 'LLM', 'GPT',
        '數據', '資料', 'Data', 'data',
        '智能', '智慧', 'Intelligence',
        '機器學習', '深度學習', 'ML', 'DL',
        '生成式', 'AIGC', 'AGI',
        '多模態', '端側', '雲端',
        '架構', '設計', '實踐', '應用',
        '創新', '技術', '系統', '平臺', '平台'
    ]
    
    keywords = []
    
    # 提取技術關鍵詞
    for keyword in tech_keywords:
        if keyword.lower() in text.lower():
            keywords.append(keyword.lower())
    
    # 提取中文詞彙（簡單分割）
    chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
    for chars in chinese_chars:
        if len(chars) >= 2:  # 至少2個字符
            keywords.append(chars)
    
    # 提取英文詞彙
    english_words = re.findall(r'[a-zA-Z]+', text)
    for word in english_words:
        if len(word) >= 2:
            keywords.append(word.lower())
    
    return keywords

if __name__ == "__main__":
    test_matching()
