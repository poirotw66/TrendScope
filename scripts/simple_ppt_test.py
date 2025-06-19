#!/usr/bin/env python3
"""
簡單的 PPT 處理測試
"""

import os
import sys
import pathlib
from typing import List, Tuple, Optional

# 添加專案根目錄到 Python 路徑
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from google.cloud import bigquery

# 配置
PPT_DIR = pathlib.Path("data/202505_aicon_ppt")
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"
SEMINAR_NAME = "202505 AICon Shanghai"

# 繁簡對照表（簡化版）
TRADITIONAL_TO_SIMPLIFIED = {
    '產': '产', '設': '设', '計': '计', '領': '领', '過': '过', 
    '現': '现', '來': '来', '數': '数', '據': '据', '應': '应',
    '實': '实', '踐': '践', '開': '开', '發': '发', '軟': '软',
    '體': '体', '驅': '驱', '動': '动', '從': '从', '協': '协',
    '編': '编', '術': '术', '進': '进', '與': '与', '創': '创',
    '時': '时', '間': '间', '場': '场', '業': '业', '務': '务',
    '營': '营', '銷': '销', '運': '运', '維': '维', '護': '护',
    '優': '优', '構': '构', '統': '统', '標': '标', '準': '准',
    '資': '资', '訊': '讯', '處': '处', '網': '络', '絡': '络',
    '連': '连', '傳': '传', '輸': '输', '儲': '储', '檢': '检',
    '識': '识', '別': '别', '語': '语', '機': '机', '學': '学',
    '習': '习', '訓': '训', '練': '练', '測': '测', '試': '试',
    '評': '评', '監': '监', '調': '调', '節': '节', '勢': '势',
    '會': '会', '風': '风', '險': '险', '問': '问', '題': '题',
    '決': '决', '規': '规', '劃': '划', '執': '执', '結': '结',
    '質': '质', '範': '范', '環': '环', '階': '阶', '層': '层',
    '級': '级', '類': '类', '種': '种', '樣': '样', '參': '参',
    '檔': '档', '報': '报', '記': '记', '錄': '录', '歷': '历',
    '條': '条', '狀': '状', '況': '况', '現': '现', '趨': '趋',
    '變': '变', '轉': '转', '換': '换', '級': '级', '維': '维',
    '運': '运', '屬': '属', '參': '参', '變': '变', '數': '数',
    '臺': '台', '組': '组', '塊': '块', '單': '单', '顯': '显',
    '輸': '输', '邏': '逻', '輯': '辑', '斷': '断', '環': '环',
    '遞': '递', '歸': '归', '較': '较', '對': '对', '預': '预',
    '價': '价', '確': '确', '認': '认', '證': '证'
}

def convert_traditional_to_simplified(text: str) -> str:
    """將繁體中文轉換為簡體中文"""
    result = ""
    for char in text:
        result += TRADITIONAL_TO_SIMPLIFIED.get(char, char)
    return result

def calculate_similarity(text1: str, text2: str) -> float:
    """計算兩個文本的相似度"""
    # 轉換為簡體中文進行比較
    text1_simplified = convert_traditional_to_simplified(text1.lower())
    text2_simplified = convert_traditional_to_simplified(text2.lower())
    
    # 如果完全匹配，返回1.0
    if text1_simplified == text2_simplified:
        return 1.0
    
    # 計算字符級相似度
    return calculate_char_similarity(text1_simplified, text2_simplified)

def calculate_char_similarity(text1: str, text2: str) -> float:
    """計算字符級相似度"""
    if not text1 or not text2:
        return 0.0
    
    # 移除標點符號和空格
    import re
    text1_clean = re.sub(r'[^\w]', '', text1)
    text2_clean = re.sub(r'[^\w]', '', text2)
    
    if not text1_clean or not text2_clean:
        return 0.0
    
    # 計算最長公共子序列
    def lcs_length(s1, s2):
        m, n = len(s1), len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]
    
    lcs_len = lcs_length(text1_clean, text2_clean)
    max_len = max(len(text1_clean), len(text2_clean))
    
    return lcs_len / max_len if max_len > 0 else 0.0

def find_best_match(session_name: str, bq_sessions: List[Tuple[str, str]]) -> Optional[Tuple[str, str, float]]:
    """找到最佳匹配的會議"""
    best_match = None
    best_score = 0.0
    
    for conf_id, bq_name in bq_sessions:
        score = calculate_similarity(session_name, bq_name)
        if score > best_score:
            best_score = score
            best_match = (conf_id, bq_name, score)
    
    # 設定相似度閾值
    if best_match and best_match[2] >= 0.7:  # 70% 相似度
        return best_match
    
    return None

def main():
    """主函數"""
    print("開始簡單的 PPT 匹配測試...")
    
    # 初始化 BigQuery 客戶端
    try:
        client = bigquery.Client()
        print("✅ BigQuery 客戶端初始化成功")
    except Exception as e:
        print(f"❌ BigQuery 客戶端初始化失敗: {e}")
        return
    
    # 獲取 BigQuery 中的所有會議
    query = f"""
    SELECT conference_id, name
    FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
    WHERE seminar = '{SEMINAR_NAME}' 
    ORDER BY name
    """
    
    print("正在查詢 BigQuery...")
    results = client.query(query)
    bq_sessions = [(row['conference_id'], row['name']) for row in results]
    print(f"BigQuery 中有 {len(bq_sessions)} 個會議記錄")
    
    # 獲取所有 PDF 檔案
    pdf_files = list(PPT_DIR.glob("*.pdf"))
    print(f"找到 {len(pdf_files)} 個 PDF 檔案")
    
    # 測試匹配
    matches = []
    
    for i, pdf_file in enumerate(pdf_files[:10], 1):  # 只測試前10個
        session_name = pdf_file.stem
        print(f"\n[{i}] 測試檔案: {session_name}")
        
        # 尋找最佳匹配
        match = find_best_match(session_name, bq_sessions)
        
        if match:
            conf_id, bq_name, score = match
            print(f"✅ 找到匹配: {bq_name} (相似度: {score:.2f})")
            matches.append((pdf_file, conf_id, bq_name, score))
        else:
            print(f"❌ 未找到匹配")
            # 顯示最相似的3個
            similarities = []
            for conf_id, bq_name in bq_sessions:
                score = calculate_similarity(session_name, bq_name)
                similarities.append((score, bq_name, conf_id))
            
            similarities.sort(reverse=True)
            print("   最相似的會議:")
            for score, name, conf_id in similarities[:3]:
                print(f"     {score:.2f}: {name}")
    
    print(f"\n📊 匹配結果總結:")
    print(f"成功匹配: {len(matches)}/{min(10, len(pdf_files))}")
    
    for pdf_file, conf_id, bq_name, score in matches:
        print(f"  {pdf_file.name} -> {bq_name} ({score:.2f})")

if __name__ == "__main__":
    main()
