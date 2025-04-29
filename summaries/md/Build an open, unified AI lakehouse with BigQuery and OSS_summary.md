Build an open, unified AI lakehouse with BigQuery and OSS

[會議影片連結](https://www.youtube.com/watch?v=8cAm9TEL5pI)
建構一個開放、統一的 AI Lakehouse，結合 BigQuery 和 OSS

## 1. 核心觀點

本次會議主要探討如何利用 BigQuery 和開源軟體（OSS）建構一個開放、統一的 AI Lakehouse。重點在於透過統一的儲存、中繼資料管理和處理引擎，簡化資料處理流程，並提供更大的靈活性和選擇。

## 2. 詳細內容

*   **傳統資料平台的挑戰：** 過去，企業面臨資料孤島、資料複製、安全性和存取控制等問題，導致資料處理複雜且耗時。

*   **Lakehouse 的優勢：** Lakehouse 旨在解決這些問題，提供單一資料副本、統一的中繼資料定義和安全策略，並允許使用各種處理引擎（例如 BigQuery 和開源工具）存取資料。

*   **開放原始碼的重要性：** 開放原始碼提供零供應商鎖定、工具靈活性、快速創新和廣泛的人才庫。

*   **Google Cloud 的解決方案：** Google Cloud 提供多種工具和服務來建構 AI Lakehouse，包括：

    *   **Serverless Spark：** 一種簡化的 Spark 執行方式，無需管理基礎架構。
    *   **Dataproc：** 一種託管的 Spark 和其他開源處理引擎服務，提供效能、安全性和成本效益。
    *   **BigQuery Metastore：** 一種統一的中繼資料儲存庫，可讓不同的處理引擎以一致的方式存取資料。

*   **BigQuery Metastore 的優勢：** BigQuery Metastore 提供跨不同引擎（例如 Spark 和 BigQuery）的統一中繼資料，實現引擎互通性、更快的上市時間和集中式管理。它還支援 Hive API 和 Iceberg Catalog，並與 BigQuery 和 Cloud Storage 等各種儲存系統整合。

*   **CME Group 的案例研究：** CME Group 分享了他們在 Google Cloud 上建構統一資料平台的經驗，強調了自動化、統一資料存取、治理、探索和可擴展性的重要性。他們使用 BigLake 和 BigQuery 實現統一的資料存取層，並使用 Atlan 作為企業目錄。

*   **CME Group 的架構：** CME Group 的平台包括登陸區、處理區和策展區。資料透過 Spark、Dataproc 和 Dataflow 等工具提取、轉換和載入。使用者可以透過 BigQuery Studio、BigQuery 連接工作表、Looker 和 Tableau 等工具存取和分析資料。

*   **CME Group 的經驗教訓：** CME Group 分享了他們在遷移到 Google Cloud 時獲得的經驗教訓，包括網路成本、自動分層儲存、KMS 金鑰管理和 Dataproc 效能最佳化。

*   **CME Group 的未來方向：** CME Group 計劃專注於細粒度存取控制、無縫資料分發、Iceberg 整合、Looker 遷移和生成式 AI。

## 3. 重要結論

透過結合 BigQuery 和開源軟體，企業可以建構一個開放、統一的 AI Lakehouse，從而簡化資料處理、提高靈活性並加速創新。Google Cloud 提供了一套全面的工具和服務來支援此架構，而 CME Group 的案例研究證明了其可行性和價值。
