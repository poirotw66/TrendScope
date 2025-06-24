#!/usr/bin/env python3
"""
智能匹配 PPT 檔案與 BigQuery 會議記錄，並上傳 PPT 內容
"""

import os
import sys
import pathlib
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# 添加專案根目錄到 Python 路徑
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from google import genai
from google.cloud import bigquery
from config.config import GEMINI_API_KEY
import opencc
from bigquery.client import BigQueryClient

# 配置
PPT_DIR = pathlib.Path("data/202505_aicon_ppt")
SEMINAR_NAME = "202505 AICon Shanghai"

# API 配置
MAX_THREADS = 1  # 降低並發數
REQUEST_INTERVAL = 10  # 增加請求間隔
MAX_RETRIES = 3
RETRY_DELAY = 15

# BigQuery 配置
BQ_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"

# 初始化客戶端
genai_client = genai.Client(api_key=GEMINI_API_KEY)
semaphore = threading.Semaphore(MAX_THREADS)

# 初始化 OpenCC 轉換器
cc = opencc.OpenCC('t2s')  # 繁體轉簡體

# 保留原有的繁簡對照表作為備用（如果 OpenCC 失敗時使用）
TRADITIONAL_TO_SIMPLIFIED_BACKUP = {
    '產': '产', '設': '设', '計': '计', '領': '领', '域': '域',
    '過': '过', '現': '现', '來': '来', '數': '数', '據': '据',
    '應': '应', '用': '用', '實': '实', '踐': '践', '開': '开',
    '發': '发', '軟': '软', '體': '体', '驅': '驱', '動': '动',
    '從': '从', '協': '协', '編': '编', '程': '程', '術': '术',
    '進': '进', '與': '与', '落': '落', '地': '地', '創': '创',
    '新': '新', '時': '时', '間': '间', '場': '场', '景': '景',
    '業': '业', '務': '务', '營': '营', '銷': '销', '運': '运',
    '營': '营', '維': '维', '護': '护', '優': '优', '化': '化',
    '構': '构', '建': '建', '統': '统', '一': '一', '標': '标',
    '準': '准', '資': '资', '訊': '讯', '處': '处', '理': '理',
    '網': '网', '絡': '络', '連': '连', '接': '接', '傳': '传',
    '輸': '输', '儲': '储', '存': '存', '檢': '检', '索': '索',
    '識': '识', '別': '别', '語': '语', '言': '言', '機': '机',
    '器': '器', '學': '学', '習': '习', '訓': '训', '練': '练',
    '測': '测', '試': '试', '評': '评', '估': '估', '監': '监',
    '控': '控', '調': '调', '節': '节', '優': '优', '勢': '势',
    '劣': '劣', '勢': '势', '挑': '挑', '戰': '战', '機': '机',
    '會': '会', '風': '风', '險': '险', '問': '问', '題': '题',
    '解': '解', '決': '决', '方': '方', '案': '案', '策': '策',
    '略': '略', '規': '规', '劃': '划', '執': '执', '行': '行',
    '結': '结', '果': '果', '效': '效', '率': '率', '質': '质',
    '量': '量', '標': '标', '準': '准', '規': '规', '範': '范',
    '流': '流', '程': '程', '環': '环', '節': '节', '階': '阶',
    '段': '段', '層': '层', '級': '级', '類': '类', '型': '型',
    '種': '种', '類': '类', '樣': '样', '式': '式', '模': '模',
    '式': '式', '範': '范', '例': '例', '參': '参', '考': '考',
    '資': '资', '料': '料', '檔': '档', '案': '案', '文': '文',
    '件': '件', '報': '报', '告': '告', '記': '记', '錄': '录',
    '紀': '纪', '錄': '录', '歷': '历', '史': '史', '背': '背',
    '景': '景', '環': '环', '境': '境', '條': '条', '件': '件',
    '狀': '状', '況': '况', '情': '情', '況': '况', '現': '现',
    '狀': '状', '趨': '趋', '勢': '势', '發': '发', '展': '展',
    '變': '变', '化': '化', '改': '改', '變': '变', '轉': '转',
    '換': '换', '升': '升', '級': '级', '更': '更', '新': '新',
    '維': '维', '護': '护', '管': '管', '理': '理', '運': '运',
    '作': '作', '操': '操', '作': '作', '使': '使', '用': '用',
    '功': '功', '能': '能', '特': '特', '性': '性', '屬': '属',
    '性': '性', '參': '参', '數': '数', '變': '变', '數': '数',
    '常': '常', '數': '数', '變': '变', '量': '量', '函': '函',
    '數': '数', '方': '方', '法': '法', '技': '技', '術': '术',
    '工': '工', '具': '具', '平': '平', '臺': '台', '系': '系',
    '統': '统', '架': '架', '構': '构', '框': '框', '架': '架',
    '組': '组', '件': '件', '模': '模', '塊': '块', '單': '单',
    '元': '元', '介': '介', '面': '面', '界': '界', '面': '面',
    '顯': '显', '示': '示', '輸': '输', '入': '入', '輸': '输',
    '出': '出', '處': '处', '理': '理', '計': '计', '算': '算',
    '運': '运', '算': '算', '邏': '逻', '輯': '辑', '判': '判',
    '斷': '断', '條': '条', '件': '件', '循': '循', '環': '环',
    '迴': '回', '圈': '圈', '遞': '递', '迴': '回', '遞': '递',
    '歸': '归', '排': '排', '序': '序', '搜': '搜', '尋': '寻',
    '查': '查', '找': '找', '匹': '匹', '配': '配', '比': '比',
    '較': '较', '對': '对', '比': '比', '分': '分', '析': '析',
    '統': '统', '計': '计', '預': '预', '測': '测', '預': '预',
    '估': '估', '評': '评', '價': '价', '測': '测', '量': '量',
    '監': '监', '測': '测', '檢': '检', '測': '测', '驗': '验',
    '證': '证', '確': '确', '認': '认', '驗': '验', '證': '证'
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
    # 轉換為簡體中文進行比較
    text1_simplified = convert_traditional_to_simplified(text1.lower())
    text2_simplified = convert_traditional_to_simplified(text2.lower())
    
    # 如果完全匹配，返回1.0
    if text1_simplified == text2_simplified:
        return 1.0
    
    # 計算關鍵詞相似度
    keywords1 = set(extract_keywords(text1_simplified))
    keywords2 = set(extract_keywords(text2_simplified))
    
    if not keywords1 or not keywords2:
        return 0.0
    
    intersection = keywords1.intersection(keywords2)
    union = keywords1.union(keywords2)
    
    jaccard_similarity = len(intersection) / len(union) if union else 0.0
    
    # 計算字符級相似度
    char_similarity = calculate_char_similarity(text1_simplified, text2_simplified)
    
    # 綜合相似度
    return max(jaccard_similarity, char_similarity)

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

def extract_keywords(text: str) -> list:
    """提取關鍵詞"""
    import re
    
    keywords = []
    
    # 提取中文詞彙
    chinese_chars = re.findall(r'[\u4e00-\u9fff]+', text)
    for chars in chinese_chars:
        if len(chars) >= 2:
            keywords.append(chars)
    
    # 提取英文詞彙
    english_words = re.findall(r'[a-zA-Z]+', text)
    for word in english_words:
        if len(word) >= 2:
            keywords.append(word.lower())
    
    return keywords

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
    if best_match and best_match[2] >= 0.6:  # 60% 相似度
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
    """更新 BigQuery 中的 ppt_context 欄位"""
    try:
        # 使用參數化查詢避免 SQL 注入和字符轉義問題
        update_query = f"""
        UPDATE `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
        SET ppt_context = @ppt_content
        WHERE conference_id = @conference_id
        """

        # 配置查詢參數
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("ppt_content", "STRING", ppt_content),
                bigquery.ScalarQueryParameter("conference_id", "STRING", conference_id),
            ]
        )

        job = client.query(update_query, job_config=job_config)
        job.result()  # 等待查詢完成

        print(f"✅ 成功更新會議 {conference_id} 的 PPT 內容")
        return True

    except Exception as e:
        print(f"❌ 更新 BigQuery 時發生錯誤: {e}")
        return False

