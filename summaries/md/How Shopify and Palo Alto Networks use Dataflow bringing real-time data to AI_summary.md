# How Shopify and Palo Alto Networks use Dataflow bringing real-time data to AI

[會議影片連結](https://www.youtube.com/watch?v=FA8_aIzk5Ts)
How Shopify and Palo Alto Networks use Dataflow bringing real-time data to AI

## 1. 核心觀點

本次會議主要探討了 Shopify 和 Palo Alto Networks 如何利用 Google Cloud Dataflow 平台，將即時數據應用於人工智慧（AI）領域。核心觀點包括：

*   **Dataflow 的優勢：** Dataflow 作為一個全託管的串流平台，能夠處理大規模的即時數據，並提供強大的 SDK 和轉型功能，簡化了複雜的 AI 應用程式開發。
*   **Shopify 的多模態 AI 應用：** Shopify 利用 Dataflow 建立了一個多模態 AI 管道，用於提取產品的結構化數據，包括圖像和文本信息，並將其映射到 Shopify 的產品分類體系中。
*   **Palo Alto Networks 的大規模數據處理：** Palo Alto Networks 利用 Dataflow 處理來自數十萬個設備的數百萬個事件，每天處理數 PB 的數據，並將這些數據用於安全分析和威脅緩解。
*   **基礎設施的重要性：** 會議強調了基礎設施在 AI 應用中的重要性，包括 GPU 加速、資源優化和低延遲數據處理。
*   **Dataflow 的新功能：** 會議介紹了 Dataflow 的一些新功能，包括 Run Inference 轉型、RAG 應用支援、Iceberg I/O 整合和數據沿襲追蹤。

## 2. 詳細內容

**Dataflow 平台概述：**

*   Dataflow 是一個全託管的串流平台，已經運行了 10 年，可以處理每秒數十 GB 的數據。
*   Dataflow 基於 Apache Beam SDK，提供豐富的 IO 整合，可以連接分析和操作系統。
*   Dataflow 支援 GPU 加速，並將支援 TPU。
*   Dataflow 提供了 Run Inference 轉型，簡化了模型推論的流程。
*   Dataflow 支援 RAG 應用，提供了知識攝取和預測的轉型。
*   Dataflow 整合了 Iceberg I/O，支援串流 CDC。
*   Dataflow 支援數據沿襲追蹤，可以檢視數據的端到端移動。
*   Dataflow 提供了 JobBuilder 工具，可以使用無程式碼方式建立管道。

**Shopify 的多模態 AI 應用：**

*   Shopify 是一個全球電子商務平台，擁有數百萬商家，每天處理數百萬條產品更新。
*   Shopify 使用 Dataflow 建立了一個串流攝取平台，將 Kafka 中的數據寫入 BigQuery。
*   Shopify 使用 BigQuery I/O 的動態目的地功能，將不同模式的數據寫入不同的表格。
*   Shopify 建立了一個檢視管理器服務，為數據科學家提供統一的數據檢視。
*   Shopify 使用多模態 LLM 作為分類器，提取產品的元數據。
*   Shopify 將 LLM 推論與 Dataflow 管道分離，以優化效能。
*   Shopify 使用 Kubernetes 集群運行 LLM 推論，並使用 NVIDIA Dynamo 和其他 LLM 框架。

**Palo Alto Networks 的大規模數據處理：**

*   Palo Alto Networks 是一個網路安全供應商，每天處理來自數十萬個設備的數 PB 數據。
*   Palo Alto Networks 使用 Dataflow 處理來自防火牆、雲安全服務和 VPN 的活動日誌。
*   Palo Alto Networks 將數據儲存在 BigQuery 中，並將其用於安全分析和威脅緩解。
*   Palo Alto Networks 經歷了從 Dataflow 到自管理解決方案，再到 Dataflow 和自管理混合方案的過程。
*   Palo Alto Networks 發現，對於複雜的轉換和聚合，Dataflow 仍然是最佳選擇。
*   Palo Alto Networks 強調了設計串流系統時需要考慮的因素，包括應用需求、控制平面獨立性、預測增長、SLA 要求和人員配置。

## 3. 重要結論

本次會議展示了 Dataflow 在處理大規模即時數據和支援 AI 應用方面的強大能力。 Shopify 和 Palo Alto Networks 的案例表明，Dataflow 可以幫助企業建立高效、可靠的數據管道，並將數據轉化為有價值的洞察。 會議還強調了基礎設施和設計考慮因素在構建可擴展的串流系統中的重要性。
