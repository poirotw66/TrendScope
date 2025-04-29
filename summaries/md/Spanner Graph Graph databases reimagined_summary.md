# Spanner Graph Graph databases reimagined
[會議影片連結](https://www.youtube.com/watch?v=tIYO0aTmv20)
Spanner Graph：重新構想的圖形資料庫

## 1. 核心觀點

本次會議主要介紹了 Google Cloud 的 Spanner Graph，一個專為圖形工作負載設計的資料庫解決方案。會議涵蓋了 Spanner Graph 的設計理念、核心功能、實際應用案例以及未來發展方向。核心觀點包括：

*   **Spanner Graph 的獨特優勢：** Spanner 的全球規模、高可用性和強一致性使其成為運行圖形工作負載的理想平台。
*   **解決圖形資料庫的挑戰：** Spanner Graph 旨在解決傳統圖形資料庫在操作開銷、可擴展性和學習曲線方面的挑戰。
*   **GQL 和 SQL 的互操作性：** Spanner Graph 支援 GQL（Graph Query Language）標準，並提供與 SQL 的無縫整合，降低學習門檻。
*   **搜尋圖形的能力：** Spanner Graph 整合了搜尋功能，方便使用者快速找到圖形中的起始節點，並利用圖形關係進行更深入的探索。
*   **與生成式 AI 的整合：** Spanner Graph 可以與生成式 AI 模型結合，提供更豐富的上下文資訊，提升 AI 應用程式的效能。
*   **Snapchat 的實際應用：** Snapchat 使用 Spanner Graph 來管理其龐大的身份圖，實現更精確的廣告歸因和使用者識別。

## 2. 詳細內容

*   **圖形資料庫的價值：** 圖形資料庫非常適合表示和查詢關係，在零售、金融、電信、供應鏈、藥物發現和網路安全等領域有廣泛的應用。
*   **Spanner Graph 的設計原則：** Spanner Graph 的設計目標是提供原生圖形體驗、搜尋圖形的能力以及卓越的可擴展性和效能。
*   **GQL 的優勢：** GQL 是一種標準化的圖形查詢語言，易於學習和使用，可以簡化複雜的圖形查詢。
*   **Spanner Graph 的查詢優化：** Spanner Graph 針對圖形查詢進行了多項優化，例如向量化處理和因子化處理，以提高查詢效能。
*   **SQL 互操作性的重要性：** Spanner Graph 允許使用者在 SQL 查詢中嵌入 GQL 查詢，或者在 GQL 查詢中使用 SQL 功能，實現更靈活的資料處理。
*   **搜尋功能的應用：** 搜尋功能可以幫助使用者快速找到圖形中的起始節點，例如，在零售圖形中搜尋 "登山鞋"，然後利用圖形關係找到相關的產品、品牌和使用者。
*   **資料儲存方式：** Spanner Graph 將節點和邊儲存在一起，以減少 I/O 操作，提高查詢效能。
*   **Spanner 作為基礎的優勢：** Spanner 提供無限的擴展性、高可用性和強一致性，為 Spanner Graph 提供了堅實的基礎。
*   **Snapchat 的身份圖應用：** Snapchat 使用 Spanner Graph 來管理其包含數十億使用者節點和數百億通訊邊的身份圖，實現更精確的廣告歸因和使用者識別。
*   **Spanner Graph 的效能表現：** Snapchat 報告稱，Spanner Graph 可以在 50 毫秒內完成三到四跳的查詢，並且可以根據流量需求進行水平擴展。
*   **現場演示：** 會議展示了一個使用 Spanner Graph 建立推薦引擎的範例，展示了如何利用圖形關係找到使用者可能感興趣的產品，並將圖形資料與關聯式資料結合。
*   **未來發展方向：** Spanner Graph 的未來發展方向包括整合 GraphRAG、改進視覺化體驗、支援從 BigQuery 反向 ETL、持續優化效能以及支援開放資料模型。
*   **與合作夥伴的整合：** Spanner Graph 與 Linkuris、Graphistry、Canvas 和 G.V. 等合作夥伴進行了整合，以提供更全面的圖形資料庫解決方案。
*   **與 BigQuery 的整合：** Spanner Graph 與 BigQuery 整合，支援操作型和分析型工作負載，並提供統一的圖形架構和查詢體驗。

## 3. 重要結論

Spanner Graph 是一個功能強大且靈活的圖形資料庫解決方案，它利用 Spanner 的全球規模和高可用性，解決了傳統圖形資料庫的挑戰。Spanner Graph 支援 GQL 標準，並提供與 SQL 的無縫整合，降低了學習門檻。此外，Spanner Graph 還整合了搜尋功能，方便使用者快速找到圖形中的起始節點，並利用圖形關係進行更深入的探索。Snapchat 的實際應用案例證明了 Spanner Graph 在處理大規模圖形資料方面的能力。Spanner Graph 的未來發展方向包括整合 GraphRAG、改進視覺化體驗、支援從 BigQuery 反向 ETL、持續優化效能以及支援開放資料模型。總之，Spanner Graph 為使用者提供了一個可靠、可擴展且易於使用的圖形資料庫解決方案，可以滿足各種圖形工作負載的需求。
