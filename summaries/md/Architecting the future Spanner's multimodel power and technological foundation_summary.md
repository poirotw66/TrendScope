# Architecting the future Spanner's multimodel power and technological foundation
[會議影片連結](https://www.youtube.com/watch?v=Xsz7m6TvXxM)
Architecting the future Spanner's multimodel power and technological foundation

## 1. 核心觀點

本次會議主要介紹了 Spanner 的多模型能力，以及如何在 Gen.AI 時代利用 Spanner 提升應用程式的效能和功能。重點包括：

*   Spanner 從擴展資料庫演進為多模型平台。
*   Shopify 如何利用 Spanner 實現高度可擴展、彈性且全球分散的應用程式。
*   Spanner 的多模型能力（全文檢索、圖形、向量搜尋）如何結合，簡化架構和操作，同時充分釋放資料的潛力。
*   Palo Alto Networks 如何利用 Spanner 的多模型能力，在概念驗證中實現高效能的網路安全解決方案。
*   Spanner 在 Google 的 AI-ready 資料雲中的關鍵作用，以及它如何提供智慧、統一和開放的平台。

## 2. 詳細內容

*   **Spanner 的演進：** Spanner 不僅是一個高度可擴展且全球一致的資料庫，還是一個多模型平台，支援關係資料模型（Postgres 介面）、鍵值資料模型（Cassandra API），以及完全可互操作的圖形、全文檢索和向量搜尋功能。
*   **Spanner 的應用場景：** Spanner 廣泛應用於需要高可用性、事務一致性和可擴展性的各種場景，例如支付平台、訂單處理、庫存管理、帳單和保險處理。
*   **AI 時代的資料庫需求：** 隨著 AI 技術的發展，應用程式需要更智慧和個人化。資料庫不僅需要儲存、組織和獲取資料，還需要推理、分析和關聯資料。
*   **Spanner 的多模型能力：** Spanner 的全文檢索、向量搜尋和圖形資料庫功能可以結合使用，例如混合搜尋（全文檢索 + 向量搜尋）和全文檢索 + 圖形，以提高搜尋品質和發現資料之間的深層關聯。
*   **Shopify 的 Spanner 之旅：** Shopify 將其基礎設施遷移到 Google Cloud，並使用 Spanner 來構建核心應用程式，以支援全球數百萬商家。他們將會話、購物車和產品目錄等資料遷移到 Spanner，以實現高可用性、可擴展性和全球一致性。
*   **Spanner 的規模：** Spanner 在高峰期處理超過 60 億 QPS，管理超過 17 exabytes 的資料。
*   **Spanner 的搜尋能力：** Spanner 嵌入了向量、全文檢索和圖形功能，並與 SQL 引擎整合。這些功能可以組合使用，以實現更強大的搜尋能力。
*   **Spanner 與 BigQuery 的整合：** Spanner 與 BigQuery 緊密整合，可以無縫地在線上和分析工作負載之間移動資料和查詢。
*   **Palo Alto Networks 的 Cortex Cloud：** Palo Alto Networks 使用 BigQuery、Spanner Search 和 Spanner Graph 來構建其下一代安全產品 Cortex Cloud。他們使用 Spanner 來實現快速搜尋、即時彙總和圖形搜尋，以解決雲端安全領域的難題。

## 3. 重要結論

Spanner 的多模型能力使其成為構建現代 AI 應用程式的理想平台。透過結合關係資料、鍵值資料、全文檢索、向量搜尋和圖形資料庫功能，Spanner 可以簡化架構、降低營運成本，並充分釋放資料的潛力。 Shopify 和 Palo Alto Networks 的案例表明，Spanner 可以幫助企業構建高度可擴展、彈性且高效能的應用程式。
