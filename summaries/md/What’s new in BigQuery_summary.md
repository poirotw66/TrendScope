# What’s new in BigQuery
[會議影片連結](https://www.youtube.com/watch?v=ds7fNK3m_dg)
BigQuery 最新功能

## 1. 核心觀點

本次會議主要介紹 BigQuery 的最新功能和創新，涵蓋三大重點：AI 輔助的智能體驗、統一的數據與 AI 基礎，以及靈活且面向未來的架構。Mattel 公司分享了他們如何利用 BigQuery 建立數據到 AI 的平台，將消費者意見轉化為可衡量的關鍵績效指標（KPI），並將原本需要一個月的工作縮短到一分鐘。Google Cloud 的產品負責人則詳細介紹了 BigQuery 在 Gemini 模型、數據工程代理、AI 查詢引擎、Spark 整合、BigQuery ML 和向量搜尋等方面的最新進展。

## 2. 詳細內容

**Mattel 的案例分享：**

*   Mattel 面臨的挑戰：海量的消費者回饋數據難以有效轉化為價值，報告製作耗時且缺乏標準化。
*   解決方案：Mattel 開發了消費者回饋分類系統（PQA 模型），利用 Gemini 模型對消費者回饋進行分類、分析情感，並將結果轉化為結構化數據。
*   技術細節：使用 BigQuery ML 和 SQL Prompt，要求 Gemini 以 JSON 格式輸出，再利用 BigQuery 的 JSON 函數解析成表格。
*   成果：報告產出時間從數月縮短到數分鐘，實現了跨組織的標準化分析，並能快速應對模型更新。
*   未來應用：競爭者分析、產品評論摘要、語言翻譯、消費者服務分析、圖像分析（詐欺檢測）和數據清理。

**BigQuery 最新功能介紹：**

*   **AI 輔助的智能體驗：**
    *   Gemini 模型整合：BigQuery 的 Gemini 功能已廣泛應用於數據準備、探索、分析和程式碼輔助，使用率大幅提升。
    *   數據準備（Data Preparation）正式發布：利用 Gemini 檢測原始數據檔案中的問題，並自動生成 SQL 程式碼進行修復。
    *   SQL 翻譯：BigQuery 遷移服務支援基於 Gemini 的 SQL 翻譯，可透過對話介面、批次服務或 API 使用。
    *   數據工程代理（Data Engineering Agents）：協助數據工程師完成從數據準備到可觀測性的整個流程。
    *   數據科學代理（Data Science Agents）：協助數據科學家完成從數據探索到模型訓練和部署的流程。
    *   對話式代理（Conversational Agents）：讓業務使用者能夠透過自然語言提問來查詢 BigQuery 數據，並可嵌入到自訂應用程式或聊天機器人中。
*   **統一的數據與 AI 基礎：**
    *   AI 查詢引擎（AI-Query Engine）：將 LLM 呼叫嵌入到 BigQuery 查詢計畫中，實現跨結構化和非結構化數據的分析。
    *   Spark 整合：在 BigQuery Studio 中整合 Spark，支援 PySpark 程式碼、無伺服器 Spark 和隨需應用的無伺服器 Spark Web UI。
    *   CoLab 強化：在 CoLab 中提供 Gemini 輔助、單次時間序列預測和模型基準測試功能。
    *   VS Code 和 Jupyter 插件：支援透過 VS Code 和 Jupyter 對 BigQuery 進行 SQL、Spark 或 BigQuery 數據框的開發。
    *   BigQuery 數據框（BigQuery DataFrames）：可擴展的 Pandas 替代方案，支援多模態數據框和 DBT 整合。
    *   BigQuery ML：支援 Gemini、Cloud Llama 和 Hugging Face 模型，以及多模態數據和列式函數。
    *   TimesFM：用於時間序列預測的基礎模型，可直接對任何數據集進行一次性預測。
    *   貢獻分析（Contribution Analysis）：自動分析指標異常的原因，並找出主要貢獻者。
    *   數據品質功能：自動檢測 BigQuery 表格中的錯誤、離群值和不一致性。
    *   向量搜尋（Vector Search）：支援新的索引技術 SCAN，並可與 Vertex AI Search 同步，支援分割表格。
*   **靈活且面向未來的架構：**
    *   連續查詢（Continuous Query）：以 SQL 語句分析即時攝取的數據，並將結果匯出到 BigQuery 表格、PubSub 主題或 Spanner 表格。
    *   BigQuery Pipelines：在 BigQuery Studio 中建立可視化的數據管道，並與 BigQuery 監控和可觀測性整合。
    *   物件表格（Object Tables）：將 GCS 中的非結構化數據作為 BigQuery 表格進行分析，並與結構化數據進行聯合查詢。
    *   通用目錄（Universal Catalog）：統一 BigQuery 的目錄，支援結構化、多模態和半結構化數據。
    *   通用搜尋（Universal Search）：在 BigQuery Studio 中使用自然語言或關鍵字搜尋，並豐富元數據。
    *   數據產品（Data Products）：將數據、元數據和業務工具打包在一起，安全地與團隊共享。
    *   Google 地圖地點數據：將 Google 地圖的商家資訊作為數據集提供，可與客戶數據結合分析。
    *   災難復原（Disaster Recovery）：提供 RPO 小於 15 分鐘和 RTO 小於 5 分鐘的 SLA 保證。
    *   Apache Iceberg 表格：支援 BigQuery 管理的 Iceberg 表格，並提供元數據管理、安全數據共享和時間旅行等功能。
    *   BigQuery 引擎適用於 Apache Airflow：提供無縫的互操作性、可觀測性和管理。
    *   SpendCommit：統一 BigQuery 引擎的商業模式，提供跨不同 BigQuery 系統的靈活性。

## 3. 重要結論

BigQuery 持續推出創新功能，整合 AI 技術，提供更強大的數據分析和 AI 應用能力。Mattel 的案例展示了 BigQuery 在實際應用中的價值，而 Google Cloud 的產品負責人則詳細介紹了 BigQuery 在各個方面的最新進展，為使用者提供了更全面的了解。BigQuery 的目標是成為一個自主的數據到 AI 平台，簡化數據工作流程，加速 ML 和 AI 模型的開發，並提供靈活且面向未來的架構。
