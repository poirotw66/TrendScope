```
# Maximize the availability and performance of your Cloud SQL workloads
[會議影片連結](https://www.youtube.com/watch?v=ccC5Sr7uuLU)
最大化 Cloud SQL 工作負載的可用性和效能

## 1. 核心觀點

本次會議主要探討如何最大化 Cloud SQL 工作負載的可用性和效能。核心觀點包括：

*   **效能提升：** 透過選擇合適的 Cloud SQL 版本（Enterprise Edition 或 Enterprise Plus Edition）、適當的運算和儲存配置，以及啟用資料快取和讀取複本等功能，可以顯著提升效能。Google Axion 機器在效能和價格效能方面都有顯著優勢。
*   **連線管理：** Cloud SQL 提供受管理的連線池，可以有效管理資料庫連線，提升效能並降低延遲。
*   **讀取擴展：** 透過讀取池，可以輕鬆擴展讀取操作，提高應用程式的效能。
*   **高可用性：** Cloud SQL Enterprise Plus Edition 提供極高的可用性，計劃性維護的停機時間低於一秒。
*   **災難復原：** Cloud SQL 提供進階災難復原功能，簡化跨區域災難復原的複雜性，並確保資料的持續可用性。
*   **備份與資料保護：** Cloud SQL 提供靈活的備份選項，包括在刪除執行個體後保留備份，確保資料安全。
*   **全球支付案例：** 全球支付分享了他們如何使用 Cloud SQL 來滿足其業務連續性需求，包括高可用性、災難復原和法規遵循。

## 2. 詳細內容

*   **Cloud SQL Enterprise Plus Edition：** 提供比 Enterprise Edition 高出約 3 倍的效能，透過最佳化的硬體、軟體和儲存來實現。提供高可用性，並提供長達 35 天的日誌保留。
*   **效能最大化：**
    *   選擇合適的版本：Enterprise Edition 或 Enterprise Plus Edition。
    *   選擇合適的運算和儲存配置。
    *   啟用資料快取：將緩衝池擴展到本機 SSD，提高讀取效能。
    *   使用讀取複本：擴展讀取效能。
*   **Google Axion 機器：** 基於 C4A 的機器系列，提供比 N2 機器系列高出 48% 的價格效能。支援 MySQL 和 PostgreSQL。
*   **HyperDisk Balanced：** 一種新的儲存架構，提供更高的 I/O 效能，吞吐量提高 2 倍，IOPS 提高 1.6 倍。允許將磁碟效能與容量分離，並可以每四小時調整 IOPs 和吞吐量。
*   **OptimizeWrite：** 一套用於監控和調整 MySQL 配置的功能，以優化寫入效能並減少延遲。包括：
    *   Adaptive Purge：優先處理前景操作。
    *   Adaptive I/O limits：智慧調整資料庫 I/O 限制。
    *   I/O mutex optimizations：減少儲存層的爭用。
*   **受管理的連線池：** 適用於 MySQL 和 PostgreSQL，透過建立可擴展的連線池層，提高效能並降低延遲。可以根據機器大小自動調整連線池大小。
*   **讀取池：** 允許建立最多 20 個節點的讀取複本池。提供讀取端點，將讀取查詢分散到池中的所有節點。
*   **可用性設計：**
    *   計劃性維護：Enterprise Plus Edition 的停機時間低於一秒。
    *   非計劃性故障：啟用高可用性，使用儲存層級的同步複製。建立第三個區域的讀取複本，以防止雙區域故障。
*   **進階災難復原：** 簡化跨區域災難復原的複雜性，維護拓撲，並提供寫入端點。
*   **備份：** 允許在刪除執行個體後保留備份，並在刪除執行個體時建立最終備份。
*   **全球支付案例：**
    *   使用 Cloud SQL 來滿足其業務連續性需求。
    *   使用多區域架構來提高可用性。
    *   使用跨區域讀取複本和進階災難復原功能。
    *   使用 Terraform 進行基礎架構即程式碼。
    *   從經驗中學習：測試故障轉移流程、定期進行故障轉移測試、優化資源、使用 Terraform。

## 3. 重要結論

Cloud SQL 透過不斷創新和最佳化，為使用者提供高效能、高可用性和可靠的資料庫服務。透過選擇合適的版本、配置和功能，使用者可以最大化其 Cloud SQL 工作負載的效能和可用性。全球支付的案例展示了 Cloud SQL 如何滿足企業級應用程式的嚴苛需求。
```