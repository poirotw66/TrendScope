#!/usr/bin/env python3
"""
安全地處理所有 PPT 檔案並上傳到 BigQuery
使用修正後的參數化查詢避免 SQL 語法錯誤
"""

import os
import sys
import pathlib
import time
from typing import List, Tuple, Optional

# 使用標準導入（專案應作為 package 安裝：pip install -e .）
from scripts._setup_path import setup_path
setup_path()

from google import genai
from google.cloud import bigquery
from config.config import GEMINI_API_KEY
import opencc

# 配置
PPT_DIR = pathlib.Path("data/202505_aicon_ppt")
SEMINAR_NAME = "202505 AICon Shanghai"
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"

# API 配置
REQUEST_INTERVAL = 15  # 增加請求間隔避免 API 限制
MAX_RETRIES = 3
RETRY_DELAY = 20

# 初始化客戶端
genai_client = genai.Client(api_key=GEMINI_API_KEY)

# 初始化 OpenCC 轉換器
cc = opencc.OpenCC('t2s')  # 繁體轉簡體

# 保留原有的繁簡對照表作為備用（如果 OpenCC 失敗時使用）
TRADITIONAL_TO_SIMPLIFIED_BACKUP = {
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
    try:
        # 優先使用 OpenCC 進行轉換
        return cc.convert(text)
    except Exception as e:
        print(f"OpenCC 轉換失敗，使用備用方法: {e}")
        # 如果 OpenCC 失敗，使用備用字典
        result = ""
        for char in text:
            result += TRADITIONAL_TO_SIMPLIFIED_BACKUP.get(char, char)
        return result

def calculate_similarity(text1: str, text2: str) -> float:
    """計算兩個文本的相似度"""
    text1_simplified = convert_traditional_to_simplified(text1.lower())
    text2_simplified = convert_traditional_to_simplified(text2.lower())
    
    if text1_simplified == text2_simplified:
        return 1.0
    
    # 計算最長公共子序列相似度
    import re
    text1_clean = re.sub(r'[^\w]', '', text1_simplified)
    text2_clean = re.sub(r'[^\w]', '', text2_simplified)
    
    if not text1_clean or not text2_clean:
        return 0.0
    
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

def extract_ppt_content(pdf_path: pathlib.Path) -> Optional[str]:
    """使用 Gemini API 提取 PPT 內容"""
    try:
        print(f"正在提取 PPT 內容: {pdf_path.name}")
        
        # 上傳檔案到 Gemini
        sample_file = genai_client.files.upload(file=pdf_path)
        
        # 提取內容的 prompt
        prompt = f"""
請提取這個 PPT 簡報的完整內容，並按照以下格式整理：

## 簡報標題
{pdf_path.stem}

## 簡報內容
請逐頁提取簡報的文字內容，包括：
- 標題
- 重點內容
- 圖表說明
- 結論

要求：
1. 保持原始內容的邏輯結構
2. 使用 Markdown 格式
3. 保留重要的技術術語和專有名詞
4. 如果有圖表，請描述其主要內容
5. 內容要完整但簡潔

請直接輸出整理後的內容，不需要額外說明。
"""

        # 呼叫 Gemini API
        response = genai_client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=[sample_file, prompt]
        )
        
        return response.text
        
    except Exception as e:
        print(f"提取 PPT 內容時發生錯誤 ({pdf_path.name}): {e}")
        return None

def update_ppt_content_in_bigquery(client: bigquery.Client, conference_id: str, ppt_content: str) -> bool:
    """更新 BigQuery 中的 ppt_context 欄位 - 使用參數化查詢"""
    try:
        update_query = f"""
        UPDATE `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
        SET ppt_context = @ppt_content
        WHERE conference_id = @conference_id
        """
        
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("ppt_content", "STRING", ppt_content),
                bigquery.ScalarQueryParameter("conference_id", "STRING", conference_id),
            ]
        )
        
        job = client.query(update_query, job_config=job_config)
        job.result()
        
        print(f"✅ 成功更新會議 {conference_id} 的 PPT 內容")
        return True
        
    except Exception as e:
        print(f"❌ 更新 BigQuery 時發生錯誤: {e}")
        return False

def process_single_ppt(pdf_path: pathlib.Path, client: bigquery.Client, bq_sessions: List[Tuple[str, str]]) -> bool:
    """處理單個 PPT 檔案"""
    session_name = pdf_path.stem
    print(f"\n處理檔案: {session_name}")
    
    # 尋找最佳匹配
    match = find_best_match(session_name, bq_sessions)
    
    if not match:
        print(f"❌ 未找到匹配的會議: {session_name}")
        return False
    
    conf_id, bq_name, score = match
    print(f"✅ 找到匹配: {bq_name} (相似度: {score:.2f})")
    
    # 檢查是否已經有 PPT 內容
    check_query = f"""
    SELECT ppt_context IS NOT NULL as has_ppt
    FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
    WHERE conference_id = @conference_id
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("conference_id", "STRING", conf_id),
        ]
    )
    
    results = client.query(check_query, job_config=job_config)
    for row in results:
        if row['has_ppt']:
            print(f"⚠️  會議已有 PPT 內容，跳過")
            return True
        break
    
    # 提取 PPT 內容
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            ppt_content = extract_ppt_content(pdf_path)
            if not ppt_content:
                print(f"❌ 無法提取 PPT 內容 (嘗試 {attempt}/{MAX_RETRIES})")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                    continue
                return False
            
            # 更新 BigQuery
            if update_ppt_content_in_bigquery(client, conf_id, ppt_content):
                print(f"✅ 成功處理: {pdf_path.name}")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"處理 {pdf_path.name} 時發生錯誤 (嘗試 {attempt}/{MAX_RETRIES}): {e}")
            if attempt < MAX_RETRIES:
                time.sleep(RETRY_DELAY)
            else:
                return False
    
    return False

def main():
    """主函數"""
    print("開始安全地處理所有 PPT 檔案...")
    print(f"PPT 目錄: {PPT_DIR}")
    print(f"研討會: {SEMINAR_NAME}")
    
    # 檢查環境變數
    if not BQ_PROJECT_ID:
        print("❌ 請設置 GOOGLE_CLOUD_PROJECT 環境變數")
        return
    
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
    WHERE seminar = @seminar_name
    ORDER BY name
    """
    
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("seminar_name", "STRING", SEMINAR_NAME),
        ]
    )
    
    results = client.query(query, job_config=job_config)
    bq_sessions = [(row['conference_id'], row['name']) for row in results]
    print(f"BigQuery 中有 {len(bq_sessions)} 個會議記錄")
    
    # 獲取所有 PDF 檔案
    pdf_files = list(PPT_DIR.glob("*.pdf"))
    print(f"找到 {len(pdf_files)} 個 PDF 檔案")
    
    if not pdf_files:
        print("❌ 沒有找到 PDF 檔案")
        return
    
    # 處理每個 PDF 檔案
    success_count = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] 處理檔案: {pdf_file.name}")
        
        if process_single_ppt(pdf_file, client, bq_sessions):
            success_count += 1
        
        # 添加延遲避免 API 限制
        if i < len(pdf_files):  # 最後一個檔案不需要延遲
            print(f"等待 {REQUEST_INTERVAL} 秒...")
            time.sleep(REQUEST_INTERVAL)
    
    print(f"\n🎉 處理完成！")
    print(f"成功: {success_count}/{len(pdf_files)}")
    print(f"成功率: {success_count/len(pdf_files)*100:.1f}%")

if __name__ == "__main__":
    main()
