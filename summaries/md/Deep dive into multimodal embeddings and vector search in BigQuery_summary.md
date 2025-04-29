# Deep dive into multimodal embeddings and vector search in BigQuery
[會議影片連結](https://www.youtube.com/watch?v=dPcta6Jvuvs)
BigQuery 中多模態嵌入和向量搜尋的深入探討

## 1. 核心觀點

本次會議深入探討了 BigQuery 中多模態嵌入和向量搜尋的應用。核心觀點包括：

*   **AI 的數據基礎：** 高品質的數據是 AI 提供卓越體驗的關鍵，BigQuery 致力於構建高品質的數據集，以支援 AI 平台。
*   **多模態數據的機會：** 除了結構化和半結構化數據，非結構化數據（如圖像、文檔、影片）也提供了巨大的機會來提升數據品質。
*   **BigQuery 的統一介面：** BigQuery 提供了一個統一的介面，可以處理各種格式的數據，包括表格數據、半結構化數據和非結構化數據。
*   **向量搜尋的應用：** 向量搜尋可以應用於各種場景，包括搜尋、個人化、分析和生成式 AI。
*   **BigQuery 的向量索引：** BigQuery 提供了向量索引，可以加速向量搜尋，並支援大規模的批次處理。
*   **Object Ref 的整合：** Object Ref 是一種新的 BigQuery 類型，可以將非結構化數據無縫整合到現有的 BigQuery 表格中。
*   **AI 查詢引擎：** BigQuery 提供了 AI 查詢引擎，可以使用 AI 來分析和轉換數據。
*   **BigQuery 與 Vertex AI 的整合：** BigQuery 可以與 Vertex AI 整合，以支援線上低延遲的向量搜尋。

## 2. 詳細內容

會議首先介紹了 AI 的數據基礎，強調了高品質數據的重要性。接著，討論了多模態數據的機會，指出非結構化數據可以提升數據品質。BigQuery 提供了一個統一的介面，可以處理各種格式的數據。

會議深入探討了向量搜尋的應用，包括搜尋、個人化、分析和生成式 AI。BigQuery 提供了向量索引，可以加速向量搜尋，並支援大規模的批次處理。

會議介紹了 Object Ref，這是一種新的 BigQuery 類型，可以將非結構化數據無縫整合到現有的 BigQuery 表格中。Object Ref 改善了可組合性，並允許在同一個表格中儲存結構化和非結構化數據。

會議展示了 AI 查詢引擎，可以使用 AI 來分析和轉換數據。AI 查詢引擎可以接受 Object Ref 作為輸入，並使用 LLM 來處理非結構化數據。

會議討論了 BigQuery 與 Vertex AI 的整合，以支援線上低延遲的向量搜尋。BigQuery 可以用於離線批次處理，而 Vertex AI 可以用於線上服務。

最後，會議分享了 MercadoLibre 如何使用 BigQuery 和 Gemini 來改善數據標註品質的案例。MercadoLibre 使用向量嵌入來尋找相似的產品，並使用 Gemini 來驗證產品是否相同。

## 3. 重要結論

BigQuery 正在成為一個強大的多模態數據平台，可以處理各種格式的數據，並使用 AI 來分析和轉換數據。BigQuery 的向量搜尋功能可以應用於各種場景，而 Object Ref 可以將非結構化數據無縫整合到現有的 BigQuery 表格中。BigQuery 與 Vertex AI 的整合可以支援線上低延遲的向量搜尋。這些功能使 BigQuery 成為構建 AI 應用程式的理想平台。
