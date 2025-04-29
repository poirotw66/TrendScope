Design business continuity for SQL Server workloads
[會議影片連結](https://www.youtube.com/watch?v=Zzb2rBuDEbo)
Design business continuity for SQL Server workloads

## 1. 核心觀點

本次會議主要討論了 Google Cloud SQL for SQL Server 的業務連續性設計，重點介紹了多項新功能和改進，旨在提高資料保護能力、縮短維護停機時間，並提供更強大的災難復原能力。核心觀點包括：

*   備份與實例解耦，即使實例刪除後也能保留備份。
*   計劃性維護和機器擴展的停機時間縮短至亞秒級。
*   Cloud SQL Enterprise Plus Edition 提供更佳的讀取效能。
*   透過異地災難復原副本實現零資料遺失的故障轉移。
*   強化資料保護，包括更長的備份保留期和更高的可用性 SLA。

## 2. 詳細內容

會議首先介紹了 Cloud SQL for SQL Server 的幾項重要更新：

*   **備份與實例解耦：** 用戶現在可以在刪除實例後保留備份，這為資料保護提供了額外的保障。
*   **亞秒級停機時間：** Cloud SQL for SQL Server 即將推出亞秒級停機時間的計劃性維護和機器擴展功能。演示展示了在不到一秒的時間內完成維護操作。
*   **Cloud SQL Enterprise Plus Edition：** 此版本提供比 Enterprise Edition 高達 4 倍的讀取效能提升，並提供兩種新的機器系列：
    *   效能優化機器：每 vCPU 8GB RAM。
    *   記憶體優化機器：每 vCPU 32GB RAM。
    *   可選的資料快取附加元件，進一步提升讀取效能。
*   **進階災難復原：** 允許在不同區域建立災難復原副本，並在發生災難時進行故障轉移，且保證零資料遺失。故障恢復後，可以切換回原始主節點。
*   **讀取端點：** 確保應用程式始終指向活動的主節點，無需更改連線字串。
*   **資料保護增強：**
    *   時間點回復備份保留期延長至 35 天。
    *   可用性 SLA 提高至四個九。
*   **最終備份：** 在刪除實例之前，Cloud SQL 會執行最終備份以確保資料完整性。
*   **保留備份：** 用戶可以在實例刪除後，將備份保留指定的期限。
*   **匯出交易日誌：** 允許將 SQL Server 的交易日誌匯出到 Google Cloud Storage 儲存桶。

會議中還展示了亞秒級停機時間的演示，展示了在執行維護操作時，停機時間僅為 844 毫秒。此外，還強調了 Cloud SQL 具有強大的備份功能，包括自動備份、隨需備份、跨專案和區域還原備份、時間點回復等。

## 3. 重要結論

Cloud SQL for SQL Server 透過引入多項新功能和改進，顯著提升了業務連續性能力。亞秒級停機時間、進階災難復原和強化的資料保護功能，使 Cloud SQL 成為企業級 SQL Server 工作負載的理想選擇。備份與實例解耦、保留備份和匯出交易日誌等功能，為資料保護提供了額外的保障。總體而言，Cloud SQL for SQL Server 是一個完全託管的資料庫服務，可以為企業關鍵業務應用提供強大的支援。
