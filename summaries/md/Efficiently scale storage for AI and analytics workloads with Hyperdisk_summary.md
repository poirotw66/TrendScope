Efficiently scale storage for AI and analytics workloads with Hyperdisk

[會議影片連結](https://www.youtube.com/watch?v=hVXCWWa0lyA)
高效地擴展 Hyperdisk 上的 AI 和分析工作負載的儲存

## 1. 核心觀點

本次會議主要介紹了 Google Cloud 的下一代區塊儲存產品 Hyperdisk，以及它如何幫助客戶高效地擴展 AI 和分析工作負載的儲存。核心觀點包括：

*   **Hyperdisk 的獨特性：** 工作負載優化、高效率、企業級功能。
*   **Hyperdisk 的四種版本：** Balanced、Throughput、Extreme 和 ML，分別針對不同的工作負載。
*   **儲存池 (Storage Pools) 的重要性：** 透過儲存池可以更有效地管理和分配儲存資源，降低總體擁有成本 (TCO)。
*   **AI 和分析工作負載對儲存的需求正在改變：** 客戶需要更動態、更靈活的儲存解決方案。
*   **客戶案例分享：** Sentry 和 HRT 分享了他們如何使用 Hyperdisk 來滿足其儲存需求。
*   **Hyperdisk 的未來發展方向：** 更大的規模、更高的效能，以及更簡化的管理。

## 2. 詳細內容

*   **Hyperdisk 簡介：**
    *   Hyperdisk 是 Google Cloud 的下一代區塊儲存產品，適用於所有第四代運算。
    *   它是 Persistent Disk 的進化版。
    *   Hyperdisk 的三個主要優勢：
        *   **工作負載優化：** 可以獨立調整容量和效能。
        *   **高效率：** 透過儲存池可以精簡配置資源，降低 TCO。
        *   **企業級功能：** 提供資料保護和高可用性功能。

*   **Hyperdisk 的四種版本：**
    *   **Hyperdisk Balanced：** 適用於大多數工作負載，提供靈活的容量、IOPS 和吞吐量配置。也是啟動磁碟產品。
    *   **Hyperdisk Throughput：** 適用於冷資料工作負載和串流工作負載，成本較低。
    *   **Hyperdisk Extreme：** 適用於需要極高效能的工作負載，例如大型資料庫。
    *   **Hyperdisk ML：** 適用於將資料載入到大量運算節點，例如用於機器學習模型訓練。

*   **儲存池 (Storage Pools)：**
    *   儲存池允許客戶將儲存資源集中管理和分配。
    *   透過儲存池，客戶可以精簡配置資源，降低 TCO。
    *   Hyperdisk 提供 Balanced、Throughput 和 Extreme 儲存池。
    *   HTML 本身就是一種池化產品。

*   **AI 和分析工作負載對儲存的需求變化：**
    *   傳統的區塊儲存模型是為每個工作負載單獨配置資源。
    *   現在，客戶需要更動態、更靈活的儲存解決方案，以便應對不斷變化的工作負載需求。
    *   雲端中的雲端 (Cloud in a Cloud) 是一種新的方法，它允許客戶建立一個共享資源池，並根據需要動態地分配資源。
    *   儲存池是實現雲端中的雲端的關鍵。

*   **客戶案例分享：**
    *   **Sentry：** 使用 Hyperdisk 來構建一個統一的資料層，以支援其應用程式。他們使用 Hyperdisk Balanced 和 Throughput 來儲存不同類型的資料，並使用儲存池來簡化管理和降低成本。
    *   **HRT：** 使用 Hyperdisk 來擴展其 AI 工作負載。他們使用 Spot VM 和 DWS 來動態地增加或減少運算資源，並使用 Hyperdisk 儲存池來管理其儲存資源。

*   **Hyperdisk 的未來發展方向：**
    *   **Hyperdisk ML：** 支援第四代運算，並提供 Volume Populator 工具，以便從 GCS 輕鬆載入模型。
    *   **Exopools：** 專為最大規模的 AI 和分析工作負載而設計，提供多個 EB 的容量和多個 TB/s 的吞吐量。

## 3. 重要結論

Hyperdisk 是一個功能強大且靈活的區塊儲存產品，可以幫助客戶高效地擴展 AI 和分析工作負載的儲存。透過工作負載優化、高效率和企業級功能，Hyperdisk 可以滿足不斷變化的儲存需求，並降低 TCO。儲存池和 Exopools 等功能進一步簡化了儲存管理，並為大規模工作負載提供了更高的效能。
