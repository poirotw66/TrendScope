#!/usr/bin/env python3
"""
添加示例 PPT 內容到 BigQuery 進行測試
"""

import os
from google.cloud import bigquery

# BigQuery 配置
BQ_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
DATASET_ID = "conference_data"
TABLE_ID = "sessions"
SEMINAR_NAME = "202505 AICon Shanghai"

def add_sample_ppt_content():
    """添加示例 PPT 內容"""
    client = bigquery.Client()
    
    # 示例 PPT 內容
    sample_ppt_content = """# 生成式 AI 在產品設計和 UI 領域：過去、現在和未來

## 簡報概述
本簡報探討生成式人工智能在產品設計和用戶界面領域的發展歷程、現狀和未來趨勢。

## 第一部分：過去 - AI 設計工具的起源

### 早期發展
- **2010-2015**: 基礎的自動化設計工具
- **2016-2019**: 機器學習輔助設計
- **2020-2022**: 深度學習在設計中的應用

### 關鍵里程碑
1. Adobe Sensei 的推出
2. Figma 自動佈局功能
3. Sketch 智能組件系統

## 第二部分：現在 - 生成式 AI 的革命

### 當前技術棧
- **文本到圖像**: DALL-E, Midjourney, Stable Diffusion
- **UI 生成**: Uizard, Galileo AI, Framer AI
- **設計系統**: Design Tokens, 自動化組件生成

### 實際應用案例
1. **品牌設計**: Logo 生成和品牌識別
2. **界面設計**: 快速原型和線框圖
3. **用戶體驗**: 個性化界面和適應性設計

### 技術優勢
- 快速迭代和原型製作
- 降低設計門檻
- 提高創意探索效率
- 自動化重複性工作

## 第三部分：未來 - AI 驅動的設計新時代

### 預期發展趨勢
1. **多模態設計**: 語音、手勢、眼動控制
2. **實時協作**: AI 助手參與設計過程
3. **個性化體驗**: 基於用戶行為的動態界面
4. **無代碼設計**: 自然語言到完整應用

### 技術突破方向
- **更精確的語義理解**
- **跨平台一致性保證**
- **設計倫理和可訪問性**
- **實時性能優化**

### 挑戰與機遇
#### 挑戰
- 創意版權問題
- 設計師角色轉變
- 技術標準化需求
- 用戶隱私保護

#### 機遇
- 民主化設計工具
- 提升設計效率
- 創新交互模式
- 全新商業模式

## 結論

生成式 AI 正在重塑產品設計和 UI 領域，從輔助工具演進為創意夥伴。未來的設計師需要：

1. **擁抱 AI 技術**: 學習與 AI 協作
2. **專注創意策略**: 從執行轉向策略思考
3. **理解技術邊界**: 知道何時使用 AI，何時依賴人類創意
4. **持續學習**: 跟上快速發展的技術趨勢

### 行動建議
- 開始實驗生成式 AI 工具
- 建立 AI 輔助的設計工作流
- 培養跨學科合作能力
- 關注設計倫理和可持續性

---

**感謝聆聽！**

*本簡報內容基於 2025 年最新的行業研究和實踐案例*"""

    # 查找對應的會議記錄
    query = f"""
    SELECT conference_id, name
    FROM `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}` 
    WHERE seminar = '{SEMINAR_NAME}' 
    AND LOWER(name) LIKE '%生成式%ai%产品设计%ui%'
    LIMIT 1
    """
    
    print("正在查找匹配的會議...")
    results = client.query(query)
    
    conference_id = None
    for row in results:
        conference_id = row['conference_id']
        print(f"找到會議: {row['name']}")
        break
    
    if not conference_id:
        print("未找到匹配的會議記錄")
        return
    
    # 更新 PPT 內容 - 使用參數化查詢避免 SQL 注入
    update_query = f"""
    UPDATE `{BQ_PROJECT_ID}.{DATASET_ID}.{TABLE_ID}`
    SET ppt_context = @ppt_content
    WHERE conference_id = @conference_id
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("ppt_content", "STRING", sample_ppt_content),
            bigquery.ScalarQueryParameter("conference_id", "STRING", conference_id),
        ]
    )
    
    print("正在更新 PPT 內容...")
    job = client.query(update_query, job_config=job_config)
    job.result()
    
    print("✅ 成功添加示例 PPT 內容！")
    print(f"會議 ID: {conference_id}")
    print(f"內容長度: {len(sample_ppt_content)} 字符")

def main():
    """主函數"""
    print("開始添加示例 PPT 內容到 BigQuery...")
    
    # 檢查環境變數
    if not BQ_PROJECT_ID:
        print("❌ 請設置 GOOGLE_CLOUD_PROJECT 環境變數")
        return
    
    add_sample_ppt_content()

if __name__ == "__main__":
    main()
