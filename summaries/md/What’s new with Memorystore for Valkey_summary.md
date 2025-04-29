# What’s new with Memorystore for Valkey
[會議影片連結](https://www.youtube.com/watch?v=R6ohpekfiRo)
Memorystore for Valkey 最新資訊

## 1. 核心觀點

本次會議主要介紹了 Google Cloud 的 Memorystore for Valkey 的最新進展，包括 Valkey 的起源、GA（正式發布）的重要意義、相較於 Redis 的優勢、以及 Memorystore for Valkey 提供的各種功能和未來發展方向。重點強調 Valkey 作為 Redis 的開源替代方案，在性能、可靠性和企業級功能方面都進行了優化，並且與 Google Cloud 深度整合，為使用者提供更強大的緩存解決方案。

## 2. 詳細內容

*   **Memorystore 的定位：** Memorystore 在 Google Cloud 數據庫中扮演著特殊的角色，作為唯一的記憶體內數據儲存服務，它能夠作為緩存補充其他數據庫，提供快速的數據存取。

*   **Valkey 的誕生與 GA：** 由於 Redis 更改了授權方式，Valkey 應運而生，並在 Google、Amazon、Oracle 等公司的支持下迅速發展。Memorystore for Valkey 7.2 和 8.0 於 2025 年 4 月 2 日正式發布 (GA)，意味著使用者可以將生產工作負載部署在該服務上，並享有 4.9 的 SLA 保證。

*   **Valkey 的優勢：**
    *   **開源解決方案：** Valkey 是一個開源項目，使用者可以放心地遷移到該解決方案。
    *   **性能提升：** Valkey 8.0 提供了更快的性能，相較於 Memorystore for Redis cluster，QPS 提升了 2 倍，延遲降低到微秒級別。
    *   **儲存優化：** Valkey 針對鍵值對儲存進行了優化，減少了記憶體佔用。
    *   **可靠性：** Valkey 透過多可用區部署和自動故障轉移等機制，提供了更高的可靠性。

*   **Memorystore for Valkey 的功能：**
    *   **高可用性：** 透過自動區域分佈和快速故障轉移，提供 4.9 的 SLA 保證。
    *   **零停機時間擴展：** 允許使用者根據工作負載的需求，隨時擴展或縮減集群規模。
    *   **垂直擴展：** Valkey 支援垂直擴展，允許使用者利用更強大的機器來提升性能。
    *   **Google Cloud 整合：** 與 Google Cloud 深度整合，提供集中式存取控制、TLS 加密和審計日誌等功能。
    *   **多 VPC 存取：** 允許來自多個 VPC 的客戶端連接到同一個 Memorystore for Valkey 端點。
    *   **單區域集群：** 針對只需要臨時緩存的使用者，提供單區域集群選項，降低成本並提升性能。
    *   **跨區域複製：** 提供暖備份拓撲，允許使用者在不同區域之間複製數據，實現災難恢復和低延遲讀取。
    *   **一鍵持久化：** 允許使用者將數據持久化到磁碟，防止數據丟失。
    *   **維護窗口：** 允許使用者設定維護窗口，並提前收到通知。

*   **未來發展方向：**
    *   **託管備份：** 提供按需備份和排程備份功能，並支援設定保留策略。
    *   **ValkeyClusterModeDisable：** 允許使用者部署單節點 Valkey 集群，並在 ClusterModeDisable 模式下運行，以支援不支援集群協議的客戶端。
    *   **客戶管理加密金鑰：** 允許使用者使用自己的金鑰來加密數據。

*   **MLB 的使用案例：** Major League Baseball (MLB) 分享了他們如何使用 Memorystore 來支援其數據平台，包括在球場緩存、實時 Gumbo 緩存和半實時數據緩存等場景。MLB 強調 Memorystore 對於滿足其 SLA 要求至關重要。

*   **Valkey 8.0 的技術細節：** 深入探討了 Valkey 8.0 的架構改進，包括非同步 I/O 和記憶體預取等技術，這些技術顯著提升了性能和記憶體效率。

## 3. 重要結論

Memorystore for Valkey 作為 Google Cloud 推薦的緩存引擎，提供了高性能、高可靠性和企業級功能，並且與 Google Cloud 深度整合。透過開源協作和持續創新，Valkey 不斷提升性能和效率，為使用者提供更強大的緩存解決方案。MLB 的使用案例也證明了 Memorystore 在實際應用中的價值。