def main():
    """主函數"""
    print("開始智能匹配 PPT 內容並上傳到 BigQuery...")
    
    # 檢查必要的環境變數
    if not BQ_CREDENTIALS or not BQ_PROJECT_ID:
        print("❌ 請設置 GOOGLE_APPLICATION_CREDENTIALS 和 GOOGLE_CLOUD_PROJECT 環境變數")
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
    WHERE seminar = '{SEMINAR_NAME}' 
    ORDER BY name
    """
    
    results = client.query(query)
    bq_sessions = [(row['conference_id'], row['name']) for row in results]
    print(f"BigQuery 中有 {len(bq_sessions)} 個會議記錄")
    
    # 獲取所有 PDF 檔案
    pdf_files = list(PPT_DIR.glob("*.pdf"))
    print(f"找到 {len(pdf_files)} 個 PDF 檔案")
    
    # 處理每個 PDF 檔案
    success_count = 0
    
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"\n[{i}/{len(pdf_files)}] 處理檔案: {pdf_file.name}")
        
        session_name = pdf_file.stem
        
        # 尋找最佳匹配
        match = find_best_match(session_name, bq_sessions)
        
        if not match:
            print(f"❌ 未找到匹配的會議: {session_name}")
            continue
        
        conf_id, bq_name, score = match
        print(f"✅ 找到匹配: {bq_name} (相似度: {score:.2f})")
        
        # 提取 PPT 內容
        ppt_content = extract_ppt_content(pdf_file)
        if not ppt_content:
            print(f"❌ 無法提取 PPT 內容: {pdf_file.name}")
            continue
        
        # 更新 BigQuery
        if update_ppt_content_in_bigquery(client, conf_id, ppt_content):
            success_count += 1
        
        # 添加延遲避免 API 限制
        time.sleep(REQUEST_INTERVAL)
    
    print(f"\n🎉 處理完成！成功: {success_count}/{len(pdf_files)}")

if __name__ == "__main__":
    main()
