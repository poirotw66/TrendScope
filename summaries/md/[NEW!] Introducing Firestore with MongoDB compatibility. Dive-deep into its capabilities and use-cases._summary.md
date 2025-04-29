# [NEW!] Introducing Firestore with MongoDB compatibility. Dive-deep into its capabilities and use-cases.

[會議影片連結](https://www.youtube.com/watch?v=ZzLFAEYV2js)
[NEW!] Introducing Firestore with MongoDB compatibility. Dive-deep into its capabilities and use-cases.

## 1. 核心觀點

本次會議主要介紹了 Google Cloud Platform (GCP) 中 Firestore 與 MongoDB 兼容性的新功能。重點在於結合 MongoDB API 和工具的便利性，以及 Firestore 的可擴展性、可用性和易用性。此外，還探討了 Firestore Enterprise Edition 的定價模式，以及 Mayo Clinic 如何利用 Firestore 進行創新。

## 2. 詳細內容

*   **GCP 非關聯式資料庫產品組合：**
    *   介紹了 GCP 提供的各種非關聯式資料庫服務，包括 Memorystore (Redis, Valkey, Memcached)、Bigtable (Key-Value, Wide-Column) 和 Firestore (Serverless Document Database)。
    *   強調了這些服務與 GenAI 的整合，例如向量搜尋和與 Vertex.AI LLM 模型的整合。

*   **Firestore 與 MongoDB 兼容性：**
    *   宣布 Firestore 與 MongoDB 兼容性進入公開預覽階段，旨在結合 MongoDB API 和工具的便利性，以及 Firestore 的可擴展性、可用性和易用性。
    *   支援 MongoDB API 版本 3.6 到 8.0，包括查詢語法、聚合管道查詢、ACID 事務等。
    *   支援各種資料類型和索引，包括多鍵、稀疏和非稀疏索引。

*   **Firestore 架構：**
    *   展示了 Firestore 的高階架構，強調儲存和計算的分離，這使得能夠根據工作負載快速擴展和縮減。

*   **使用案例：**
    *   討論了 Firestore 與 MongoDB 兼容性的各種使用案例，包括資料目錄、使用者個人化、遊戲、即時分析和內容管理。

*   **企業功能和安全性：**
    *   介紹了 Firestore 的企業功能，包括客戶管理加密金鑰 (CMEK)、IAM 存取、私有服務連接、雲端稽核日誌記錄和監控。
    *   討論了災難復原功能，包括託管備份、時間點恢復和託管匯入/匯出。
    *   強調了 Firestore 符合各種合規性認證，例如 SOC、PCI 和 FedRAMP。

*   **Firestore Enterprise Edition 定價：**
    *   介紹了 Firestore Enterprise Edition，這是一個新的 Firestore 版本，旨在為客戶提供更多控制。
    *   在 Enterprise Edition 中，預設情況下不會對資料建立索引，而是將控制權交給客戶，讓他們可以決定要為哪些資料屬性建立索引，以提高效能並管理成本。
    *   Enterprise Edition 還提供進階功能和改進的效能，尤其是在尾部延遲方面。
    *   定價模式基於讀取單元和寫入單元，客戶可以根據文件大小和索引大小來控制成本。

*   **Firestore 深入探討：**
    *   展示了如何輕鬆建立 Firestore 與 MongoDB 兼容的資料庫，只需選擇 Enterprise Edition 即可。
    *   強調可以使用現有的 MongoDB 工具和程式碼與 Firestore 互動。
    *   介紹了使用 Mongo Import 工具匯入資料，以及使用 Mongo SH shell 查詢資料。
    *   展示了 Firestore 的查詢編輯器，以及對各種索引類型（包括非稀疏、稀疏和多鍵索引）的支援。
    *   討論了身份驗證選項，包括使用密碼和不使用密碼 (OIDC)。

*   **Firestore 的價值：**
    *   強調了 Firestore 的關鍵價值，包括可用性、可擴展性、無伺服器和易用性。
    *   解釋了 Firestore 如何使用分離式架構來實現可擴展性，以及如何使用 Paxos 進行同步資料複製來實現高可用性。
    *   介紹了資料庫中心整合、查詢說明和查詢洞察等功能，以簡化操作和開發。

*   **Mayo Clinic 的使用案例：**
    *   分享了 Mayo Clinic 如何利用 Firestore 和其他託管服務來推動創新。
    *   介紹了 Cloud App Factory，這是一個用於建置、測試和部署生產級應用程式的平台，其中 80% 的資料儲存在 Firestore 中。
    *   展示了 Maya，這是一個 AI 輔助的聊天機器人體驗，使用 Firestore 來追蹤聊天記錄和維護最近存取的患者清單。
    *   介紹了 Mayo Clinic TV，這是一個在患者房間中提供個人化內容的產品，使用 Firestore 作為其主要資料庫。

## 3. 重要結論

Firestore 與 MongoDB 兼容性的推出，為開發者提供了更多選擇和靈活性，同時利用了 Firestore 的可擴展性、可用性和易用性。Firestore Enterprise Edition 的定價模式旨在為客戶提供更多控制權，並優化成本。Mayo Clinic 的使用案例展示了 Firestore 如何在醫療保健領域推動創新。
