Bring the power of BigQuery to your Apache Iceberg lakehouse

[會議影片連結](https://www.youtube.com/watch?v=ik6gS35HWCs)
將 BigQuery 的強大功能帶到您的 Apache Iceberg lakehouse

## 1. 核心觀點

本次會議主要介紹了 Google Cloud 的 BigQuery 如何與 Apache Iceberg 整合，以提供更強大的湖倉一體解決方案。核心觀點包括：

*   **結合開放與託管的優勢：** BigQuery 旨在結合 Apache Iceberg 的開放性與 BigQuery 的完全託管特性，提供高效能、可擴展且易於管理的湖倉解決方案。
*   **增強 Iceberg 的功能：** BigQuery 為 Iceberg 表格帶來了許多增強功能，例如高吞吐量串流、細粒度變更、多表格交易和持續分析。
*   **簡化資料管理：** 透過 BigQuery，使用者可以更輕鬆地管理 Iceberg 資料，無需擔心底層基礎架構的複雜性。
*   **與 GCS 深度整合：** BigQuery 與 Google Cloud Storage (GCS) 深度整合，提供軟刪除、自動分層和自動 NL 產生洞察等功能。
*   **Spotify 的實際應用案例：** Spotify 分享了他們如何使用 BigQuery 和 Iceberg 來解決資料孤島問題，並實現成本節約和效率提升。

## 2. 詳細內容

*   **BigQuery 對 Apache Iceberg 的支援演進：**
    *   最初，BigQuery 提供了查詢 Iceberg 表格的能力（自管 Iceberg 表格）。
    *   現在，BigQuery 透過 BigQuery tables for Apache Iceberg，將完全託管的企業級儲存功能引入 Iceberg。
*   **BigQuery tables for Apache Iceberg 的主要優勢：**
    *   **高效能串流：** 支援高吞吐量串流，實現即時資料攝取。
    *   **細粒度變更：** 允許對 Iceberg 表格進行細粒度的更新和刪除，減少寫入放大和成本。
    *   **多表格交易：** 支援多個 Iceberg 表格之間的 ACID 交易，確保資料一致性。
    *   **與 GCS 整合：** 與 GCS 深度整合，提供簡化的資料管理體驗。
    *   **內建治理：** 提供內建的精細化存取控制和治理功能。
*   **BigQuery 的願景：**
    *   今年夏天，BigQuery 和 GCS 將共同發布符合 Iceberg 開放標準規範的開放目錄。
    *   透過此目錄，使用者可以從任何引擎存取 GCS 中的資料，實現無縫的 Iceberg 表格存取。
*   **現代 Iceberg 湖倉的特性：**
    *   高吞吐量串流。
    *   營運資料庫的複寫。
    *   細粒度變更。
    *   多表格交易。
    *   持續分析。
*   **示範：**
    *   **情境一：** 使用 MERGE DML 語句將變更從暫存表格合併到大型事實表格中，展示了 BigQuery 的資料轉換能力以及與 Spark 的互通性。
    *   **情境二：** 展示了多表格交易和細粒度變更的功能，使用單一交易原子性地修改多個表格。
    *   **情境三：** 使用 BigQuery 儲存寫入 API 將串流變更直接應用於 Iceberg 表格，展示了即時資料更新的能力。
*   **Spotify 的 Iceberg 旅程：**
    *   **挑戰：** Spotify 面臨資料孤島問題，資料分散在 GCS 和 BigQuery 原生儲存中，導致資料複製、成本增加和開發人員體驗不佳。
    *   **解決方案：** Spotify 採用 Apache Iceberg 作為通用儲存介面，並使用 BigQuery Iceberg 外部表格來橋接 GCS 和 BigQuery。
    *   **成果：** Spotify 透過遷移到 Iceberg 外部表格，節省了大量儲存成本，並簡化了資料管理流程。
    *   **未來展望：** Spotify 計劃將 Iceberg 作為資料工程管線的主要儲存介面，並試用 BigQuery tables for Apache Iceberg。

## 3. 重要結論

BigQuery 與 Apache Iceberg 的整合為企業提供了一個強大且靈活的湖倉解決方案。透過結合開放標準和完全託管的服務，BigQuery 簡化了資料管理，提高了效能，並降低了成本。Spotify 的案例證明了這種整合在實際應用中的價值，並展示了其在解決資料孤島問題和實現資料驅動決策方面的潛力。
