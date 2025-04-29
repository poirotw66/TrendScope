# Truth or dare Grounding your LLM outputs
[會議影片連結](https://www.youtube.com/watch?v=OiX_3WbwX6o)
用「真相或大冒險」來讓你的 LLM 輸出更可靠

## 1. 核心觀點

本次會議主要探討如何透過 Grounding（將 LLM 連接到外部資訊來源）來提升 LLM 輸出的準確性、即時性和可靠性。Grounding 可以有效降低 LLM 產生幻覺的風險，並讓 LLM 能夠利用企業自身的資料、即時資訊和第三方資料。

## 2. 詳細內容

會議內容主要分為以下幾個部分：

*   **Grounding 的重要性：** Grounding 將模型連接到額外的資訊來源，以提供準確、最新的回應。這對於減少幻覺、提供最新內容以及利用企業自身資料的力量至關重要。

*   **企業私有資料的 Grounding：** 企業可以透過 RAG（Retrieval Augmented Generation，檢索增強生成）方法，將自身的私有資料索引化，並在 LLM 回應使用者查詢時，檢索相關資訊。Vertex AI Search、RAG Engine 和 Google 的搜尋平台都提供了 RAG 解決方案，以滿足不同的使用案例和需求。

*   **即時世界資訊的 Grounding：** 將 LLM 連接到即時世界資訊，可以讓 LLM 提供關於最新事件和地點的最新答案。Google Search 提供了相關的 Grounding 功能，而 Grounding with Google Maps 則可以讓使用者獲取本地、新鮮的地點資訊。

*   **第三方資料來源的 Grounding：** 將 LLM 連接到第三方資料來源，可以提供更豐富、更有幫助的體驗。Google 已經與各行業的知名資料提供商合作，以方便使用者利用這些資料來源。

*   **Demo 演示：** 會議展示了一個 Grounding 整合的範例，其中一個醫療保險代理人使用 Google Maps Grounding 來尋找 Sunnyvale, California 的最佳過敏專科醫生，並使用 Vertex 搜尋來回答關於保險政策的問題。

## 3. 重要結論

透過結合企業自身的資料、網路資訊和專業的第三方資料集，Grounding 提供了一個強大的解決方案，可以涵蓋各種企業使用案例，並提供新鮮、準確的答案。Grounding 是提升 LLM 輸出品質和可靠性的關鍵技術。
