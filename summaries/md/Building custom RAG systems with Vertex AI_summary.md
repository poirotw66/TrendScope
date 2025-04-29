# Building custom RAG systems with Vertex AI
[會議影片連結](https://www.youtube.com/watch?v=vSL68n5MG5g)
使用 Vertex AI 構建自定義 RAG 系統

## 1. 核心觀點

本次會議主要探討如何使用 Google Cloud 的 Vertex AI 構建自定義的 RAG（Retrieval-Augmented Generation，檢索增強生成）系統。核心觀點包括：

*   RAG 系統的關鍵在於將 AI 代理連接到正確的數據，並依賴於強大且精確的檢索方法。
*   Vertex AI 提供了一系列 RAG 解決方案，從開箱即用的 Vertex AI Search 到高度可定制的搜尋平台 API。
*   Google 內部使用雙階段檢索流程，首先使用混合嵌入和向量搜尋進行候選檢索，然後使用排序來縮小範圍。
*   DocAI Layout Parser、Vertex AI Embeddings、Vector Search 和 Ranking API 是構建 RAG 系統的關鍵組件。
*   Gemini 可以通過主動檢索器智能地決定如何查詢檢索方法，從而實現更準確、更有幫助的 RAG。
*   實際案例展示了 AstraZeneca、Home Depot 和 RCS Media Group 如何利用 RAG 解決方案解決其特定業務挑戰。

## 2. 詳細內容

*   **RAG 系統的設計：**
    *   RAG 系統的設計包含索引、檢索和生成三個階段。
    *   索引階段涉及使企業數據可搜尋。
    *   檢索階段涉及快速且精確地檢索與查詢相關的上下文。
    *   生成階段涉及將搜尋結果打包並傳遞給模型以進行生成。
*   **Vertex AI 的 RAG 解決方案：**
    *   Vertex AI Search 是一個開箱即用的解決方案，可以與 Gemini 結合使用。
    *   搜尋平台 API 提供了一套組件，可以混合和匹配以構建自定義 RAG 解決方案。
    *   這些組件包括 DocAI Layout Parser、Vertex AI Embeddings、Vector Search 和 Ranking API。
*   **Google 的雙階段檢索流程：**
    *   第一階段使用密集和稀疏嵌入以及向量搜尋進行混合檢索，以獲得數百個候選結果。
    *   第二階段使用排序對候選結果進行評分，並將其縮小到最相關的結果，然後傳遞給模型。
*   **DocAI Layout Parser：**
    *   DocAI Layout Parser 是一個用於準備 RAG 工作流程文檔的一站式商店。
    *   它可以將原始文檔（如 PDF）轉換為結構化、高質量的數據。
    *   通過多模態處理，可以獲取視覺佈局信息，例如元素在頁面上的位置及其與文本信息的關係。
    *   Table-to-Markdown 功能可以提取表格中每個單元格的數據，並了解其在表格中的位置。
    *   Bring-Your-Own-Schema 允許定義一組自定義字段，並匹配所需的精確信息和架構。
*   **Vertex AI Embeddings：**
    *   Vertex AI Embeddings 模型將數據轉換為數值向量，從而捕獲輸入的語義含義。
    *   多模態嵌入支持文本、圖像和視頻。
    *   Matryoshka 表示學習確保最關鍵的語義信息被捕獲在嵌入向量的前幾個維度中。
*   **Vector Search：**
    *   向量數據庫存儲嵌入，並實現極快的相似性搜尋。
    *   新增功能包括元數據存儲、BigQuery 連接器和存儲優化。
    *   元數據存儲允許將額外的元數據（如文檔來源、日期或類別標籤）與向量一起存儲。
    *   BigQuery 連接器使存儲在 BigQuery 中的客戶更容易利用 Vertex Vector Search 的功能。
    *   存儲優化降低了向量搜尋的存儲成本，對於流量較低的部署尤其有用。
*   **Ranking API：**
    *   Ranking API 使用專用模型來重新評估和重新評分向量搜尋產生的候選結果。
    *   最新模型版本 4 在多個公共基準測試中提供了領先的性能。
    *   對於延遲至關重要的用例，它可以將深度排序任務的延遲降低多達 3 倍。
    *   Ranking API 可以根據數據和業務上下文進行微調，並支持高達 32K tokens 的大型文檔。
*   **Gemini 和主動檢索器：**
    *   Gemini 可以首先分析查詢，然後智能地決定如何查詢檢索方法，從而實現更準確、更有幫助的 RAG。
    *   對於複雜的問題，它可以將複雜的查詢分解為更小、更易於管理的檢索步驟。
    *   它可以插入各種數據源，包括 Vertex AI Search、自定義檢索器 API、Elastic Search 和 MongoDB Atlas。
    *   Gemini 可以自動混合來自多個來源的數據，包括 Google Search 和 Google Maps。
*   **實際案例：**
    *   **AstraZeneca：** 使用多模態 RAG 應用程序來查詢專家討論的視頻記錄，並結合來自不同上下文和模式的信息。
    *   **Home Depot：** 在 homedepot.com 上使用 Magic Apron 功能，通過自然語言界面與產品互動，並從產品文檔中獲取信息。
    *   **RCS Media Group：** 構建了一個搜尋基礎層，用於索引 150 年的報紙檔案和數字文章，並使用 Gemini 豐富圖像和視頻。

## 3. 重要結論

本次會議展示了如何使用 Vertex AI 的各種工具和技術構建強大的自定義 RAG 系統。通過結合 DocAI Layout Parser、Vertex AI Embeddings、Vector Search、Ranking API 和 Gemini，開發人員可以創建能夠從各種數據源中檢索相關信息並生成有意義的響應的 AI 代理。實際案例強調了 RAG 系統在解決不同行業的特定業務挑戰方面的價值。
