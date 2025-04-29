Use real-time data for AIML workloads in BigQuery

[會議影片連結](https://www.youtube.com/watch?v=SKv6bbwSL5I)
在 BigQuery 中使用即時資料進行 AIML 工作負載

## 1. 核心觀點

本次會議主要探討如何利用 BigQuery 和 PubSub 等 Google Cloud 服務，構建高效、可擴展的即時資料處理平台，以支援 AI/ML 工作負載。核心觀點包括：

*   **AI 的普及與即時性的重要性：** 各行各業都在擁抱 AI，而即時能力是 AI 發展的關鍵驅動力。
*   **簡化串流架構：** 透過 PubSub 和 BigQuery 的整合，可以簡化事件驅動的 AI/ML 工作負載。
*   **BigQuery 的核心地位：** BigQuery 在資料擷取、分析和事件驅動處理中都扮演著核心角色。
*   **PubSub 的關鍵作用：** PubSub 提供可擴展、可靠的訊息傳遞服務，支援各種事件串流和擷取場景。
*   **Flipkart 的成功案例：** Flipkart 利用 BigQuery 和 PubSub 構建了大規模的串流資料平台，支援其電商業務。
*   **BigQuery Continuous Queries 的強大功能：** Continuous Queries 能夠以 SQL 為基礎，即時處理串流資料，並與 Vertex AI 模型整合，實現即時 AI 應用。

## 2. 詳細內容

*   **AI 與即時性的結合：**
    *   AI 正在滲透到各個行業和市場，改善效率、個人化和發現新機會。
    *   即時能力是 AI 進步背後的一大驅動力。
*   **簡化串流架構：**
    *   傳統的串流模式包括資料擷取、分析和事件驅動處理。
    *   簡化的架構是使用 Cloud PubSub，然後是 BigQuery。
    *   資料擷取到 Cloud PubSub 中，然後使用 BigQuery 訂閱將資料傳輸到 BigQuery。
    *   BigQuery 可以使用標準 SQL 或連續查詢來分析資料。
    *   Cloud PubSub 是一個完全託管的無伺服器訊息傳遞服務，易於使用、可靠且可擴展。
    *   PubSub 具有全球路由、多種傳遞類型（包括 BigQuery 和 Cloud Storage 訂閱）以及訊息排序和精確一次傳遞等功能。
*   **PubSub 的新功能：**
    *   Import Topics for Streaming Ingestion：支援從 AWS MSK、Azure Event Hubs 和 Confluent Cloud 等跨雲 Kafka 來源擷取資料到 PubSub。
    *   PubSub Single Message Transforms in JavaScript UDFs：允許在 PubSub 內轉換單個訊息，而無需額外的產品。
*   **Flipkart 的案例研究：**
    *   Flipkart 是一家大型印度電子商務公司，每天處理大量的資料。
    *   他們使用 PubSub 進行點擊流資料和伺服器事件的擷取，並使用 BigQuery 進行即時分析。
    *   他們將 Kafka 遷移到 PubSub，以實現自動擴展、無伺服器體驗和多區域支援。
    *   他們使用 BigQuery 進行即時 AI/ML 工作負載，例如個人化、產品推薦和詐欺偵測。
    *   他們使用 BigQuery 進行 AutoSuggest 功能，該功能根據使用者屬性提供個人化的搜尋建議。
*   **BigQuery Continuous Queries：**
    *   BigQuery Continuous Queries 是一個基於 SQL 的、完全無伺服器且完全託管的方法來執行串流管道。
    *   它允許您編寫一個長時間執行的 SQL 作業，該作業可以即時擷取、處理、轉換和分析資料。
    *   Continuous Queries 可以與 Vertex AI 模型整合，以進行即時情感分析、客戶個人化和異常偵測。
    *   Continuous Queries 允許您將查詢的結果串流匯出到 PubSub、BigTable、Spanner 或另一個 BigQuery 表格。
*   **Symbol Pets 示範：**
    *   Symbol Pets 是一家虛構的寵物公司，它使用 IoT 感測器來監控魚缸的水質。
    *   資料串流到 BigQuery 中，然後 Continuous Queries 會檢測不健康的水質狀況。
    *   如果檢測到問題，則會呼叫 Gemini 來尋求修復問題的指導，然後將其串流到 ServiceNow。
    *   該示範展示了 PubSub 單一訊息轉換如何用於修正不正確的時間戳記。

## 3. 重要結論

本次會議強調了在 AI/ML 工作負載中使用即時資料的重要性，並展示了如何利用 BigQuery 和 PubSub 等 Google Cloud 服務構建高效、可擴展的解決方案。Flipkart 的案例研究和 Symbol Pets 的示範都證明了這些技術的強大功能。BigQuery Continuous Queries 的推出進一步簡化了串流資料處理，並為即時 AI 應用開闢了新的可能性。
