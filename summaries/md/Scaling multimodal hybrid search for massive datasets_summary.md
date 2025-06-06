Scaling multimodal hybrid search for massive datasets
[會議影片連結](https://www.youtube.com/watch?v=uf17IwYg4nE)
大規模數據集的多模態混合搜索擴展

## 1. 核心觀點

本次演講主要介紹了 Google Cloud 的產品經理 Aron Lewis 關於如何擴展多模態混合搜索以應用於海量數據集。核心觀點包括：

*   搜索的重要性日益提升，尤其是在大型語言模型（LLM）普及的背景下，使用者期望 AI 驅動的、能深入理解其意圖的體驗。
*   向量搜索和嵌入（embeddings）是實現這些智能體驗的基礎技術，能夠理解數據背後的含義，超越了簡單的關鍵字搜索。
*   Vertex-i vector search 基於 Google 的 Scan 技術，具有快速、可擴展、易於使用、高質量和高成本效益等優點。
*   Vertex-i vector search 的新功能包括元數據存儲、BigQuery 連接器和存儲優化向量搜索。

## 2. 詳細內容

演講首先強調了搜索的重要性，指出隨著大型語言模型的發展，使用者期望更智能、更個性化的搜索體驗。向量搜索和嵌入技術是實現這些體驗的關鍵，它們能夠理解數據的語義信息，而不仅仅是匹配關鍵字。

Vertex-i vector search 是 Google Cloud 提供的全託管向量搜索服務，它基於 Google 內部使用的 Scan 技術，該技術被廣泛應用於 Google 搜索、廣告、Google Play 和 YouTube 等服務中。Vertex-i vector search 具有以下優勢：

*   **快速且可擴展：** 即使在數十億向量的數據集中，也能在毫秒級別內找到最近鄰。
*   **易於使用：** 全託管服務，具有自動擴展功能，並與 Llama Index 和 Langchain 等流行框架原生集成。
*   **高質量：** 提供高召回率的搜索結果。
*   **高成本效益：** 在大規模應用中，成本效益比主要競爭對手高達四倍。
*   **內置重要功能：** 包括增量索引、過濾、結果多樣性和混合搜索（結合向量和關鍵字技術）。
*   **企業級特性：** 具有 99.9% 的 SLA、VPCSC 支持等。

演講中展示了 Vertex-i vector search 在不同標準數據集上的性能基準測試，證明了其在保持高召回率的同時，能夠實現單位數毫秒級別的查詢延遲。

此外，演講還介紹了 Vertex-i vector search 的新功能：

*   **元數據存儲：** 允許將任意元數據（如描述、評級等）與向量嵌入一起存儲在索引中，避免了額外的查找步驟。
*   **BigQuery 連接器：** 簡化了數據管道，可以直接從 BigQuery 連接數據進行索引，並通過流式更新保持索引的新鮮度。
*   **存儲優化向量搜索：** 針對具有非常大的數據集和較低流量模式的部署，提供更具成本效益的選擇。

演講最後分享了 MercadoLibre 使用 Vertex-i vector search 的案例，展示了其如何利用該服務為數千萬用戶提供快速、高質量的搜索體驗。

## 3. 重要結論

Vertex-i vector search 是一個強大且多功能的向量搜索服務，它能夠幫助企業構建智能、個性化的搜索體驗，並在海量數據集中實現快速、高效的數據檢索。通過元數據存儲、BigQuery 連接器和存儲優化等新功能，Vertex-i vector search 變得更加易於使用、更具成本效益，並能滿足更廣泛的應用場景需求。
